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
