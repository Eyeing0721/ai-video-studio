import os
import json
from pathlib import Path

CONFIG_DIR = Path(os.environ.get('AVS_CONFIG_DIR', Path.home() / '.ai-video-studio'))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / 'config.json'

DEFAULTS = {
    'comfyui_url': 'http://127.0.0.1:8188',
    'deepseek_api_key': '',
    'deepseek_base_url': 'https://api.deepseek.com/anthropic',
    'bailian_api_key': '',
    'output_dir': 'N:/ai-video-studio-output',
    'media_library_dir': str(Path.home() / 'ai-video-studio' / 'media_library'),
    'models': {
        'z_image': 'z_image_turbo_bf16.safetensors',
        'wan_i2v_high': 'wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors',
        'wan_i2v_low': 'wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors',
        'sulphur_fp8': 'sulphur_dev_fp8mixed.safetensors',
        'sulphur_gguf': 'sulphur_dev-Q4_K_M.gguf',
    },
    'generation': {
        'z_image_width': 1024,
        'z_image_height': 1024,
        'sulphur_width': 1024,
        'sulphur_height': 1024,
        'wan_width': 640,
        'wan_height': 640,
        'upscale_factor': 4,
        'max_duration_sec': 120,
        'shot_duration_min': 2,
        'shot_duration_max': 5,
    },
}

def load_config() -> dict:
    cfg = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            cfg.update(json.load(f))
    # Local override (not committed)
    local_file = Path(__file__).parent / 'config.local.json'
    if local_file.exists():
        with open(local_file) as f:
            cfg.update(json.load(f))
    return cfg

def save_config(config: dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

config = load_config()
