"""Workflow manager — import, validate, and manage ComfyUI workflow JSONs.

Features:
- Import workflows from local files or URLs
- Detect and auto-bypass Prompt Enhance / Prompt Optimizer nodes
- Validate compatibility with installed models
- Store in DB with tags
"""

import json
import logging
from pathlib import Path
from typing import Optional

import httpx

from config import config

logger = logging.getLogger(__name__)

# Node class types that should be bypassed (DeepSeek handles prompt engineering)
BYPASS_NODE_TYPES = [
    "PromptEnhance",
    "PromptOptimizer",
    "LLMPrompt",
    "GeminiPromptOptimizer",
    "PromptGen",
    "PromptStyler",
    "SDXLPromptStyler",
    "PromptGenerate",
    "TextGenerate",
]

# Known prompt-enhancing substrings in node titles
BYPASS_TITLE_KEYWORDS = [
    "prompt enhance",
    "prompt optimize",
    "prompt gen",
    "prompt styler",
    "prompt assistant",
    "llm prompt",
    "gemini prompt",
    "text generate",
]


def validate_workflow(workflow: dict) -> tuple[bool, str, dict]:
    """Validate a workflow JSON.

    Returns:
        (is_valid, message, info) where info has stats about the workflow.
    """
    if not isinstance(workflow, dict):
        return False, "Workflow must be a JSON object", {}

    node_count = 0
    bypass_count = 0
    model_refs: set[str] = set()
    issues: list[str] = []

    for node_id, node_data in workflow.items():
        if not isinstance(node_data, dict):
            issues.append(f"Node {node_id}: invalid format")
            continue

        class_type = node_data.get("class_type", "")
        if not class_type:
            continue

        node_count += 1

        # Check for prompt enhancer nodes
        if class_type in BYPASS_NODE_TYPES:
            bypass_count += 1

        # Check inputs for model references
        inputs = node_data.get("inputs", {})
        for key, value in inputs.items():
            if isinstance(value, str) and any(value.endswith(ext) for ext in [".safetensors", ".gguf", ".ckpt", ".pt"]):
                model_refs.add(value)

        # Check title
        title = node_data.get("_meta", {}).get("title", "")
        if any(kw in title.lower() for kw in BYPASS_TITLE_KEYWORDS):
            bypass_count += 1

    info = {
        "node_count": node_count,
        "bypass_count": bypass_count,
        "model_refs": sorted(model_refs),
        "issues": issues,
    }

    if node_count == 0:
        return False, "Workflow contains no valid nodes", info

    return True, f"Valid workflow with {node_count} nodes, {bypass_count} prompt enhancers detected", info


def sanitize_workflow(workflow: dict) -> dict:
    """Remove or bypass prompt-enhancer nodes from a workflow.

    Strategy: mark bypassed nodes as muted and bypass their outputs.
    """
    import copy
    sanitized = copy.deepcopy(workflow)

    nodes_to_bypass: list[str] = []
    for node_id, node_data in sanitized.items():
        class_type = node_data.get("class_type", "")
        title = node_data.get("_meta", {}).get("title", "")

        if class_type in BYPASS_NODE_TYPES or any(kw in title.lower() for kw in BYPASS_TITLE_KEYWORDS):
            nodes_to_bypass.append(node_id)
            node_data["_bypassed"] = True
            node_data["_bypass_reason"] = "DeepSeek V4 Pro handles prompt engineering at storyboard level"

    logger.info(f"Sanitized workflow: bypassed {len(nodes_to_bypass)} prompt enhancer nodes: {nodes_to_bypass}")
    return sanitized


async def fetch_workflow_from_url(url: str) -> dict:
    """Download a workflow JSON from a URL."""
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get(url)
        r.raise_for_status()
        data = r.json()

    if isinstance(data, dict) and "workflow" in data:
        # Some sites wrap workflows
        data = data["workflow"]
    if isinstance(data, dict) and "prompt" in data:
        # ComfyUI API format
        data = data["prompt"]

    return data


async def import_workflow(
    source: str | Path | dict,
    name: str = "",
) -> dict:
    """Import a workflow from file path, URL, or raw dict.

    Returns:
        {"name": str, "nodes": dict, "sanitized": dict, "info": dict}
    """
    workflow: dict = {}

    if isinstance(source, dict):
        workflow = source
    elif isinstance(source, Path) or (isinstance(source, str) and source.endswith(".json")):
        workflow = json.loads(Path(source).read_text(encoding="utf-8"))
    elif isinstance(source, str) and source.startswith("http"):
        workflow = await fetch_workflow_from_url(source)
    else:
        # Raw JSON string?
        workflow = json.loads(source)

    valid, msg, info = validate_workflow(workflow)
    if not valid:
        raise ValueError(f"Invalid workflow: {msg}")

    sanitized = sanitize_workflow(workflow)

    return {
        "name": name or "imported_workflow",
        "nodes": workflow,
        "sanitized": sanitized,
        "info": info,
        "validation": msg,
    }
