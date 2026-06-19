"""
ComfyUI API client — build workflow JSONs, submit prompts, track execution.

ComfyUI API reference (from server.py):
  POST /prompt  {"prompt": {node_id: {class_type, inputs}}}
  GET  /history/{prompt_id}
  GET  /queue
  GET  /system_stats
  GET  /object_info
  WS   /ws?clientId=...  (status, executing, progress, executed)

Workflow JSON format:
  {
    "node_id": {
      "class_type": "NodeClassName",
      "inputs": {
        "param": value,           # literal
        "link": ["src_id", slot]  # connection to another node's output
      }
    }
  }

Nodes connect via ["source_node_id", output_slot_index] tuples.
"""

import asyncio
import json
import logging
import uuid
import time
from pathlib import Path
from typing import Any
import httpx
import websockets

from config import config

logger = logging.getLogger(__name__)

COMFY_URL = config["comfyui_url"]
MODELS = config["models"]
GEN = config["generation"]


class ComfyUIClient:
    """Async client for ComfyUI's REST + WebSocket API."""

    def __init__(self, base_url: str = COMFY_URL):
        self.base_url = base_url.rstrip("/")
        self.client_id = str(uuid.uuid4())
        self.ws = None

    # ── REST ──────────────────────────────────────────────

    async def _post(self, path: str, data: dict) -> dict:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(f"{self.base_url}{path}", json=data)
            r.raise_for_status()
            return r.json()

    async def _get(self, path: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base_url}{path}")
            r.raise_for_status()
            return r.json()

    async def system_stats(self) -> dict:
        return await self._get("/system_stats")

    async def health_check(self) -> bool:
        try:
            await self.system_stats()
            return True
        except Exception:
            return False

    async def get_models(self, folder: str) -> list[str]:
        """List models in a folder (e.g. 'diffusion_models', 'vae', 'loras')."""
        return await self._get(f"/models/{folder}")

    async def queue_prompt(self, workflow: dict) -> str:
        """Submit a workflow JSON, return prompt_id."""
        payload = {"prompt": workflow, "client_id": self.client_id}
        resp = await self._post("/prompt", payload)
        if "error" in resp:
            raise RuntimeError(f"ComfyUI rejected prompt: {resp['error']}")
        return resp["prompt_id"]

    async def get_history(self, prompt_id: str) -> dict:
        return await self._get(f"/history/{prompt_id}")

    async def upload_image(self, file_path: str | Path) -> dict:
        """Upload an image to ComfyUI's input directory."""
        path = Path(file_path)
        async with httpx.AsyncClient(timeout=30) as c:
            with open(path, "rb") as f:
                form = httpx.HTTPFiles({"image": (path.name, f, "image/png")})
                r = await c.post(f"{self.base_url}/upload/image", files=form, data={"overwrite": "true"})
                r.raise_for_status()
                return r.json()

    # ── WebSocket ─────────────────────────────────────────

    async def ws_connect(self):
        self.ws = await websockets.connect(
            f"{self.base_url.replace('http', 'ws')}/ws?clientId={self.client_id}"
        )

    async def ws_listen(self, prompt_id: str, on_progress=None, on_preview=None) -> dict:
        """Listen for execution events until prompt_id completes, return final outputs."""
        if not self.ws:
            await self.ws_connect()

        outputs: dict[str, list[dict]] = {}
        while True:
            msg = json.loads(await self.ws.recv())
            msg_type = msg.get("type")
            data = msg.get("data", {})

            if msg_type == "progress" and on_progress:
                await on_progress(data.get("value", 0), data.get("max", 1))
            elif msg_type == "executing":
                node_id = data.get("node")
                if node_id is None:
                    # Execution finished — fetch final outputs from history
                    history = await self.get_history(prompt_id)
                    prompt_data = history.get(prompt_id, {})
                    outputs = prompt_data.get("outputs", {})
                    break
            elif msg_type == "executed" and on_preview:
                await on_preview(data)

        return outputs

    async def ws_close(self):
        if self.ws:
            await self.ws.close()

    # ── Workflow builders ─────────────────────────────────

    def _node_id(self) -> str:
        """Generate a unique node ID (ComfyUI uses string keys)."""
        return str(int(time.time() * 1000) % 1000000)

    def build_txt2img_workflow(
        self,
        positive_prompt: str,
        negative_prompt: str = "",
        width: int = GEN["z_image_width"],
        height: int = GEN["z_image_height"],
        model_name: str = MODELS["z_image"],
        seed: int = -1,
    ) -> dict:
        """Build a Z-Image Turbo text-to-image workflow."""
        import random
        seed = seed if seed >= 0 else random.randint(0, 2**31 - 1)

        loader = self._node_id()
        clip = self._node_id()
        pos = self._node_id()
        neg = self._node_id()
        latent = self._node_id()
        sampler = self._node_id()
        decode = self._node_id()
        save = self._node_id()

        return {
            loader: {
                "class_type": "UNETLoader",
                "inputs": {"unet_name": model_name, "weight_dtype": "default"},
            },
            clip: {
                "class_type": "CLIPLoader",
                "inputs": {"clip_name": "t5xxl_fp8_e4m3fn.safetensors", "type": "wan", "device": "default"},
            },
            pos: {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": [clip, 0], "text": positive_prompt},
            },
            neg: {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": [clip, 0], "text": negative_prompt or "worst quality, blurry, distorted"},
            },
            latent: {
                "class_type": "EmptyLatentImage",
                "inputs": {"width": width, "height": height, "batch_size": 1},
            },
            sampler: {
                "class_type": "KSampler",
                "inputs": {
                    "model": [loader, 0], "positive": [pos, 0], "negative": [neg, 0],
                    "latent_image": [latent, 0], "seed": seed, "steps": 8, "cfg": 1.0,
                    "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0,
                },
            },
            decode: {
                "class_type": "VAEDecode",
                "inputs": {"samples": [sampler, 0], "vae": [loader, 1]},
            },
            save: {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": "avs_txt2img", "images": [decode, 0]},
            },
        }

    def build_img2video_workflow_wan(
        self,
        image_filename: str,
        positive_prompt: str,
        negative_prompt: str = "",
        width: int = GEN["wan_width"],
        height: int = GEN["wan_height"],
        length_frames: int = 81,
        seed: int = -1,
    ) -> dict:
        """Build a Wan 2.2 image-to-video workflow."""
        import random
        seed = seed if seed >= 0 else random.randint(0, 2**31 - 1)

        clip_loader = self._node_id()
        vae_loader = self._node_id()
        unet_high = self._node_id()
        unet_low = self._node_id()
        lora_high = self._node_id()
        lora_low = self._node_id()
        shift_high = self._node_id()
        shift_low = self._node_id()
        pos = self._node_id()
        neg = self._node_id()
        wan_i2v = self._node_id()
        samp_high = self._node_id()
        samp_low = self._node_id()
        decode = self._node_id()
        save = self._node_id()

        return {
            clip_loader: {
                "class_type": "CLIPLoader",
                "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default"},
            },
            vae_loader: {
                "class_type": "VAELoader",
                "inputs": {"vae_name": "wan_2.1_vae.safetensors"},
            },
            unet_high: {
                "class_type": "UNETLoader",
                "inputs": {"unet_name": MODELS["wan_i2v_high"], "weight_dtype": "default"},
            },
            unet_low: {
                "class_type": "UNETLoader",
                "inputs": {"unet_name": MODELS["wan_i2v_low"], "weight_dtype": "default"},
            },
            lora_high: {
                "class_type": "LoraLoaderModelOnly",
                "inputs": {"model": [unet_high, 0], "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors", "strength_model": 1.0},
            },
            lora_low: {
                "class_type": "LoraLoaderModelOnly",
                "inputs": {"model": [unet_low, 0], "lora_name": "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", "strength_model": 1.0},
            },
            shift_high: {
                "class_type": "ModelSamplingSD3",
                "inputs": {"model": [lora_high, 0], "shift": 5.0},
            },
            shift_low: {
                "class_type": "ModelSamplingSD3",
                "inputs": {"model": [lora_low, 0], "shift": 5.0},
            },
            pos: {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": [clip_loader, 0], "text": positive_prompt},
            },
            neg: {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": [clip_loader, 0], "text": negative_prompt or "static, blurry, low quality, distorted"},
            },
            wan_i2v: {
                "class_type": "WanImageToVideo",
                "inputs": {
                    "positive": [pos, 0], "negative": [neg, 0],
                    "vae": [vae_loader, 0], "start_image": image_filename,
                    "width": width, "height": height, "length": length_frames, "batch_size": 1,
                },
            },
            samp_high: {
                "class_type": "KSamplerAdvanced",
                "inputs": {
                    "model": [shift_high, 0], "positive": [wan_i2v, 0], "negative": [wan_i2v, 1],
                    "latent_image": [wan_i2v, 2], "add_noise": "enable", "noise_seed": seed,
                    "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple",
                    "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable",
                },
            },
            samp_low: {
                "class_type": "KSamplerAdvanced",
                "inputs": {
                    "model": [shift_low, 0], "positive": [wan_i2v, 0], "negative": [wan_i2v, 1],
                    "latent_image": [samp_high, 0], "add_noise": "disable", "noise_seed": seed,
                    "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple",
                    "start_at_step": 2, "end_at_step": 4, "return_with_leftover_noise": "disable",
                },
            },
            decode: {
                "class_type": "VAEDecode",
                "inputs": {"samples": [samp_low, 0], "vae": [vae_loader, 0]},
            },
            save: {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": "avs_i2v", "images": [decode, 0]},
            },
        }

    def build_img2video_workflow_sulphur(
        self,
        image_filename: str,
        positive_prompt: str,
        negative_prompt: str = "",
        width: int = GEN["sulphur_width"],
        height: int = GEN["sulphur_height"],
        length_frames: int = 81,
        seed: int = -1,
    ) -> dict:
        """Build a Sulphur 2 (LTX 2.3) image-to-video workflow.
        The prompt is auto-prefixed with no-speech constraint.
        """
        import random
        seed = seed if seed >= 0 else random.randint(0, 2**31 - 1)

        # Automatically inject no-speech directive
        speech_ban = "[no speech, no dialogue, silent, instrumental only]"
        if speech_ban not in positive_prompt.lower():
            positive_prompt = f"{speech_ban} {positive_prompt}"

        loader = self._node_id()
        clip = self._node_id()
        pos = self._node_id()
        neg = self._node_id()
        sampler = self._node_id()
        decode = self._node_id()
        save = self._node_id()

        return {
            loader: {
                "class_type": "LTXVLoader",
                "inputs": {
                    "ckpt_name": MODELS["sulphur_fp8"],
                    "vae_name": "sulphur_vae.safetensors",
                },
            },
            clip: {
                "class_type": "CLIPLoader",
                "inputs": {"clip_name": "sulphur_text_encoder.safetensors", "type": "ltxv", "device": "default"},
            },
            pos: {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": [clip, 0], "text": positive_prompt},
            },
            neg: {
                "class_type": "CLIPTextEncode",
                "inputs": {"clip": [clip, 0], "text": negative_prompt or "static, blurry, low quality, distorted, speech, talking"},
            },
            sampler: {
                "class_type": "LTXVScheduler",
                "inputs": {
                    "model": [loader, 0], "positive": [pos, 0], "negative": [neg, 0],
                    "image": image_filename, "seed": seed,
                    "width": width, "height": height, "length": length_frames,
                    "steps": 8, "cfg": 2.0,
                },
            },
            decode: {
                "class_type": "VAEDecode",
                "inputs": {"samples": [sampler, 0], "vae": [loader, 1]},
            },
            save: {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": "avs_sulphur", "images": [decode, 0]},
            },
        }

    def build_upscale_workflow(
        self,
        video_path: str,
        scale_factor: int = 4,
        model_name: str = "4x-UltraSharp.pth",
        frame_rate: int = 24,
    ) -> dict:
        """Build a video upscale workflow using GAN x4.

        Pipeline: UpscaleModelLoader -> VHS_LoadVideo -> ImageUpscaleWithModel -> VHS_VideoCombine
        The video_path should be a filename accessible from ComfyUI's input directory.
        """
        load_model = self._node_id()
        load_video = self._node_id()
        upscaler = self._node_id()
        combine = self._node_id()
        return {
            load_model: {
                "class_type": "UpscaleModelLoader",
                "inputs": {"model_name": model_name},
            },
            load_video: {
                "class_type": "VHS_LoadVideo",
                "inputs": {
                    "video": video_path,
                    "force_rate": 0,
                    "force_size": "Disabled",
                },
            },
            upscaler: {
                "class_type": "ImageUpscaleWithModel",
                "inputs": {
                    "upscale_model": [load_model, 0],
                    "images": [load_video, 0],
                },
            },
            combine: {
                "class_type": "VHS_VideoCombine",
                "inputs": {
                    "images": [upscaler, 0],
                    "frame_rate": frame_rate,
                    "format": "video/h264-mp4",
                    "pix_fmt": "yuv420p",
                    "filename_prefix": "avs_upscale",
                },
            },
        }

    # ── High-level runner ─────────────────────────────────

    async def run_workflow(
        self,
        workflow: dict,
        on_progress=None,
        on_preview=None,
        timeout: int = 600,
    ) -> dict:
        """Submit workflow, wait for completion, return outputs."""
        prompt_id = await self.queue_prompt(workflow)
        logger.info(f"ComfyUI prompt submitted: {prompt_id}")

        outputs = {}
        try:
            outputs = await asyncio.wait_for(
                self.ws_listen(prompt_id, on_progress, on_preview),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            logger.error(f"ComfyUI workflow timed out after {timeout}s, prompt_id={prompt_id}")
            raise
        finally:
            await self.ws_close()

        return {"prompt_id": prompt_id, "outputs": outputs}


# Singleton
comfyui = ComfyUIClient()
