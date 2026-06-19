"""Built-in editing presets — template skeletons for micro-drama, documentary, vlog.

Each template defines:
- timing: shot duration range, pacing rules, structure segments
- transitions: preferred transition types per segment
- subtitles: font, color, stroke, animation style
- bgm: ducking params, genre preference
- color: LUT preference, contrast target
- ai_hints: keywords that guide AI dynamic parameter decisions
"""

from typing import Optional

Template = dict

# ── Micro Drama (微短剧) ────────────────────────────────

MICRO_DRAMA: Template = {
    "id": "micro_drama",
    "name": "微短剧",
    "description": "快节奏、强冲突、高密度信息，适合60-120秒短剧",
    "timing": {
        "structure": [
            {"segment": "hook", "duration_pct": 0.2, "max_duration_sec": 15},
            {"segment": "friction", "duration_pct": 0.4, "max_duration_sec": 45},
            {"segment": "spike", "duration_pct": 0.25, "max_duration_sec": 30},
            {"segment": "button", "duration_pct": 0.15, "max_duration_sec": 10},
        ],
        "shot_duration_min": 1.5,
        "shot_duration_max": 3.0,
        "cut_every_n_seconds": 3,
        "bpm_preferred": 120,
    },
    "transitions": {
        "hook": ["hard_cut", "flash_white"],
        "friction": ["hard_cut", "j_cut"],
        "spike": ["hard_cut"],
        "button": ["dip_to_black"],
        "crossfade_duration_sec": 0.3,
    },
    "subtitles": {
        "font": "Noto Sans SC Bold",
        "font_size": 36,
        "color": "#FFFFFF",
        "stroke_color": "#000000",
        "stroke_width": 2,
        "animation": "cut",  # no fade-in, instant appearance
    },
    "bgm": {
        "ducking_ratio": 0.15,  # music to 15% during dialogue
        "ducking_attack_ms": 100,
        "ducking_release_ms": 500,
        "genre": ["electronic", "tension", "fast_beat"],
        "volume_db": -8,
    },
    "color": {
        "lut": "",  # auto-select
        "contrast": 1.2,
        "saturation": 1.1,
    },
    "ai_hints": [
        "快节奏剪辑, 每个镜头不超过3秒",
        "对话时硬切, 情绪变化时闪白",
        "高潮段使用快速交替镜头(0.5-1s切换)",
        "结尾切在'问题'而非'答案'上",
        "BPM 120+电子乐, 打击乐驱动的节奏",
    ],
}

# ── Documentary (纪录片) ─────────────────────────────────

DOCUMENTARY: Template = {
    "id": "documentary",
    "name": "纪录片",
    "description": "叙事沉稳、情感深沉、信息密度适中，适合人文/纪实内容",
    "timing": {
        "structure": [
            {"segment": "intro", "duration_pct": 0.15, "max_duration_sec": 30},
            {"segment": "development", "duration_pct": 0.55, "max_duration_sec": 120},
            {"segment": "climax", "duration_pct": 0.2, "max_duration_sec": 40},
            {"segment": "resolution", "duration_pct": 0.1, "max_duration_sec": 20},
        ],
        "shot_duration_min": 3.0,
        "shot_duration_max": 8.0,
        "cut_every_n_seconds": 6,
        "bpm_preferred": 80,
    },
    "transitions": {
        "intro": ["cross_dissolve", "fade_in"],
        "development": ["cross_dissolve", "j_cut", "l_cut"],
        "climax": ["cross_dissolve"],
        "resolution": ["cross_dissolve", "fade_out"],
        "crossfade_duration_sec": 1.0,
    },
    "subtitles": {
        "font": "Noto Serif SC",
        "font_size": 32,
        "color": "#F5F0E8",
        "stroke_color": "#1A1A1A",
        "stroke_width": 1,
        "animation": "fade",  # gentle fade in/out
    },
    "bgm": {
        "ducking_ratio": 0.2,
        "ducking_attack_ms": 200,
        "ducking_release_ms": 1000,
        "genre": ["orchestral", "ambient", "piano"],
        "volume_db": -6,
    },
    "color": {
        "lut": "",  # auto-select
        "contrast": 1.1,
        "saturation": 0.95,
    },
    "ai_hints": [
        "长镜头传递信息, 特写给情绪细节",
        "旁白间歇, 让画面呼吸",
        "叠化过渡而非硬切, 营造时间流动感",
        "高潮段用稍快的镜头切换, 但仍保持沉稳",
        "结尾留白3-5秒, 给观众回味空间",
    ],
}

# ── Vlog ────────────────────────────────────────────────

VLOG: Template = {
    "id": "vlog",
    "name": "Vlog",
    "description": "轻松自然、节奏轻快、个人化风格，适合日常/旅行/生活记录",
    "timing": {
        "structure": [
            {"segment": "opener", "duration_pct": 0.1, "max_duration_sec": 5},
            {"segment": "body", "duration_pct": 0.75, "max_duration_sec": 90},
            {"segment": "closer", "duration_pct": 0.15, "max_duration_sec": 10},
        ],
        "shot_duration_min": 1.5,
        "shot_duration_max": 4.0,
        "cut_every_n_seconds": 3,
        "bpm_preferred": 110,
    },
    "transitions": {
        "opener": ["hard_cut"],
        "body": ["hard_cut", "slide_left", "slide_right", "zoom_in"],
        "closer": ["cross_dissolve", "fade_out"],
        "crossfade_duration_sec": 0.5,
    },
    "subtitles": {
        "font": "Noto Sans SC Medium",
        "font_size": 30,
        "color": "#FFFFFF",
        "stroke_color": "#333333",
        "stroke_width": 2,
        "animation": "pop",  # slight scale-up on appearance
    },
    "bgm": {
        "ducking_ratio": 0.25,
        "ducking_attack_ms": 150,
        "ducking_release_ms": 600,
        "genre": ["pop", "folk", "lo-fi", "upbeat"],
        "volume_db": -7,
    },
    "color": {
        "lut": "",
        "contrast": 1.05,
        "saturation": 1.15,
    },
    "ai_hints": [
        "片头3秒内动作+文字触发",
        "每3秒一个视觉变化(切点/变焦/叠化/文字层)",
        "753节奏: 7s引入→5s铺垫→3s高潮→循环",
        "BGM节奏点处对齐切点(100ms窗口)",
        "片尾加CTA文字和订阅提示",
    ],
}

# ── Cinematic Trailer (电影感预告片) ────────────────────

CINEMATIC_TRAILER: Template = {
    "id": "cinematic_trailer",
    "name": "电影感预告片",
    "description": "史诗感、强冲击、蒙太奇节奏，适合宣传/预告/精华剪辑",
    "timing": {
        "structure": [
            {"segment": "teaser", "duration_pct": 0.1, "max_duration_sec": 8},
            {"segment": "build_up", "duration_pct": 0.35, "max_duration_sec": 30},
            {"segment": "climax_montage", "duration_pct": 0.35, "max_duration_sec": 30},
            {"segment": "title_card", "duration_pct": 0.2, "max_duration_sec": 15},
        ],
        "shot_duration_min": 0.5,
        "shot_duration_max": 2.5,
        "cut_every_n_seconds": 1.5,
        "bpm_preferred": 140,
    },
    "transitions": {
        "teaser": ["fade_in", "dip_to_black"],
        "build_up": ["hard_cut", "dip_to_black"],
        "climax_montage": ["hard_cut", "flash_white"],
        "title_card": ["dip_to_black", "fade_out"],
        "crossfade_duration_sec": 0.2,
    },
    "subtitles": {
        "font": "Noto Sans SC Bold",
        "font_size": 48,
        "color": "#FFFFFF",
        "stroke_color": "#000000",
        "stroke_width": 3,
        "animation": "cut",
    },
    "bgm": {
        "ducking_ratio": 0.12,
        "ducking_attack_ms": 50,
        "ducking_release_ms": 300,
        "genre": ["epic", "orchestral", "hybrid", "trailer"],
        "volume_db": -4,
    },
    "color": {
        "lut": "",
        "contrast": 1.4,
        "saturation": 1.2,
    },
    "ai_hints": [
        "蒙太奇快切, 每个镜头0.5-1.5秒",
        "鼓点/重音处对齐画面切换",
        "开场慢→加速→高潮爆发→戛然而止",
        "最后一个镜头切黑, 留白0.5秒后出标题",
        "音效层叠加(riser, hit, whoosh)",
    ],
}

# ── Simple Slideshow (图文幻灯片) ───────────────────────

SLIDESHOW: Template = {
    "id": "slideshow",
    "name": "图文幻灯片",
    "description": "静态图+字幕+音乐，适合故事导读/产品展示/知识科普",
    "timing": {
        "structure": [
            {"segment": "slide", "duration_pct": 1.0, "max_duration_sec": 120},
        ],
        "shot_duration_min": 4.0,
        "shot_duration_max": 8.0,
        "cut_every_n_seconds": 6,
        "bpm_preferred": 90,
    },
    "transitions": {
        "slide": ["cross_dissolve", "slide_left", "zoom_in"],
        "crossfade_duration_sec": 0.8,
    },
    "subtitles": {
        "font": "Noto Sans SC Medium",
        "font_size": 34,
        "color": "#FFFFFF",
        "stroke_color": "#000000",
        "stroke_width": 2,
        "animation": "fade",
    },
    "bgm": {
        "ducking_ratio": 0.2,
        "ducking_attack_ms": 200,
        "ducking_release_ms": 800,
        "genre": ["ambient", "piano", "acoustic"],
        "volume_db": -6,
    },
    "color": {
        "lut": "",
        "contrast": 1.05,
        "saturation": 1.1,
    },
    "ai_hints": [
        "每张图展示4-8秒, 配合字幕阅读速度",
        "Ken Burns效果(缓慢缩放+平移)增加动感",
        "配乐舒缓, 人声优先",
    ],
}

# ── Registry ────────────────────────────────────────────

PRESETS: dict[str, Template] = {
    "micro_drama": MICRO_DRAMA,
    "documentary": DOCUMENTARY,
    "vlog": VLOG,
    "cinematic_trailer": CINEMATIC_TRAILER,
    "slideshow": SLIDESHOW,
}


def get_template(template_id: str) -> Optional[Template]:
    return PRESETS.get(template_id)


def list_templates() -> list[dict]:
    return [
        {"id": k, "name": v["name"], "description": v["description"]}
        for k, v in PRESETS.items()
    ]


def merge_template_with_ai(
    template: Template,
    shot_moods: list[str],
    total_duration: float,
) -> dict:
    """Merge a template skeleton with AI dynamic decisions based on shot moods.

    Returns a complete editing recipe with concrete parameters.
    """
    import copy
    recipe = copy.deepcopy(template)

    # Derive transition choices based on mood keywords
    mood_keywords: set[str] = set()
    for m in shot_moods:
        for w in m.replace("，", ",").replace("、", ",").split(","):
            mood_keywords.add(w.strip().lower())

    # Dynamic transition selection per mood
    trans_map = {
        "压抑": "dip_to_black",
        "紧张": "hard_cut",
        "温馨": "cross_dissolve",
        "欢乐": "slide_left",
        "悲伤": "cross_dissolve",
        "孤独": "fade_in",
        "热血": "flash_white",
        "悬疑": "dip_to_black",
        "恐惧": "hard_cut",
        "浪漫": "cross_dissolve",
        "史诗": "zoom_in",
    }

    # Pick dominant transition
    trans_votes: dict[str, int] = {}
    for mood in mood_keywords:
        if mood in trans_map:
            t = trans_map[mood]
            trans_votes[t] = trans_votes.get(t, 0) + 1
    if trans_votes:
        recipe["ai_selected_transition"] = max(trans_votes, key=trans_votes.get)

    # Dynamic BGM shift based on mood
    if "紧张" in mood_keywords or "悬疑" in mood_keywords:
        recipe["ai_bgm_shift"] = {"genre_boost": ["tension", "dark"], "volume_db_boost": -2}
    elif "欢乐" in mood_keywords or "温馨" in mood_keywords:
        recipe["ai_bgm_shift"] = {"genre_boost": ["warm", "upbeat"], "volume_db_boost": 0}
    elif "悲伤" in mood_keywords or "孤独" in mood_keywords:
        recipe["ai_bgm_shift"] = {"genre_boost": ["ambient", "piano"], "volume_db_boost": -3}

    # Shot timing per mood
    if any(m in mood_keywords for m in ["热血", "紧张", "悬疑"]):
        recipe["timing"]["shot_duration_max"] = min(3.0, recipe["timing"]["shot_duration_max"])
    elif any(m in mood_keywords for m in ["悲伤", "孤独", "温馨"]):
        recipe["timing"]["shot_duration_min"] = max(3.0, recipe["timing"]["shot_duration_min"])

    return recipe
