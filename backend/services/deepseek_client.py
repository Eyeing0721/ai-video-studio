"""DeepSeek V4 Pro client — storyboarding + text creation via Anthropic-compatible API.

The user's Claude Code config routes to DeepSeek's Anthropic endpoint:
  base_url: https://api.deepseek.com/anthropic
  model: deepseek-v4-pro[1m]
  reasoning is available (extended thinking)

For storyboarding we enable reasoning; for text creation we use standard chat.
"""

import json
import logging
from typing import Optional

import httpx

from config import config

logger = logging.getLogger(__name__)

DEEPSEEK_URL = config["deepseek_base_url"].rstrip("/")
API_KEY = config["deepseek_api_key"]

# The model string from user's config
MODEL = "deepseek-v4-pro"
# With 1M context if the provider supports it — for storyboarding long novels
MODEL_LONG = "deepseek-v4-pro[1m]"

STORYBOARD_SYSTEM = """你是一位资深影视分镜师和导演。你的任务是将小说文本拆解为精确的分镜脚本。

每个分镜必须包含以下字段：
- id: 整数, 镜头编号
- duration_sec: 浮点数, 时长(秒), 范围2.0-5.0
- shot_type: 字符串, 景别 (extreme_wide/wide/medium/medium_close_up/close_up/extreme_close_up)
- description: 字符串, 画面描述 (中文, 30-80字, 包含构图、光影、色彩)
- action: 字符串, 角色动作 (中文, 10-30字)
- dialogue: 字符串, 台词或旁白 (中文, 可为空字符串)
- mood: 字符串, 氛围关键词 (中文, 2-5个词, 如"压抑 孤独 暖色调")
- camera_motion: 字符串, 镜头运动 (static/slow_push_in/slow_pull_out/pan_left/pan_right/tilt_up/tilt_down/handheld)
- lighting: 字符串, 光效描述 (如"暖色逆光 高对比度" 或 "柔光 低对比")

规则：
1. 每个分镜2-5秒, 适应短视频节奏
2. 动作幅度大的分镜缩短(2-3s), 情绪沉淀的分镜稍长(3-5s)
3. 台词/旁白需考虑语速(中文约3字/秒), 确保文字量在时长内读完
4. 相邻分镜的景别应有变化, 避免连续同景别
5. 关键情绪节点使用特写或大特写
6. 输出纯JSON数组, 不要markdown包裹, 不要额外文字

示例输出格式：
[{"id":1,"duration_sec":3.5,"shot_type":"medium_close_up","description":"...","action":"...","dialogue":"...","mood":"...","camera_motion":"slow_push_in","lighting":"..."}]"""


STORYBOARD_USER = """请将以下小说拆解为分镜脚本, 共{N}个分镜, 每个2-5秒。

小说内容：
{text}"""


async def generate_storyboard(
    text: str,
    shot_count: Optional[int] = None,
    api_key: str = API_KEY,
) -> list[dict]:
    """Generate a shot list from story text using DeepSeek V4 reasoning mode."""

    # Estimate shot count based on text length if not specified (~4 shots per 1000 chars)
    if shot_count is None:
        shot_count = max(4, min(40, len(text) // 250))

    user_msg = STORYBOARD_USER.format(N=shot_count, text=text[:30000])  # cap for API

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }

    body = {
        "model": MODEL,
        "max_tokens": 8192,
        "system": STORYBOARD_SYSTEM,
        "messages": [{"role": "user", "content": user_msg}],
        "thinking": {"type": "enabled", "budget_tokens": 2048},
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            f"{DEEPSEEK_URL}/v1/messages",
            headers=headers,
            json=body,
        )
        r.raise_for_status()
        data = r.json()

    if isinstance(data["content"], list):
        text_blocks = [b for b in data["content"] if b.get("type") == "text"]
        content = text_blocks[0]["text"] if text_blocks else data["content"][0].get("text", "")
    else:
        content = data["content"]

    # Parse JSON from response — strip markdown wrappers if present
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    shots = json.loads(content)
    logger.info(f"Storyboard generated: {len(shots)} shots")
    return shots


# ── Text creation ───────────────────────────────────────

CREATION_SYSTEM = """你是一位专业作家和故事策划。根据用户的需求创作高质量的中文小说内容。

写作要求：
1. 语言流畅自然, 避免AI腔
2. 情节有起承转合, 人物性格鲜明
3. 场景描写具体可感, 便于后续转化为画面
4. 对话简洁有力, 符合人物性格
5. 每段以可视觉化的场景为基础"""


async def continue_text(
    text: str,
    length: str = "3个段落",
    api_key: str = API_KEY,
) -> str:
    """Auto-continue a story from existing text."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    body = {
        "model": MODEL,
        "max_tokens": 4096,
        "system": CREATION_SYSTEM,
        "messages": [{
            "role": "user",
            "content": f"请续写以下故事, 续写{length}, 保持风格一致:\n\n{text}",
        }],
        "temperature": 0.8,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{DEEPSEEK_URL}/v1/messages", headers=headers, json=body)
        r.raise_for_status()
        data = r.json()

    return data["content"][0]["text"] if isinstance(data["content"], list) else data["content"]


async def expand_one_liner(
    sentence: str,
    word_count: int = 2000,
    api_key: str = API_KEY,
) -> str:
    """Expand a one-line description into a full story."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    body = {
        "model": MODEL,
        "max_tokens": 8192,
        "system": CREATION_SYSTEM,
        "messages": [{
            "role": "user",
            "content": f"根据以下一句话描述, 扩写为约{word_count}字的完整故事, 含起承转合结构:\n\n{sentence}",
        }],
        "temperature": 0.8,
    }

    async with httpx.AsyncClient(timeout=180) as client:
        r = await client.post(f"{DEEPSEEK_URL}/v1/messages", headers=headers, json=body)
        r.raise_for_status()
        data = r.json()

    return data["content"][0]["text"] if isinstance(data["content"], list) else data["content"]


async def structured_create(
    characters: str,
    persona: str,
    world: str,
    style: str,
    plot: str,
    word_count: int = 3000,
    api_key: str = API_KEY,
) -> str:
    """Create a story from structured elements."""
    prompt = f"""根据以下设定创作一篇约{word_count}字的中文小说：

角色名称：{characters}
角色人设：{persona}
世界观：{world}
风格：{style}
剧情走向：{plot}

要求：起承转合完整, 场景具象可感, 对话生动。"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    body = {
        "model": MODEL,
        "max_tokens": 8192,
        "system": CREATION_SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
    }

    async with httpx.AsyncClient(timeout=180) as client:
        r = await client.post(f"{DEEPSEEK_URL}/v1/messages", headers=headers, json=body)
        r.raise_for_status()
        data = r.json()

    return data["content"][0]["text"] if isinstance(data["content"], list) else data["content"]


async def auto_edit_instruction(
    instruction: str,
    current_recipe: dict,
    api_key: str = API_KEY,
) -> dict:
    """Translate natural language editing instructions into concrete parameter changes.

    Given a user instruction like '把第二幕氛围调暗一些' or '转场不要太花哨',
    returns a dict of parameter adjustments for the MLT pipeline and template recipe.
    """
    recipe_json = json.dumps(current_recipe, ensure_ascii=False, indent=2)
    system = """你是一位资深视频后期导演。用户会用自然语言描述想要的剪辑效果调整。
请分析指令，输出一个JSON对象，包含具体可执行的参数修改。

可调整的参数：
- transitions.type: 转场类型 (cross_dissolve, hard_cut, fade_out, wipe_left, zoom_in, dip_to_black, flash_white)
- transitions.duration_sec: 转场时长 (0.1-2.0)
- subtitles.font_size: 字幕字号
- subtitles.color: 字幕颜色
- subtitles.animation: 字幕动画 (fade, cut, pop, slide)
- bgm.ducking_ratio: BGM闪避比例 (0-1)
- bgm.volume_db: BGM音量
- color.contrast: 对比度 (0.5-2.0)
- color.saturation: 饱和度 (0-2.0)
- color.brightness: 亮度 (-1到1)
- timing.shot_duration_min: 最小镜头时长(秒)
- timing.shot_duration_max: 最大镜头时长(秒)
- global.vignette_intensity: 暗角强度 (0-1)
- global.film_grain: 胶片颗粒 (0-1)

只输出需要修改的参数，不改的不要输出。输出纯JSON，不要markdown包裹。

当前设置作为参考：
{recipe}

用户指令：{instruction}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    body = {
        "model": MODEL,
        "max_tokens": 1024,
        "system": system.format(recipe=recipe_json[:3000], instruction=instruction),
        "messages": [{"role": "user", "content": instruction}],
        "temperature": 0.3,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{DEEPSEEK_URL}/v1/messages", headers=headers, json=body)
        r.raise_for_status()
        data = r.json()

    if isinstance(data["content"], list):
        text_blocks = [b for b in data["content"] if b.get("type") == "text"]
        content = text_blocks[0]["text"] if text_blocks else data["content"][0].get("text", "")
    else:
        content = data["content"]
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    adjustments = json.loads(content)
    logger.info(f"Auto-edit: '{instruction[:50]}...' -> {len(adjustments)} parameter changes")
    return adjustments


async def revise_text(
    original_text: str,
    instruction: str,
    api_key: str = API_KEY,
) -> str:
    """Revise text based on natural language instruction, maintaining context."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    body = {
        "model": MODEL,
        "max_tokens": 8192,
        "system": "你是专业文字编辑。根据用户的修改指令修订文本, 保持上下文一致, 仅修改被要求的部分, 其余内容原样保留。",
        "messages": [{
            "role": "user",
            "content": f"原文：\n{original_text}\n\n修改指令：{instruction}\n\n请输出修订后的完整文本：",
        }],
        "temperature": 0.6,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{DEEPSEEK_URL}/v1/messages", headers=headers, json=body)
        r.raise_for_status()
        data = r.json()

    return data["content"][0]["text"] if isinstance(data["content"], list) else data["content"]
