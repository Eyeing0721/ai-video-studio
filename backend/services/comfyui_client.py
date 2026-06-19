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
        self._node_counter = 0

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
        """Generate a unique node ID."""
        self._node_counter += 1
        return str(self._node_counter)

    def build_txt2img_workflow(
        self,
        positive_prompt: str,
        negative_prompt: str = "",
        width: int = GEN["z_image_width"],
        height: int = GEN["z_image_height"],
        seed: int = -1,
        enable_upscale: bool = True,
    ) -> dict:
        """Build a Z-Image Turbo text-to-image workflow with optional 4x upscale.

        Uses standard ComfyUI nodes: UNETLoader + CLIPLoader (qwen lumina2) + KSampler.
        Based on verified working workflow: Text_to_Image_(Z-Image-Turbo)my.json
        """
        import random
        seed = seed if seed >= 0 else random.randint(0, 2**31 - 1)

        clip = self._node_id()
        vae = self._node_id()
        unet = self._node_id()
        sampling = self._node_id()
        positive = self._node_id()
        negative = self._node_id()
        latent = self._node_id()
        sampler = self._node_id()
        decode = self._node_id()

        nodes = {
            clip: {
                "class_type": "CLIPLoader",
                "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"},
            },
            vae: {
                "class_type": "VAELoader",
                "inputs": {"vae_name": "ae.safetensors"},
            },
            unet: {
                "class_type": "UNETLoader",
                "inputs": {"unet_name": MODELS["z_image"], "weight_dtype": "default"},
            },
            sampling: {
                "class_type": "ModelSamplingAuraFlow",
                "inputs": {"shift": 3, "model": [unet, 0]},
            },
            positive: {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": positive_prompt, "clip": [clip, 0]},
            },
            negative: {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": negative_prompt or "worst quality, blurry, distorted, lowres", "clip": [clip, 0]},
            },
            latent: {
                "class_type": "EmptySD3LatentImage",
                "inputs": {"width": width, "height": height, "batch_size": 1},
            },
            sampler: {
                "class_type": "KSampler",
                "inputs": {
                    "seed": seed, "steps": 8, "cfg": 1.0, "sampler_name": "res_multistep", "scheduler": "simple",
                    "denoise": 1.0, "model": [sampling, 0], "positive": [positive, 0],
                    "negative": [0, 0], "latent_image": [latent, 0],  # replaced below
                },
            },
            decode: {
                "class_type": "VAEDecode",
                "inputs": {"samples": [sampler, 0], "vae": [vae, 0]},
            },
        }

        # Add ConditioningZeroOut for negative
        conditioning_zero = self._node_id()
        nodes[conditioning_zero] = {
            "class_type": "ConditioningZeroOut",
            "inputs": {"conditioning": [negative, 0]},
        }
        # Fix the sampler's negative reference
        nodes[sampler]["inputs"]["negative"] = [conditioning_zero, 0]

        if enable_upscale:
            upscale_loader = self._node_id()
            upscaler = self._node_id()
            resize = self._node_id()
            save = self._node_id()
            nodes.update({
                upscale_loader: {
                    "class_type": "UpscaleModelLoader",
                    "inputs": {"model_name": "4x-UltraSharp.pth"},
                },
                upscaler: {
                    "class_type": "ImageUpscaleWithModel",
                    "inputs": {"upscale_model": [upscale_loader, 0], "image": [decode, 0]},
                },
                resize: {
                    "class_type": "ResizeImagesByLongerEdge",
                    "inputs": {"longer_edge": max(width, height) * 2, "images": [upscaler, 0]},
                },
                save: {
                    "class_type": "SaveImage",
                    "inputs": {"filename_prefix": "avs_txt2img", "images": [resize, 0]},
                },
            })
        else:
            save = self._node_id()
            nodes[save] = {
                "class_type": "SaveImage",
                "inputs": {"filename_prefix": "avs_txt2img", "images": [decode, 0]},
            }

        return nodes

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
        duration_sec: int = 8,
        fps: int = 25,
        seed: int = -1,
        enable_prompt_enhance: bool = False,
    ) -> dict:
        """Build a Sulphur 2 (LTX 2.3) image-to-video workflow.

        Based on verified working workflow: video_mysulphur_i2v.json
        Uses GGUF model + LTXV native nodes + LTXV latent upsampler.
        Prompt auto-prefixed with no-speech constraint.

        Args:
            image_filename: Input image file name (in ComfyUI input dir)
            positive_prompt: Text prompt
            width/height: Output dimensions (will be doubled by latent upsampler)
            duration_sec: Video duration in seconds
            fps: Frames per second
            enable_prompt_enhance: If True, use TextGenerateLTX2Prompt node
        """
        import random
        seed = seed if seed >= 0 else random.randint(0, 2**31 - 1)

        # Auto-inject no-speech directive
        speech_ban = "[no speech, no dialogue, silent, instrumental only]"
        if speech_ban not in positive_prompt.lower():
            positive_prompt = f"{speech_ban} {positive_prompt}"

        # ── Model loaders ──────────────────────────────────
        unet_gguf = self._node_id()      # UnetLoaderGGUF
        text_enc = self._node_id()       # LTXAVTextEncoderLoader
        vae = self._node_id()            # VAELoader
        audio_vae = self._node_id()      # LTXVAudioVAELoader

        # ── LoRA chain ─────────────────────────────────────
        lora_gemma = self._node_id()     # LoraLoader (gemma uncensored)
        lora_ltx = self._node_id()       # LoraLoaderModelOnly (distilled)

        # ── Prompt ─────────────────────────────────────────
        prompt_str = self._node_id()     # PrimitiveStringMultiline
        prompt_switch = self._node_id()  # ComfySwitchNode (enhance on/off)
        prompt_enhance = self._node_id() # TextGenerateLTX2Prompt
        prompt_enh_switch = self._node_id() # PrimitiveBoolean

        # ── Dimension/param primitives ─────────────────────
        p_width = self._node_id()        # PrimitiveInt
        p_height = self._node_id()       # PrimitiveInt
        p_fps = self._node_id()          # PrimitiveInt
        p_duration = self._node_id()     # PrimitiveInt
        p_bypass = self._node_id()       # PrimitiveBoolean (T2V switch)

        # ── Math ───────────────────────────────────────────
        math_length = self._node_id()    # ComfyMathExpression (duration*fps+1)
        math_fps = self._node_id()       # ComfyMathExpression (fps pass-through)
        math_w = self._node_id()         # ComfyMathExpression (width/2)
        math_h = self._node_id()         # ComfyMathExpression (height/2)

        # ── Text encoding ──────────────────────────────────
        pos_encode = self._node_id()     # CLIPTextEncode (positive)
        neg_encode = self._node_id()     # CLIPTextEncode (negative)
        condition = self._node_id()      # LTXVConditioning
        crop_guides = self._node_id()    # LTXVCropGuides

        # ── Image preprocessing ────────────────────────────
        resize_img = self._node_id()     # ResizeImagesByLongerEdge (1536)
        preprocess = self._node_id()     # LTXVPreprocess
        resize_mask = self._node_id()    # ResizeImageMaskNode

        # ── Latent space ───────────────────────────────────
        empty_latent = self._node_id()   # EmptyLTXVLatentVideo
        empty_audio = self._node_id()    # LTXVEmptyLatentAudio
        latent_upscaler = self._node_id()# LTXVLatentUpsampler
        img2video_init = self._node_id() # LTXVImgToVideoInplace (init)
        img2video_refine = self._node_id()# LTXVImgToVideoInplace (refine)

        # ── Samplers ───────────────────────────────────────
        sampler_select1 = self._node_id()# KSamplerSelect
        sampler_select2 = self._node_id()# KSamplerSelect
        sigmas1 = self._node_id()        # ManualSigmas
        sigmas2 = self._node_id()        # ManualSigmas
        cfg1 = self._node_id()           # CFGGuider
        cfg2 = self._node_id()           # CFGGuider
        noise1 = self._node_id()         # RandomNoise
        noise2 = self._node_id()         # RandomNoise

        # ── Sampling passes ────────────────────────────────
        sampler_pass1 = self._node_id()  # SamplerCustomAdvanced (noise→latent)
        sampler_pass2 = self._node_id()  # SamplerCustomAdvanced (refine)

        # ── Audio/Video concat ─────────────────────────────
        concat1 = self._node_id()        # LTXVConcatAVLatent
        concat2 = self._node_id()        # LTXVConcatAVLatent
        separate1 = self._node_id()      # LTXVSeparateAVLatent
        separate2 = self._node_id()      # LTXVSeparateAVLatent

        # ── Decode ─────────────────────────────────────────
        vae_decode = self._node_id()     # VAEDecodeTiled
        audio_decode = self._node_id()   # LTXVAudioVAEDecode
        create_video = self._node_id()   # CreateVideo

        nodes: dict[str, dict] = {
            # ── Image input (from LoadImage or passed via filename) ──
            "load_image": {
                "class_type": "LoadImage",
                "inputs": {"image": image_filename},
            },

            # ── Model loaders ──────────────────────────────
            unet_gguf: {
                "class_type": "UnetLoaderGGUF",
                "inputs": {"unet_name": MODELS["sulphur_gguf"]},
            },
            text_enc: {
                "class_type": "LTXAVTextEncoderLoader",
                "inputs": {
                    "text_encoder": "gemma_3_12B_it_fp4_mixed.safetensors",
                    "ckpt_name": MODELS["sulphur_fp8"],
                    "device": "default",
                },
            },
            vae: {
                "class_type": "VAELoader",
                "inputs": {"vae_name": "sulphur_vae.safetensors"},
            },
            audio_vae: {
                "class_type": "LTXVAudioVAELoader",
                "inputs": {"ckpt_name": MODELS["sulphur_fp8"]},
            },

            # ── LoRA ───────────────────────────────────────
            lora_gemma: {
                "class_type": "LoraLoader",
                "inputs": {
                    "lora_name": "gemma-3-12b-it-abliterated_lora_rank64_bf16.safetensors",
                    "strength_model": 1, "strength_clip": 1,
                    "model": [unet_gguf, 0], "clip": [text_enc, 0],
                },
            },
            lora_ltx: {
                "class_type": "LoraLoaderModelOnly",
                "inputs": {
                    "lora_name": "ltx-2.3-22b-distilled-lora-1.1_fro90_ceil72_condsafe.safetensors",
                    "strength_model": 0.5, "model": [lora_gemma, 0],
                },
            },

            # ── Prompt ─────────────────────────────────────
            prompt_str: {
                "class_type": "PrimitiveStringMultiline",
                "inputs": {"value": positive_prompt},
            },
            prompt_enh_switch: {
                "class_type": "PrimitiveBoolean",
                "inputs": {"value": enable_prompt_enhance},
            },
            prompt_enhance: {
                "class_type": "TextGenerateLTX2Prompt",
                "inputs": {
                    "prompt": [prompt_str, 0], "max_length": 2048,
                    "sampling_mode": "on", "thinking": False,
                    "use_default_template": True,
                    "clip": [lora_gemma, 1],
                },
            },

            # ── Params ─────────────────────────────────────
            p_width: {"class_type": "PrimitiveInt", "inputs": {"value": width}},
            p_height: {"class_type": "PrimitiveInt", "inputs": {"value": height}},
            p_fps: {"class_type": "PrimitiveInt", "inputs": {"value": fps}},
            p_duration: {"class_type": "PrimitiveInt", "inputs": {"value": duration_sec}},
            p_bypass: {"class_type": "PrimitiveBoolean", "inputs": {"value": False}},

            # ── Math ───────────────────────────────────────
            math_length: {
                "class_type": "ComfyMathExpression",
                "inputs": {"expression": "a * b + 1", "values.a": [p_duration, 0], "values.b": [p_fps, 0]},
            },
            math_fps: {
                "class_type": "ComfyMathExpression",
                "inputs": {"expression": "a", "values.a": [p_fps, 0]},
            },
            math_w: {
                "class_type": "ComfyMathExpression",
                "inputs": {"expression": "a/2", "values.a": [p_width, 0]},
            },
            math_h: {
                "class_type": "ComfyMathExpression",
                "inputs": {"expression": "a/2", "values.a": [p_height, 0]},
            },

            # ── Text encoding ──────────────────────────────
            pos_encode: {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": [prompt_str, 0], "clip": [lora_gemma, 1]},
            },
            neg_encode: {
                "class_type": "CLIPTextEncode",
                "inputs": {"text": negative_prompt or "pc game, cartoon, childish, ugly", "clip": [lora_gemma, 1]},
            },
            condition: {
                "class_type": "LTXVConditioning",
                "inputs": {
                    "frame_rate": [math_fps, 0],
                    "positive": [pos_encode, 0], "negative": [neg_encode, 0],
                },
            },
            crop_guides: {
                "class_type": "LTXVCropGuides",
                "inputs": {
                    "positive": [condition, 0], "negative": [condition, 1],
                    "latent": [separate1, 0],
                },
            },

            # ── Image preprocessing ────────────────────────
            resize_img: {
                "class_type": "ResizeImagesByLongerEdge",
                "inputs": {"longer_edge": 1536, "images": ["load_image", 0]},
            },
            preprocess: {
                "class_type": "LTXVPreprocess",
                "inputs": {"img_compression": 18, "image": [resize_img, 0]},
            },
            resize_mask: {
                "class_type": "ResizeImageMaskNode",
                "inputs": {
                    "resize_type": "scale dimensions",
                    "resize_type.width": [p_width, 0],
                    "resize_type.height": [p_height, 0],
                    "resize_type.crop": "center", "scale_method": "lanczos",
                    "input": ["load_image", 0],
                },
            },

            # ── Latent space ───────────────────────────────
            empty_latent: {
                "class_type": "EmptyLTXVLatentVideo",
                "inputs": {
                    "width": [math_w, 1], "height": [math_h, 1],
                    "length": [math_length, 1], "batch_size": 1,
                },
            },
            empty_audio: {
                "class_type": "LTXVEmptyLatentAudio",
                "inputs": {
                    "frames_number": [math_length, 1],
                    "frame_rate": [math_fps, 1],
                    "batch_size": 1,
                    "audio_vae": [audio_vae, 0],
                },
            },
            latent_upscaler: {
                "class_type": "LTXVLatentUpsampler",
                "inputs": {
                    "samples": [separate1, 0],
                    "upscale_model": ["ltx_upscaler", 0],
                    "vae": [vae, 0],
                },
            },
            "ltx_upscaler": {
                "class_type": "LatentUpscaleModelLoader",
                "inputs": {"model_name": "ltx-2.3-spatial-upscaler-x2-1.0.safetensors"},
            },

            # ── I2V stages ────────────────────────────────
            img2video_init: {
                "class_type": "LTXVImgToVideoInplace",
                "inputs": {
                    "strength": 0.7, "bypass": [p_bypass, 0],
                    "vae": [vae, 0], "image": [preprocess, 0],
                    "latent": [empty_latent, 0],
                },
            },
            img2video_refine: {
                "class_type": "LTXVImgToVideoInplace",
                "inputs": {
                    "strength": 1, "bypass": [p_bypass, 0],
                    "vae": [vae, 0], "image": [preprocess, 0],
                    "latent": [latent_upscaler, 0],
                },
            },

            # ── Samplers ───────────────────────────────────
            sampler_select1: {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
            sampler_select2: {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
            sigmas1: {"class_type": "ManualSigmas", "inputs": {"sigmas": "1.0, 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0"}},
            sigmas2: {"class_type": "ManualSigmas", "inputs": {"sigmas": "0.85, 0.7250, 0.4219, 0.0"}},
            cfg1: {
                "class_type": "CFGGuider",
                "inputs": {"cfg": 1, "model": [lora_ltx, 0], "positive": [condition, 0], "negative": [condition, 1]},
            },
            cfg2: {
                "class_type": "CFGGuider",
                "inputs": {"cfg": 1, "model": [lora_ltx, 0], "positive": [crop_guides, 0], "negative": [crop_guides, 1]},
            },
            noise1: {"class_type": "RandomNoise", "inputs": {"noise_seed": 42}},
            noise2: {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},

            # ── Sampling passes ────────────────────────────
            concat1: {
                "class_type": "LTXVConcatAVLatent",
                "inputs": {"video_latent": [img2video_init, 0], "audio_latent": [empty_audio, 0]},
            },
            sampler_pass1: {
                "class_type": "SamplerCustomAdvanced",
                "inputs": {
                    "noise": [noise1, 0], "guider": [cfg1, 0],
                    "sampler": [sampler_select1, 0], "sigmas": [sigmas1, 0],
                    "latent_image": [concat1, 0],
                },
            },
            separate1: {
                "class_type": "LTXVSeparateAVLatent",
                "inputs": {"av_latent": [sampler_pass1, 0]},
            },

            concat2: {
                "class_type": "LTXVConcatAVLatent",
                "inputs": {"video_latent": [img2video_refine, 0], "audio_latent": [empty_audio, 0]},
            },
            sampler_pass2: {
                "class_type": "SamplerCustomAdvanced",
                "inputs": {
                    "noise": [noise2, 0], "guider": [cfg2, 0],
                    "sampler": [sampler_select2, 0], "sigmas": [sigmas2, 0],
                    "latent_image": [concat2, 0],
                },
            },
            separate2: {
                "class_type": "LTXVSeparateAVLatent",
                "inputs": {"av_latent": [sampler_pass2, 0]},
            },

            # ── Decode ─────────────────────────────────────
            vae_decode: {
                "class_type": "VAEDecodeTiled",
                "inputs": {
                    "tile_size": 768, "overlap": 64,
                    "temporal_size": 4096, "temporal_overlap": 4,
                    "samples": [separate2, 0], "vae": [vae, 0],
                },
            },
            audio_decode: {
                "class_type": "LTXVAudioVAEDecode",
                "inputs": {"samples": [separate1, 1], "audio_vae": [audio_vae, 0]},
            },
            create_video: {
                "class_type": "CreateVideo",
                "inputs": {
                    "fps": [math_fps, 0],
                    "images": [vae_decode, 0],
                    "audio": [audio_decode, 0],
                },
            },
            self._node_id(): {
                "class_type": "SaveVideo",
                "inputs": {
                    "filename_prefix": "avs_sulphur",
                    "format": "auto", "codec": "auto",
                    "video": [create_video, 0],
                },
            },
        }

        return nodes

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
