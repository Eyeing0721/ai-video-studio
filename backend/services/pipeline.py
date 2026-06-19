"""Pipeline orchestrator — chains storyboarding, image gen, video gen, TTS, composite.

Error recovery features:
- Per-step retry with exponential backoff (max 2 retries, 5s base)
- Bidirectional model fallback (Sulphur 2 <-> Wan 2.2 I2V)
- Video quality check via OpenCV Laplacian variance
- Pipeline timeout at 60 minutes
- Individual shot failure does NOT abort the entire pipeline
"""

import asyncio
import json
import logging
import shutil
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

from config import config
from models.task import Task, TaskStatus, Shot
from services.comfyui_client import comfyui
from services.templates import get_template, merge_template_with_ai
from services.tts_client import tts

logger = logging.getLogger(__name__)

OUTPUT_ROOT = Path(config["output_dir"])
GEN = config["generation"]

# ── Error recovery constants ──────────────────────────────

PIPELINE_TIMEOUT_SEC = 60 * 60        # 60 minutes
MAX_RETRIES = 2                        # per-model retries
RETRY_BACKOFF_SEC = 5                  # base backoff (doubles each attempt)
LAPLACIAN_THRESHOLD = 50.0            # below this = likely broken frame


async def create_output_dirs(task_id: str) -> Path:
    base = OUTPUT_ROOT / task_id
    base.mkdir(parents=True, exist_ok=True)
    (base / "shots").mkdir(exist_ok=True)
    (base / "final").mkdir(exist_ok=True)
    return base


async def notify(manager, task_id: str, status: str, label: str, progress: float, **extra):
    """Send WebSocket notification to frontend."""
    if manager:
        try:
            await manager.send(task_id, {
                "type": "status",
                "status": status,
                "label": label,
                "progress": progress,
                **extra,
            })
        except Exception:
            pass


async def retry_with_backoff(func, max_retries=MAX_RETRIES, backoff_sec=RETRY_BACKOFF_SEC, label=""):
    """Execute async func with retries and exponential backoff.

    Args:
        func: Async callable to execute.
        max_retries: Maximum retry attempts (total calls = 1 + max_retries).
        backoff_sec: Base backoff in seconds (doubles each attempt).
        label: Human-readable label for log messages.

    Returns:
        The return value of func() on success.

    Raises:
        The last exception if all attempts fail.
    """
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return await func()
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries:
                delay = backoff_sec * (2 ** attempt)
                logger.warning(
                    "%s attempt %d/%d failed: %s, retrying in %.1fs...",
                    label, attempt + 1, max_retries + 1, exc, delay,
                )
                await asyncio.sleep(delay)
    raise last_exc


def check_video_quality(video_path: str, threshold: float = LAPLACIAN_THRESHOLD) -> bool:
    """Check video quality using OpenCV Laplacian variance.

    Samples the first frame, middle frame, and last frame.  If more than
    half fall below the threshold the video is considered broken.

    Args:
        video_path: Path to the video file.
        threshold: Minimum Laplacian variance to consider a frame good.

    Returns:
        True if video quality is acceptable, False if likely broken.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        logger.warning("Video quality check: cannot open %s", video_path)
        return False

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count == 0:
        cap.release()
        logger.warning("Video quality check: zero frames in %s", video_path)
        return False

    # Sample first, middle, last frame
    sample_indices = [0, frame_count // 2, max(0, frame_count - 1)]
    sample_indices = sorted(set(sample_indices))  # deduplicate for very short clips

    bad_count = 0
    for idx in sample_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            bad_count += 1
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        logger.debug("Frame %d Laplacian variance: %.2f (threshold=%.2f)", idx, variance, threshold)
        if variance < threshold:
            bad_count += 1

    cap.release()

    # Acceptable if at most half the sampled frames are bad
    ok = bad_count <= len(sample_indices) // 2
    if not ok:
        logger.warning(
            "Video quality FAILED for %s: %d/%d sampled frames below threshold %.1f",
            video_path, bad_count, len(sample_indices), threshold,
        )
    return ok


def _check_timeout(start_time: float, task_id: str) -> Optional[float]:
    """Return remaining seconds before timeout, or None if already timed out."""
    elapsed = time.time() - start_time
    if elapsed >= PIPELINE_TIMEOUT_SEC:
        return None
    return PIPELINE_TIMEOUT_SEC - elapsed


async def run_full_pipeline(
    task_id: str,
    session_factory: async_sessionmaker,
    manager=None,
    template_id: str = "micro_drama",
    skip_storyboard: bool = False,
):
    """Execute the complete generation pipeline for a task.

    When skip_storyboard=False (default), the pipeline stops after
    storyboarding and waits for user approval via POST /api/tasks/{id}/approve.
    When skip_storyboard=True, continues from image generation onward.
    """

    pipeline_start = time.time()

    async with session_factory() as s:
        t = await s.get(Task, task_id)
        if not t:
            logger.error(f"Task {task_id} not found")
            return

        output_dir = await create_output_dirs(task_id)
        t.output_dir = str(output_dir)
        comfy_input_dir = Path("F:/ComfyUI/input")
        comfy_input_dir.mkdir(parents=True, exist_ok=True)

        # ── Load template ────────────────────────────────
        template = get_template(template_id) or get_template("micro_drama")

        try:
            # ── Step 1: Storyboarding ────────────────────
            await notify(manager, task_id, "storyboarding", "分镜拆解", 5)
            t.status = TaskStatus.storyboarding
            await s.commit()

            from services.deepseek_client import generate_storyboard

            shots_data = await retry_with_backoff(
                lambda: generate_storyboard(t.input_text or ""),
                max_retries=1,
                backoff_sec=5,
                label="Storyboarding",
            )

            t.storyboard_json = json.dumps(shots_data, ensure_ascii=False)
            await s.commit()

            # Save storyboard to disk
            with open(output_dir / "storyboard.json", "w", encoding="utf-8") as f:
                json.dump(shots_data, f, ensure_ascii=False, indent=2)

            # Insert shots into DB
            for i, shot in enumerate(shots_data):
                s.add(Shot(
                    task_id=task_id,
                    shot_index=i,
                    description=shot.get("description", ""),
                    dialogue=shot.get("dialogue", ""),
                    mood=shot.get("mood", ""),
                    duration_sec=shot.get("duration_sec", 3.0),
                ))
            await s.commit()

            # Re-fetch DB Shot objects so status updates persist to DB
            shots_result = await s.execute(
                select(Shot).where(Shot.task_id == task_id).order_by(Shot.shot_index)
            )
            db_shots = list(shots_result.scalars().all())

            # ── AI dynamic template merge ─────────────────
            moods = [sh.get("mood", "") for sh in shots_data]
            recipe = merge_template_with_ai(
                template, moods,
                sum(sh.get("duration_sec", 3) for sh in shots_data),
            )
            t.recipe_json = json.dumps(recipe, ensure_ascii=False)
            await s.commit()

            # ── Pause for user approval ───────────────────
            if not skip_storyboard:
                await notify(manager, task_id, "awaiting_approval", "等待审批", 10,
                             storyboard=shots_data, recipe=recipe)
                await s.commit()
                return  # Stop here — user calls /approve to continue

            # ── Step 2: Generate keyframes ────────────────
            await notify(manager, task_id, "generating_images", "静态图生成", 15)
            t.status = TaskStatus.generating_images
            await s.commit()

            total_shots = len(shots_data)
            for idx, (shot_dict, db_shot) in enumerate(zip(shots_data, db_shots)):
                # Timeout check
                if _check_timeout(pipeline_start, task_id) is None:
                    raise TimeoutError("Pipeline timed out during keyframe generation")

                shot_path = output_dir / "shots" / f"{shot_dict['id']:03d}"
                shot_path.mkdir(exist_ok=True)

                prompt = shot_dict.get('english_prompt') or f"{shot_dict['description']}, {shot_dict['mood']}, {shot_dict['lighting']}"
                workflow = comfyui.build_txt2img_workflow(
                    positive_prompt=prompt,
                    width=GEN["z_image_width"],
                    height=GEN["z_image_height"],
                )

                try:
                    result = await retry_with_backoff(
                        lambda wf=workflow: comfyui.run_workflow(wf),
                        max_retries=MAX_RETRIES,
                        backoff_sec=RETRY_BACKOFF_SEC,
                        label=f"Keyframe shot {shot_dict['id']}",
                    )
                    # Copy images from ComfyUI output → task dir + input dir
                    for node_id, node_output in result.get("outputs", {}).items():
                        for img in node_output.get("images", []):
                            filename = img.get("filename", "")
                            if filename:
                                src = Path("F:/ComfyUI/output") / filename
                                dst = shot_path / f"keyframe_{shot_dict['id']:03d}.png"
                                if src.exists():
                                    shutil.copy2(src, dst)
                                    db_shot.keyframe_path = str(dst)
                                    input_name = f"avs_shot_{task_id}_{shot_dict['id']:03d}.png"
                                    shutil.copy2(src, comfy_input_dir / input_name)
                    db_shot.status = "keyframe_done"
                except Exception as exc:
                    logger.error(f"Keyframe gen failed for shot {shot_dict['id']}: {exc}")
                    db_shot.status = "failed"
                    db_shot.attempts = MAX_RETRIES + 1
                    await s.commit()
                    continue  # continue pipeline — do not abort

                await s.commit()

                progress = 15 + (idx / total_shots) * 20
                await notify(manager, task_id, "generating_images",
                             f"静态图生成 ({idx+1}/{total_shots})", progress)

            # ── Step 3: Image-to-video ────────────────────
            await notify(manager, task_id, "generating_videos", "图生视频", 35)
            t.status = TaskStatus.generating_videos
            await s.commit()

            prev_last_frame: Optional[Path] = None
            shot_engines: dict[int, str] = {}  # shot AI id -> engine name ("sulphur" | "wan")

            for idx, (shot_dict, db_shot) in enumerate(zip(shots_data, db_shots)):
                # Timeout check
                if _check_timeout(pipeline_start, task_id) is None:
                    raise TimeoutError("Pipeline timed out during video generation")

                shot_id = shot_dict["id"]
                shot_path = output_dir / "shots" / f"{shot_id:03d}"

                prompt = f"{shot_dict['description']}, {shot_dict['mood']}"
                # ComfyUI LoadImage expects filename relative to input/ dir
                comfy_input_name = f"avs_shot_{task_id}_{shot_id:03d}.png"
                image_input = comfy_input_name  # filename only, ComfyUI resolves from input/

                # ── Bidirectional model fallback with per-model retry ──
                # Tries Sulphur first, then Wan. Each model gets retry_with_backoff.
                model_rounds = [
                    ("sulphur", lambda: comfyui.build_img2video_workflow_sulphur(
                        image_input, prompt,
                        width=GEN["sulphur_width"], height=GEN["sulphur_height"],
                    )),
                    ("wan", lambda: comfyui.build_img2video_workflow_wan(
                        image_input, prompt,
                        width=GEN["wan_width"], height=GEN["wan_height"],
                    )),
                ]

                video_generated = False
                for model_label, builder in model_rounds:
                    if video_generated:
                        break
                    try:
                        workflow = builder()
                        result = await retry_with_backoff(
                            lambda wf=workflow: comfyui.run_workflow(wf),
                            max_retries=MAX_RETRIES,
                            backoff_sec=RETRY_BACKOFF_SEC,
                            label=f"I2V shot {shot_id} ({model_label})",
                        )

                        # Copy output from ComfyUI output dir
                        for node_id, outputs in result.get("outputs", {}).items():
                            for out in outputs:
                                if out.get("type") == "image":
                                    filename = out.get("filename", "")
                                    src = Path("F:/ComfyUI/output") / filename
                                    dst = shot_path / f"video_{shot_id:03d}.mp4"
                                    if src.exists():
                                        shutil.copy2(src, dst)
                                        db_shot.video_path = str(dst)

                        # ── Video quality check ────────────
                        if db_shot.video_path and Path(db_shot.video_path).exists():
                            if check_video_quality(db_shot.video_path):
                                video_generated = True
                                db_shot.status = "video_done"
                                shot_engines[shot_id] = model_label
                                logger.info("Shot %d video quality PASSED (%s)", shot_id, model_label)
                                break
                            else:
                                logger.warning(
                                    "Shot %d video quality FAILED (%s), trying alternate model",
                                    shot_id, model_label,
                                )
                                # Clean up bad video file before retry
                                try:
                                    Path(db_shot.video_path).unlink(missing_ok=True)
                                except Exception:
                                    pass
                                db_shot.video_path = None
                                continue
                    except Exception as exc:
                        logger.warning(
                            "Shot %d %s failed: %s", shot_id, model_label, exc,
                        )
                        continue

                if not video_generated:
                    db_shot.status = "video_failed"
                    db_shot.attempts = (MAX_RETRIES + 1) * len(model_rounds)
                    logger.error("Shot %d: all models exhausted, marking failed", shot_id)
                    await s.commit()
                    prev_last_frame = None  # reset continuity for next shot
                else:
                    await s.commit()

                progress = 35 + (idx / total_shots) * 25
                await notify(manager, task_id, "generating_videos",
                             f"图生视频 ({idx+1}/{total_shots})", progress)

                # Extract last frame for next shot continuity
                if db_shot.video_path and Path(db_shot.video_path).exists():
                    cap = cv2.VideoCapture(str(db_shot.video_path))
                    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1))
                    ret, frame = cap.read()
                    if ret:
                        last_frame_path = shot_path / f"last_frame_{shot_id:03d}.png"
                        cv2.imwrite(str(last_frame_path), frame)
                        db_shot.last_frame_path = str(last_frame_path)
                        # Copy to ComfyUI input for next shot's LoadImage
                        next_name = f"avs_shot_{task_id}_{shot_id+1:03d}.png"
                        shutil.copy2(str(last_frame_path), str(comfy_input_dir / next_name))
                        prev_last_frame = next_name
                    cap.release()
                else:
                    prev_last_frame = None

            # ── Timeout check after video step ────────────
            if _check_timeout(pipeline_start, task_id) is None:
                raise TimeoutError("Pipeline timed out after video generation")

            # ── Step 4: Upscale ───────────────────────────
            await notify(manager, task_id, "upscaling", "超分辨率", 65)
            t.status = TaskStatus.upscaling
            await s.commit()

            # Re-query DB shots so we can persist per-shot results
            result = await s.execute(
                select(Shot).where(Shot.task_id == task_id).order_by(Shot.shot_index)
            )
            db_shots = result.scalars().all()
            # Map shot_index -> AI-assigned shot id for directory lookup
            shot_id_map = {i: shot["id"] for i, shot in enumerate(shots_data)}

            for db_shot in db_shots:
                ai_id = shot_id_map.get(db_shot.shot_index, db_shot.shot_index + 1)
                shot_dir = output_dir / "shots" / f"{ai_id:03d}"

                # Determine if this shot needs upscaling (Wan 640x640 shots)
                engine = shot_engines.get(ai_id, "")
                if engine != "wan":
                    logger.info(
                        f"Shot {db_shot.shot_index} (engine={engine or 'unknown'}): "
                        f"no upscale needed (not Wan-generated)"
                    )
                    continue

                # Find the video file
                if not db_shot.video_path:
                    logger.warning(f"Shot {db_shot.shot_index}: no video_path, skipping upscale")
                    continue
                video_file = Path(db_shot.video_path)
                if not video_file.exists():
                    logger.warning(f"Shot {db_shot.shot_index}: video file missing: {video_file}")
                    continue

                # Verify resolution via cv2 before upscaling
                cap = cv2.VideoCapture(str(video_file))
                vw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                vh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cap.release()
                logger.info(f"Shot {db_shot.shot_index} current resolution: {vw}x{vh}")

                if vw > 640 or vh > 640:
                    logger.info(f"Shot {db_shot.shot_index}: already > 640px, skip upscale")
                    continue

                # Copy video to ComfyUI input directory so VHS_LoadVideo can find it
                import tempfile
                comfy_input = Path("F:/ComfyUI/input")
                upload_name = f"avs_upscale_{task_id}_{db_shot.shot_index:03d}.mp4"
                upload_dst = comfy_input / upload_name
                shutil.copy2(str(video_file), str(upload_dst))
                logger.info(f"Uploaded video for upscale: {upload_dst}")

                try:
                    workflow = comfyui.build_upscale_workflow(
                        video_path=upload_name,
                        scale_factor=GEN.get("upscale_factor", 4),
                        frame_rate=config["fps"] if isinstance(config.get("fps"), int) else 24,
                    )
                    up_result = await comfyui.run_workflow(workflow)

                    # VHS_VideoCombine writes to ComfyUI output dir;
                    # look for files with our prefix
                    comfy_output = Path("F:/ComfyUI/output")
                    found = list(comfy_output.glob("avs_upscale*.mp4"))
                    if found:
                        # Pick the most recent match
                        found.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                        upscaled_src = found[0]
                        upscaled_dst = shot_dir / f"video_{ai_id:03d}_upscaled.mp4"
                        upscaled_dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(str(upscaled_src), str(upscaled_dst))
                        # Update shot to point to upscaled video
                        db_shot.video_path = str(upscaled_dst)
                        logger.info(f"Shot {db_shot.shot_index} upscaled: {upscaled_dst}")
                    else:
                        # Fallback: check outputs dict
                        for node_id, outputs in up_result.get("outputs", {}).items():
                            for out in outputs:
                                fname = out.get("filename", "") or out.get("image", "")
                                if fname:
                                    src = comfy_output / fname
                                    if src.exists():
                                        upscaled_dst = shot_dir / f"video_{ai_id:03d}_upscaled.mp4"
                                        shutil.copy2(str(src), str(upscaled_dst))
                                        db_shot.video_path = str(upscaled_dst)
                                        logger.info(
                                            f"Shot {db_shot.shot_index} upscaled (outputs dict): {upscaled_dst}"
                                        )
                                        break

                    db_shot.status = "upscaled"
                except Exception as exc:
                    logger.error(f"Upscale failed for shot {db_shot.shot_index}: {exc}")
                    db_shot.status = "upscale_failed"
                    # Keep the original 640x640 video — composite will use it as-is

                await s.commit()
                progress = 65 + (db_shot.shot_index / max(len(db_shots), 1)) * 5
                await notify(
                    manager, task_id, "upscaling",
                    f"超分辨率 ({db_shot.shot_index + 1}/{len(db_shots)})",
                    progress,
                )

            # ── Step 5: TTS ───────────────────────────────
            await notify(manager, task_id, "generating_audio", "配音生成", 70)
            t.status = TaskStatus.generating_audio
            await s.commit()

            tts_count = 0
            for db_shot in db_shots:
                dialogue = (db_shot.dialogue or "").strip()
                if dialogue:
                    logger.info(
                        f"TTS for shot {db_shot.shot_index}: {len(dialogue)} chars"
                    )
                    try:
                        audio_path = await tts.generate_shot_audio(
                            task_output_dir=output_dir,
                            shot_id=db_shot.shot_index + 1,
                            dialogue=dialogue,
                        )
                        db_shot.audio_path = str(audio_path)
                        db_shot.status = "audio_done"
                        tts_count += 1
                        logger.info(f"TTS saved: {audio_path}")
                    except Exception as exc:
                        logger.error(f"TTS failed for shot {db_shot.shot_index}: {exc}")
                        db_shot.status = "audio_failed"
                        # Write silent placeholder so composite doesn't fail
                        silent = output_dir / "shots" / f"{db_shot.shot_index + 1:03d}" / "audio.wav"
                        silent.parent.mkdir(parents=True, exist_ok=True)
                        try:
                            silent.write_bytes(b"\x00" * 8000)
                            db_shot.audio_path = str(silent)
                        except Exception:
                            pass
                else:
                    logger.info(f"Shot {db_shot.shot_index}: no dialogue, silent placeholder")
                    silent = output_dir / "shots" / f"{db_shot.shot_index + 1:03d}" / "audio.wav"
                    silent.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        silent.write_bytes(b"\x00" * 8000)
                    except Exception:
                        pass
                    db_shot.audio_path = str(silent)
                    db_shot.status = "audio_done"

                await s.commit()
                progress = 70 + (db_shot.shot_index / max(len(db_shots), 1)) * 10
                await notify(
                    manager, task_id, "generating_audio",
                    f"配音生成 ({db_shot.shot_index + 1}/{len(db_shots)})",
                    progress,
                )

            logger.info(f"TTS complete: {tts_count} shots with dialogue synthesized")

            # ── Step 6: Composite ─────────────────────────
            await notify(manager, task_id, "compositing", "后期合成", 80)
            t.status = TaskStatus.compositing
            await s.commit()

            shot_videos: list[Path] = []
            shot_audios: list[Path] = []
            subtitles: list[dict] = []
            time_cursor = 0.0

            for db_shot in db_shots:
                dur = float(db_shot.duration_sec or 3.0)

                # Collect video
                vp = db_shot.video_path
                if vp:
                    vpath = Path(vp)
                    if vpath.exists():
                        shot_videos.append(vpath)
                    else:
                        logger.warning(f"Shot {db_shot.shot_index}: video missing: {vpath}")
                else:
                    logger.warning(f"Shot {db_shot.shot_index}: no video_path")

                # Collect audio
                ap = db_shot.audio_path
                if ap:
                    apath = Path(ap)
                    if apath.exists():
                        shot_audios.append(apath)
                    else:
                        logger.warning(f"Shot {db_shot.shot_index}: audio missing: {apath}")
                else:
                    logger.warning(f"Shot {db_shot.shot_index}: no audio_path")

                # Build subtitle entry
                dialogue = (db_shot.dialogue or "").strip()
                if dialogue:
                    subtitles.append({
                        "text": dialogue,
                        "start_sec": time_cursor,
                        "end_sec": time_cursor + dur,
                    })

                time_cursor += dur

            if not shot_videos:
                raise RuntimeError("No valid shot videos available for compositing")

            final_dir = output_dir / "final"
            final_dir.mkdir(parents=True, exist_ok=True)
            final_path = final_dir / "output.mp4"

            recipe_data = json.loads(t.recipe_json) if t.recipe_json else {}

            from services.mlt_pipeline import composite_mlt

            logger.info(
                f"Compositing {len(shot_videos)} shots, {len(subtitles)} subtitle entries"
            )
            await composite_mlt(
                output_path=final_path,
                shot_videos=shot_videos,
                shot_audios=shot_audios,
                subtitles=subtitles,
                recipe=recipe_data,
                width=recipe_data.get("resolution", {}).get("width", 1920),
                height=recipe_data.get("resolution", {}).get("height", 1080),
                fps=recipe_data.get("fps", 24),
            )

            logger.info(f"Composite output: {final_path}")
            t.output_dir = str(output_dir)  # ensure output_dir is current

            # ── Step 7: Package ───────────────────────────
            await notify(manager, task_id, "packaging", "资产打包", 95)
            t.status = TaskStatus.packaging
            await s.commit()

            # Build a self-contained archive: shots/ + storyboard.json + recipe.json
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                tmppath = Path(tmpdir)

                # Copy shots directory
                shots_src = output_dir / "shots"
                if shots_src.exists():
                    shutil.copytree(shots_src, tmppath / "shots")
                    logger.info(f"Packaged shots dir: {shots_src}")

                # Copy storyboard JSON
                storyboard_src = output_dir / "storyboard.json"
                if storyboard_src.exists():
                    shutil.copy2(storyboard_src, tmppath / "storyboard.json")
                    logger.info(f"Packaged storyboard: {storyboard_src}")

                # Write recipe JSON
                if t.recipe_json:
                    recipe_dst = tmppath / "recipe.json"
                    recipe_dst.write_text(t.recipe_json, encoding="utf-8")
                    logger.info(f"Packaged recipe JSON ({len(t.recipe_json)} bytes)")

                # Write a manifest with task metadata
                manifest = {
                    "task_id": task_id,
                    "template_id": template_id,
                    "shot_count": len(shots_data),
                    "pipeline_version": "1.0",
                }
                manifest_dst = tmppath / "manifest.json"
                manifest_dst.write_text(
                    json.dumps(manifest, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

                # Create archive
                zip_base = output_dir / "assets"
                zip_path = Path(shutil.make_archive(
                    str(zip_base), "zip", tmppath
                ))
                logger.info(f"Assets packaged: {zip_path} ({zip_path.stat().st_size:,} bytes)")

            await s.commit()

            # ── Done ──────────────────────────────────────
            t.status = TaskStatus.completed
            t.progress = 100
            await s.commit()

            await notify(manager, task_id, "completed", "完成", 100,
                         output_dir=str(output_dir),
                         recipe=recipe)

        except TimeoutError as exc:
            elapsed_min = (time.time() - pipeline_start) / 60
            msg = f"Pipeline timed out after {elapsed_min:.0f} minutes (limit: {PIPELINE_TIMEOUT_SEC // 60} min)"
            logger.error(msg)
            t.status = TaskStatus.failed
            t.error_message = msg
            t.progress = 0
            await s.commit()
            await notify(manager, task_id, "failed", "超时", 0, error=msg)

        except Exception as exc:
            logger.exception(f"Pipeline failed for task {task_id}")
            t.status = TaskStatus.failed
            t.error_message = str(exc)
            t.progress = 0
            await s.commit()
            await notify(manager, task_id, "failed", "失败", 0, error=str(exc))
