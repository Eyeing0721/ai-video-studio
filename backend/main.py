"""AI Video Studio — FastAPI backend entry point."""

import asyncio
import json
import logging
import uuid
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import config
from models.task import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("avs")

# ── Database ────────────────────────────────────────────

DB_PATH = Path(config.get("db_path", str(Path.home() / ".ai-video-studio" / "data.db")))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=False)
Session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ── App ─────────────────────────────────────────────────

app = FastAPI(title="AI Video Studio", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"AI Video Studio started. Output dir: {output_dir}")


# ── WebSocket connections ───────────────────────────────

class ConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, ws: WebSocket, task_id: str):
        await ws.accept()
        self.active[task_id] = ws

    def disconnect(self, task_id: str):
        self.active.pop(task_id, None)

    async def send(self, task_id: str, data: dict):
        ws = self.active.get(task_id)
        if ws:
            await ws.send_json(data)


manager = ConnectionManager()


# ── Routes ──────────────────────────────────────────────

@app.get("/api/health")
async def health():
    from services.comfyui_client import comfyui
    comfy_ok = await comfyui.health_check()
    return {
        "status": "ok",
        "comfyui": "connected" if comfy_ok else "disconnected",
    }


@app.get("/api/tasks")
async def list_tasks():
    async with Session() as s:
        from sqlalchemy import select
        from models.task import Task
        result = await s.execute(select(Task).order_by(Task.created_at.desc()).limit(50))
        tasks = result.scalars().all()
    return [
        {
            "id": t.id, "type": t.type, "status": t.status.value,
            "progress": t.progress, "created_at": t.created_at.isoformat(),
            "error_message": t.error_message,
        }
        for t in tasks
    ]


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    async with Session() as s:
        from sqlalchemy import select
        from models.task import Task, Shot
        t = await s.get(Task, task_id)
        if not t:
            return {"error": "not found"}
        shots_result = await s.execute(
            select(Shot).where(Shot.task_id == task_id).order_by(Shot.shot_index)
        )
        shots = shots_result.scalars().all()
    return {
        "id": t.id, "type": t.type, "status": t.status.value,
        "progress": t.progress, "created_at": t.created_at.isoformat(),
        "error_message": t.error_message,
        "resolution": t.resolution, "fps": t.fps,
        "storyboard": t.storyboard,
        "shots": [
            {
                "id": s.id, "shot_index": s.shot_index,
                "description": s.description, "dialogue": s.dialogue,
                "mood": s.mood, "duration_sec": s.duration_sec,
                "status": s.status,
            }
            for s in shots
        ],
    }


@app.post("/api/tasks")
async def create_task(data: dict):
    task_id = str(uuid.uuid4())
    task_type = data.get("type", "generate")
    async with Session() as s:
        from models.task import Task
        t = Task(
            id=task_id, type=task_type, status="pending",
            input_text=data.get("text", ""),
            resolution=data.get("resolution", "1080p"),
            fps=data.get("fps", 24),
            output_dir=str(Path(config["output_dir"]) / task_id),
        )
        s.add(t)
        await s.commit()

    # Kick off pipeline in background
    asyncio.create_task(run_pipeline(task_id))
    return {"task_id": task_id, "status": "pending"}


@app.websocket("/ws/tasks/{task_id}")
async def ws_task(ws: WebSocket, task_id: str):
    await manager.connect(ws, task_id)
    try:
        while True:
            await ws.receive_text()  # keep alive, client can ping
    except WebSocketDisconnect:
        manager.disconnect(task_id)


# ── Pipeline runner (stub — to be fleshed out) ──────────

async def run_pipeline(task_id: str):
    """Full pipeline: storyboarding -> images -> videos -> upscale -> TTS -> composite."""
    async with Session() as s:
        from models.task import Task, TaskStatus, Shot
        t = await s.get(Task, task_id)
        if not t:
            return

        steps = [
            ("storyboarding", "分镜拆解"),
            ("generating_images", "静态图生成"),
            ("generating_videos", "图生视频"),
            ("upscaling", "超分辨率"),
            ("generating_audio", "配音生成"),
            ("compositing", "后期合成"),
            ("packaging", "资产打包"),
        ]

        for status_key, label in steps:
            t.status = TaskStatus(status_key)
            t.progress = (steps.index((status_key, label)) / len(steps)) * 100
            await s.commit()
            await manager.send(task_id, {
                "type": "status", "status": status_key, "label": label,
                "progress": t.progress,
            })
            await asyncio.sleep(0.5)  # placeholder — real work goes here

        t.status = TaskStatus.completed
        t.progress = 100
        await s.commit()
        await manager.send(task_id, {"type": "completed", "progress": 100})


# ── Entry point ─────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
