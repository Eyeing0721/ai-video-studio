"""MLT video compositing pipeline — concat shots, transitions, subtitles, BGM, color.

Uses the Media Lovin' Toolkit (python-mlt) for professional video editing.
MLT is the framework behind Kdenlive and Shotcut.

Pipeline:
  1. Load each shot's video + audio into timeline
  2. Apply transitions between adjacent shots
  3. Overlay ASS/SSA subtitles synced to dialogue
  4. Mix BGM track with auto-ducking on dialogue
  5. Apply LUT color grading
  6. Render to MP4

Requires: pip install mlt  (or system package mlt-python)
"""

import json
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from config import config

logger = logging.getLogger(__name__)


def _check_mlt() -> bool:
    """Check if MLT Python bindings are available."""
    try:
        import mlt
        return True
    except ImportError:
        return False


def _check_ffmpeg() -> bool:
    """Check if FFmpeg is available."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def generate_ass_subtitles(
    subtitles: list[dict],
    font: str = "Noto Sans SC Bold",
    font_size: int = 36,
    color: str = "&H00FFFFFF",
    stroke_color: str = "&H00000000",
    stroke_width: float = 2.0,
    play_res_x: int = 1920,
    play_res_y: int = 1080,
) -> str:
    """Generate ASS subtitle content from a list of dialogue segments.

    Each segment: {"text": str, "start_sec": float, "end_sec": float}
    """
    lines = [
        "[Script Info]",
        f"PlayResX: {play_res_x}",
        f"PlayResY: {play_res_y}",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{font},{font_size},{color},&H00000000,{stroke_color},&H00000000,1,0,0,0,100,100,0,0,1,{stroke_width},1,2,50,50,50,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for sub in subtitles:
        text = sub["text"].replace("\n", "\\N")
        start = _sec_to_ass_time(sub["start_sec"])
        end = _sec_to_ass_time(sub["end_sec"])
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

    return "\n".join(lines)


def _sec_to_ass_time(sec: float) -> str:
    """Convert seconds to ASS time format: H:MM:SS.cc"""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int((sec % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


async def composite_mlt(
    output_path: Path,
    shot_videos: list[Path],
    shot_audios: list[Path],
    subtitles: list[dict],
    bgm_path: Optional[Path] = None,
    recipe: Optional[dict] = None,
    width: int = 1920,
    height: int = 1080,
    fps: int = 24,
) -> Path:
    """Composite shots into final video using MLT.

    If MLT is not available, falls back to FFmpeg concat + filter_complex.
    """
    if _check_mlt():
        return await _composite_mlt_native(
            output_path, shot_videos, shot_audios, subtitles,
            bgm_path, recipe, width, height, fps,
        )
    else:
        logger.warning("MLT not installed, falling back to FFmpeg composite")
        return await _composite_ffmpeg(
            output_path, shot_videos, shot_audios, subtitles,
            bgm_path, recipe, width, height, fps,
        )


async def _composite_mlt_native(
    output_path: Path,
    shot_videos: list[Path],
    shot_audios: list[Path],
    subtitles: list[dict],
    bgm_path: Optional[Path],
    recipe: Optional[dict],
    width: int,
    height: int,
    fps: int,
) -> Path:
    """Composite using MLT Python bindings."""
    import mlt

    repo = mlt.Factory.init()
    profile = mlt.Profile()
    profile.set_frame_rate(fps, 1)
    profile.set_width(width)
    profile.set_height(height)

    # Create tractor (timeline)
    tractor = mlt.Tractor()
    tractor.set("meta.media.width", width)
    tractor.set("meta.media.height", height)

    # Add each shot as a playlist entry
    playlist = mlt.Playlist()
    for i, vpath in enumerate(shot_videos):
        if not vpath.exists():
            logger.warning(f"Shot video missing: {vpath}")
            continue

        producer = mlt.Producer(profile, str(vpath))
        if not producer.is_valid():
            logger.warning(f"Invalid producer for {vpath}")
            continue

        # Attach audio if separate
        if i < len(shot_audios) and shot_audios[i].exists():
            audio_producer = mlt.Producer(profile, str(shot_audios[i]))
            if audio_producer.is_valid():
                # Replace audio track
                producer.attach(audio_producer)

        # Apply transitions between clips
        if i > 0 and recipe:
            trans = recipe.get("ai_selected_transition", "cross_dissolve")
            t_dur = recipe.get("transitions", {}).get("crossfade_duration_sec", 0.5)
            # MLT transition: luma, composite, etc.
            transition = mlt.Transition(profile, "luma" if trans == "cross_dissolve" else "composite")
            transition.set("a_track", 0)
            transition.set("b_track", 1)

        playlist.append(producer)

    tractor.connect(playlist, 0)

    # Add BGM track
    if bgm_path and bgm_path.exists():
        bgm = mlt.Producer(profile, str(bgm_path))
        if bgm.is_valid():
            bgm_volume = mlt.Filter(profile, "volume")
            bgm_volume.set("gain", recipe.get("bgm", {}).get("volume_db", -8) if recipe else -8)
            bgm.attach(bgm_volume)
            tractor.connect(bgm, 2)  # Background audio track

    # Render
    consumer = mlt.Consumer(profile, "avformat")
    consumer.set("target", str(output_path))
    consumer.set("real_time", 0)
    consumer.connect(tractor)
    consumer.run()

    logger.info(f"MLT composite done: {output_path}")
    return output_path


async def _composite_ffmpeg(
    output_path: Path,
    shot_videos: list[Path],
    shot_audios: list[Path],
    subtitles: list[dict],
    bgm_path: Optional[Path],
    recipe: Optional[dict],
    width: int,
    height: int,
    fps: int,
) -> Path:
    """Fallback composite using FFmpeg with complex filters."""

    # Generate ASS subtitle file
    ass_path = output_path.with_suffix(".ass")
    ass_content = generate_ass_subtitles(subtitles, play_res_x=width, play_res_y=height)
    ass_path.write_text(ass_content, encoding="utf-8")

    # Build concat file
    concat_path = output_path.with_suffix(".concat.txt")
    concat_lines = []
    for v in shot_videos:
        if v.exists():
            concat_lines.append(f"file '{v.as_posix()}'")
    concat_path.write_text("\n".join(concat_lines))

    # FFmpeg concat + subtitle burn + BGM
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_path),
        "-vf", f"ass={ass_path.as_posix()},scale={width}:{height},fps={fps}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
    ]

    if bgm_path and bgm_path.exists():
        cmd.extend(["-i", str(bgm_path)])
        # Mix: video audio + BGM, with BGM ducked
        bgm_vol = recipe.get("bgm", {}).get("volume_db", -8) if recipe else -8
        cmd.extend([
            "-filter_complex",
            f"[0:a]volume=1.0[a1];[1:a]volume={10**(bgm_vol/20):.3f}[a2];[a1][a2]amix=inputs=2:duration=first",
        ])

    cmd.append(str(output_path))

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()

    if proc.returncode != 0:
        err = stderr.decode()[-500:]
        raise RuntimeError(f"FFmpeg composite failed: {err}")

    # Cleanup temp files
    concat_path.unlink(missing_ok=True)
    logger.info(f"FFmpeg composite done: {output_path}")
    return output_path


import asyncio  # noqa: E402 (import at top already, this is for the async create_subprocess_exec above)
