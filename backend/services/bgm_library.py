"""Built-in royalty-free BGM library metadata.

Sources: Pixabay Music, YouTube Audio Library (CC0 / royalty-free).
These are metadata entries only — actual audio files go in media_library/bgm/.

Tags follow spec: 情绪/节奏/乐器/BPM/时长/来源
"""

BGM_CATALOG: list[dict] = [
    # ── Ambient / Calm ────────────────────────────────────
    {
        "id": "bgm_ambient_dreams",
        "name": "Ambient Dreams",
        "genre": "ambient",
        "tags": ["平静", "环境", "合成器", "慢节奏"],
        "bpm": 70,
        "duration_sec": 180,
        "mood": ["calm", "reflective", "neutral"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/ambient-ambient-dreams",
    },
    {
        "id": "bgm_peaceful_piano",
        "name": "Peaceful Piano",
        "genre": "piano",
        "tags": ["钢琴", "情感", "柔和", "慢节奏"],
        "bpm": 72,
        "duration_sec": 150,
        "mood": ["sad", "romantic", "reflective"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/solo-piano-peaceful-piano",
    },
    # ── Cinematic / Epic ──────────────────────────────────
    {
        "id": "bgm_epic_trailer",
        "name": "Epic Trailer",
        "genre": "orchestral",
        "tags": ["史诗", "管弦乐", "高潮", "电影感"],
        "bpm": 120,
        "duration_sec": 120,
        "mood": ["epic", "powerful", "triumphant"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/main-title-epic-trailer",
    },
    {
        "id": "bgm_cinematic_rise",
        "name": "Cinematic Rise",
        "genre": "hybrid",
        "tags": ["上升", "紧张", "管弦乐", "电子"],
        "bpm": 100,
        "duration_sec": 90,
        "mood": ["tension", "anticipation", "buildup"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/build-up-cinematic-rise",
    },
    # ── Electronic / Upbeat ───────────────────────────────
    {
        "id": "bgm_cyber_chase",
        "name": "Cyber Chase",
        "genre": "electronic",
        "tags": ["电子", "快节奏", "悬疑", "赛博"],
        "bpm": 140,
        "duration_sec": 105,
        "mood": ["tension", "action", "dark"],
        "source": "youtube_audio_library",
        "license": "CC0",
        "url": "",
    },
    {
        "id": "bgm_synthwave_night",
        "name": "Synthwave Night",
        "genre": "synthwave",
        "tags": ["合成波", "复古", "夜", "电子"],
        "bpm": 110,
        "duration_sec": 160,
        "mood": ["nostalgic", "cool", "driving"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/synthwave-synthwave-night",
    },
    # ── Folk / Acoustic ───────────────────────────────────
    {
        "id": "bgm_gentle_morning",
        "name": "Gentle Morning",
        "genre": "folk",
        "tags": ["温暖", "民谣", "吉他", "轻松"],
        "bpm": 95,
        "duration_sec": 150,
        "mood": ["warm", "happy", "peaceful"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/acoustic-group-gentle-morning",
    },
    {
        "id": "bgm_acoustic_vlog",
        "name": "Acoustic Vlog",
        "genre": "acoustic",
        "tags": ["原声", "吉他", "愉快", "Vlog"],
        "bpm": 105,
        "duration_sec": 130,
        "mood": ["upbeat", "happy", "casual"],
        "source": "youtube_audio_library",
        "license": "CC0",
        "url": "",
    },
    # ── Lo-fi / Chill ─────────────────────────────────────
    {
        "id": "bgm_lofi_study",
        "name": "Lo-fi Study",
        "genre": "lo-fi",
        "tags": ["低保真", "放松", "钢琴", "节拍"],
        "bpm": 80,
        "duration_sec": 180,
        "mood": ["relaxed", "focused", "chill"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/beats-lo-fi-study",
    },
    # ── Japanese / Traditional ────────────────────────────
    {
        "id": "bgm_sakura_tears",
        "name": "Sakura Tears",
        "genre": "traditional",
        "tags": ["日本", "弦乐", "情感", "和风"],
        "bpm": 65,
        "duration_sec": 190,
        "mood": ["sad", "beautiful", "nostalgic"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/world-sakura-tears",
    },
    {
        "id": "bgm_zen_garden",
        "name": "Zen Garden",
        "genre": "traditional",
        "tags": ["日本", "禅", "竹笛", "冥想"],
        "bpm": 50,
        "duration_sec": 200,
        "mood": ["peaceful", "meditative", "elegant"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/world-zen-garden",
    },
    # ── Tension / Suspense ────────────────────────────────
    {
        "id": "bgm_dark_mystery",
        "name": "Dark Mystery",
        "genre": "tension",
        "tags": ["悬疑", "黑暗", "低频", "紧张"],
        "bpm": 85,
        "duration_sec": 120,
        "mood": ["suspense", "dark", "mysterious"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/mystery-dark-mystery",
    },
    # ── Happy / Upbeat ────────────────────────────────────
    {
        "id": "bgm_sunny_day",
        "name": "Sunny Day",
        "genre": "pop",
        "tags": ["愉快", "流行", "轻快", "正面"],
        "bpm": 125,
        "duration_sec": 140,
        "mood": ["happy", "energetic", "positive"],
        "source": "pixabay",
        "license": "CC0",
        "url": "https://pixabay.com/music/pop-sunny-day",
    },
]


def search_bgm(
    mood: str | None = None,
    genre: str | None = None,
    bpm_min: int | None = None,
    bpm_max: int | None = None,
    tags: list[str] | None = None,
) -> list[dict]:
    """Search the built-in BGM catalog by mood, genre, BPM range, or tags."""
    results = BGM_CATALOG

    if mood:
        results = [b for b in results if mood.lower() in [m.lower() for m in b["mood"]]]
    if genre:
        results = [b for b in results if genre.lower() == b["genre"].lower()]
    if bpm_min is not None:
        results = [b for b in results if b["bpm"] >= bpm_min]
    if bpm_max is not None:
        results = [b for b in results if b["bpm"] <= bpm_max]
    if tags:
        tag_set = {t.lower() for t in tags}
        results = [b for b in results if tag_set & {t.lower() for t in b["tags"]}]

    return results


def recommend_for_template(template_id: str, shot_moods: list[str] | None = None) -> list[dict]:
    """Recommend BGM tracks for a given editing template and shot moods."""
    template_genre_map = {
        "micro_drama": ["electronic", "tension"],
        "documentary": ["ambient", "piano", "orchestral"],
        "vlog": ["pop", "folk", "lo-fi"],
        "cinematic_trailer": ["orchestral", "hybrid"],
        "slideshow": ["ambient", "piano", "acoustic"],
    }

    genres = template_genre_map.get(template_id, ["ambient"])

    # Search by genre first
    results: list[dict] = []
    for g in genres:
        results.extend(search_bgm(genre=g))

    # Deduplicate
    seen: set[str] = set()
    unique: list[dict] = []
    for b in results:
        if b["id"] not in seen:
            seen.add(b["id"])
            unique.append(b)

    return unique[:5]  # Top 5 matches


# ── Reference Track Catalog ──────────────────────────────
# Commonly-used editing tracks. Some are copyrighted — listed as reference
# with climax timestamps so users can source their own licensed copies.
# Public domain tracks include download URLs.

REFERENCE_TRACKS: list[dict] = [
    # ── Public Domain Classical ────────────────────────────
    {
        "id": "ref_gymnopedie_no1",
        "name": "Gymnopedie No.1",
        "name_cn": "裸体舞曲第一号",
        "composer": "Erik Satie",
        "era": "1888",
        "genre": "classical",
        "tags": ["钢琴", "忧伤", "宁静", "法国", "印象派"],
        "bpm": 65,
        "duration_sec": 180,
        "mood": ["melancholic", "peaceful", "nostalgic"],
        "use_case": ["纪录片", "文艺片", "情感段落"],
        "climax_sections": [
            {"label": "标志性开场", "start_sec": 0, "end_sec": 45, "note": "最常使用的段落，缓慢下行旋律"},
            {"label": "情感高潮", "start_sec": 90, "end_sec": 135, "note": "和声变化最丰富的段落"},
        ],
        "license": "Public Domain",
        "download_url": "https://musopen.org/music/4733-gymnopedie-no-1/",
        "bundled": False,
    },
    {
        "id": "ref_clair_de_lune",
        "name": "Clair de Lune",
        "name_cn": "月光",
        "composer": "Claude Debussy",
        "era": "1905",
        "genre": "classical",
        "tags": ["钢琴", "印象派", "梦幻", "法国"],
        "bpm": 55,
        "duration_sec": 300,
        "mood": ["dreamy", "romantic", "ethereal"],
        "use_case": ["纪录片", "婚礼", "情感高潮"],
        "climax_sections": [
            {"label": "最常用高潮段", "start_sec": 120, "end_sec": 210, "note": "琶音上行后主题再现，情感最饱满"},
        ],
        "license": "Public Domain",
        "download_url": "https://musopen.org/music/4413-clair-de-lune/",
        "bundled": False,
    },
    {
        "id": "ref_ave_maria",
        "name": "Ave Maria",
        "name_cn": "圣母颂",
        "composer": "Franz Schubert",
        "era": "1825",
        "genre": "classical",
        "tags": ["声乐", "神圣", "庄严", "弦乐"],
        "bpm": 45,
        "duration_sec": 270,
        "mood": ["sacred", "solemn", "beautiful"],
        "use_case": ["婚礼", "纪念", "情感段落"],
        "climax_sections": [
            {"label": "高潮段落", "start_sec": 90, "end_sec": 180, "note": "旋律上升至最高音后回落"},
        ],
        "license": "Public Domain",
        "download_url": "https://musopen.org/music/8823-ave-maria-d839/",
        "bundled": False,
    },
    {
        "id": "ref_canon_in_d",
        "name": "Canon in D",
        "name_cn": "D大调卡农",
        "composer": "Johann Pachelbel",
        "era": "1680",
        "genre": "classical",
        "tags": ["弦乐", "婚礼", "经典", "巴洛克"],
        "bpm": 70,
        "duration_sec": 330,
        "mood": ["elegant", "romantic", "joyful"],
        "use_case": ["婚礼", "广告", "温馨场景"],
        "climax_sections": [
            {"label": "最经典段落", "start_sec": 60, "end_sec": 180, "note": "主题层层叠加，弦乐渐强至最著名段落"},
        ],
        "license": "Public Domain",
        "download_url": "https://musopen.org/music/4711-canon-in-d/",
        "bundled": False,
    },
    {
        "id": "ref_four_seasons_spring",
        "name": "The Four Seasons - Spring (I. Allegro)",
        "name_cn": "四季·春 第一乐章",
        "composer": "Antonio Vivaldi",
        "era": "1723",
        "genre": "classical",
        "tags": ["小提琴", "巴洛克", "欢快", "活力"],
        "bpm": 120,
        "duration_sec": 200,
        "mood": ["energetic", "joyful", "bright"],
        "use_case": ["Vlog", "广告", "欢快场景"],
        "climax_sections": [
            {"label": "标志性开场", "start_sec": 0, "end_sec": 30, "note": "最强辨识度的段落"},
        ],
        "license": "Public Domain",
        "download_url": "https://musopen.org/music/2212-the-four-seasons-spring/",
        "bundled": False,
    },
    # ── Chinese Domestic (国内常用) ───────────────────────
    {
        "id": "ref_the_truth",
        "name": "The Truth That You Leave",
        "name_cn": "你离开的真相",
        "artist": "Pianoboy",
        "genre": "piano",
        "tags": ["钢琴", "忧伤", "抖音热曲", "回忆"],
        "bpm": 72,
        "duration_sec": 210,
        "mood": ["sad", "nostalgic", "bittersweet"],
        "use_case": ["情感短片", "回忆段落", "抖音", "B站"],
        "climax_sections": [
            {"label": "最常用段落", "start_sec": 40, "end_sec": 100, "note": "右手旋律第一次高潮"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    {
        "id": "ref_anniversary",
        "name": " Anniversary ",
        "name_cn": "周年",
        "artist": "α·Pav",
        "genre": "piano",
        "tags": ["钢琴", "感人", "毕业", "B站"],
        "bpm": 68,
        "duration_sec": 240,
        "mood": ["sentimental", "warm", "nostalgic"],
        "use_case": ["毕业视频", "纪录片", "生日祝福"],
        "climax_sections": [
            {"label": "高潮段", "start_sec": 60, "end_sec": 140, "note": "左手琶音加速+右手八度和弦"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    {
        "id": "ref_faded",
        "name": "Faded",
        "name_cn": " faded ",
        "artist": "Alan Walker",
        "genre": "electronic",
        "tags": ["电子", "空灵", "高潮", "抖音"],
        "bpm": 90,
        "duration_sec": 210,
        "mood": ["epic", "melancholic", "anthemic"],
        "use_case": ["混剪", "高潮段落", "预告片"],
        "climax_sections": [
            {"label": "Drop高潮", "start_sec": 55, "end_sec": 95, "note": "电子Drop最常用段落"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    {
        "id": "ref_liangliang",
        "name": "凉凉",
        "name_cn": "凉凉",
        "artist": "张碧晨/杨宗纬",
        "genre": "cpop_ballad",
        "tags": ["中国风", "对唱", "情感", "古装"],
        "bpm": 80,
        "duration_sec": 310,
        "mood": ["tragic", "romantic", "bittersweet"],
        "use_case": ["古风短片", "情感段落", "仙侠"],
        "climax_sections": [
            {"label": "副歌高潮", "start_sec": 60, "end_sec": 110, "note": "男女声合唱副歌，情感最满"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    {
        "id": "ref_guangnianzhwai",
        "name": "光年之外",
        "name_cn": "光年之外",
        "artist": "邓紫棋",
        "genre": "cpop",
        "tags": ["流行", "女声", "力量", "高潮"],
        "bpm": 88,
        "duration_sec": 230,
        "mood": ["powerful", "emotional", "epic"],
        "use_case": ["混剪", "高潮段落", "科幻/太空"],
        "climax_sections": [
            {"label": "爆发副歌", "start_sec": 55, "end_sec": 95, "note": "「我没想到」起，高音爆发"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    # ── Commonly Used Japanese (Copyrighted — Reference) ──
    {
        "id": "ref_tori_no_uta",
        "name": "Tori no Uta",
        "name_cn": "鸟之诗",
        "artist": "Lia",
        "source": "AIR (Key/Visual Arts)",
        "genre": "anime_op",
        "tags": ["动漫", "钢琴", "情感", "女声", "经典"],
        "bpm": 122,
        "duration_sec": 360,
        "mood": ["nostalgic", "emotional", "beautiful", "epic"],
        "use_case": ["MAD/AMV", "情感高潮", "回忆段落"],
        "climax_sections": [
            {"label": "副歌高潮", "start_sec": 57, "end_sec": 97, "note": "最常用段落，「あの鳥は」开始"},
            {"label": "钢琴间奏后高潮", "start_sec": 157, "end_sec": 197, "note": "第二段副歌，情感递进"},
            {"label": "最终副歌", "start_sec": 270, "end_sec": 330, "note": "编曲最饱满的段落"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    {
        "id": "ref_arigatou_kokia",
        "name": "Arigatou...",
        "name_cn": "ありがとう... (谢谢)",
        "artist": "KOKIA",
        "source": "KOKIA",
        "genre": "jpop_ballad",
        "tags": ["日本", "女声", "感人", "钢琴", "弦乐"],
        "bpm": 70,
        "duration_sec": 250,
        "mood": ["emotional", "grateful", "tearful", "heartfelt"],
        "use_case": ["纪录片", "毕业/离别", "情感高潮", "催泪段落"],
        "climax_sections": [
            {"label": "最强情感爆发段", "start_sec": 110, "end_sec": 160, "note": "1分50秒起「ありがとう」重复段落，弦乐全开+高音"},
            {"label": "结尾感人段", "start_sec": 200, "end_sec": 240, "note": "最后的「ありがとう」渐弱收束"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    {
        "id": "ref_river_flows_in_you",
        "name": "River Flows in You",
        "name_cn": "你的心河",
        "artist": "Yiruma",
        "genre": "new_age",
        "tags": ["钢琴", "韩国", "情感", "清新"],
        "bpm": 65,
        "duration_sec": 180,
        "mood": ["romantic", "peaceful", "bittersweet"],
        "use_case": ["婚礼", "Vlog", "回忆段落"],
        "climax_sections": [
            {"label": "高潮段落", "start_sec": 60, "end_sec": 120, "note": "左手琶音加速，右手旋律上行至最高音"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
    {
        "id": "ref_merry_go_round",
        "name": "Merry-Go-Round of Life",
        "name_cn": "人生的旋转木马",
        "artist": "Joe Hisaishi",
        "source": "Howl's Moving Castle",
        "genre": "soundtrack",
        "tags": ["宫崎骏", "久石让", "管弦乐", "梦幻", "华尔兹"],
        "bpm": 90,
        "duration_sec": 300,
        "mood": ["magical", "romantic", "whimsical"],
        "use_case": ["纪录片", "文艺片", "梦幻场景"],
        "climax_sections": [
            {"label": "最经典段落", "start_sec": 30, "end_sec": 90, "note": "主旋律首次完整呈现，辨识度最高"},
        ],
        "license": "Copyrighted",
        "download_url": "",
        "bundled": False,
    },
]

# ── LUT / Color Grading Catalog ──────────────────────────

LUT_CATALOG: list[dict] = [
    {
        "id": "lut_teal_orange",
        "name": "Teal Orange Hollywood",
        "name_cn": "青橙好莱坞",
        "style": "cinematic",
        "tags": ["电影感", "暖肤色", "冷暗部", "大片"],
        "color_temp": "mixed",
        "contrast": "high",
        "use_case": ["微短剧", "预告片", "电影感内容"],
        "url": "",
        "bundled": False,
    },
    {
        "id": "lut_tokyo_night",
        "name": "Tokyo Night",
        "name_cn": "东京之夜",
        "style": "urban",
        "tags": ["赛博", "冷色调", "霓虹", "暗调"],
        "color_temp": "cool",
        "contrast": "high",
        "use_case": ["合成波风格", "夜拍", "都市内容"],
        "url": "",
        "bundled": False,
    },
    {
        "id": "lut_vintage_film",
        "name": "Vintage Film Fade",
        "name_cn": "复古胶片褪色",
        "style": "vintage",
        "tags": ["胶片", "褪色", "暖调", "颗粒感"],
        "color_temp": "warm",
        "contrast": "low",
        "use_case": ["纪录片", "回忆段落", "文艺Vlog"],
        "url": "",
        "bundled": False,
    },
    {
        "id": "lut_sakura_bloom",
        "name": "Sakura Bloom",
        "name_cn": "樱花绽放",
        "style": "japanese",
        "tags": ["日系", "粉色调", "清新", "低饱和"],
        "color_temp": "slightly_warm",
        "contrast": "low",
        "use_case": ["和风主题", "旅行Vlog", "文艺内容"],
        "url": "",
        "bundled": False,
    },
    {
        "id": "lut_forest_mood",
        "name": "Forest Mood",
        "name_cn": "森林色调",
        "style": "nature",
        "tags": ["自然", "绿色增强", "柔和", "户外"],
        "color_temp": "neutral",
        "contrast": "medium",
        "use_case": ["自然纪录片", "户外Vlog", "旅行"],
        "url": "",
        "bundled": False,
    },
    {
        "id": "lut_bw_dramatic",
        "name": "Black & White Dramatic",
        "name_cn": "黑白戏剧",
        "style": "monochrome",
        "tags": ["黑白", "高对比", "经典", "严肃"],
        "color_temp": "bw",
        "contrast": "high",
        "use_case": ["严肃题材", "纪录片采访", "艺术短片"],
        "url": "",
        "bundled": False,
    },
]


def search_reference(
    mood: str | None = None,
    genre: str | None = None,
    use_case: str | None = None,
    public_domain_only: bool = False,
) -> list[dict]:
    """Search reference tracks with optional filters."""
    results = REFERENCE_TRACKS
    if public_domain_only:
        results = [t for t in results if t["license"] == "Public Domain"]
    if mood:
        results = [t for t in results if mood.lower() in [m.lower() for m in t["mood"]]]
    if genre:
        results = [t for t in results if genre.lower() == t["genre"].lower()]
    if use_case:
        results = [t for t in results if any(use_case.lower() in u.lower() for u in t["use_case"])]
    return results


def get_climax_segments(track_id: str) -> list[dict]:
    """Get the commonly-used climax/hot sections for a specific track."""
    all_tracks = BGM_CATALOG + REFERENCE_TRACKS
    for t in all_tracks:
        if t["id"] == track_id:
            return t.get("climax_sections", [])
    return []
