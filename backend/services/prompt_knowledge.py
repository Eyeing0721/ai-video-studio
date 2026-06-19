"""Comprehensive AI Prompt Engineering Knowledge Base.

Organized into focused modules that the storyboard AI references.
Each module is self-contained and can be selected by the AI based on task needs.

Total knowledge: ~25,000 characters across 12 modules.
"""

# ═══════════════════════════════════════════════════════════
# MODULE 1: First-Frame Principle (CRITICAL)
# ═══════════════════════════════════════════════════════════

FIRST_FRAME_RULE = """
╔══════════════════════════════════════════════════════════════╗
║  CRITICAL: FIRST-FRAME PRINCIPLE — IMAGE = SETUP, VIDEO = PAYOFF ║
╚══════════════════════════════════════════════════════════════╝

The generated image IS the first frame of the video.
Therefore every prompt_image MUST capture the MOMENT BEFORE the action.

VIDEO ACTION              →  IMAGE MUST SHOW (moment before)
─────────────────────────────────────────────────────────
Head smashed on table     →  Head still raised mid-air, muscles tensed, victim's eyes wide with fear, blood still contained in veins
Water droplet splashing   →  Droplet still attached to bulb, surface tension at breaking point, perfect teardrop shape
Bubble bursting           →  Bubble fully intact, iridescent rainbow surface, maximum tension before rupture
Door slamming open        →  Door completely closed, hand reaching for handle, knuckles white
Blood splattering          →  Object mid-air, trajectory aimed, blood still contained within intact skin
Character collapsing       →  Character standing, knees beginning to buckle, balance shifting
Glass shattering           →  Glass intact, hairline crack just beginning to form from impact point
Gun firing                 →  Trigger finger just beginning to squeeze, hammer not yet released
Explosion                  →  Fuse burning, last spark, everything still intact
Punch landing              →  Fist mid-swing, target's guard still up, faces show anticipation
Kiss                       →  Lips millimeters apart, eyes half-closed, breath visible
Scream                     →  Mouth closed or just opening, deep inhale visible in throat

GOLDEN RULE: Describe POTENTIAL ENERGY, not kinetic release.
The viewer should feel "this is about to happen" — not "this is happening."
"""

# ═══════════════════════════════════════════════════════════
# MODULE 2: Hyperrealistic Photography Protocol
# ═══════════════════════════════════════════════════════════

HYPERREALISTIC_PROTOCOL = """
╔══════════════════════════════════════════════════════════════╗
║  HYPERREALISTIC PHOTOGRAPHY PROTOCOL — MANDATORY ║
╚══════════════════════════════════════════════════════════════╝

CAMERA SYSTEM:
- Shot on Arri Alexa 65 with Panavision Primo lenses
- 35mm film grain (Kodak Portra 400 color science)
- Anamorphic 2.39:1 aspect ratio when cinematic
- f/2.8 for portraits (shallow depth of field), f/5.6 for wide shots (environment detail)
- Focal lengths: 24mm (wide establishing), 35mm (environmental), 50mm (natural eye), 85mm (portrait), 135mm (compressed detail)

LIGHTING PROTOCOL:
- Volumetric lighting with visible light cones and dust particles
- Ray tracing global illumination for natural light bounce
- Subsurface scattering on all skin (light penetrates skin, scatters, exits — never flat)
- Key-to-fill ratio: 4:1 for dramatic, 2:1 for natural, 1:1 for flat/documentary
- Color temperature: 2800K (tungsten warm), 5600K (daylight neutral), 8000K (cold blue)
- Practical light sources visible in frame (lamps, windows, candles — motivated lighting)

TEXTURE REQUIREMENTS:
- Skin: visible pores (0.05-0.2mm), fine vellus hair, sebaceous filaments on nose, micro-wrinkles
- Fabric: individual thread weave visible at close range, lint, pilling on old clothes
- Surfaces: wood grain with scratches and cup rings, metal with patina and fingerprint oils
- Atmosphere: dust motes in light beams, condensation on cold surfaces, smoke wisps

COLOR SCIENCE:
- Professional 16-bit RAW color grading
- Kodak Portra 400 film emulation for natural skin tones
- Subtle color contrast: warm highlights (skin) vs cool shadows (environment)
- No over-saturation — real life is slightly desaturated
- Black point at true black (RGB 5,5,5), white point just below clipping (RGB 250,250,250)

WHAT TO AVOID (ANTI-AI):
✗ Plastic skin, pore-less faces, beauty filters
✗ Perfect symmetry — real faces are asymmetrical
✗ Generic "handsome/beautiful" templates
✗ Over-saturated HDR look
✗ Cartoon proportions
✗ AI smoothness/gradient artifacts
✗ Same-face syndrome across characters
✓ Real human variation: scars, moles, wrinkles, uneven teeth, asymmetrical eyes, skin conditions
"""

# ═══════════════════════════════════════════════════════════
# MODULE 3: Prompt Construction Formula
# ═══════════════════════════════════════════════════════════

PROMPT_CONSTRUCTION = """
╔══════════════════════════════════════════════════════════════╗
║  PROMPT CONSTRUCTION FORMULA — LAYER BY LAYER ║
╚══════════════════════════════════════════════════════════════╝

Every prompt_image must follow this 8-layer construction:

LAYER 1 — QUALITY MODIFIERS (prepend to every prompt):
"hyperrealistic, photorealistic, 8k raw, cinematic lighting, volumetric lighting,
ray tracing global illumination, subsurface scattering, shot on Arri Alexa 65,
35mm film grain, anamorphic lens, shallow depth of field, Kodak Portra 400"

LAYER 2 — SHOT TYPE + LENS:
"[Shot type] [angle], [focal length]mm lens, f/[aperture]"
Examples: "Medium close-up, eye-level, 85mm lens, f/2.8"
         "Wide establishing shot, high angle, 24mm lens, f/5.6"
         "Extreme close-up, macro, 135mm lens, f/2.8"

LAYER 3 — SUBJECT (WHO, DETAILED):
"Nationality + age + body type + face details (eyes/nose/lips/jaw/skin/scars) +
hair (color/style/texture/condition) + clothing (garment/material/color/wear)"

LAYER 4 — POSE + ACTION (moment before):
"Body language: [specific posture]. Action: [what they're about to do].
Expression: [specific facial muscle activation]"

LAYER 5 — ENVIRONMENT (WHERE, DETAILED):
"Location: [room type, dimensions, materials]. Objects: [furniture, props, surfaces].
Atmosphere: [dust, humidity, temperature, smell]. Colors: [wall/floor/ceiling]"

LAYER 6 — LIGHTING (HOW LIT):
"Key light: [source, direction, color temp]. Fill: [source, ratio].
Rim: [source, intensity]. Practicals: [visible lights in frame].
Shadows: [depth, direction, softness]"

LAYER 7 — CAMERA (HOW SHOT):
"Camera movement: [one move, speed, direction]. Depth of field: [shallow/deep, what's in focus]"

LAYER 8 — QUALITY SUFFIX (append to every prompt):
"dark atmospheric, moody cinematography, professional color grading,
masterpiece, trending on artstation, cgsociety, hyperdetailed, 8k"

COMPLETE EXAMPLE (all 8 layers):
"hyperrealistic, photorealistic, 8k raw, cinematic lighting, volumetric lighting,
ray tracing, shot on Arri Alexa 65, 35mm film grain. Wide establishing shot,
high corner angle, 24mm lens, f/5.6. A sealed 30-square-meter room with no
windows or doors. Cream-colored lime plaster walls peeling at corners revealing
gray concrete. 3-meter ceiling. Single flickering tungsten filament bulb hanging
from black braided wire at center, casting unstable 2800K warm orange light —
each flicker makes room shadows jump. Thick dust motes dancing slowly in the
light cone. Dark brown round oak table 2m diameter at center, surface covered
with decades of scratches, cup rings, and wear. Antique brass mantel clock 40cm
tall at table center, enamel face yellowed, acanthus leaf relief corroded by
green patina. Ten men and women of various ages (25-60) slumped unconscious
around the table — some faces pressed against wood, others leaning back in
chairs. Various clothing: worn wool sweaters, stained cotton shirts, faded
denim. One figure stands beside the table: tall lean man in tailored black wool
suit, wearing an actual taxidermied goat head as a mask — yellowed white fur
matted and clumped, irregular gray eye holes revealing wet human eyes behind.
Key light: single tungsten bulb overhead, 2800K. Deep shadows in all four
corners approaching pure black. Camera slowly pushes in. dark atmospheric,
moody cinematography, masterpiece."
"""

# ═══════════════════════════════════════════════════════════
# MODULE 4: Camera Movement Encyclopedia
# ═══════════════════════════════════════════════════════════

CAMERA_ENCYCLOPEDIA = """
╔══════════════════════════════════════════════════════════════╗
║  CAMERA MOVEMENT ENCYCLOPEDIA — 17 TECHNIQUES ║
╚══════════════════════════════════════════════════════════════╝

PUSH MOVEMENTS (toward subject — intensify, reveal detail):
  slow dolly in — camera physically moves forward, background expands, subject grows
  creeping zoom — lens focal length increases, compresses space, isolates subject
  subtle push forward — minimal movement, just enough to feel alive
  crash zoom — extremely fast zoom, shock/comedy/emphasis

PULL MOVEMENTS (away from subject — reveal context, isolate):
  slow pull out — camera backs away, more environment revealed
  dramatic dolly back — fast pull, subject shrinks, overwhelmed by space
  vertigo dolly zoom — dolly + zoom opposite directions, perspective warps (Hitchcock)

PAN MOVEMENTS (horizontal rotation — follow, reveal):
  slow pan left/right — horizontal sweep, landscape or room reveal
  whip pan — extremely fast horizontal blur, energy, transition
  180-degree rule — stay on same side of action axis between cuts

TILT MOVEMENTS (vertical rotation — power, height):
  tilt up — subject grows in frame, conveys power/dominance
  tilt down — subject shrinks, conveys vulnerability/smallness
  Dutch angle — camera tilted diagonally, unease/disorientation

TRACKING MOVEMENTS (lateral follow — immersion):
  tracking shot alongside subject — camera moves parallel, subject stays in frame
  dolly track — camera on rails, smooth lateral flow
  following shot — camera behind subject, viewer follows their journey

ORBIT/ARC MOVEMENTS (circular — dramatic emphasis):
  slow orbit — camera circles subject, reveals all angles
  hero arc — 180-degree arc around subject, epic moment
  360-degree rotation — full circle, bullet-time effect

CRANE/JIB MOVEMENTS (vertical — scale, grandeur):
  crane up — camera ascends, reveals larger scene
  crane down — camera descends, focuses on detail
  jib swing — curved path, dynamic transition

HANDHELD (organic — realism, tension):
  subtle handheld — micro-shake, documentary realism, presence
  shaky handheld — pronounced shake, chaos/urgency/fear
  shoulder mount — natural breathing rhythm, immersive POV

STEADICAM/GIMBAL (smooth — cinematic tracking):
  floating glide — weightless smooth movement through space
  gimbal walk — following subject with stabilized camera

STATIC (contemplative — only when motivated):
  locked tripod — zero movement, meditation, stillness, let action speak
  USE SPARINGLY — every other shot should have movement

KEY RULES:
1. ONE camera move per shot. Multiple simultaneous moves cause video artifacts.
2. Describe speed: "slow", "gentle", "subtle", "gradual" or "fast", "rapid", "dramatic"
3. Describe direction: "left to right", "bottom to top", "clockwise", "toward subject"
4. Match movement to emotion: push= intensify, pull= isolate, handheld= tension
"""

# ═══════════════════════════════════════════════════════════
# MODULE 5: Character Bible System
# ═══════════════════════════════════════════════════════════

CHARACTER_BIBLE = """
╔══════════════════════════════════════════════════════════════╗
║  CHARACTER BIBLE SYSTEM — IDENTITY LOCKING ║
╚══════════════════════════════════════════════════════════════╝

Each character must be defined ONCE in the characters array, then referenced
consistently in every shot. The AI must copy the exact same description.

REQUIRED FIELDS per character:
  name: full name or identifier
  nationality: specific country + ethnicity (affects bone structure, skin, hair)
  age: exact number + visible age signs (wrinkles, grey hair, skin texture)
  height_cm: exact height in centimeters
  build: body type description (not just "average" but specific)
  face_shape: oval/round/square/heart/diamond/rectangular
  skin: color + undertone + texture + conditions (acne, scars, pores, freckles, moles)

  eyes:
    shape (almond/round/hooded/monolid/deep-set)
    color (specific shade, not just "brown")
    spacing (wide-set/close-set/normal)
    details (crow's feet, dark circles, epicanthal fold, eyelash length)

  nose:
    bridge (high/low/flat)
    width (narrow/wide)
    tip (pointed/rounded/bulbous/upturned)
    details (nostril shape, deviation, broken nose scar)

  mouth:
    lip_shape (full/thin/cupid's bow/uneven)
    lip_color (natural pink/pale/dark/chapped)
    teeth (straight/crooked/gap/missing/yellowed/white)
    details (laugh lines, lip scars, facial hair pattern)

  jaw_chin: shape + definition + facial hair

  hair:
    style (exact cut description)
    color (specific shade + highlights/grey)
    length (measurement)
    texture (straight/wavy/curly/coarse/fine)
    condition (oily/dry/split ends/healthy/greying pattern)

  distinguishing_mark: at least ONE unique, instantly recognizable feature
    (scar, birthmark, tattoo, missing tooth, heterochromia, crooked feature, mole constellation)

  clothing:
    each garment (type + material + color + fit + condition)
    shoes (type + condition)
    accessories (watch, jewelry, glasses — be specific)

  posture: how they hold themselves (slouch, erect, guarded, relaxed)

  voice: speaking style for dialogue (pace, pitch, accent, vocal fry, breathiness)

CHARACTER CONSISTENCY RULES:
1. First appearance = full description. Subsequent shots = reference by name + distinguishing mark only
2. Clothing does NOT change between shots (same scene)
3. Lighting changes how features appear but not the features themselves
4. Camera angle changes perspective but not the subject
5. NEVER create new details for a character after their first definition
"""

# ═══════════════════════════════════════════════════════════
# MODULE 6: Scene Continuity System
# ═══════════════════════════════════════════════════════════

SCENE_CONTINUITY = """
╔══════════════════════════════════════════════════════════════╗
║  SCENE CONTINUITY SYSTEM — SPATIAL LOCKING ║
╚══════════════════════════════════════════════════════════════╝

The scene must be defined ONCE in the scene object, then EVERY shot
must maintain spatial consistency.

SCENE DEFINITION (in scene object):
  location: name and type of space
  dimensions: width × depth × height in meters
  walls: material + color + condition + details (peeling paint, cracks, stains)
  floor: material + color + pattern + wear
  ceiling: height + material + features (beams, pipes, light fixtures)

  light_sources (array, each with):
    type: (tungsten bulb / window / candle / neon / fluorescent / LED)
    position: exact location in room coordinates
    color_temp: in Kelvin (2800K warm, 5600K neutral, 8000K cold)
    intensity: bright/dim/flickering/steady
    direction: where the light falls, what it illuminates

  furniture (array, each with):
    name: item identifier
    position: location relative to walls or other objects
    material: wood/metal/fabric/plastic + specific type
    color: exact shade
    condition: new/worn/damaged/antique + specific wear marks

  atmosphere:
    temperature_feel: cold/drafty/stuffy/warm
    humidity: dry/normal/damp/wet
    air_quality: clear/dusty/smoky/foggy
    smell_hints: what would you smell (mold, coffee, blood, old wood, perfume)

SPATIAL CONTINUITY RULES:
1. Light source positions NEVER change between shots
2. Furniture positions NEVER move
3. Shadow directions must be consistent (light from window A means shadows fall AWAY from window A)
4. Characters maintain spatial relationships (if A is left of B in shot 1, A is left of B in shot 3)
5. 180-degree rule: camera stays on same side of the action axis
6. Eye-line matches: if character looks at clock in shot 2, clock must be at that position in all shots
"""

# ═══════════════════════════════════════════════════════════
# MODULE 7: Director Style Reference
# ═══════════════════════════════════════════════════════════

DIRECTOR_STYLE_REFERENCE = """
╔══════════════════════════════════════════════════════════════╗
║  DIRECTOR & FILM STYLE REFERENCE ║
╚══════════════════════════════════════════════════════════════╝

When a style is specified, apply its visual language to ALL shots.

WES ANDERSON — symmetrical composition, pastel candy colors, centered framing,
flat lay aesthetic, meticulous production design, retro props, whimsical tone

WONG KAR-WAI — saturated emotional colors (deep red, emerald green, electric blue),
slow motion, handheld camera, neon signs, motion blur, nostalgic romantic, dreamy bokeh,
cigarette smoke atmosphere, Hong Kong urban isolation

ZHANG YIMOU — bold monochromatic dominance (red/black/white), Chinese cultural symbolism,
epic scale, theatrical spotlighting, traditional architecture, ink wash aesthetic,
dramatic colored gels, martial arts elegance

CHRISTOPHER NOLAN — cool desaturated palette (steel blue, grey), architectural grandeur,
IMAX wide format, practical effects aesthetic, chiaroscuro lighting, cerebral atmosphere,
time manipulation visual motifs, realistic sci-fi

QUENTIN TARANTINO — vivid saturated retro (yellow, orange, red), 1970s grindhouse,
extreme close-ups, trunk shot perspective, low/high dramatic angles, violence aesthetics,
theatrical blood effects, stylized action

RIDLEY SCOTT — epic widescreen, industrial design, volumetric god rays, atmospheric haze,
desaturated earth tones, smoke and fog, gritty realism, detailed production design

AKIRA KUROSAWA — dynamic symmetry, weather as narrative (rain, wind, fog), monochrome
or desaturated, telephoto compression, axial cuts, Japanese classical architecture,
humanistic depth, nature elements

TIM BURTON — gothic macabre, German expressionist lighting, exaggerated character
proportions (large eyes, thin limbs), twisted surreal architecture, black and white
spiral patterns, stop-motion texture, dark fantasy

ANG LEE — East-West fusion, poetic natural lighting, restrained elegant composition,
emotional subtlety, cultural symbolism, contemplative mood, soft muted palette

FILM NOIR — high contrast B&W, low-key lighting, dramatic venetian blind shadows,
urban nightscape, 1940s aesthetic, moody crime atmosphere, chiaroscuro

CYBERPUNK — neon-drenched cityscape (cyan, magenta, purple), rain-soaked streets,
holographic ads, urban decay, high-tech low-life, Blade Runner aesthetic

STUDIO GHIBLI — soft pastels (green, blue, gold), hand-drawn watercolor, detailed
nature, fluffy clouds, gentle diffused lighting, whimsical dreamy, nostalgic

FRENCH NEW WAVE — handheld camera, natural lighting, candid street photography,
on-location shooting, 1960s Parisian, existential mood, jump cuts, spontaneous
"""

# ═══════════════════════════════════════════════════════════
# MODULE 8: Video Generation Technical Reference
# ═══════════════════════════════════════════════════════════

VIDEO_TECH_REFERENCE = """
╔══════════════════════════════════════════════════════════════╗
║  VIDEO GENERATION TECHNICAL REFERENCE ║
╚══════════════════════════════════════════════════════════════╝

SULPHUR 2 / LTX 2.3 (primary model):
  Architecture: 22B DiT (Lightricks LTX 2.3 base), MIT license, T2V + I2V + audio native
  Resolution: up to 4K (divisible by 32), 1024×1024 or 1088×608 (16:9) for 16GB GGUF Q4
  CFG: 2.0-5.0 (default 3.0-3.5; lower = more motion, higher = more faithful)
  Image Strength: 0.75-0.85
  Sampler: Euler + ManualSigmas
  Valid Frames: (F-1) % 8 == 0 → 49, 73, 97, 121, 201, 241
  Duration: 4-8 seconds at 24fps optimal
  VRAM: 16GB with GGUF Q4 handles 1024×1024 at 121 frames; FP8 needs 24GB+
  Built-in audio VAE: generates synchronized audio from latent (use "no speech" in negative prompt)
  Built-in x2 spatial upscaler + x2 temporal upscaler (FPS doubling)

  MOTION TIERS (success rate):
  HIGH SUCCESS (>90%): subtle head turns, slow hand gestures, micro-expressions,
    breathing motion, slow push in/out, gentle pan, hair sway, blinking
  MEDIUM SUCCESS (~70%): walking slowly, reaching for objects, turning around,
    simple object pick-up, standing up from chair, light hug
  LOW SUCCESS (<40%): running, fighting, dancing, complex multi-person interaction,
    hand-object precision tasks, undressing, large turns

WAN 2.2 (secondary/fallback model):
  Architecture: 14B dual-stage (High Noise + Low Noise)
  Resolution: 640×640 → 4x upscale to 2560×2560
  CFG: 1.0 (both stages)
  Steps: 4 per stage (with Lightning LoRAs)
  Sampler: Euler, Scheduler: Simple
  Shift: 5.0
  Performance: ~97s first gen, ~71s subsequent gens

  CRITICAL: At CFG 1.0, negative prompts are IGNORED entirely
  CRITICAL: Bake ALL constraints into positive prompt

PROMPT_VIDEO FORMAT:
  The prompt_video field describes MOTION and CAMERA MOVEMENT ONLY.
  The input image already anchors all visual details (who, what, where).

  DO describe: camera direction + speed + subject movement + expression change
  DO NOT describe: visual appearance, colors, clothing, environment (image has these)

  Always include: "no speech, no dialogue, silent, instrumental only" (for Sulphur)

  Example prompt_video: "Slow dolly in toward subject's face. Subject's eyes widen
  slightly, jaw tightens. Subtle micro-shake from handheld breathing. Camera pushes
  forward gradually through dusty air. No speech, no dialogue, silent."
"""

# ═══════════════════════════════════════════════════════════
# MODULE 9: Z-Image Turbo Reference
# ═══════════════════════════════════════════════════════════

ZIMAGE_REFERENCE = """
╔══════════════════════════════════════════════════════════════╗
║  Z-IMAGE TURBO — STILL IMAGE GENERATION ║
╚══════════════════════════════════════════════════════════════╝

Model: 6B S3-DiT, few-step distilled text-to-image
Sampler: Euler (primary), DPM++ 2M Karras (alternative)
Steps: 8 (sweet spot), range 4-9
CFG: 1.0 (MANDATORY — model designed for this)
Scheduler: Beta or Simple
Resolution: 1024×1024 standard, portrait 832×1216, landscape 1216×832
Prompt Length: 80-300 words optimal (longer may truncate)

CRITICAL: At CFG 1.0, negative prompts are SILENTLY IGNORED.
Do NOT use negative prompts. Bake all exclusions into positive prompt.
Instead of "no text, no watermark" → "clean professional photograph, no overlays"

ANTI-PATTERNS:
✗ CFG > 2.0 (10x slower, saturation artifacts)
✗ Negative prompts (ignored, wastes tokens)
✗ Contradictory style words ("photorealistic cartoon")
✗ Vague descriptors ("beautiful", "nice", "good")
✗ Over 300 word prompts (truncation risk)

OPTIMAL PROMPT STRUCTURE:
[Quality modifiers] + [Shot type + composition] + [Subject with ALL details] +
[Environment with ALL details] + [Lighting with ALL details] +
[Camera/Lens] + [Style reference] + [Quality suffix]

The CLIP text encoder is qwen_3_4b, type=lumina2.
VAE: ae.safetensors
Model file: z_image_turbo_bf16.safetensors
"""

# ═══════════════════════════════════════════════════════════
# MODULE 10: Editing & Pacing Reference
# ═══════════════════════════════════════════════════════════

EDITING_REFERENCE = """
╔══════════════════════════════════════════════════════════════╗
║  EDITING & PACING REFERENCE ║
╚══════════════════════════════════════════════════════════════╝

MICRO-DRAMA PACING (60-120 second content):
  Hook (0-15s): immediate conflict reveal, no setup, grab attention in 3 seconds
  Friction (15-60s): visible conflict escalation, each line advances conflict
  Spike (60-90s): maximum turning point, silent visual should still convey impact
  Button (last 5-10s): cut on "question" not "answer", end 2 seconds early

SHOT DURATION GUIDELINES:
  Fast action: ≤1.5 seconds per shot
  Dialogue: 2.5-4 seconds (Chinese ~3 chars/second speech rate)
  Emotional beat: 3-5 seconds (let emotion land)
  Montage: 0.3-0.7 seconds (rapid cuts)
  Establishing wide: 4-8 seconds (let viewer absorb environment)

TRANSITION RULES:
  Same scene, continuous action → HARD CUT (no transition)
  Scene change, time passage → CROSS DISSOLVE (0.5-1 second)
  Emotional shift → DIP TO BLACK (0.3 seconds)
  High energy/impact → FLASH WHITE (0.1-0.2 seconds)
  Match cut → direct cut on similar composition/shape/motion

J-CUT / L-CUT:
  J-cut: audio from next shot starts BEFORE video cuts (pre-lap, 0.2-0.5 seconds)
  L-cut: audio from current shot continues AFTER video cuts (post-lap)
  Use for natural dialogue flow and emotional transitions

BGM DUCKING:
  Dialogue active → music volume 15-30% of original
  Attack time: 100ms (fast duck)
  Release time: 500-1000ms (slow return)
  Genre match: micro-drama = electronic/tension, documentary = ambient/piano
"""

# ═══════════════════════════════════════════════════════════
# MODULE 11: Cinematic Shot Grammar
# ═══════════════════════════════════════════════════════════

CINEMATIC_GRAMMAR = """
╔══════════════════════════════════════════════════════════════╗
║  CINEMATIC SHOT GRAMMAR ║
╚══════════════════════════════════════════════════════════════╝

SHOT SIZE PROGRESSION:
  Establishing (wide) → Medium coverage → Close-up reveal → Return to wide (breather)
  Each cut should jump at least 2 shot sizes (wide→close-up, not wide→medium)
  Close-ups are EARNED — use only for emotional peaks, max 20% of shots

CAMERA ANGLES AND MEANING:
  Eye-level: neutral, objective, observational — the viewer is present
  Low angle (looking up): power, dominance, intimidation, heroism
  High angle (looking down): vulnerability, weakness, isolation, overview
  Dutch angle: unease, disorientation, psychological instability
  Over-the-shoulder: intimacy, conversation, shared perspective
  POV: immersion, identification with character

DEPTH OF FIELD GUIDELINES:
  Shallow (f/1.4-f/2.8): isolate subject from environment, emotional focus, portrait
  Medium (f/4-f/8): balance subject and environment, narrative coverage
  Deep (f/11-f/16): everything in focus, environmental storytelling, establishing

COMPOSITION RULES:
  Rule of thirds: key elements at intersection points of 3×3 grid
  Leading lines: architecture/nature lines that guide eye to subject
  Frame within frame: doorways, windows, arches that contain the subject
  Negative space: empty area that emphasizes isolation or scale
  Headroom: space above subject's head (more = vulnerable, less = confined)
  Look room: space in direction subject is facing/looking

180-DEGREE RULE:
  Draw imaginary line through the action axis
  Camera stays on ONE side of this line for the entire scene
  Crossing the line disorients the viewer (only break intentionally for effect)

30-DEGREE RULE:
  Between cuts on same subject, camera angle must change ≥30 degrees
  Smaller angle changes feel like awkward jump cuts
"""

# ═══════════════════════════════════════════════════════════
# MODULE 12: Professional Editing Workflow
# ═══════════════════════════════════════════════════════════

PROFESSIONAL_WORKFLOW = """
╔══════════════════════════════════════════════════════════════╗
║  PROFESSIONAL EDITING WORKFLOW ║
╚══════════════════════════════════════════════════════════════╝

9-STEP EDITING PIPELINE (industry standard):
  1. MATERIAL REVIEW: watch ALL footage 1-2 times, note key moments, log shots
  2. STORY STRUCTURE: outline narrative arc, identify emotional beats, plan rhythm
  3. SHOT SELECTION: categorize by scene/shot type, select best takes
  4. ROUGH CUT: assemble in narrative order, focus on story flow not timing
  5. FINE CUT: adjust rhythm and pacing, remove redundant frames, tighten every scene
  6. SOUND DESIGN: add music track, sync sound effects, balance levels
  7. COLOR GRADE: unify look across all shots, apply creative LUT, match skin tones
  8. TITLES + GRAPHICS: add subtitles, lower thirds, opening/closing titles
  9. FINAL EXPORT: render at target resolution, verify on multiple screens

3-SECOND VISUAL CHANGE RULE:
  Every ~3 seconds, something must visually change — a cut, a zoom, a new text layer,
  a transition effect, a camera move. This maintains viewer attention.

ATTENTION RESET:
  Insert a rhythm change every 45-60 seconds (fast→slow or slow→fast)
  Create a peak moment every 60-90 seconds (emotional high point)
"""

# ═══════════════════════════════════════════════════════════
# AGGREGATION
# ═══════════════════════════════════════════════════════════

def get_prompt_knowledge() -> str:
    """Return all knowledge modules concatenated."""
    modules = [
        FIRST_FRAME_RULE,
        HYPERREALISTIC_PROTOCOL,
        PROMPT_CONSTRUCTION,
        CAMERA_ENCYCLOPEDIA,
        CHARACTER_BIBLE,
        SCENE_CONTINUITY,
        DIRECTOR_STYLE_REFERENCE,
        VIDEO_TECH_REFERENCE,
        ZIMAGE_REFERENCE,
        EDITING_REFERENCE,
        CINEMATIC_GRAMMAR,
        PROFESSIONAL_WORKFLOW,
    ]
    return "\n\n".join(modules)


def get_module(name: str) -> str:
    """Get a specific knowledge module by name."""
    modules = {
        "first_frame": FIRST_FRAME_RULE,
        "hyperrealistic": HYPERREALISTIC_PROTOCOL,
        "prompt_formula": PROMPT_CONSTRUCTION,
        "camera": CAMERA_ENCYCLOPEDIA,
        "characters": CHARACTER_BIBLE,
        "scene": SCENE_CONTINUITY,
        "directors": DIRECTOR_STYLE_REFERENCE,
        "video": VIDEO_TECH_REFERENCE,
        "zimage": ZIMAGE_REFERENCE,
        "editing": EDITING_REFERENCE,
        "grammar": CINEMATIC_GRAMMAR,
        "workflow": PROFESSIONAL_WORKFLOW,
    }
    return modules.get(name, "")
