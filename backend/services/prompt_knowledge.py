"""Prompt Engineering Knowledge Base — injected into storyboard generation.

All techniques learned from:
- Z-Image Turbo prompt guide
- Sulphur 2/LTX video generation best practices
- Wan 2.2 I2V workflow optimization
- Cinematography camera movement vocabulary
- 15 director/film style presets
- AI portrait prompt engineering
- 2025-2026 community best practices
"""

# ── Core Style: Hyperrealistic ───────────────────────────

FIRST_FRAME_RULE = """
CRITICAL: FIRST-FRAME PRINCIPLE (MANDATORY FOR ALL prompt_image FIELDS)

The generated image will be used as the FIRST FRAME for video generation.
Therefore, the image MUST capture the MOMENT BEFORE the main action — the tension, the anticipation, the setup.

VIDEO ACTION → IMAGE (FIRST FRAME):
- Head smashing on table → Head still raised, about to descend; muscles tensed, victim's eyes wide with terror
- Water droplet splashing → Droplet still hanging from the bulb, surface tension at breaking point
- Bubble bursting → Bubble fully intact, iridescent surface at maximum tension
- Door slamming open → Door still closed, hand reaching for handle
- Blood splattering → Object still mid-air, trajectory aimed, blood still contained
- Character collapsing → Character still standing, knees beginning to buckle
- Glass shattering → Glass intact, crack just beginning to form
- Scream/Shout → Mouth closed or just beginning to open, inhale visible in throat
- Punch landing → Fist still traveling, target's guard still up
- Explosion → Fuse still burning, last spark before ignition

Think like a film director: the STILL image is the SETUP. The VIDEO is the PAYOFF.
Every prompt_image must describe a moment of POTENTIAL ENERGY — not kinetic release.
"""

HYPERREALISTIC_STANDARD = """
HYPERREALISTIC PHOTOGRAPHY PROTOCOL (MANDATORY FOR ALL SHOTS):

1. CAMERA: Shot on Arri Alexa 65, 35mm film grain, anamorphic lens, shallow depth of field f/2.8
2. LIGHTING: Volumetric lighting, ray tracing global illumination, subsurface scattering on skin, cinematic lighting ratio 4:1 key-to-fill
3. TEXTURE: Visible skin pores, fabric weave, surface wear, dust particles, micro-details — NOT plastic, NOT smooth, NOT CGI
4. COLOR: Professional color grading, 16-bit RAW, Kodak Portra 400 color science, natural skin tones
5. QUALITY: 8k raw, photorealistic, hyperrealistic, masterpiece, trending on artstation, cgsociety
6. ANTI-AI: No plastic skin, no over-smoothing, no cartoon proportions, no symmetry obsession, no generic beauty standards
7. UNIQUE FACES: Asymmetrical features real humans have — uneven eyes, crooked noses, scars, acne marks, wrinkles, age spots, freckles, pores
8. BODY DIVERSITY: Real body types — not all slim, not all tall, not all young. Include ages 20-70, various builds, postures.
"""

# ── Prompt Structure Formula ─────────────────────────────

PROMPT_FORMULA = """
AI IMAGE PROMPT FORMULA (apply to EVERY shot's prompt_image field):

[Shot type + angle + lens] + [Subject: age + nationality + detailed face + body type + clothing] + [Action: specific pose, body language, what they're doing] + [Environment: exact location, materials, objects, atmosphere] + [Lighting: source, direction, color temp, shadows, quality] + [Camera: movement, focal length, depth of field] + [Style: director reference or film style] + [Quality: hyperrealistic, 8k, cinematic, masterpiece]

Example prompt_image:
\"Medium close-up, 85mm f/2.8 anamorphic lens, shallow depth of field. A 28-year-old Chinese man with asymmetrical features — left eye slightly higher than right, a small scar on his right jaw from childhood, unkempt black hair with 3 days of stubble, sallow skin with visible pores under the flickering tungsten light. He sits at a scratched dark oak round table, his right hand unconsciously gripping the edge, knuckles white. Single tungsten bulb overhead casts harsh 2800K orange light, creating deep shadows under his brow and cheekbones. Volumetric dust particles visible in the light cone. Shot on Arri Alexa 65, 35mm film grain, hyperrealistic, 8k raw, cinematic color grading, dark atmospheric moody cinematography, masterpiece.\"
"""

# ── Camera Movement Vocabulary ───────────────────────────

CAMERA_MOVEMENTS = """
CAMERA MOVEMENT VOCABULARY (choose one per shot, be specific):

PUSH: slow dolly in, subtle push forward, creeping zoom — build tension, reveal detail
PULL: slow pull out, gradual dolly back — reveal context, create isolation
PAN: slow pan left/right, horizontal sweep — reveal landscape, follow action
TILT: tilt up/down, vertical reveal — emphasize height, power dynamics
TRACK: tracking shot, lateral follow — follow walking subject, lateral flow
ORBIT: slow orbit, arc around subject, 360-degree rotation — dramatic emphasis, hero moment
CRANE: crane up/down, jib rise/descend — grand establishing, dramatic reveal
HANDHELD: subtle handheld micro-shake, documentary unsteadiness — realism, urgency, chaos
STEADICAM: smooth floating glide through space — cinematic tracking, immersion
ZOOM: slow zoom in, dolly zoom (vertigo effect) — psychological tension, disorientation
STATIC: locked tripod, zero movement — contemplation, stillness, MEDITATION (use sparingly)

Key rule: ONE camera move per shot. Multiple simultaneous movements cause video artifacts.
"""

# ── Video Generation Knowledge ───────────────────────────

VIDEO_GEN_RULES = """
VIDEO GENERATION RULES (for prompt_video field):

1. MOTION ONLY: Describe only what MOVES and how. The image anchors all visual details.
2. SIMPLE FIRST: Subtle head turns, slow hand gestures, micro-expressions, breathing — succeed reliably
3. AVOID: Dancing, running, fighting, complex multi-person interactions — high failure rate
4. CAMERA MOVE: One clear camera movement direction with speed modifier (slow, gentle, subtle)
5. NO SPEECH: Always include 'no speech, no dialogue, silent, instrumental only' for Sulphur model
6. SULPHUR CFG: 3.0-5.5, image strength 0.75-0.85
7. WAN CFG: 1.0, dual-stage sampling, 4 steps each with Lightning LoRAs
8. FRAMES: (F-1) % 8 == 0 rule — valid counts: 49, 73, 97, 121, 201, 241
9. RESOLUTION: 1024x1024 Sulphur, 640x640 Wan + 4x upscale

WRONG prompt_video: \"A woman in a red dress walks through a neon-lit street, her long black hair flowing in the wind, the city lights reflecting in puddles...\" (too much visual description)
CORRECT prompt_video: \"Slow dolly in. The woman turns her head slightly to the left. Gentle breathing motion. Subtle micro-expressions of concern. Camera pushes forward slowly. No speech, no dialogue, silent.\"
"""

# ── Z-Image Turbo Rules ──────────────────────────────────

ZIMAGE_RULES = """
Z-IMAGE TURBO GENERATION RULES:

MODEL: 6B S3-DiT, few-step distilled
SETTINGS: Euler sampler, 8 steps, CFG 1.0, Beta scheduler
CRITICAL: At CFG 1.0, negative prompts are IGNORED. Bake ALL constraints into positive prompt.
ANTI-PATTERNS: No \"no text, no watermark\" in negative (won't work). Instead: \"clean image, professional photography, no overlays\"
PROMPT LENGTH: 80-300 words optimal. Over 300 may truncate.
RESOLUTION: 1024x1024 standard, 832x1216 portrait, 1216x832 landscape
CONTRA-INDICATED: CFG > 2 causes artifacts and 10x slowdown. Never use high CFG on Turbo.
"""

# ── Combined Knowledge (injected into system prompt) ────

def get_prompt_knowledge() -> str:
    """Return consolidated knowledge for injection into the AI storyboard prompt."""
    return f"""
{FIRST_FRAME_RULE}

{PROMPT_FORMULA}

{HYPERREALISTIC_STANDARD}

{CAMERA_MOVEMENTS}

{VIDEO_GEN_RULES}

{ZIMAGE_RULES}
"""
