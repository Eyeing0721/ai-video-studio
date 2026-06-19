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
MODEL = "deepseek-v4-pro[1m]"
MODEL_LONG = "deepseek-v4-pro[1m]"
THINKING_BUDGET = 4096  # max reasoning tokens
TEMPERATURE = 0.9       # higher creativity for diverse shots

from services.prompt_knowledge import get_prompt_knowledge

STORYBOARD_SYSTEM = """你是一位资深电影摄影师和分镜师。运用纪录片和影视叙事的专业技法，将文本拆解为电影级分镜。

【已学习知识库——以下知识必须应用于每个镜头】
""" + get_prompt_knowledge() + """

【默认风格】统一使用 Photorealistic/Hyperrealistic 超写实风格。追求真实的人物、真实的场景、真实的光影。

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
  * 【每个镜头必须包含】场景空间——不是泛写"房间里"，而是具体到"约30平米的密闭房间，没有窗户，四面是发黄的乳白色石灰墙，墙皮在四个角落处大面积剥落露出灰色水泥，天花板约3米高，中央垂下一根编织电线"。要写房间尺寸、墙壁材质颜色状态、地面材质、家具位置大小材质、光源数量和位置、温度湿度暗示、空气可见度（灰尘/烟雾）。每个镜头的场景描述不得省略，必须在150字以内把空间说清楚。
  * 每个角色必须明确定义【国籍+年龄+身高体型+发型发色+脸型+五官特征+肤色+独特标志】：
    - 国籍和民族必须明确（中国人/日本人/韩国人/俄罗斯人/印度人/美国人/英国人/中东人等），影响面部骨骼结构、肤色、毛发特征
    - 精确年龄（不是"年轻"，是"23岁"或"看起来不超过19岁"或"约45岁，眼角有细纹"）
    - 发型要具体（不是"长发"，是"及腰黑色直发，中分，发尾有分叉，左侧鬓角别到耳后，右侧自然垂落遮住半边脸"）
    - 五官逐个描述（眉形/眼睛形状和间距/鼻子高度和宽窄/嘴唇厚薄和颜色/下巴形状/颧骨高低/耳朵大小和角度）
    - 不要模板化的"帅""美"。要真人：不对称的、有瑕疵的、有辨识度的
    - 每个角色必须有至少一个"在人群中一眼认出"的独特标志
- action: 【铁律】所有角色不得直视镜头。角色只看场景内的物体、其他角色、或自己的手。眼神方向必须合理——看对方眼睛、看桌上的物品、看地面、看墙上的点。绝对禁止角色看向摄影机方向。
  * 角色衣着（品牌、材质、新旧、褶皱、污渍、不合身处）
  * 身体语言和姿态（不是站着/坐着，而是"右肩靠在墙上，左腿微曲，手指无意识地抠着墙皮"）
  * 光影来源和方向（"从唯一窗口射入的月光在地板上切出一个银蓝色矩形"）
  * 色彩调性（"整体偏青灰，只有钨丝灯周围有暖橙色渐变"）
  * 摄影技法暗示（"浅景深使背景虚化，焦点锁定在她颤抖的手指上"）
- action: 画面内发生的动作 (15-40字)
- dialogue: 台词或旁白 (可为空字符串)
- mood: 情感氛围 (3-6个中文词)
- camera_motion: 【必须选择，不能用static】slow_push_in / slow_pull_out / pan_left / pan_right / tilt_up / tilt_down / handheld / dolly / crane / orbit / dutch_angle_tilt
  * 每个镜头必须有摄影机运动！即使是对话镜头也要有微小的推拉或手持微晃
  * handheld: 紧张/混乱/纪录片临场感（微晃0.5-2cm幅度）
  * slow_push_in: 情绪递进/揭示/紧张升级
  * dolly/追踪: 跟随角色动作
  * orbit: 环绕角色制造空间感
  * pan/tilt: 展示环境/角色视线引导
  * action描述中也要体现运镜产生的画面变化（如"镜头缓缓推近，他的表情从阴影中逐渐显现"）
- lighting: 具体光效——光源类型+方向+色温+阴影特性

【最高优先级】场景与人物一致性圣经：
- 在第一个分镜的description中必须完整描述场景空间（房间尺寸/墙壁材质/光源位置/家具布局/物品清单）
- 在第一个出现某角色的分镜中必须完整定义其外貌（年龄/身高体型/发型发色/脸型/五官特征/肤色纹理/衣着/体态）
- 后续所有分镜必须复用这些定义，不得新增或改变任何细节
- 光照方向、物品位置、角色衣着一经定义，后续镜头中绝不改变
- 如果镜头1里钨丝灯在桌子正上方，镜头5里钨丝灯必须还在桌子正上方
- 每个镜头description末尾用括号标注「同场景#1」「同角色定义」，表明继承关系

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

每个分镜新增english_prompt字段——用于AI图像生成模型的英文长提示词。格式要求：
- 全部用英文，详细描述画面，包含所有角色外貌、衣着、场景、光影细节
- 开头必须加画质修饰词：hyperrealistic, photorealistic, 8k, cinematic lighting, volumetric lighting, ray tracing, subsurface scattering, shallow depth of field, film grain, anamorphic lens, arri alexa, shot on 35mm
- 结尾必须加统一风格词：dark atmospheric, moody cinematography, professional color grading, masterpiece, trending on artstation
- 镜头类型对应修饰：close-up加skin texture/pores/细节，wide加epic scale/architectural/环境细节
- 长度150-400个英文单词

示例镜头：
[{"id":1,"duration_sec":4.5,"shot_type":"wide","description":"从房间高处角落的视角俯瞰...（中文同前）","english_prompt":"hyperrealistic, photorealistic, 8k raw, cinematic lighting, volumetric lighting with visible dust particles in light beam, ray tracing global illumination, anamorphic lens flare, shot on Arri Alexa 65, 35mm film grain. Wide establishing shot from high corner angle of a sealed 30-square-meter room with no windows or doors. Peeling cream-colored lime plaster walls with gray concrete exposed at corners, 3-meter ceiling. Single flickering tungsten filament bulb hanging from black braided wire at center, casting unstable 2800K warm orange light that makes shadows jump with each flicker. Thick layer of dust motes dancing slowly in the light cone. Dark brown round wooden table 2 meters diameter at center, surface covered with scratches, cup rings, and decades of wear. Antique brass mantel clock 40cm tall at table center, enamel face yellowed with age, intricate acanthus leaf relief corroded by green patina. Ten men and women of various ages slumped around the table — some faces pressed against wood, others leaning back in chairs, all in deep unconsciousness. One figure stands beside the table: tall lean man in tailored black wool suit, wearing an actual taxidermied goat head as a mask — yellowed white fur matted and clumped, irregular gray eye holes revealing wet human eyes behind. Deep shadows in all four corners, almost black. dark atmospheric, moody cinematography, professional color grading, masterpiece, trending on artstation","action":"钨丝灯闪烁，十个沉睡者无声呼吸，山羊头缓缓转动头部扫视众人","dialogue":"","mood":"压抑 诡异 窒息 潮湿 时间停滞","camera_motion":"slow_push_in","lighting":"单一钨丝灯泡顶光，2800K暖橙，浓重硬阴影，四个角落接近全黑，灰尘在光柱中缓慢飘浮"}]"""


STORYBOARD_USER = """Create a cinematography storyboard for this story. Output ONLY a JSON array of shots. Keep it simple and valid.

Each shot object:
{{
  "id": 1,
  "duration_sec": 3.5,
  "shot_type": "wide/medium/close_up etc",
  "camera_motion": "specific camera move",
  "prompt_image": "English AI image prompt. MUST capture the MOMENT BEFORE the main action. Include: hyperrealistic, photorealistic, 8k raw quality modifiers at start. Include: detailed character appearance, scene description, lighting. End with: masterpiece, cinematic.",
  "prompt_video": "English AI video prompt. Describe MOTION + CAMERA MOVEMENT only. Visual details come from the image.",
  "dialogue_cn": "Chinese dialogue (can be empty string)",
  "mood": "3-6 English mood keywords"
}}

Keep each prompt_image 100-200 words. Keep prompt_video 20-50 words.
Output ONLY the JSON array. No markdown, no explanation.

Story: {text}"""


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
        "max_tokens": 65536,
        "system": STORYBOARD_SYSTEM,
        "messages": [{"role": "user", "content": user_msg}],
        "thinking": {"type": "disabled"},
        "temperature": TEMPERATURE,
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
        "temperature": 0.9,
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
        "temperature": 0.9,
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
        "temperature": 0.9,
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
