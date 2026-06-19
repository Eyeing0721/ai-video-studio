"""Workflow fetcher — background service that pulls ComfyUI workflow JSONs
from CivitAI community sources, validates them, and stores compatible templates.

Features:
- Fetch workflows tagged "ComfyUI" from CivitAI API
- Validate each workflow via workflow_manager.validate_workflow()
- Sanitize via workflow_manager.sanitize_workflow()
- Store valid workflows in the workflow_templates table
- Check compatibility with installed models: Z-Image, Wan, Sulphur, FLUX
- Log imported / skipped counts
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timezone
from typing import Optional

import httpx
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import config
from services.workflow_manager import validate_workflow, sanitize_workflow

logger = logging.getLogger(__name__)

# ── CivitAI endpoints ──────────────────────────────────────

CIVITAI_IMAGES_URL = "https://civitai.com/api/v1/images"
CIVITAI_DEFAULT_LIMIT = 100

# ── Known model identifiers for compatibility ─────────────

# Model family keywords found in workflow node inputs/metadata
COMPAT_MODEL_FAMILIES: dict[str, list[str]] = {
    "Z-Image": [
        "z_image", "z-image", "zimage",
        "z_image_turbo", "z_image_turbo_bf16",
    ],
    "Wan": [
        "wan", "wan2.2", "wan2.1",
        "wan_i2v", "wan_i2v_high", "wan_i2v_low",
    ],
    "Sulphur": [
        "sulphur", "sulphur_dev",
        "sulphur_fp8", "sulphur_gguf",
        "sulphur_q4", "sulphur_q8",
    ],
    "FLUX": [
        "flux", "flux.1", "flux_dev",
        "flux_schnell", "flux_pro",
        "flux1", "flux_1",
    ],
}


# ── Background task state ─────────────────────────────────

_running: bool = False
_task: Optional[asyncio.Task] = None
_imported_count: int = 0
_skipped_count: int = 0
_last_run: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════
#  API fetching
# ═══════════════════════════════════════════════════════════

async def _fetch_workflow_images(
    limit: int = CIVITAI_DEFAULT_LIMIT,
) -> list[dict]:
    """Fetch images with ComfyUI metadata from the CivitAI API.

    We request images sorted by Most Reactions that have workflow metadata
    (indicated by the presence of a ComfyUI-style meta.prompt graph).
    """
    params = {
        "limit": limit,
        "period": "Month",
        "sort": "Most Reactions",
        "nsfw": "None",
        "types": "image",  # exclude video-only for now
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(CIVITAI_IMAGES_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

    items = data.get("items", [])
    logger.info("Fetched %d items from CivitAI for workflow screening", len(items))
    return items


def _extract_workflow_json(item: dict) -> Optional[dict]:
    """Attempt to extract a ComfyUI workflow JSON from a CivitAI image item.

    CivitAI may store workflows in:
      - meta.prompt (ComfyUI API format: {"prompt": {nodes...}})
      - meta.workflow
      - A direct dict under meta where value keys look like node IDs
    """
    meta = item.get("meta") or {}
    if not isinstance(meta, dict):
        return None

    # Shape 1: Direct ComfyUI API prompt format
    prompt_data = meta.get("prompt")
    if isinstance(prompt_data, dict):
        # Check if it's wrapped: {"prompt": {...nodes...}}
        inner = prompt_data.get("prompt")
        if isinstance(inner, dict) and _has_node_ids(inner):
            return inner
        if _has_node_ids(prompt_data):
            return prompt_data

    # Shape 2: meta.workflow
    wf = meta.get("workflow")
    if isinstance(wf, dict):
        if isinstance(wf.get("prompt"), dict):
            inner = wf["prompt"]
            if isinstance(inner.get("prompt"), dict) and _has_node_ids(inner["prompt"]):
                return inner["prompt"]
            if _has_node_ids(inner):
                return inner
        if _has_node_ids(wf):
            return wf

    # Shape 3: meta itself looks like a node dict (keys are numeric IDs)
    if _has_node_ids(meta):
        return meta

    return None


def _has_node_ids(data: dict) -> bool:
    """Heuristic: at least one key maps to a dict with 'class_type'."""
    count = 0
    for _k, v in data.items():
        if isinstance(v, dict) and "class_type" in v:
            count += 1
            if count >= 2:
                return True
    return count >= 1 and len(data) >= 2


# ═══════════════════════════════════════════════════════════
#  Compatibility detection
# ═══════════════════════════════════════════════════════════

def _detect_model_compatibility(workflow: dict, sanitized: dict) -> tuple[str, bool]:
    """Determine which model family a workflow targets and whether it is compatible
    with the locally installed models.

    Returns:
        (model_family, is_compatible) — model_family is the best-guess family string.
    """
    # Collect all strings from the workflow (sanitized version)
    all_text = json.dumps(sanitized, default=str).lower()

    # Also check node class_type values and model references in sanitized
    model_refs: set[str] = set()
    for _node_id, node_data in sanitized.items():
        if isinstance(node_data, dict):
            class_type = (node_data.get("class_type") or "").lower()
            if class_type:
                all_text += " " + class_type
            inputs = node_data.get("inputs", {})
            if isinstance(inputs, dict):
                for val in inputs.values():
                    if isinstance(val, str):
                        model_refs.add(val.lower())
                        all_text += " " + val.lower()

    # Check each model family
    matched_families: list[tuple[str, int]] = []
    for family, keywords in COMPAT_MODEL_FAMILIES.items():
        score = 0
        for kw in keywords:
            if kw in all_text:
                score += 1
            # Check model refs specifically
            for ref in model_refs:
                if kw in ref:
                    score += 1
        if score > 0:
            matched_families.append((family, score))

    if not matched_families:
        return ("unknown", False)

    # Pick the family with the highest score
    matched_families.sort(key=lambda x: x[1], reverse=True)
    best_family = matched_families[0][0]

    # Determine compatibility: check if the family's model is in local config
    installed_models = config.get("models", {})
    family_config_key = best_family.lower().replace("-", "_")
    # Map to known config keys
    compat_map = {
        "Z-Image": any(k for k in installed_models if "z_image" in k),
        "Wan": any(k for k in installed_models if "wan" in k),
        "Sulphur": any(k for k in installed_models if "sulphur" in k),
        "FLUX": any(k for k in installed_models if "flux" in k.lower()),
    }
    is_compatible = compat_map.get(best_family, False)

    return (best_family, is_compatible)


# ═══════════════════════════════════════════════════════════
#  Background scraper loop
# ═══════════════════════════════════════════════════════════

async def _fetch_cycle(session_factory: async_sessionmaker) -> tuple[int, int]:
    """Run a single fetch cycle. Returns (imported, skipped)."""
    global _imported_count, _skipped_count, _last_run

    try:
        items = await _fetch_workflow_images()
    except Exception:
        logger.exception("Failed to fetch images from CivitAI for workflow extraction")
        return (0, 0)

    imported = 0
    skipped = 0

    async with session_factory() as session:
        for item in items:
            try:
                workflow_json = _extract_workflow_json(item)
                if not workflow_json:
                    skipped += 1
                    continue

                # Validate
                valid, msg, info = validate_workflow(workflow_json)
                if not valid:
                    logger.debug("Skipping invalid workflow: %s", msg)
                    skipped += 1
                    continue

                # Sanitize
                sanitized = sanitize_workflow(workflow_json)
                sanitized_str = json.dumps(sanitized, ensure_ascii=False)

                # Detect model compatibility
                model_type, compatible = _detect_model_compatibility(workflow_json, sanitized)

                # Derive a name from the item
                name = item.get("username", "") or ""
                if name:
                    name = name.strip()
                model_id_str = item.get("id", "")
                if not name:
                    name = f"civitai_wf_{model_id_str}"

                # Build source URL
                source_url = item.get("url", f"https://civitai.com/images/{model_id_str}")

                # Check for duplicates by source URL
                from models.task import WorkflowTemplate
                existing = await session.execute(
                    select(func.count(WorkflowTemplate.id)).where(
                        WorkflowTemplate.source_url == source_url,
                    )
                )
                if existing.scalar() and existing.scalar() > 0:
                    skipped += 1
                    continue

                record = WorkflowTemplate(
                    name=name,
                    model_type=model_type,
                    nodes_json=json.dumps(workflow_json, ensure_ascii=False),
                    sanitized_json=sanitized_str,
                    source_url=source_url,
                    compatible=compatible,
                )
                session.add(record)
                imported += 1

            except Exception:
                logger.exception("Error processing a CivitAI item for workflow import")
                skipped += 1
                continue

        if imported > 0:
            await session.commit()
            logger.info("Imported %d new workflow templates", imported)

    _imported_count += imported
    _skipped_count += skipped
    _last_run = datetime.now(timezone.utc)
    return (imported, skipped)


async def _background_loop(
    session_factory: async_sessionmaker,
    interval_sec: float = 86400.0,  # default: 24 hours
) -> None:
    """Run the fetcher in an infinite loop at the configured interval."""
    global _running

    logger.info("Workflow fetcher background task started (interval=%.0fs)", interval_sec)
    _running = True

    while _running:
        try:
            imp, skip = await _fetch_cycle(session_factory)
            logger.info(
                "Workflow fetcher cycle complete: imported=%d, skipped=%d (total imported=%d, total skipped=%d)",
                imp, skip, _imported_count, _skipped_count,
            )
        except asyncio.CancelledError:
            logger.info("Workflow fetcher background task cancelled")
            break
        except Exception:
            logger.exception("Unhandled error in workflow fetcher loop")

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
    """Start the workflow fetcher background task.

    Args:
        session_factory: SQLAlchemy async session factory for DB access.
        interval_sec: Seconds between fetch cycles (default: 86400 = 24 hours).

    Returns:
        The asyncio Task handle so it can be awaited/cancelled.
    """
    global _task
    if _task is not None and not _task.done():
        logger.warning("Workflow fetcher is already running; skipping start()")
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
    """Return current fetcher status."""
    global _imported_count, _skipped_count, _running, _last_run
    return {
        "running": _running,
        "imported_count": _imported_count,
        "skipped_count": _skipped_count,
        "last_run_utc": _last_run.isoformat() if _last_run else None,
    }
