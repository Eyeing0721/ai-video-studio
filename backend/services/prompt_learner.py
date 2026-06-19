"""Prompt learner — background service that fetches trending prompt templates
from CivitAI and optimizes local generation prompts using learned patterns.

Features:
- Periodic scraping of CivitAI trending images API
- Parse prompt structure: positive/negative prompts, keyword weights, style tags
- Store learned prompts in the prompt_templates table
- get_optimized_prompt(): enhance a base prompt with learned style patterns
- Configurable interval (default: 24 hours)
"""

import asyncio
import json
import logging
import re
import time
from collections import Counter
from datetime import datetime, timezone
from typing import Optional

import httpx
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import config

logger = logging.getLogger(__name__)

# ── CivitAI API endpoint ──────────────────────────────────

CIVITAI_IMAGES_URL = "https://civitai.com/api/v1/images"
CIVITAI_DEFAULT_LIMIT = 100
CIVITAI_DEFAULT_PERIOD = "Month"
CIVITAI_DEFAULT_SORT = "Most Reactions"

# ── Prompt weight pattern: (keyword:1.2) or (keyword:0.8) ─
WEIGHT_RE = re.compile(r"\(([^()]+):\s*([\d.]+)\)")
# ── LoRA trigger pattern: <lora:name:weight> ──────────────
LORA_RE = re.compile(r"<lora:([^:>]+)(?::([\d.]+))?>", re.IGNORECASE)
# ── Style tag separator heuristics ─────────────────────────
STYLE_RE = re.compile(r"(?:artist:|style of |in the style of |by )([\w\s\-]+)", re.IGNORECASE)


# ── Background task state ─────────────────────────────────

_running: bool = False
_task: Optional[asyncio.Task] = None
_findings_count: int = 0
_last_run: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════
#  API fetching
# ═══════════════════════════════════════════════════════════

async def _fetch_trending_images(
    limit: int = CIVITAI_DEFAULT_LIMIT,
    period: str = CIVITAI_DEFAULT_PERIOD,
    sort: str = CIVITAI_DEFAULT_SORT,
) -> list[dict]:
    """Fetch trending image metadata from the CivitAI public API."""
    params = {
        "limit": limit,
        "period": period,
        "sort": sort,
        "nsfw": "None",  # skip NSFW content
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(CIVITAI_IMAGES_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    items = data.get("items", [])
    logger.info("Fetched %d trending images from CivitAI", len(items))
    return items


# ═══════════════════════════════════════════════════════════
#  Prompt parsing
# ═══════════════════════════════════════════════════════════

def _parse_prompt_structure(meta: dict | None) -> dict:
    """Extract prompt structure from CivitAI image metadata.

    CivitAI stores prompt info inside the `meta` field (varies by generator:
    Automatic1111, ComfyUI, etc.).  Returns a dict with:
      - positive_prompt (str)
      - negative_prompt (str)
      - weighted_keywords (list[tuple[str, float]])
      - loras (list[tuple[str, float]])
      - style_tags (list[str])
    """
    if not meta or not isinstance(meta, dict):
        return {}

    # CivitAI nests the actual prompt inside meta.prompt in some API shapes
    prompt_str = meta.get("prompt", "")
    negative_str = meta.get("negativePrompt", "")

    # If meta itself has no prompt but sub-keys do, try common shapes
    if not prompt_str:
        for key in ("positive", "pos", "Positive", "prompt"):
            val = meta.get(key)
            if isinstance(val, str) and len(val) > 5:
                prompt_str = val
                break
    if not negative_str:
        for key in ("negative", "neg", "Negative", "negativePrompt", "negative_prompt"):
            val = meta.get(key)
            if isinstance(val, str) and len(val) > 3:
                negative_str = val
                break

    # Extract weighted keywords: (keyword:1.3), (keyword:0.7)
    weighted_keywords: list[tuple[str, float]] = []
    for match in WEIGHT_RE.finditer(prompt_str):
        kw = match.group(1).strip()
        w = float(match.group(2))
        weighted_keywords.append((kw, w))

    # Strip weight syntax from prompt for style-tag extraction
    clean_prompt = WEIGHT_RE.sub(r"\1", prompt_str)

    # Extract LoRA references
    loras: list[tuple[str, float]] = []
    for match in LORA_RE.finditer(prompt_str):
        name = match.group(1).strip()
        weight = float(match.group(2)) if match.group(2) else 1.0
        loras.append((name, weight))

    # Extract style tags: artist:..., by ..., style of ..., etc.
    style_tags: list[str] = []
    for match in STYLE_RE.finditer(prompt_str):
        tag = match.group(1).strip().lower()
        if tag and len(tag) > 2:
            style_tags.append(tag)

    # Additionally grab explicit "styles" array if present
    explicit_styles = meta.get("styles", []) or meta.get("style", [])
    if isinstance(explicit_styles, list):
        for s in explicit_styles:
            if isinstance(s, str) and s.strip():
                style_tags.append(s.strip().lower())
    elif isinstance(explicit_styles, str) and explicit_styles.strip():
        style_tags.append(explicit_styles.strip().lower())

    return {
        "positive_prompt": prompt_str[:8000] if prompt_str else None,
        "negative_prompt": negative_str[:4000] if negative_str else None,
        "weighted_keywords": weighted_keywords,
        "loras": loras,
        "style_tags": list(dict.fromkeys(style_tags)),  # deduplicate, preserve order
    }


def _infer_category(tags: list[str], positive: str) -> str:
    """Heuristically assign a category based on style tags and prompt content."""
    text = positive.lower() + " " + " ".join(tags).lower()
    categories = {
        "portrait": ["portrait", "face", "close-up", "headshot"],
        "landscape": ["landscape", "scenery", "panorama", "vista"],
        "fantasy": ["fantasy", "magic", "dragon", "elf", "wizard"],
        "sci-fi": ["sci-fi", "cyberpunk", "futuristic", "robot", "space"],
        "anime": ["anime", "manga", "waifu"],
        "realistic": ["realistic", "photorealistic", "photography"],
        "concept_art": ["concept art", "concept_art", "illustration"],
        "abstract": ["abstract", "geometric", "surreal"],
    }
    scores = {cat: sum(1 for kw in kws if kw in text) for cat, kws in categories.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


# ═══════════════════════════════════════════════════════════
#  Prompt optimization
# ═══════════════════════════════════════════════════════════

async def get_optimized_prompt(
    base_prompt: str,
    style_tags: Optional[list[str]] = None,
    session_factory: Optional[async_sessionmaker] = None,
) -> str:
    """Enhance a base prompt using patterns learned from trending prompts.

    Strategy:
    1. Find top-scoring templates whose style_tags overlap with the requested tags.
    2. Extract common positive keywords and negative-prompt patterns.
    3. Append quality-boosting modifiers that appear frequently in high-score prompts.

    Args:
        base_prompt: The raw/user prompt to enhance.
        style_tags: Optional list of style/theme tags to match against.
        session_factory: SQLAlchemy async session factory (required for DB lookup).

    Returns:
        An enhanced prompt string.
    """
    if not session_factory:
        logger.warning("get_optimized_prompt called without session_factory; returning base prompt unchanged")
        return base_prompt

    tags = style_tags or []
    enhanced = base_prompt.strip()

    try:
        from models.task import PromptTemplate

        async with session_factory() as session:
            # Fetch top-score templates, optionally filtered by matching tags
            query = select(PromptTemplate).order_by(PromptTemplate.score.desc()).limit(50)
            result = await session.execute(query)
            templates = result.scalars().all()

            if not templates:
                logger.info("No prompt templates in DB; returning base prompt as-is")
                return enhanced

            # Collect common quality keywords from high-score positives
            keyword_counter: Counter = Counter()
            negative_counter: Counter = Counter()

            for t in templates:
                tag_list: list[str] = []
                if t.tags_json:
                    try:
                        tag_list = json.loads(t.tags_json)
                    except (json.JSONDecodeError, TypeError):
                        pass

                # Weight match: templates whose tags intersect with requested tags get higher weight
                match_score = 0
                if tags and tag_list:
                    intersection = set(tags) & set(t.lower() for t in tag_list)
                    match_score = len(intersection)
                else:
                    match_score = 1  # neutral fallback

                weight = (t.score or 0) + match_score

                if t.positive_prompt:
                    # Tokenize naively on common delimiters
                    tokens = re.split(r"[,;\n]+", t.positive_prompt)
                    for token in tokens:
                        token = token.strip().rstrip(".")
                        if len(token) > 3:
                            keyword_counter[token] += weight

                if t.negative_prompt:
                    neg_tokens = re.split(r"[,;\n]+", t.negative_prompt)
                    for token in neg_tokens:
                        token = token.strip().rstrip(".")
                        if len(token) > 3:
                            negative_counter[token] += weight

            # Build quality booster suffix from top keywords not already in the base prompt
            base_lower = enhanced.lower()
            booster_keywords = []
            for kw, _count in keyword_counter.most_common(15):
                if kw.lower() not in base_lower and len(kw) < 80:
                    booster_keywords.append(kw)
                if len(booster_keywords) >= 6:
                    break

            if booster_keywords:
                enhanced = enhanced.rstrip(".,; ") + ", " + ", ".join(booster_keywords)

            # Append consolidated negative prompt hints (only the top patterns)
            top_negatives = [kw for kw, _c in negative_counter.most_common(5) if kw.lower() not in base_lower]
            if top_negatives and tags:
                # Return as a structured dict-like string so callers can use it
                # The base prompt itself stays clean; negatives are returned separately
                # For simplicity we tag them onto the end
                enhanced += " --neg " + ", ".join(top_negatives[:3])

            logger.debug("Optimized prompt: %d keywords added from %d templates", len(booster_keywords), len(templates))
            return enhanced

    except Exception:
        logger.exception("Error during prompt optimization; returning base prompt unchanged")
        return base_prompt


# ═══════════════════════════════════════════════════════════
#  Background scraper loop
# ═══════════════════════════════════════════════════════════

async def _scrape_cycle(session_factory: async_sessionmaker) -> int:
    """Run a single scrape cycle. Returns the number of new prompts stored."""
    global _findings_count, _last_run

    try:
        items = await _fetch_trending_images()
    except Exception:
        logger.exception("Failed to fetch trending images from CivitAI")
        return 0

    inserted = 0

    async with session_factory() as session:
        for item in items:
            try:
                meta = item.get("meta") or {}
                parsed = _parse_prompt_structure(meta)

                if not parsed.get("positive_prompt"):
                    continue  # nothing useful

                tags = parsed.get("style_tags", [])
                category = _infer_category(tags, parsed["positive_prompt"] or "")

                # Score based on reaction count from the API item
                stats = item.get("stats", {})
                reaction_count = (
                    stats.get("cryCount", 0)
                    + stats.get("laughCount", 0)
                    + stats.get("likeCount", 0)
                    + stats.get("heartCount", 0)
                )

                # Check for duplicate by source URL + positive prompt prefix
                source_url = item.get("url", f"civitai:{item.get('id', '')}")
                prompt_prefix = (parsed["positive_prompt"] or "")[:200]

                from models.task import PromptTemplate
                existing = await session.execute(
                    select(func.count(PromptTemplate.id)).where(
                        PromptTemplate.source == source_url,
                        PromptTemplate.positive_prompt.startswith(prompt_prefix[:100]),
                    )
                )
                if existing.scalar() and existing.scalar() > 0:
                    continue  # skip duplicates

                record = PromptTemplate(
                    category=category,
                    positive_prompt=parsed.get("positive_prompt"),
                    negative_prompt=parsed.get("negative_prompt"),
                    tags_json=json.dumps(tags, ensure_ascii=False) if tags else None,
                    source=source_url,
                    score=float(reaction_count),
                )
                session.add(record)
                inserted += 1

            except Exception:
                logger.exception("Error processing a CivitAI image item")
                continue

        if inserted > 0:
            await session.commit()
            logger.info("Stored %d new prompt templates", inserted)

    _findings_count += inserted
    _last_run = datetime.now(timezone.utc)
    return inserted


async def _background_loop(
    session_factory: async_sessionmaker,
    interval_sec: float = 86400.0,  # default: 24 hours
) -> None:
    """Run the scraper in an infinite loop at the configured interval."""
    global _running

    logger.info("Prompt learner background task started (interval=%.0fs)", interval_sec)
    _running = True

    while _running:
        try:
            n = await _scrape_cycle(session_factory)
            logger.info("Prompt learner cycle complete: %d new prompts (total findings: %d)", n, _findings_count)
        except asyncio.CancelledError:
            logger.info("Prompt learner background task cancelled")
            break
        except Exception:
            logger.exception("Unhandled error in prompt learner loop")

        # Sleep between cycles
        try:
            await asyncio.sleep(interval_sec)
        except asyncio.CancelledError:
            break

    _running = False


# ═══════════════════════════════════════════════════════════
#  Public API
# ═══════════════════════════════════════════════════════════

def start(
    session_factory: async_sessionmaker,
    interval_sec: float = 86400.0,
) -> asyncio.Task:
    """Start the prompt learner background task.

    Args:
        session_factory: SQLAlchemy async session factory for DB access.
        interval_sec: Seconds between scrape cycles (default: 86400 = 24 hours).

    Returns:
        The asyncio Task handle so it can be awaited/cancelled.
    """
    global _task
    if _task is not None and not _task.done():
        logger.warning("Prompt learner is already running; skipping start()")
        return _task

    _task = asyncio.create_task(_background_loop(session_factory, interval_sec=interval_sec))
    return _task


def stop() -> None:
    """Signal the background task to stop."""
    global _running, _task
    _running = False
    if _task and not _task.done():
        _task.cancel()


def status() -> dict:
    """Return current learner status."""
    global _findings_count, _running, _last_run
    return {
        "running": _running,
        "findings_count": _findings_count,
        "last_run_utc": _last_run.isoformat() if _last_run else None,
    }
