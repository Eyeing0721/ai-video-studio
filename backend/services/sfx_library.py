"""Sound effects & environmental audio catalog.

Categories:
- Reverb IR (impulse responses for convolution reverb)
- Environment (rain, wind, city, forest, cafe, office)
- Transitions (whoosh, riser, impact, swoosh)
- Foley (footsteps, doors, cloth)
- Special (underwater, dream, distortion)
- UI (clicks, notifications)

Sources: Pixabay, Mixkit, Freesound, Zapsplat (all CC0/royalty-free for commercial use)
"""

SFX_CATALOG: list[dict] = [
    # ── Reverb / 混响 Impulse Responses ────────────────────
    {
        "id": "sfx_ir_hall_large",
        "name": "Large Concert Hall IR",
        "name_cn": "大音乐厅混响",
        "type": "reverb_ir",
        "tags": ["混响", "大厅", "古典", "空间感", "长混响"],
        "duration_sec": 3.0,
        "use_case": ["交响乐", "史诗配乐", "庄严场景"],
        "source": "freesound",
        "license": "CC0",
        "url": "https://freesound.org/people/klankbeeld/sounds/",
        "bundled": False,
    },
    {
        "id": "sfx_ir_room_small",
        "name": "Small Room IR",
        "name_cn": "小房间混响",
        "type": "reverb_ir",
        "tags": ["混响", "室内", "自然", "短混响", "对白"],
        "duration_sec": 1.5,
        "use_case": ["对白", "室内场景", "Vlog"],
        "source": "freesound",
        "license": "CC0",
        "url": "https://freesound.org/",
        "bundled": False,
    },
    {
        "id": "sfx_ir_cathedral",
        "name": "Cathedral IR",
        "name_cn": "大教堂混响",
        "type": "reverb_ir",
        "tags": ["混响", "教堂", "神圣", "超长混响", "空灵"],
        "duration_sec": 5.0,
        "use_case": ["神圣场景", "梦境", "闪回", "超强空间感"],
        "source": "openairlib",
        "license": "CC BY",
        "url": "https://www.openair.hosted.york.ac.uk/",
        "bundled": False,
    },
    # ── Environment / 环境音 ────────────────────────────────
    {
        "id": "sfx_rain_gentle",
        "name": "Gentle Rain",
        "name_cn": "小雨",
        "type": "ambience",
        "tags": ["雨", "自然", "白噪音", "舒缓", "ASMR"],
        "duration_sec": 120,
        "use_case": ["治愈场景", "读书", "睡觉", "忧郁氛围"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/rain/",
        "bundled": False,
    },
    {
        "id": "sfx_thunderstorm",
        "name": "Thunderstorm",
        "name_cn": "雷雨",
        "type": "ambience",
        "tags": ["雷", "雨", "暴风雨", "黑暗", "紧张"],
        "duration_sec": 90,
        "use_case": ["悬疑", "恐怖", "高潮前夕"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/thunderstorm/",
        "bundled": False,
    },
    {
        "id": "sfx_wind_howling",
        "name": "Howling Wind",
        "name_cn": "呼啸风声",
        "type": "ambience",
        "tags": ["风", "呼啸", "荒凉", "冬季", "户外"],
        "duration_sec": 60,
        "use_case": ["荒凉场景", "冬季", "西部", "孤独"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/wind/",
        "bundled": False,
    },
    {
        "id": "sfx_forest_day",
        "name": "Forest Daytime",
        "name_cn": "森林白天",
        "type": "ambience",
        "tags": ["森林", "鸟鸣", "自然", "阳光", "户外"],
        "duration_sec": 120,
        "use_case": ["自然纪录片", "户外Vlog", "治愈"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/forest/",
        "bundled": False,
    },
    {
        "id": "sfx_city_traffic",
        "name": "City Traffic",
        "name_cn": "城市交通",
        "type": "ambience",
        "tags": ["城市", "交通", "嘈杂", "街道", "都市"],
        "duration_sec": 90,
        "use_case": ["都市场景", "街道", "现代生活"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/city/",
        "bundled": False,
    },
    {
        "id": "sfx_cafe_ambience",
        "name": "Cafe Ambience",
        "name_cn": "咖啡馆氛围",
        "type": "ambience",
        "tags": ["咖啡馆", "人声", "杯碟", "室内", "温暖"],
        "duration_sec": 90,
        "use_case": ["对话场景", "Vlog", "文艺氛围"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/cafe/",
        "bundled": False,
    },
    {
        "id": "sfx_ocean_waves",
        "name": "Ocean Waves",
        "name_cn": "海浪",
        "type": "ambience",
        "tags": ["海", "浪", "自然", "广阔", "平静"],
        "duration_sec": 120,
        "use_case": ["海边场景", "沉思", "旅行"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/ocean/",
        "bundled": False,
    },
    # ── Underwater / 水下 ───────────────────────────────────
    {
        "id": "sfx_underwater_deep",
        "name": "Deep Underwater",
        "name_cn": "深水水下",
        "type": "special",
        "tags": ["水下", "低通", "沉闷", "深海", "压抑"],
        "duration_sec": 30,
        "use_case": ["水下场景", "梦境", "压抑氛围", "溺水"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/underwater/",
        "bundled": False,
    },
    {
        "id": "sfx_underwater_bubbles",
        "name": "Underwater Bubbles",
        "name_cn": "水泡",
        "type": "special",
        "tags": ["水泡", "水下", "咕噜", "轻快"],
        "duration_sec": 10,
        "use_case": ["水下细节", "过渡", "轻松场景"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/bubbles/",
        "bundled": False,
    },
    # ── Transitions / 转场音效 ──────────────────────────────
    {
        "id": "sfx_whoosh_fast",
        "name": "Fast Whoosh",
        "name_cn": "快速嗖声",
        "type": "transition",
        "tags": ["转场", "嗖", "快切", "运动"],
        "duration_sec": 0.8,
        "use_case": ["快速转场", "动作切换", "卡点"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/whoosh/",
        "bundled": False,
    },
    {
        "id": "sfx_riser_epic",
        "name": "Epic Riser",
        "name_cn": "史诗上扬",
        "type": "transition",
        "tags": ["上扬", "积累", "预期", "高潮前"],
        "duration_sec": 5.0,
        "use_case": ["高潮铺垫", "预告片", "揭晓前"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/riser/",
        "bundled": False,
    },
    {
        "id": "sfx_impact_heavy",
        "name": "Heavy Impact",
        "name_cn": "重击",
        "type": "transition",
        "tags": ["冲击", "重击", "低音", "震撼"],
        "duration_sec": 1.5,
        "use_case": ["标题出现", "剧情转折", "打击感"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/impact/",
        "bundled": False,
    },
    {
        "id": "sfx_swoosh_smooth",
        "name": "Smooth Swoosh",
        "name_cn": "平滑滑动",
        "type": "transition",
        "tags": ["滑动", "平滑", "UI转场", "轻量"],
        "duration_sec": 0.5,
        "use_case": ["UI转场", "轻过渡", "字幕出现"],
        "source": "mixkit",
        "license": "CC0",
        "url": "https://mixkit.co/free-sound-effects/",
        "bundled": False,
    },
    # ── Foley / 拟音 ────────────────────────────────────────
    {
        "id": "sfx_footsteps_wood",
        "name": "Footsteps on Wood",
        "name_cn": "木地板脚步",
        "type": "foley",
        "tags": ["脚步", "木头", "室内"],
        "duration_sec": 5.0,
        "use_case": ["室内行走", "悬疑", "恐怖"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/footsteps/",
        "bundled": False,
    },
    {
        "id": "sfx_door_close",
        "name": "Door Close",
        "name_cn": "关门",
        "type": "foley",
        "tags": ["门", "关闭", "室内", "离开"],
        "duration_sec": 1.5,
        "use_case": ["场景结束", "角色离开", "悬念"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/sound-effects/search/door/",
        "bundled": False,
    },
    # ── UI / Notification ───────────────────────────────────
    {
        "id": "sfx_ui_click",
        "name": "UI Click",
        "name_cn": "界面点击",
        "type": "ui",
        "tags": ["UI", "点击", "按钮", "交互"],
        "duration_sec": 0.2,
        "use_case": ["按钮反馈", "交互音效"],
        "source": "mixkit",
        "license": "CC0",
        "url": "https://mixkit.co/free-sound-effects/",
        "bundled": False,
    },
    {
        "id": "sfx_notification_chime",
        "name": "Notification Chime",
        "name_cn": "通知铃声",
        "type": "ui",
        "tags": ["通知", "提醒", "铃声", "完成"],
        "duration_sec": 1.0,
        "use_case": ["任务完成", "消息提醒", "导出完成"],
        "source": "mixkit",
        "license": "CC0",
        "url": "https://mixkit.co/free-sound-effects/",
        "bundled": False,
    },
]


def search_sfx(
    sfx_type: str | None = None,
    tags: list[str] | None = None,
    use_case: str | None = None,
) -> list[dict]:
    """Search sound effects catalog."""
    results = SFX_CATALOG
    if sfx_type:
        results = [s for s in results if s["type"] == sfx_type]
    if tags:
        tag_set = {t.lower() for t in tags}
        results = [s for s in results if tag_set & {t.lower() for t in s["tags"]}]
    if use_case:
        results = [s for s in results if any(use_case.lower() in u.lower() for u in s["use_case"])]
    return results


def get_reverb_ir(scene: str = "") -> list[dict]:
    """Get reverb impulse response recommendations for a scene type."""
    mapping = {
        "indoor": ["sfx_ir_room_small"],
        "outdoor": [],
        "church": ["sfx_ir_cathedral"],
        "hall": ["sfx_ir_hall_large"],
        "dream": ["sfx_ir_cathedral"],
        "epic": ["sfx_ir_hall_large"],
        "对话": ["sfx_ir_room_small"],
        "室内": ["sfx_ir_room_small"],
        "教堂": ["sfx_ir_cathedral"],
        "音乐会": ["sfx_ir_hall_large"],
        "梦境": ["sfx_ir_cathedral"],
    }
    ids = mapping.get(scene.lower(), [])
    return [s for s in SFX_CATALOG if s["id"] in ids]


# ── Audio Processing Presets ──────────────────────────────

AUDIO_PRESETS: dict[str, dict] = {
    "indoor_dialogue": {
        "name": "室内对白",
        "reverb": {"room_size": 0.2, "damping": 0.5, "wet_level": 0.15, "dry_level": 0.85},
        "eq": {"low_shelf_gain": -2, "high_shelf_gain": 1},
        "description": "小房间自然混响，对白清晰",
        "use_case": ["Vlog", "访谈", "室内场景"],
    },
    "cinematic_spatial": {
        "name": "电影空间感",
        "reverb": {"room_size": 0.7, "damping": 0.3, "wet_level": 0.35, "dry_level": 0.65},
        "eq": {"low_shelf_gain": 2, "high_shelf_gain": 2},
        "description": "大空间混响，增强空间感和氛围",
        "use_case": ["预告片", "纪录片", "史诗"],
    },
    "underwater_muffle": {
        "name": "水下闷响",
        "reverb": {"room_size": 0.1, "damping": 0.9, "wet_level": 0.5, "dry_level": 0.5},
        "eq": {"low_pass_cutoff": 800, "low_shelf_gain": 3},
        "description": "低通滤波+短混响，模拟水下听觉",
        "use_case": ["水下场景", "梦境", "压抑氛围"],
    },
    "dream_ethereal": {
        "name": "梦境空灵",
        "reverb": {"room_size": 0.9, "damping": 0.1, "wet_level": 0.6, "dry_level": 0.4},
        "eq": {"high_shelf_gain": 4, "low_shelf_gain": -1},
        "description": "超长混响+高频增强，空灵梦幻感",
        "use_case": ["闪回", "梦境", "虚幻场景"],
    },
    "phone_voice": {
        "name": "电话声音",
        "reverb": {"room_size": 0.05, "damping": 0.8, "wet_level": 0.1, "dry_level": 0.9},
        "eq": {"low_pass_cutoff": 3400, "high_pass_cutoff": 300, "low_shelf_gain": -5, "high_shelf_gain": -5},
        "description": "带通滤波，模拟电话/对讲机音质",
        "use_case": ["电话对话", "对讲机", "老式收音机"],
    },
    "megaphone": {
        "name": "扩音器",
        "reverb": {"room_size": 0.3, "damping": 0.2, "wet_level": 0.2, "dry_level": 0.8},
        "eq": {"mid_boost_freq": 1500, "mid_boost_gain": 8, "low_shelf_gain": -10, "high_shelf_gain": -6},
        "description": "中频凸起+失真感，模拟扩音器/广播",
        "use_case": ["操场广播", "集会", "体育赛事"],
    },
    "intimate_whisper": {
        "name": "亲密耳语",
        "reverb": {"room_size": 0.05, "damping": 0.6, "wet_level": 0.05, "dry_level": 0.95},
        "eq": {"high_shelf_gain": 2, "low_shelf_gain": -3},
        "description": "几乎无混响，高频微增，亲密距离感",
        "use_case": ["ASMR", "亲密对话", "内心独白"],
    },
}


def get_audio_preset(preset_id: str) -> dict | None:
    return AUDIO_PRESETS.get(preset_id)
