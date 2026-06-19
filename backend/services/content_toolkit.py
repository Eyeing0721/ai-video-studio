"""Content creation toolkit — fonts, visual effects, titles, covers, copywriting.

Covers the full post-production text/vfx layer for the AI video pipeline.
"""

# ── Font Catalog (Free Commercial-Use) ─────────────────────

FONT_CATALOG: list[dict] = [
    # ── Sans-serif (标题/UI) ──────────────────────────────
    {
        "id": "font_siyuan_black",
        "name": "思源黑体",
        "name_en": "Source Han Sans",
        "type": "sans",
        "weight": "regular/bold/heavy",
        "style": ["现代", "通用", "UI"],
        "best_for": ["标题", "字幕", "UI界面", "科技内容"],
        "license": "SIL Open Font License (免费商用)",
        "url": "https://github.com/adobe-fonts/source-han-sans",
        "bundled": False,
    },
    {
        "id": "font_siyuan_serif",
        "name": "思源宋体",
        "name_en": "Source Han Serif",
        "type": "serif",
        "weight": "regular/bold",
        "style": ["传统", "优雅", "文艺"],
        "best_for": ["正文", "纪录片", "文艺片", "出版物"],
        "license": "SIL Open Font License (免费商用)",
        "url": "https://github.com/adobe-fonts/source-han-serif",
        "bundled": False,
    },
    {
        "id": "font_alibaba_puhui",
        "name": "阿里巴巴普惠体",
        "name_en": "Alibaba PuHuiTi",
        "type": "sans",
        "weight": "light/regular/medium/bold/heavy (5档)",
        "style": ["电商", "现代", "通用"],
        "best_for": ["电商标题", "广告", "UI", "全部场景"],
        "license": "阿里巴巴普惠体许可 (免费商用)",
        "url": "https://www.alibabafonts.com",
        "bundled": False,
    },
    {
        "id": "font_zcool_kuhei",
        "name": "站酷酷黑",
        "name_en": "ZCOOL KuHei",
        "type": "display",
        "weight": "regular",
        "style": ["力量", "个性", "硬朗"],
        "best_for": ["大标题", "封面", "海报", "综艺/热血"],
        "license": "SIL Open Font License (免费商用)",
        "url": "https://www.zcool.com.cn/special/freefonts",
        "bundled": False,
    },
    {
        "id": "font_zcool_qingke",
        "name": "站酷庆科黄油体",
        "name_en": "ZCOOL QingKe HuangYou",
        "type": "display",
        "weight": "regular",
        "style": ["趣味", "创意", "卡通"],
        "best_for": ["趣味标题", "Vlog", "美食", "轻松内容"],
        "license": "SIL Open Font License (免费商用)",
        "url": "https://www.zcool.com.cn/special/freefonts",
        "bundled": False,
    },
    {
        "id": "font_lxgwwenkai",
        "name": "霞鹜文楷",
        "name_en": "LXGW WenKai",
        "type": "serif",
        "weight": "light/regular/bold",
        "style": ["手写", "文艺", "温暖"],
        "best_for": ["文艺Vlog", "读书类", "治愈内容", "引用"],
        "license": "SIL Open Font License (免费商用)",
        "url": "https://github.com/lxgw/LxgwWenKai",
        "bundled": False,
    },
    {
        "id": "font_youshe_title",
        "name": "优设标题黑",
        "name_en": "YouShe Title Black",
        "type": "display",
        "weight": "heavy",
        "style": ["力量", "醒目", "标题专用"],
        "best_for": ["封面大标题", "海报", "抖音封面", "促销"],
        "license": "SIL Open Font License (免费商用)",
        "url": "https://www.uisdc.com/free-commercial-fonts",
        "bundled": False,
    },
    # ── English Cinematic ──────────────────────────────────
    {
        "id": "font_montserrat",
        "name": "Montserrat",
        "name_en": "Montserrat",
        "type": "sans",
        "weight": "thin to black (9档)",
        "style": ["现代", "几何", "干净"],
        "best_for": ["英文字幕", "UI", "现代品牌"],
        "license": "SIL Open Font License",
        "url": "https://fonts.google.com/specimen/Montserrat",
        "bundled": False,
    },
    {
        "id": "font_playfair",
        "name": "Playfair Display",
        "name_en": "Playfair Display",
        "type": "serif",
        "weight": "regular/bold/black",
        "style": ["经典", "优雅", "时尚"],
        "best_for": ["时尚/Vogue风格标题", "婚礼", "高端品牌"],
        "license": "SIL Open Font License",
        "url": "https://fonts.google.com/specimen/Playfair+Display",
        "bundled": False,
    },
    {
        "id": "font_bebas_neue",
        "name": "Bebas Neue",
        "name_en": "Bebas Neue",
        "type": "display",
        "weight": "regular",
        "style": ["力量", "紧凑", "电影感"],
        "best_for": ["电影标题", "预告片", "封面", "动作/燃向"],
        "license": "SIL Open Font License",
        "url": "https://fonts.google.com/specimen/Bebas+Neue",
        "bundled": False,
    },
]

# ── Visual Effects Catalog ─────────────────────────────────

VFX_CATALOG: list[dict] = [
    # ── Film/Texture ──────────────────────────────────────
    {
        "id": "vfx_film_grain",
        "name": "胶片颗粒",
        "name_en": "Film Grain",
        "type": "texture",
        "tags": ["胶片", "颗粒", "复古", "电影感"],
        "use_case": ["纪录片", "复古", "文艺片", "回忆段落"],
        "intensity": "subtle (建议0.05-0.15)",
        "source": "pixabay/overlay packs",
    },
    {
        "id": "vfx_dust_scratches",
        "name": "灰尘划痕",
        "name_en": "Dust & Scratches",
        "type": "texture",
        "tags": ["老胶片", "划痕", "做旧", "年代感"],
        "use_case": ["年代戏", "闪回", "留声机/怀旧氛围"],
        "intensity": "medium",
        "source": "mixkit/free overlays",
    },
    {
        "id": "vfx_light_leak",
        "name": "漏光",
        "name_en": "Light Leak",
        "type": "light",
        "tags": ["漏光", "暖调", "梦幻", "转场"],
        "use_case": ["Vlog转场", "温馨场景", "回忆", "婚礼"],
        "intensity": "subtle-medium",
        "source": "pixabay/light-leaks",
    },
    {
        "id": "vfx_lens_flare",
        "name": "镜头光晕",
        "name_en": "Lens Flare",
        "type": "light",
        "tags": ["光晕", "逆光", "氛围", "电影感"],
        "use_case": ["逆光场景", "梦幻", "大片开场", "阳光感"],
        "intensity": "variable",
        "source": "mixkit/free overlays",
    },
    # ── Glitch/Digital ─────────────────────────────────────
    {
        "id": "vfx_glitch_rgb",
        "name": "RGB分离/故障",
        "name_en": "RGB Glitch",
        "type": "glitch",
        "tags": ["故障", "RGB", "赛博", "失真"],
        "use_case": ["赛博朋克", "科幻", "转场冲击", "技术故障"],
        "intensity": "high",
        "source": "mixkit/glitch overlays",
    },
    {
        "id": "vfx_vhs_retro",
        "name": "VHS录像带",
        "name_en": "VHS Retro",
        "type": "glitch",
        "tags": ["VHS", "录像带", "复古", "90s"],
        "use_case": ["年代戏", "恐怖片", "合成波风格", "90年代回忆"],
        "intensity": "high (tracking lines + chroma bleed)",
        "source": "pixabay/VHS overlay",
    },
    {
        "id": "vfx_scanlines",
        "name": "扫描线",
        "name_en": "Scanlines",
        "type": "glitch",
        "tags": ["CRT", "扫描线", "监视器", "复古"],
        "use_case": ["监控画面", "老电视", "赛博朋克"],
        "intensity": "subtle",
        "source": "mixkit/free overlays",
    },
    # ── Atmospheric ────────────────────────────────────────
    {
        "id": "vfx_fog_mist",
        "name": "雾气/薄雾",
        "name_en": "Fog & Mist",
        "type": "atmosphere",
        "tags": ["雾", "梦幻", "神秘", "氛围"],
        "use_case": ["梦境", "神秘场景", "山林", "文艺"],
        "intensity": "subtle (叠加模式: screen)",
        "source": "pixabay/fog overlays",
    },
    {
        "id": "vfx_snow_particles",
        "name": "雪花粒子",
        "name_en": "Snow Particles",
        "type": "atmosphere",
        "tags": ["雪", "冬季", "浪漫", "氛围"],
        "use_case": ["冬季场景", "圣诞节", "浪漫"],
        "intensity": "variable",
        "source": "mixkit/particles",
    },
    {
        "id": "vfx_fire_sparkle",
        "name": "火星/火花",
        "name_en": "Fire Sparks",
        "type": "atmosphere",
        "tags": ["火", "火花", "篝火", "温暖"],
        "use_case": ["篝火场景", "魔法", "温暖氛围"],
        "intensity": "medium",
        "source": "pixabay/fire overlays",
    },
    # ── Border/Frame ───────────────────────────────────────
    {
        "id": "vfx_cinemascope_bars",
        "name": "电影宽幅黑条",
        "name_en": "CinemaScope Bars",
        "type": "border",
        "tags": ["电影", "宽幅", "2.35:1", "黑边"],
        "use_case": ["电影感内容", "预告片", "高端品牌"],
        "intensity": "structural (2.35:1 mask)",
        "source": "built-in (MLT crop filter)",
    },
    {
        "id": "vfx_vignette",
        "name": "暗角",
        "name_en": "Vignette",
        "type": "border",
        "tags": ["暗角", "聚焦", "电影感", "氛围"],
        "use_case": ["通用增强聚焦", "情感段落", "肖像"],
        "intensity": "subtle (0.2-0.4)",
        "source": "built-in (MLT vignette filter)",
    },
]

# ── Title/Text Templates ───────────────────────────────────

TITLE_TEMPLATES: list[dict] = [
    {
        "id": "title_cinematic_main",
        "name": "电影主标题",
        "font": "font_bebas_neue",
        "font_cn": "font_zcool_kuhei",
        "size": "screen_width * 0.08",
        "position": "center",
        "animation": "fade_in_up + scale(0.95→1.0, 0.6s)",
        "use_case": ["预告片片头", "成片标题", "章节标题"],
        "layout": {"safe_margin": "10% from edges", "max_width": "80%"},
    },
    {
        "id": "title_lower_third",
        "name": "下三分之一字幕条",
        "font": "font_siyuan_black",
        "size": "screen_height * 0.035",
        "position": "bottom_left",
        "animation": "slide_right(0.3s)",
        "use_case": ["人物介绍", "地点标注", "采访信息"],
        "layout": {
            "position": "left: 5%, bottom: 15%",
            "bg_bar": "accent_color at 80% opacity",
            "bar_height": "text_height + 16px",
            "text_padding": "12px left, 8px vertical",
        },
    },
    {
        "id": "title_subtitle_standard",
        "name": "标准字幕",
        "font": "font_siyuan_black",
        "size": "screen_height * 0.04",
        "position": "bottom_center",
        "animation": "fade(0.15s)",
        "use_case": ["对白字幕", "旁白"],
        "layout": {
            "position": "center_x, bottom: 8%",
            "stroke": "2px black at 60% opacity",
            "shadow": "2px offset, 4px blur at 50% opacity",
        },
    },
    {
        "id": "title_burn_subtitle",
        "name": "烧录字幕（嵌入）",
        "font": "font_siyuan_black",
        "size": "screen_height * 0.04",
        "position": "bottom_center",
        "animation": "none (hard cut per segment)",
        "use_case": ["微短剧字幕", "抖音/快手竖屏"],
        "layout": {
            "position": "center_x, bottom: 12%",
            "max_lines": 2,
            "line_spacing": "1.2",
            "bg": "none (clean look)",
            "stroke": "3px black at 70% opacity for readability",
        },
    },
    {
        "id": "title_callout",
        "name": "强调标注",
        "font": "font_youshe_title",
        "size": "variable (比主字幕大 30%)",
        "position": "dynamic (follow subject)",
        "animation": "pop_scale(0→1.15→1.0, 0.4s)",
        "use_case": ["关键词强调", "价格标注", "重点信息"],
        "layout": {
            "bg": "accent_color pill, 90% opacity",
            "padding": "8px horizontal, 4px vertical",
            "corner_radius": "pill (border-radius: 999px)",
        },
    },
]

# ── Cover/Thumbnail Templates ──────────────────────────────

COVER_TEMPLATES: list[dict] = [
    {
        "id": "cover_youtube_standard",
        "name": "YouTube 标准封面",
        "aspect_ratio": "16:9",
        "resolution": "1280x720",
        "layout": {
            "title_area": "left 60% or center bottom third",
            "face_area": "right 40%, center",
            "text_max_chars": 30,
            "text_lines": "1-2 lines max",
            "text_size": "large (fills 60-80% width)",
        },
        "color_rules": ["高对比度", "暖色+冷色对冲", "避免与YouTube白/黑UI同色"],
        "best_practice": "大脸+大标题+情绪表达，缩略图尺寸下仍然可读",
    },
    {
        "id": "cover_douyin_vertical",
        "name": "抖音/快手竖屏封面",
        "aspect_ratio": "9:16",
        "resolution": "1080x1920",
        "layout": {
            "title_area": "center, top 40%",
            "text_max_chars": 15,
            "text_lines": "1 line preferred",
            "text_size": "extra large (fills 70% width)",
        },
        "color_rules": ["鲜艳/高饱和抓眼球", "冷色背景+暖色文字（或反之）"],
        "best_practice": "竖屏单行大字，前3秒停留时清晰可读",
    },
    {
        "id": "cover_bilibili",
        "name": "B站封面",
        "aspect_ratio": "16:9 (推荐) 或 1:1",
        "resolution": "1920x1080",
        "layout": {
            "title_area": "可变，分图层设计",
            "text_style": "二次元/扁平化/高对比度标题字",
        },
        "color_rules": ["蓝白/粉黑是B站高频配色", "扁平化风格优先"],
        "best_practice": "信息密度高可接受，文字+关键帧截图+表情包拼贴",
    },
    {
        "id": "cover_thumb_story",
        "name": "故事类/微短剧封面",
        "aspect_ratio": "3:4 (推荐) 或 9:16",
        "layout": {
            "top": "剧名/集数标识",
            "middle": "关键帧截图 (带人物表情)",
            "bottom": "一句台词/冲突提示",
        },
        "best_practice": "1张人物特写 + 1行冲突文字，不堆砌",
    },
]

# ── Title Copywriting Formulas ─────────────────────────────

TITLE_FORMULAS: list[dict] = [
    {
        "id": "formula_curiosity_gap",
        "name": "好奇心缺口",
        "template": "{数字}个{事物}，{出人意料的事实/问题}",
        "example": "3个你每天都在用的App，其实在偷看你的相册",
        "platform": ["YouTube", "B站"],
        "max_chars": 60,
    },
    {
        "id": "formula_how_to",
        "name": "教程/How-To",
        "template": "如何{动词}{结果}（{时间/成本约束}）",
        "example": "如何用AI 5分钟做出一条爆款短视频（完全免费）",
        "platform": ["YouTube", "B站", "抖音"],
        "max_chars": 50,
    },
    {
        "id": "formula_emotional_hook",
        "name": "情绪钩子",
        "template": "{情绪词}！{极端场景描述}，{转折}",
        "example": "泪崩！AI续写了奶奶没来得及讲完的睡前故事",
        "platform": ["抖音", "快手", "小红书"],
        "max_chars": 30,
    },
    {
        "id": "formula_controversy",
        "name": "争议/对比",
        "template": "{公认观点}？{反常识/新发现}",
        "example": "都说AI会取代剪辑师？我做了一个实验",
        "platform": ["B站", "知乎"],
        "max_chars": 50,
    },
    {
        "id": "formula_listicle",
        "name": "列表/合集",
        "template": "{数字}个{主题}，{结果/推荐}",
        "example": "10个免费商用BGM网站，剪辑师收藏这一篇就够了",
        "platform": ["B站", "YouTube"],
        "max_chars": 50,
    },
    {
        "id": "formula_story_opener",
        "name": "故事开场",
        "template": "{时间/地点}，{人物} {动作}，{出人意料的结果}",
        "example": "昨天凌晨3点，我给AI喂了一本小说，生成的视频让我睡不着",
        "platform": ["抖音", "小红书"],
        "max_chars": 40,
    },
]

# ── Usage Logic: Decision Trees ────────────────────────────

FONT_RULES = {
    "微短剧": {"title": "font_youshe_title", "subtitle": "font_siyuan_black", "size": "large"},
    "纪录片": {"title": "font_siyuan_serif", "subtitle": "font_siyuan_black", "size": "medium"},
    "Vlog": {"title": "font_alibaba_puhui", "subtitle": "font_lxgwwenkai", "size": "medium"},
    "预告片": {"title": "font_bebas_neue", "subtitle": "font_montserrat", "size": "xlarge"},
    "电商": {"title": "font_alibaba_puhui", "subtitle": "font_alibaba_puhui", "size": "large"},
    "知识科普": {"title": "font_siyuan_black", "subtitle": "font_siyuan_black", "size": "medium"},
    "游戏": {"title": "font_zcool_kuhei", "subtitle": "font_siyuan_black", "size": "large"},
}

VFX_RULES = {
    "微短剧": ["vfx_vignette", "vfx_cinemascope_bars"],
    "纪录片": ["vfx_film_grain", "vfx_vignette"],
    "Vlog": ["vfx_light_leak"],
    "预告片": ["vfx_lens_flare", "vfx_cinemascope_bars"],
    "赛博朋克": ["vfx_glitch_rgb", "vfx_scanlines"],
    "年代戏/怀旧": ["vfx_dust_scratches", "vfx_vhs_retro"],
    "恐怖/悬疑": ["vfx_fog_mist", "vfx_vignette"],
    "梦幻/回忆": ["vfx_light_leak", "vfx_fog_mist"],
    "户外/自然": ["vfx_lens_flare"],
    "冬季/圣诞": ["vfx_snow_particles"],
}


def recommend_fonts(template_id: str) -> dict:
    return FONT_RULES.get(template_id, FONT_RULES["Vlog"])


def recommend_vfx(template_id: str) -> list[str]:
    return VFX_RULES.get(template_id, [])


def generate_title(style: str, context: dict) -> str:
    """Generate a video title using a copywriting formula."""
    import random
    formula = next((f for f in TITLE_FORMULAS if f["id"] == style), TITLE_FORMULAS[0])
    return formula["template"].format(**context) if context else formula["example"]


def get_cover_template(platform: str) -> dict:
    mapping = {
        "youtube": "cover_youtube_standard",
        "douyin": "cover_douyin_vertical",
        "kuaishou": "cover_douyin_vertical",
        "bilibili": "cover_bilibili",
    }
    template_id = mapping.get(platform, "cover_youtube_standard")
    return next(c for c in COVER_TEMPLATES if c["id"] == template_id)
