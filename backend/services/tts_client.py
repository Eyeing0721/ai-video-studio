"""Aliyun Bailian Qwen TTS client — voice generation with optional voice cloning.

API docs: https://help.aliyun.com/document_detail/bailian-tts.html

Features:
- Text-to-speech with pre-built voices
- Voice cloning from 3-10s reference audio
- Output: raw WAV (no background music)
"""

import asyncio
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Optional

import httpx

from config import config

logger = logging.getLogger(__name__)

BAILIAN_KEY = config["bailian_api_key"]
BAILIAN_BASE = "https://dashscope.aliyuncs.com/api/v1"


class BailianTTSClient:
    """Async client for Aliyun Bailian Qwen TTS."""

    def __init__(self, api_key: str = BAILIAN_KEY):
        self.api_key = api_key
        self.base = BAILIAN_BASE

    async def _post(self, path: str, body: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{self.base}{path}", headers=headers, json=body)
            r.raise_for_status()
            return r.json()

    async def synthesize(
        self,
        text: str,
        voice_id: str = "cosyvoice-v1",
        speed: float = 1.0,
        volume: int = 50,
        output_path: Optional[Path] = None,
    ) -> bytes:
        """Generate speech from text using a pre-built voice ID.

        Common voices: cosyvoice-v1 (通用男声), cosyvoice-v2 (通用女声), or custom IDs from Bailian console.
        """
        body = {
            "model": "qwen-tts",
            "input": {"text": text},
            "parameters": {
                "voice": voice_id,
                "speed": speed,
                "volume": volume,
                "format": "wav",
            },
        }

        result = await self._post("/services/aigc/multimodal-generation/generation", body)
        audio_url = result.get("output", {}).get("audio", {}).get("url", "")

        if not audio_url:
            raise RuntimeError(f"TTS returned no audio URL: {result}")

        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(audio_url)
            r.raise_for_status()
            audio_bytes = r.content

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(audio_bytes)

        return audio_bytes

    async def clone_voice(
        self,
        text: str,
        reference_audio_path: str | Path,
        output_path: Optional[Path] = None,
    ) -> bytes:
        """Generate speech with voice cloned from reference audio (3-10 seconds)."""

        import base64

        ref_path = Path(reference_audio_path)
        ref_bytes = ref_path.read_bytes()
        ref_b64 = base64.b64encode(ref_bytes).decode()

        body = {
            "model": "qwen-tts",
            "input": {
                "text": text,
                "reference_audio": ref_b64,
            },
            "parameters": {
                "format": "wav",
            },
        }

        result = await self._post("/services/aigc/multimodal-generation/generation", body)
        audio_url = result.get("output", {}).get("audio", {}).get("url", "")

        if not audio_url:
            raise RuntimeError(f"Voice clone TTS returned no audio URL: {result}")

        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(audio_url)
            r.raise_for_status()
            audio_bytes = r.content

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(audio_bytes)

        return audio_bytes

    async def generate_shot_audio(
        self,
        task_output_dir: Path,
        shot_id: int,
        dialogue: str,
        voice_id: str = "cosyvoice-v1",
    ) -> Path:
        """Generate TTS for a single shot's dialogue and save to disk."""
        if not dialogue or not dialogue.strip():
            # Create silent placeholder
            audio_path = task_output_dir / "shots" / f"{shot_id:03d}" / "audio.wav"
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            # 0.5s silence
            audio_path.write_bytes(b"\x00" * 8000)
            return audio_path

        audio_path = task_output_dir / "shots" / f"{shot_id:03d}" / "audio.wav"
        await self.synthesize(
            text=dialogue.strip(),
            voice_id=voice_id,
            output_path=audio_path,
        )
        logger.info(f"TTS generated: shot {shot_id}, {len(dialogue)} chars -> {audio_path}")
        return audio_path


# Singleton
tts = BailianTTSClient()
