"""Cinematic director/film style presets — prompt templates for AI generation."""

DIRECTOR_STYLES: dict[str, dict] = {
    "wes_anderson": {
        "name": "Wes Anderson",
        "name_cn": "韦斯·安德森",
        "genre": "whimsical comedy drama",
        "visual_prompt": "Wes Anderson cinematography, perfectly symmetrical composition, centered framing, pastel candy color palette (pink, yellow, mint green), meticulous production design, flat lay aesthetic, retro vintage props, whimsical atmosphere, quirky character styling, The Grand Budapest Hotel inspired, ultra-precise staging",
        "color_palette": "pastel pink, yellow, mint green, soft beige",
        "lighting": "even diffused lighting, minimal shadows, warm balanced tones",
        "camera": "static centered shots, 90-degree pans, symmetrical tracking"
    },
    "wong_kar_wai": {
        "name": "Wong Kar-wai",
        "name_cn": "王家卫",
        "genre": "romantic drama",
        "visual_prompt": "Wong Kar-wai cinematography, highly saturated emotional color grading (deep red, emerald green, electric blue), slow motion effect, handheld camera aesthetic, urban isolation atmosphere, motion blur, Hong Kong neon signs, nostalgic romantic mood, In the Mood for Love inspired, dreamy bokeh, cigarette smoke atmosphere",
        "color_palette": "deep red, emerald green, electric blue, warm amber",
        "lighting": "practical lights, neon glow, window light with curtains, underexposed shadows",
        "camera": "handheld, slow motion, step-printing, intimate close-ups"
    },
    "zhang_yimou": {
        "name": "Zhang Yimou",
        "name_cn": "张艺谋",
        "genre": "epic historical drama",
        "visual_prompt": "Zhang Yimou cinematography, bold monochromatic color scheme (dominant red, black, or white), Chinese cultural symbolism, epic historical scale, strong visual impact, traditional Chinese architecture, ink wash painting aesthetic, dramatic composition, Hero or Raise the Red Lantern inspired, martial arts elegance",
        "color_palette": "dominant red, jet black, pure white, gold accents",
        "lighting": "high contrast, dramatic colored gels, theatrical spotlighting",
        "camera": "epic crane shots, sweeping panoramas, slow dramatic pushes"
    },
    "nolan": {
        "name": "Christopher Nolan",
        "name_cn": "克里斯托弗·诺兰",
        "genre": "sci-fi thriller",
        "visual_prompt": "Christopher Nolan cinematography, cool desaturated color palette (steel blue, grey), epic architectural scale, IMAX wide format, practical effects aesthetic, realistic sci-fi visual, time manipulation or fragmented narrative visual, dramatic chiaroscuro lighting, Inception or Interstellar inspired, cerebral atmosphere",
        "color_palette": "steel blue, gunmetal grey, desaturated earth tones",
        "lighting": "chiaroscuro, practical light sources, dramatic god rays, low-key",
        "camera": "IMAX wide shots, slow push-ins, cross-cutting, practical effects"
    },
    "tarantino": {
        "name": "Quentin Tarantino",
        "name_cn": "昆汀·塔伦蒂诺",
        "genre": "crime action",
        "visual_prompt": "Quentin Tarantino cinematography, violence aesthetics, vivid saturated retro color palette (yellow, orange, red), dramatic low or high angles, stylized action choreography, 1970s grindhouse aesthetic, extreme close-ups, trunk shot perspective, Pulp Fiction or Kill Bill inspired, theatrical blood effects",
        "color_palette": "vivid yellow, orange, blood red, 1970s brown",
        "lighting": "harsh top light, practical fluorescents, dramatic side lighting",
        "camera": "trunk shots, extreme close-ups, low angles, whip pans, crash zooms"
    },
    "scott": {
        "name": "Ridley Scott",
        "name_cn": "雷德利·斯科特",
        "genre": "sci-fi epic",
        "visual_prompt": "Ridley Scott cinematography, epic widescreen composition, industrial design aesthetic, atmospheric volumetric lighting, dramatic god rays or light shafts, highly detailed production design, desaturated earth tone palette, smoke and fog atmospheric effects, Blade Runner or Gladiator inspired, cinematic grandeur, gritty realism",
        "color_palette": "desaturated earth, industrial metal, sepia, blue-grey smoke",
        "lighting": "volumetric god rays, atmospheric haze, dramatic shafts, low-key",
        "camera": "epic establishing shots, slow reveals, smoke-filled atmosphere"
    },
    "kurosawa": {
        "name": "Akira Kurosawa",
        "name_cn": "黑泽明",
        "genre": "samurai epic",
        "visual_prompt": "Akira Kurosawa cinematography, dynamic symmetrical composition, samurai warrior aesthetic, dramatic weather elements (rain, wind, fog), black and white or desaturated color palette, Japanese classical architecture, epic movement choreography, Seven Samurai or Rashomon inspired, humanistic storytelling, nature as narrative element",
        "color_palette": "monochrome or desaturated, deep black, rain silver",
        "lighting": "natural weather light, high contrast, stark shadows, rain reflections",
        "camera": "telephoto compression, multi-camera action, weather elements, axial cuts"
    },
    "burton": {
        "name": "Tim Burton",
        "name_cn": "蒂姆·波顿",
        "genre": "gothic fantasy",
        "visual_prompt": "Tim Burton cinematography, gothic aesthetic, dark fantasy atmosphere, exaggerated character design with large eyes and thin limbs, stop-motion handcrafted texture, black and white spiral patterns, twisted surreal architecture, whimsical macabre mood, Edward Scissorhands or Nightmare Before Christmas inspired, German expressionism lighting",
        "color_palette": "black, white, deep purple, sickly green, pale blue",
        "lighting": "German expressionist, harsh angular shadows, moonlight, practical lamps",
        "camera": "dutch angles, expressionist composition, crane shots, dolly zooms"
    },
    "ang_lee": {
        "name": "Ang Lee",
        "name_cn": "李安",
        "genre": "drama",
        "visual_prompt": "Ang Lee cinematography, East-meets-West aesthetic fusion, poetic natural lighting, emotionally subtle expression, restrained elegant composition, cultural symbolism and reflection, contemplative introspective mood, Crouching Tiger Hidden Dragon or Brokeback Mountain inspired, soft color palette, technical cinematographic innovation",
        "color_palette": "soft natural tones, muted greens, warm earth, misty blues",
        "lighting": "soft natural light, window light, overcast diffusion, candlelight",
        "camera": "fluid steadicam, slow zooms, contemplative static, floating wire work"
    },
}

FILM_STYLES: dict[str, dict] = {
    "film_noir": {
        "name": "Film Noir",
        "name_cn": "黑色电影",
        "visual_prompt": "film noir style, high contrast black and white photography, low-key lighting, dramatic shadows, urban nightscape, venetian blind light patterns, chiaroscuro effect, 1940s crime drama aesthetic, moody atmosphere, hardboiled detective scene",
        "color_palette": "black and white, deep shadows, silver highlights"
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "name_cn": "赛博朋克",
        "visual_prompt": "cyberpunk aesthetic, neon-drenched cityscape, futuristic metropolis night scene, high-tech low-life atmosphere, vibrant neon colors (cyan, magenta, purple), rain-soaked streets, holographic advertisements, urban decay, Blade Runner inspired, technological dystopia, moody cinematic lighting",
        "color_palette": "cyan, magenta, neon purple, electric blue, rain black"
    },
    "french_new_wave": {
        "name": "French New Wave",
        "name_cn": "法国新浪潮",
        "visual_prompt": "French New Wave cinematography, handheld camera aesthetic, natural lighting, candid street photography style, on-location shooting, 1960s Parisian atmosphere, existential mood, cinematic realism, auteur theory visual language, spontaneous composition, jump cuts",
        "color_palette": "natural muted, grey Parisian sky, warm indoor practicals"
    },
    "epic_fantasy": {
        "name": "Epic Fantasy",
        "name_cn": "史诗奇幻",
        "visual_prompt": "epic fantasy cinematography, magical realism style, ethereal lighting, mystical atmosphere, enchanted forest or castle setting, mythical elements, medieval architecture, dreamlike quality, otherworldly color palette, cinematic grandeur, dramatic sky, Lord of the Rings inspired",
        "color_palette": "ethereal gold, enchanted green, mystical blue, warm firelight"
    },
    "ghibli": {
        "name": "Studio Ghibli",
        "name_cn": "吉卜力工作室",
        "visual_prompt": "Studio Ghibli animation style, soft pastel color palette (green, blue, gold), hand-drawn watercolor aesthetic, highly detailed natural environments, fluffy cumulus clouds, gentle diffused lighting, lush landscapes, whimsical dreamy atmosphere, Spirited Away or My Neighbor Totoro inspired, nostalgic emotional mood, fine linework",
        "color_palette": "soft green, sky blue, warm gold, cream white"
    },
    "chinese_ink": {
        "name": "Chinese Ink Wash",
        "name_cn": "中国水墨动画",
        "visual_prompt": "Chinese ink wash animation style, traditional sumi-e painting aesthetic, monochromatic black ink gradients, soft brush strokes with bleeding edges, poetic atmospheric perspective, flowing water effects, delicate bamboo and landscape details, ethereal misty atmosphere, Shanghai Animation Film Studio inspired, calligraphic line work",
        "color_palette": "ink black, rice paper white, subtle grey washes, vermillion seal"
    },
}

ALL_STYLES = {**DIRECTOR_STYLES, **FILM_STYLES}


def get_style(style_id: str) -> dict | None:
    return ALL_STYLES.get(style_id)


def get_director_styles() -> list[dict]:
    return [{"id": k, "name": v["name"], "name_cn": v["name_cn"], "genre": v["genre"]}
            for k, v in DIRECTOR_STYLES.items()]


def get_film_styles() -> list[dict]:
    return [{"id": k, "name": v["name"], "name_cn": v["name_cn"]}
            for k, v in FILM_STYLES.items()]
