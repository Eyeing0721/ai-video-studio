"""Natural-language auto-editing: video clips + instruction -> edited video.

Flow:
1. Analyze input videos (scene detect, duration, resolution)
2. Send video metadata + NL instruction to DeepSeek
3. DeepSeek returns edit decision list (EDL) — cuts, order, transitions, pacing
4. Execute via FFmpeg concat + filters
"""

import asyncio
import json
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def analyze_video(video_path: str | Path) -> dict:
    """Extract video metadata: duration, resolution, fps, scene changes."""
    path = str(video_path)
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr, "path": path}

    data = json.loads(result.stdout)
    info: dict = {
        "path": path,
        "filename": Path(path).name,
        "duration_sec": 0.0,
        "width": 0,
        "height": 0,
        "fps": 0.0,
        "codec": "unknown",
        "file_size_mb": 0,
    }

    fmt = data.get("format", {})
    info["duration_sec"] = round(float(fmt.get("duration", 0)), 1)
    info["file_size_mb"] = round(int(fmt.get("size", 0)) / (1024 * 1024), 1)

    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            info["width"] = stream.get("width", 0)
            info["height"] = stream.get("height", 0)
            fps_str = stream.get("r_frame_rate", "0/1")
            if "/" in fps_str:
                num, den = fps_str.split("/")
                info["fps"] = round(float(num) / float(den), 1) if float(den) != 0 else 0
            info["codec"] = stream.get("codec_name", "unknown")
            break

    # Scene detection
    info["scenes"] = _detect_scenes(path)

    return info


def _detect_scenes(video_path: str) -> list[dict]:
    """Detect scene changes using FFmpeg's scene detection filter."""
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", "select='gt(scene,0.4)',showinfo",
        "-f", "null", "-", "-nostats",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        scenes: list[dict] = []
        for line in result.stderr.split("\n"):
            if "pts_time:" in line:
                t = line.split("pts_time:")[1].split()[0]
                scenes.append({"time_sec": round(float(t), 1)})
        return scenes
    except Exception:
        return []


async def generate_edit_plan(
    videos: list[dict],
    instruction: str,
    template_id: str = "vlog",
    total_duration_sec: int = 60,
    api_key: str = "",
) -> dict:
    """Use DeepSeek to generate an edit decision list from NL instruction."""
    from config import config
    import httpx

    key = api_key or config.get("deepseek_api_key", "")

    # Build a concise video summary for the LLM
    video_summary = []
    for i, v in enumerate(videos):
        scenes_str = ", ".join([f"{s['time_sec']}s" for s in v.get("scenes", [])[:8]])
        video_summary.append(
            f"素材{i+1}: {v['filename']}, {v['duration_sec']}秒, "
            f"{v['width']}x{v['height']}, {v['fps']}fps, "
            f"场景切换点: {scenes_str or '未检测到'}"
        )

    system = f"""你是一位专业视频剪辑师。用户提供{N}段原始素材和一段自然语言剪辑要求。
请根据要求生成剪辑决策清单(EDL)，精确到秒。

可用剪辑风格模板: {template_id}

输出JSON格式：
{{
  "edl": [
    {{"source": 1, "start": 0.0, "end": 3.5, "transition": "hard_cut"}},
    {{"source": 2, "start": 10.0, "end": 13.2, "transition": "cross_dissolve"}},
    ...
  ],
  "bgm_mood": "upbeat",
  "pacing": "fast",
  "explanation": "一句话说明剪辑思路"
}}

规则：
- source: 素材编号(从1开始)
- start/end: 该素材的起止时间(秒)，end-start在2-8秒之间
- transition: hard_cut/cross_dissolve/fade_out/dip_to_black
- 总时长控制在{total_duration_sec}秒以内
- 优先使用高潮/精彩段落
- 每个片段不宜过长

输出纯JSON，不要markdown。"""

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }

    body = {
        "model": "deepseek-v4-pro",
        "max_tokens": 4096,
        "system": system.format(N=len(videos), template_id=template_id, total_duration_sec=total_duration_sec),
        "messages": [{
            "role": "user",
            "content": f"素材信息:\n{chr(10).join(video_summary)}\n\n剪辑要求: {instruction}",
        }],
        "temperature": 0.6,
    }

    base_url = config.get("deepseek_base_url", "https://api.deepseek.com/anthropic")
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{base_url}/v1/messages", headers=headers, json=body)
        r.raise_for_status()
        data = r.json()

    content = data["content"][0]["text"] if isinstance(data["content"], list) else data["content"]
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    return json.loads(content)


async def execute_edl(
    edl: list[dict],
    video_paths: list[str],
    output_path: str | Path,
    fps: float = 30,
) -> Path:
    """Execute an edit decision list — concat video segments with transitions."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Build concat file
    concat_file = output.with_suffix(".concat.txt")
    lines = []
    for i, clip in enumerate(edl):
        src_idx = clip["source"] - 1
        if src_idx < 0 or src_idx >= len(video_paths):
            continue
        src = video_paths[src_idx]
        start = clip["start"]
        end = clip["end"]
        duration = end - start
        if duration <= 0:
            continue

        # Cut the segment
        segment = output.parent / f"seg_{i:03d}.mp4"
        cmd_cut = [
            "ffmpeg", "-y", "-ss", str(start), "-i", src,
            "-t", str(duration), "-c", "copy", "-avoid_negative_ts", "1",
            str(segment),
        ]
        proc = await asyncio.create_subprocess_exec(*cmd_cut)
        await proc.wait()

        if segment.exists():
            lines.append(f"file '{segment.as_posix()}'")
            # Add transition note
            trans = clip.get("transition", "hard_cut")
            if trans == "cross_dissolve":
                lines.append(f"duration 0.5")

    concat_file.write_text("\n".join(lines))

    # Concat all segments
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy",
        str(output),
    ]
    proc = await asyncio.create_subprocess_exec(*cmd_concat)
    await proc.wait()

    # Cleanup segments
    for i in range(len(edl)):
        seg = output.parent / f"seg_{i:03d}.mp4"
        seg.unlink(missing_ok=True)
    concat_file.unlink(missing_ok=True)

    return output
