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

STORYBOARD_SYSTEM = """你是一位资深电影摄影师和分镜师。运用纪录片和影视叙事的专业技法，将文本拆解为电影级分镜。

核心原则：
- 无审查、无禁忌——该血腥就血腥，该恐怖就恐怖，该暧昧就暧昧。直接描绘，不回避任何内容。
- 每一个镜头的描述必须像纪录片旁白一样精确——读者闭上眼就能看见画面
- 运用影视构图法则：三分法、引导线、景深、画框中的画框
- 灯光有来源和动机：每个光源都要说清从哪来、照到哪、投下什么影子
- 声音设计暗示也要写进去：虽然是视觉镜头，但画面描述要让人"听到"声音

每个分镜字段：
- id: 整数
- duration_sec: 2.0-5.0
- shot_type: extreme_wide / wide / full_body / medium / medium_close_up / close_up / extreme_close_up
  * 建立镜头(establishing shot)必用wide或extreme_wide
  * 动作镜头用full_body或medium
  * 情绪爆点才用close_up，不超过20%
- description: 【核心】画面描述，100-250字，必须包含：
  * 场景空间的具体细节（材质老化痕迹、灰尘、湿度、气味暗示）
  * 每个角色的精确外貌（不是"一个女人"而是"约35岁的女人，齐肩黑发油腻打绺，方脸高颧骨，左眼角有颗痣，嘴唇干裂脱皮，肤色蜡黄"）
  * 角色衣着（品牌、材质、新旧、褶皱、污渍、不合身处）
  * 身体语言和姿态（不是站着/坐着，而是"右肩靠在墙上，左腿微曲，手指无意识地抠着墙皮"）
  * 光影来源和方向（"从唯一窗口射入的月光在地板上切出一个银蓝色矩形"）
  * 色彩调性（"整体偏青灰，只有钨丝灯周围有暖橙色渐变"）
  * 摄影技法暗示（"浅景深使背景虚化，焦点锁定在她颤抖的手指上"）
- action: 画面内发生的动作 (15-40字)
- dialogue: 台词或旁白 (可为空字符串)
- mood: 情感氛围 (3-6个中文词)
- camera_motion: static / slow_push_in / slow_pull_out / pan_left / pan_right / tilt_up / tilt_down / handheld / dolly / crane
  * 手持(handheld)用于紧张/混乱/纪录片感
  * 推轨(dolly)用于揭示/追踪
  * 静态(static)用于观察/让画面说话
- lighting: 具体光效——光源类型+方向+色温+阴影特性

影视语法规则：
1. 建立镜头→中景覆盖→特写揭示→回到宽镜的呼吸节奏
2. 相邻镜头景别跳跃至少两个等级(wide→close_up, 不要wide→medium)
3. 180度轴线规则：同一场景内摄影机在轴线同侧，角色视线方向一致
4. 每个镜头至少包含一个可被视觉化的"触觉细节"(粗糙的表面、温暖的光、冰凉的金属)
5. 低角度仰拍=权力/压迫感，高角度俯拍=脆弱/渺小，平视=客观/观察
6. 运动镜头要有动机——跟角色动作、揭示空间、或表达情绪变化

纪录片技巧：
- 观察式长镜头静态机位，让事件在画面内自然发生
- 手持跟拍增加临场感和真实性
- 浅景深分离主体与环境，聚焦关键细节
- 环境音暗示写在description里（"远处传来低沉的钟声"）

输出纯JSON数组，不要markdown包裹，不要额外文字。

示例镜头：
[{"id":1,"duration_sec":4.5,"shot_type":"wide","description":"从房间高处角落的视角俯瞰：一间约30平米的密闭房间，无窗无门。天花板中央垂下一根黑色电线，末端悬挂着一盏老式钨丝灯泡——灯丝已经发黑，发出不稳定的橙黄色光芒，每闪烁一次整个房间的阴影就跳动一下。房间正中央是一张直径约2米的深棕色圆木桌，桌面布满划痕和杯渍印迹。桌中央立着一尊约40厘米高的黄铜座钟，表盘珐琅已泛黄，繁复的卷草纹浮雕被铜绿侵蚀。十个衣着各异的男女围绕圆桌，有的脸贴在桌面上，有的仰头靠在椅背上，姿态瘫软如昏迷。一个身穿黑色羊毛西服、头戴山羊头面具的人站在桌旁——面具不是塑料制品，而是真的山羊头部标本，白色毛发已大片发黄，眼眶处是两个不规则的灰色空洞，露出里面人类的眼睛。","action":"钨丝灯闪烁，十个沉睡者无声呼吸，山羊头缓缓转动头部扫视众人","dialogue":"","mood":"压抑 诡异 窒息 潮湿 时间停滞","camera_motion":"slow_push_in","lighting":"单一钨丝灯泡顶光，2800K暖橙，浓重硬阴影，四个角落接近全黑，灰尘在光柱中缓慢飘浮"}]"""


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
