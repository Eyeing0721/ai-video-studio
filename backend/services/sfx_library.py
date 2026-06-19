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
        "compressor": {"threshold": -24, "ratio": 3, "makeup_gain": 6},
        "description": "几乎无混响，高频微增+压缩拉近，亲密距离感",
        "use_case": ["ASMR", "亲密对话", "内心独白"],
    },
    "gramophone_vintage": {
        "name": "老式留声机",
        "reverb": {"room_size": 0.25, "damping": 0.7, "wet_level": 0.2, "dry_level": 0.8},
        "eq": {"low_pass_cutoff": 3500, "high_pass_cutoff": 200, "low_shelf_gain": -8, "high_shelf_gain": -4, "mid_boost_freq": 1200, "mid_boost_gain": 4},
        "noise": {"type": "vinyl_crackle", "level": 0.08, "hum_60hz": 0.03},
        "modulation": {"wow_depth": 0.002, "flutter_depth": 0.003, "rate": 0.5},
        "description": "频带压缩+唱片噼啪声+轻微抖晃，模拟1920年代留声机",
        "use_case": ["复古场景", "年代戏", "旁白回忆", "怀旧"],
    },
    "radio_broadcast": {
        "name": "电台播音",
        "reverb": {"room_size": 0.1, "damping": 0.5, "wet_level": 0.1, "dry_level": 0.9},
        "eq": {"low_pass_cutoff": 5000, "high_pass_cutoff": 200, "mid_boost_freq": 800, "mid_boost_gain": 6, "high_shelf_gain": -2},
        "compressor": {"threshold": -18, "ratio": 5, "makeup_gain": 8},
        "description": "窄频带+中频凸起+强压缩，模拟电台/新闻联播质感",
        "use_case": ["新闻播报", "收音机场景", "纪录片旁白"],
    },
    "distortion_overdrive": {
        "name": "过载失真",
        "reverb": {"room_size": 0.15, "damping": 0.4, "wet_level": 0.15, "dry_level": 0.85},
        "eq": {"low_pass_cutoff": 8000, "high_pass_cutoff": 100, "mid_boost_freq": 2000, "mid_boost_gain": 6},
        "distortion": {"drive": 0.4, "tone": 0.6, "mix": 0.3},
        "description": "软削波失真+中频激励，给声音增加颗粒感",
        "use_case": ["摇滚/金属配乐", "愤怒独白", "赛博朋克"],
    },
    "old_tv_crt": {
        "name": "老电视/CRT",
        "reverb": {"room_size": 0.15, "damping": 0.8, "wet_level": 0.12, "dry_level": 0.88},
        "eq": {"low_pass_cutoff": 4000, "high_pass_cutoff": 300, "low_shelf_gain": -6, "high_shelf_gain": -4},
        "noise": {"type": "white_noise", "level": 0.04, "hum_50hz": 0.05},
        "description": "窄频带+白噪+50Hz嗡声，模拟CRT老电视",
        "use_case": ["电视新闻场景", "怀旧", "监控画面"],
    },
    "stadium_announcement": {
        "name": "体育馆广播",
        "reverb": {"room_size": 0.8, "damping": 0.2, "wet_level": 0.6, "dry_level": 0.4, "pre_delay": 120},
        "eq": {"low_pass_cutoff": 6000, "high_pass_cutoff": 80, "mid_boost_freq": 2500, "mid_boost_gain": 8},
        "description": "长预延迟+大厅混响+中高音穿透力，体育馆PA系统感",
        "use_case": ["体育赛事", "大型集会", "演出报幕"],
    },
    # ── Spatial / 空间音频 ──────────────────────────────────
    "stereo_widen": {
        "name": "立体声展宽",
        "spatial": {"width": 1.5, "mid_side_ratio": 0.6, "haas_delay_ms": 15},
        "description": "M/S处理+Haas效应延迟，展宽立体声场但不失相位",
        "use_case": ["BGM增强", "环境音", "电影配乐"],
    },
    "mono_collapse": {
        "name": "单声道化",
        "spatial": {"width": 0.0, "mid_side_ratio": 1.0},
        "description": "双声道混合为中央单声道，消除相位问题",
        "use_case": ["手机播放兼容", "对白/旁白", "老设备播放"],
    },
    "binaural_3d": {
        "name": "双耳3D空间",
        "reverb": {"room_size": 0.6, "damping": 0.3, "wet_level": 0.4, "dry_level": 0.6},
        "spatial": {"hrtf_enabled": True, "elevation": 0, "azimuth": 0, "distance": 1.5},
        "description": "HRTF双耳渲染，模拟真实3D空间定位",
        "use_case": ["VR/AR内容", "沉浸式体验", "ASMR"],
    },
    "surround_upmix": {
        "name": "环绕声上混",
        "spatial": {"upmix": "stereo_to_5.1", "center_level": 0.7, "surround_level": 0.3, "lfe_crossover": 120},
        "description": "立体声→5.1上混，提取环境信息分散到环绕声道",
        "use_case": ["电影输出", "家庭影院", "沉浸式短片"],
    },
    "voice_isolation": {
        "name": "人声提取",
        "spatial": {"mode": "center_extraction", "vocal_boost": 3},
        "eq": {"high_pass_cutoff": 100, "mid_boost_freq": 2500, "mid_boost_gain": 4},
        "description": "中置声道提取+中频增强，分离人声/对白",
        "use_case": ["对白增强", "配音提取", "降噪"],
    },
    # ── Creative / 创意效果 ─────────────────────────────────
    "reverse_reverb": {
        "name": "反向混响",
        "reverb": {"room_size": 0.7, "damping": 0.3, "wet_level": 0.8, "dry_level": 0.2},
        "description": "先放湿信号再放干信号（需音频反向处理），营造诡异氛围",
        "use_case": ["恐怖片", "闪回前兆", "梦境进入"],
    },
    "pitch_down_horror": {
        "name": "降调恐怖",
        "pitch": {"semitone_shift": -6, "preserve_tempo": True},
        "eq": {"low_shelf_gain": 6, "high_shelf_gain": -6},
        "reverb": {"room_size": 0.8, "damping": 0.1, "wet_level": 0.5, "dry_level": 0.5},
        "description": "降6个半音+低频增强+大混响，恐怖/怪物感",
        "use_case": ["恐怖片", "怪物声音", "噩梦场景"],
    },
    "helicopter_comms": {
        "name": "直升机通讯",
        "reverb": {"room_size": 0.05, "damping": 0.9, "wet_level": 0.15, "dry_level": 0.85},
        "eq": {"high_pass_cutoff": 400, "low_pass_cutoff": 3000, "mid_boost_freq": 1500, "mid_boost_gain": 5},
        "noise": {"type": "rotor_blade_modulation", "level": 0.1, "frequency": 8},
        "compressor": {"threshold": -20, "ratio": 6, "makeup_gain": 12},
        "description": "强压缩+低频旋转调制+窄带，模拟直升机/飞行器内通讯",
        "use_case": ["军事/战争场景", "直升机", "对讲机"],
    },
}


def get_audio_preset(preset_id: str) -> dict | None:
    return AUDIO_PRESETS.get(preset_id)
