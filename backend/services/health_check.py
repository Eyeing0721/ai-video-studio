"""Startup environment health check for AI Video Studio.

Verifies every dependency before a pipeline runs so we can distinguish
"not ready yet" from "failed at runtime".
"""

import asyncio
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

import httpx

from config import config

logger = logging.getLogger(__name__)

# Minimum free disk space required (50 GB)
MIN_FREE_DISK_GB = 50

# Model -> ComfyUI folder name mapping (covers diffusion_models, unet, checkpoints)
_MODEL_FOLDERS = [
    "diffusion_models",
    "unet",
    "checkpoints",
]


async def _check_comfyui() -> dict:
    """Verify ComfyUI service is reachable via GET /system_stats."""
    url = config["comfyui_url"].rstrip("/")
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{url}/system_stats")
            r.raise_for_status()
        return {"status": "ok", "detail": "ComfyUI reachable"}
    except httpx.ConnectError:
        return {"status": "error", "detail": f"Connection refused at {url}"}
    except httpx.TimeoutException:
        return {"status": "error", "detail": f"Timeout connecting to {url}"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}


async def _check_models() -> dict[str, bool]:
    """Check required model files via ComfyUI /models/{folder} API.

    Returns a dict keyed by model config key (e.g. "z_image", "wan_i2v_high")
    with boolean values indicating whether the model was found.
    """
    url = config["comfyui_url"].rstrip("/")
    model_names: dict[str, str] = config.get("models", {})

    results: dict[str, bool] = {}

    # Fetch model lists from all relevant folders, cache per folder
    folder_contents: dict[str, list[str]] = {}
    for folder in _MODEL_FOLDERS:
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(f"{url}/models/{folder}")
                if r.status_code == 200:
                    folder_contents[folder] = r.json()
                else:
                    folder_contents[folder] = []
        except Exception:
            folder_contents[folder] = []

    # Check each configured model against all folders
    for key, name in model_names.items():
        found = False
        for folder, files in folder_contents.items():
            if name in files:
                found = True
                break
        results[key] = found

    return results


def _check_ffmpeg() -> bool:
    """Verify FFmpeg is available on PATH."""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        try:
            subprocess.run(
                [ffmpeg_path, "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
            return True
        except Exception:
            return False
    return False


def _check_output_writable() -> bool:
    """Verify the configured output directory is writable."""
    output_dir = Path(config["output_dir"])
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        test_file = output_dir / ".health_check_write_test"
        test_file.write_text("ok")
        test_file.unlink()
        return True
    except Exception:
        return False


def _check_disk_space() -> float:
    """Return free disk space in GB on the output drive."""
    output_dir = Path(config["output_dir"])
    try:
        usage = shutil.disk_usage(output_dir)
        return usage.free / (1024 ** 3)  # bytes -> GB
    except Exception:
        return -1.0


def _check_deepseek_api() -> bool:
    """Verify DeepSeek API key is configured (non-empty)."""
    key = config.get("deepseek_api_key", "")
    return bool(key and key.strip())


async def run_health_check() -> dict[str, Any]:
    """Run all health checks and return the composite result.

    Returns:
        {
            "comfyui": {"status": "ok"|"error", "detail": "..."},
            "models": {"z_image": True|False, "wan_i2v_high": True|False, ...},
            "ffmpeg": True|False,
            "disk_space_gb": 123.4,
            "deepseek_api": True|False,
            "overall": "ready"|"degraded"|"blocked"
        }
    """
    comfyui = await _check_comfyui()
    ffmpeg = _check_ffmpeg()
    output_writable = _check_output_writable()
    disk_space_gb = _check_disk_space()
    deepseek_api = _check_deepseek_api()

    # Models check requires ComfyUI to be reachable
    if comfyui["status"] == "ok":
        models = await _check_models()
    else:
        models = {}

    # Determine overall status
    blocked = False
    degraded = False

    # BLOCKED if ComfyUI is unreachable
    if comfyui["status"] != "ok":
        blocked = True

    # DEGRADED if any model is missing
    if models and not all(models.values()):
        degraded = True

    # DEGRADED if FFmpeg missing
    if not ffmpeg:
        degraded = True

    # DEGRADED if output dir not writable (but not blocked since we might fix it)
    if not output_writable:
        degraded = True

    # BLOCKED if disk space below threshold
    if disk_space_gb < MIN_FREE_DISK_GB:
        blocked = True

    # BLOCKED if DeepSeek API key not configured
    if not deepseek_api:
        blocked = True

    if blocked:
        overall = "blocked"
    elif degraded:
        overall = "degraded"
    else:
        overall = "ready"

    return {
        "comfyui": comfyui,
        "models": models,
        "ffmpeg": ffmpeg,
        "disk_space_gb": round(disk_space_gb, 1),
        "deepseek_api": deepseek_api,
        "overall": overall,
    }
