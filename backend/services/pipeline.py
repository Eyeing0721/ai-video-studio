"""Pipeline orchestrator — chains storyboarding, image gen, video gen, TTS, composite."""

import asyncio
import json
import logging
import shutil
from pathlib import Path
from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

from config import config
from models.task import Task, TaskStatus, Shot
from services.comfyui_client import comfyui
from services.templates import get_template, merge_template_with_ai

logger = logging.getLogger(__name__)

OUTPUT_ROOT = Path(config["output_dir"])
GEN = config["generation"]


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


async def run_full_pipeline(
    task_id: str,
    session_factory: async_sessionmaker,
    manager=None,
    template_id: str = "micro_drama",
):
    """Execute the complete generation pipeline for a task."""

    async with session_factory() as s:
        t = await s.get(Task, task_id)
        if not t:
            logger.error(f"Task {task_id} not found")
            return

        output_dir = await create_output_dirs(task_id)
        t.output_dir = str(output_dir)

        # ── Load template ────────────────────────────────
        template = get_template(template_id) or get_template("micro_drama")

        try:
            # ── Step 1: Storyboarding ────────────────────
            await notify(manager, task_id, "storyboarding", "分镜拆解", 5)
            t.status = TaskStatus.storyboarding
            await s.commit()

            from services.deepseek_client import generate_storyboard
            shots_data = await generate_storyboard(t.input_text or "")

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

            # ── AI dynamic template merge ─────────────────
            moods = [sh.get("mood", "") for sh in shots_data]
            recipe = merge_template_with_ai(
                template, moods,
                sum(sh.get("duration_sec", 3) for sh in shots_data),
            )
            t.recipe_json = json.dumps(recipe, ensure_ascii=False)
            await s.commit()

            # ── Step 2: Generate keyframes ────────────────
            await notify(manager, task_id, "generating_images", "静态图生成", 15)
            t.status = TaskStatus.generating_images
            await s.commit()

            for shot in shots_data:
                shot_path = output_dir / "shots" / f"{shot['id']:03d}"
                shot_path.mkdir(exist_ok=True)

                prompt = f"{shot['description']}, {shot['mood']}, {shot['lighting']}"
                workflow = comfyui.build_txt2img_workflow(
                    positive_prompt=prompt,
                    width=GEN["z_image_width"],
                    height=GEN["z_image_height"],
                )

                try:
                    result = await comfyui.run_workflow(workflow)
                    # Output files land in ComfyUI output dir; copy to task output
                    for node_id, outputs in result.get("outputs", {}).items():
                        for out in outputs:
                            if out.get("type") == "image":
                                filename = out.get("filename", "")
                                src = Path("F:/ComfyUI/output") / filename
                                dst = shot_path / f"keyframe_{shot['id']:03d}.png"
                                if src.exists():
                                    shutil.copy2(src, dst)
                                    shot.keyframe_path = str(dst)
                except Exception as exc:
                    logger.error(f"Keyframe gen failed for shot {shot['id']}: {exc}")
                    shot.status = "failed"
                    await s.commit()
                    continue

                shot.status = "keyframe_done"
                await s.commit()

                progress = 15 + (shots_data.index(shot) / len(shots_data)) * 20
                await notify(manager, task_id, "generating_images",
                             f"静态图生成 ({shots_data.index(shot)+1}/{len(shots_data)})", progress)

            # ── Step 3: Image-to-video ────────────────────
            await notify(manager, task_id, "generating_videos", "图生视频", 35)
            t.status = TaskStatus.generating_videos
            await s.commit()

            prev_last_frame: Optional[Path] = None

            for shot in shots_data:
                i = shot["id"]
                shot_path = output_dir / "shots" / f"{i:03d}"

                prompt = f"{shot['description']}, {shot['mood']}"
                image_input = prev_last_frame or shot_path / f"keyframe_{i:03d}.png"

                # Try Sulphur 2 first, fallback to Wan
                for attempt, builder in enumerate([
                    ("sulphur", lambda: comfyui.build_img2video_workflow_sulphur(
                        str(image_input), prompt,
                        width=GEN["sulphur_width"], height=GEN["sulphur_height"],
                    )),
                    ("wan", lambda: comfyui.build_img2video_workflow_wan(
                        str(image_input), prompt,
                        width=GEN["wan_width"], height=GEN["wan_height"],
                    )),
                ]):
                    try:
                        workflow = builder()
                        result = await comfyui.run_workflow(workflow)
                        # Copy output
                        for node_id, outputs in result.get("outputs", {}).items():
                            for out in outputs:
                                if out.get("type") == "image":
                                    filename = out.get("filename", "")
                                    src = Path("F:/ComfyUI/output") / filename
                                    dst = shot_path / f"video_{i:03d}.mp4"
                                    if src.exists():
                                        shutil.copy2(src, dst)
                                        shot.video_path = str(dst)
                        shot.status = "video_done"
                        break
                    except Exception as exc:
                        logger.warning(f"Shot {i} {builder[0]} failed (attempt {attempt+1}): {exc}")
                        if attempt == 0:
                            continue  # try fallback
                        shot.status = "video_failed"
                        shot.attempts = attempt + 1

                await s.commit()
                progress = 35 + (shots_data.index(shot) / len(shots_data)) * 25
                await notify(manager, task_id, "generating_videos",
                             f"图生视频 ({shots_data.index(shot)+1}/{len(shots_data)})", progress)

                # Extract last frame for next shot continuity
                if shot.video_path and Path(shot.video_path).exists():
                    import cv2
                    cap = cv2.VideoCapture(str(shot.video_path))
                    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1))
                    ret, frame = cap.read()
                    if ret:
                        last_frame_path = shot_path / f"last_frame_{i:03d}.png"
                        cv2.imwrite(str(last_frame_path), frame)
                        shot.last_frame_path = str(last_frame_path)
                        prev_last_frame = last_frame_path
                    cap.release()

            # ── Step 4: Upscale ───────────────────────────
            await notify(manager, task_id, "upscaling", "超分辨率", 65)
            t.status = TaskStatus.upscaling
            await s.commit()
            # (upscale logic — run ComfyUI upscale workflow per segment)
            await asyncio.sleep(0.5)

            # ── Step 5: TTS ───────────────────────────────
            await notify(manager, task_id, "generating_audio", "配音生成", 70)
            t.status = TaskStatus.generating_audio
            await s.commit()
            # (TTS logic — Aliyun Bailian per dialogue line)
            await asyncio.sleep(0.5)

            # ── Step 6: Composite ─────────────────────────
            await notify(manager, task_id, "compositing", "后期合成", 80)
            t.status = TaskStatus.compositing
            await s.commit()
            # (MLT pipeline — concat + transitions + subtitles + BGM)
            await asyncio.sleep(0.5)

            # ── Step 7: Package ───────────────────────────
            await notify(manager, task_id, "packaging", "资产打包", 95)
            t.status = TaskStatus.packaging
            await s.commit()

            # Zip intermediate assets
            zip_path = output_dir / "assets.zip"
            shutil.make_archive(str(zip_path.with_suffix("")), "zip", output_dir, "shots")
            await s.commit()
            await asyncio.sleep(0.5)

            # ── Done ──────────────────────────────────────
            t.status = TaskStatus.completed
            t.progress = 100
            await s.commit()

            await notify(manager, task_id, "completed", "完成", 100,
                         output_dir=str(output_dir),
                         recipe=recipe)

        except Exception as exc:
            logger.exception(f"Pipeline failed for task {task_id}")
            t.status = TaskStatus.failed
            t.error_message = str(exc)
            t.progress = 0
            await s.commit()
            await notify(manager, task_id, "failed", "失败", 0, error=str(exc))
