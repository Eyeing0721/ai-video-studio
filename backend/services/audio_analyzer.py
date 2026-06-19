"""Audio auto-tagging — detect BPM, key, energy, beat positions for uploaded audio.

Uses librosa for analysis when available, with a fallback to basic FFmpeg metadata.
This feeds the asset tagging system: upload a BGM track and get auto-suggested tags.

Beat positions enable automatic 卡点 (beat-sync) editing — cutting on detected beats.
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def _has_librosa() -> bool:
    try:
        import librosa  # noqa: F401
        return True
    except ImportError:
        return False


def analyze_ffmpeg_basic(audio_path: str | Path) -> dict:
    """Basic analysis using FFmpeg (always available)."""
    path = str(audio_path)
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}

    data = json.loads(result.stdout)

    info: dict = {
        "duration_sec": 0.0,
        "sample_rate": 0,
        "channels": 0,
        "bitrate_kbps": 0,
        "codec": "unknown",
    }

    fmt = data.get("format", {})
    info["duration_sec"] = float(fmt.get("duration", 0))
    info["bitrate_kbps"] = int(int(fmt.get("bit_rate", 0)) / 1000)

    for stream in data.get("streams", []):
        if stream.get("codec_type") == "audio":
            info["sample_rate"] = int(stream.get("sample_rate", 0))
            info["channels"] = stream.get("channels", 0)
            info["codec"] = stream.get("codec_name", "unknown")
            break

    return info


def analyze_librosa(audio_path: str | Path) -> dict:
    """Full analysis using librosa: BPM, key, spectral features, beat positions."""
    import librosa
    import numpy as np

    path = str(audio_path)

    # Load audio (first 120 seconds max for speed)
    y, sr = librosa.load(path, sr=None, duration=120, mono=True)

    info: dict = analyze_ffmpeg_basic(path)

    # ── Tempo (BPM) ──────────────────────────────────────
    try:
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        info["bpm"] = round(float(tempo))
        # Beat positions in seconds
        beat_times = librosa.frames_to_time(beats, sr=sr)
        info["beat_times"] = [round(float(t), 2) for t in beat_times[:100]]  # first 100 beats
        info["beat_count"] = len(beat_times)
    except Exception as e:
        logger.warning(f"BPM detection failed: {e}")
        info["bpm"] = 0

    # ── Spectral features ────────────────────────────────
    try:
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        info["spectral_centroid_mean"] = round(float(np.mean(spectral_centroid)), 1)
    except Exception:
        pass

    try:
        # Energy / RMS
        rms = librosa.feature.rms(y=y)
        energy = float(np.mean(rms))
        info["rms_energy"] = round(energy, 4)
    except Exception:
        pass

    # ── Key detection (simple Krumhansl-Schmuckler) ─────
    try:
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        # Major and minor key profiles
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        best_major = -1
        best_minor = -1
        best_major_score = -999
        best_minor_score = -999

        for i in range(12):
            score = np.corrcoef(chroma_mean, np.roll(major_profile, i))[0, 1]
            if score > best_major_score:
                best_major_score = score
                best_major = i
            score = np.corrcoef(chroma_mean, np.roll(minor_profile, i))[0, 1]
            if score > best_minor_score:
                best_minor_score = score
                best_minor = i

        info["key_major"] = keys[best_major] if best_major >= 0 else "?"
        info["key_minor"] = keys[best_minor] if best_minor >= 0 else "?"
        info["key_confidence"] = round(float(max(best_major_score, best_minor_score)), 3)
    except Exception as e:
        logger.warning(f"Key detection failed: {e}")

    # ── Onset detection (transient points for beat-sync) ─
    try:
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units="time")
        info["onset_times"] = [round(float(t), 2) for t in onset_frames[:200]]
        info["onset_count"] = len(onset_frames)
    except Exception:
        pass

    # ── Mood inference from features ─────────────────────
    info["suggested_tags"] = _infer_tags_from_audio(info)

    return info


def _infer_tags_from_audio(info: dict) -> list[str]:
    """Infer mood/genre tags from audio features."""
    tags: list[str] = []

    bpm = info.get("bpm", 0)
    energy = info.get("rms_energy", 0)
    centroid = info.get("spectral_centroid_mean", 0)

    # Tempo-based
    if bpm < 60:
        tags.extend(["慢节奏", "舒缓"])
    elif bpm < 90:
        tags.extend(["中速", "轻松"])
    elif bpm < 120:
        tags.extend(["中等", "流畅"])
    elif bpm < 150:
        tags.extend(["快节奏", "动感"])
    else:
        tags.extend(["高速", "激烈"])

    # Energy-based
    if energy < 0.02:
        tags.extend(["柔和", "环境"])
    elif energy < 0.05:
        tags.extend(["中等能量"])
    elif energy < 0.1:
        tags.extend(["高能量", "强劲"])
    else:
        tags.extend(["极高能量", "爆发"])

    # Spectral centroid (brightness)
    if centroid < 1500:
        tags.append("暗色调")
    elif centroid < 3000:
        tags.append("中性")
    else:
        tags.append("明亮")

    # Key-based emotional hint
    key = info.get("key_minor", "")
    if key and key != "?":
        tags.append(f"小调-{key}")
    key = info.get("key_major", "")
    if key and key != "?":
        tags.append(f"大调-{key}")

    return tags


def analyze(audio_path: str | Path) -> dict:
    """Analyze an audio file and return comprehensive metadata."""
    path = str(audio_path)

    if _has_librosa():
        logger.info(f"Analyzing with librosa: {path}")
        return analyze_librosa(path)
    else:
        logger.info(f"Analyzing with FFmpeg only: {path} (pip install librosa for full analysis)")
        info = analyze_ffmpeg_basic(path)
        info["_limited"] = "librosa not installed, BPM/key detection unavailable"
        return info


def get_beat_grid(audio_path: str | Path, bpm: float | None = None) -> list[float]:
    """Get a beat grid (timestamps for each beat) for beat-sync editing.

    If BPM is known, generates the grid without loading the full file.
    Otherwise uses librosa onset detection.
    """
    if bpm:
        info = analyze_ffmpeg_basic(str(audio_path))
        duration = info.get("duration_sec", 30)
        beat_interval = 60.0 / bpm
        return [round(i * beat_interval, 2) for i in range(int(duration / beat_interval))]

    if _has_librosa():
        import librosa
        y, sr = librosa.load(str(audio_path), sr=None, duration=120, mono=True)
        _, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        return [round(float(t), 2) for t in beat_times]

    return []
