"""AI Video Studio — FastAPI backend entry point."""

import asyncio
import json
import logging
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import config
from models.task import Base
from services import prompt_learner, workflow_fetcher

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
    global _prompt_learner_task, _workflow_fetcher_task
    await init_db()
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "uploads").mkdir(parents=True, exist_ok=True)
    logger.info(f"AI Video Studio started. Output dir: {output_dir}")

    # Start background services
    _prompt_learner_task = prompt_learner.start(Session)
    _workflow_fetcher_task = workflow_fetcher.start(Session)
    logger.info("Background services started: prompt_learner, workflow_fetcher")


@app.on_event("shutdown")
async def shutdown():
    prompt_learner.stop()
    workflow_fetcher.stop()
    logger.info("Background services stopped")


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

# Background service task handles
_prompt_learner_task = None
_workflow_fetcher_task = None


# ── Routes ──────────────────────────────────────────────

@app.get("/api/health")
async def health():
    from services.comfyui_client import comfyui
    comfy_ok = await comfyui.health_check()
    return {
        "status": "ok",
        "comfyui": "connected" if comfy_ok else "disconnected",
    }


@app.get("/api/health/detailed")
async def health_detailed():
    """Full environment health check covering all pipeline dependencies."""
    from services.health_check import run_health_check
    return await run_health_check()


# ── File Upload ──────────────────────────────────────────

ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".json", ".yaml", ".yml", ".csv", ".xml", ".html",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg",
    ".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac",
}

TEXT_EXTS = {".txt", ".md", ".json", ".yaml", ".yml", ".csv", ".xml", ".html"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"}


def _file_type(ext: str) -> str:
    if ext in TEXT_EXTS:
        return "text"
    if ext in IMAGE_EXTS:
        return "image"
    if ext in AUDIO_EXTS:
        return "audio"
    return "unknown"


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return {"error": f"File type '{ext}' not allowed."}

    uploads_dir = Path(config["output_dir"]) / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Avoid collisions by prefixing with a short uuid
    safe_name = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    dest = uploads_dir / safe_name

    contents = await file.read()
    dest.write_bytes(contents)

    return {
        "filename": file.filename,
        "path": str(dest),
        "type": _file_type(ext),
        "size": len(contents),
    }


# ── Tasks ───────────────────────────────────────────────

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
        "recipe": t.recipe_json,
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
    template_id = data.get("template", "micro_drama")

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

    # Kick off full pipeline in background
    asyncio.create_task(
        run_pipeline(task_id, template_id=template_id)
    )
    return {"task_id": task_id, "status": "pending", "template": template_id}


@app.websocket("/ws/tasks/{task_id}")
async def ws_task(ws: WebSocket, task_id: str):
    await manager.connect(ws, task_id)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(task_id)


# ── Templates ──────────────────────────────────────────

@app.get("/api/templates")
async def list_templates():
    from services.templates import list_templates as lt
    return lt()


@app.get("/api/templates/{template_id}")
async def get_template(template_id: str):
    from services.templates import get_template as gt
    t = gt(template_id)
    if not t:
        return {"error": "not found"}
    return t


# ── BGM Library ───────────────────────────────────────

@app.get("/api/bgm")
async def bgm_search(mood: str = "", genre: str = "", bpm_min: int = 0, bpm_max: int = 300):
    from services.bgm_library import search_bgm
    return search_bgm(
        mood=mood if mood else None,
        genre=genre if genre else None,
        bpm_min=bpm_min if bpm_min > 0 else None,
        bpm_max=bpm_max if bpm_max < 300 else None,
    )

@app.get("/api/bgm/recommend")
async def bgm_recommend(template: str = "micro_drama"):
    from services.bgm_library import recommend_for_template
    return recommend_for_template(template)

@app.get("/api/bgm/reference")
async def bgm_reference(mood: str = "", genre: str = "", use_case: str = "", pd_only: bool = False):
    from services.bgm_library import search_reference
    return search_reference(
        mood=mood if mood else None,
        genre=genre if genre else None,
        use_case=use_case if use_case else None,
        public_domain_only=pd_only,
    )

@app.get("/api/luts")
async def list_luts():
    from services.bgm_library import LUT_CATALOG
    return LUT_CATALOG

@app.post("/api/audio/analyze")
async def analyze_audio(file: UploadFile):
    """Analyze an uploaded audio file: BPM, key, energy, beat positions."""
    import tempfile
    from services.audio_analyzer import analyze
    suffix = Path(file.filename).suffix if file.filename else ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        result = analyze(tmp_path)
        return result
    finally:
        Path(tmp_path).unlink(missing_ok=True)


# ── Text Creation ──────────────────────────────────────

@app.post("/api/text/continue")
async def text_continue(data: dict):
    from services.deepseek_client import continue_text
    text = data.get("text", "")
    length = data.get("length", "3个段落")
    key = data.get("api_key", "")
    result = await continue_text(text, length, api_key=key or config["deepseek_api_key"])
    return {"text": result}


@app.post("/api/text/expand")
async def text_expand(data: dict):
    from services.deepseek_client import expand_one_liner
    sentence = data.get("sentence", "")
    word_count = data.get("word_count", 2000)
    key = data.get("api_key", "")
    result = await expand_one_liner(sentence, word_count, api_key=key or config["deepseek_api_key"])
    return {"text": result}


@app.post("/api/text/structured")
async def text_structured(data: dict):
    from services.deepseek_client import structured_create
    key = data.get("api_key", "")
    result = await structured_create(
        characters=data.get("characters", ""),
        persona=data.get("persona", ""),
        world=data.get("world", ""),
        style=data.get("style", ""),
        plot=data.get("plot", ""),
        word_count=data.get("word_count", 3000),
        api_key=key or config["deepseek_api_key"],
    )
    return {"text": result}


@app.post("/api/text/revise")
async def text_revise(data: dict):
    from services.deepseek_client import revise_text
    original = data.get("text", "")
    instruction = data.get("instruction", "")
    key = data.get("api_key", "")
    result = await revise_text(original, instruction, api_key=key or config["deepseek_api_key"])
    return {"text": result}


# ── Pipeline runner (wired to real services) ───────────

async def run_pipeline(task_id: str, template_id: str = "micro_drama"):
    from services.pipeline import run_full_pipeline
    try:
        await run_full_pipeline(
            task_id=task_id,
            session_factory=Session,
            manager=manager,
            template_id=template_id,
        )
    except Exception as exc:
        logger.exception(f"Pipeline {task_id} crashed")
        async with Session() as s:
            from models.task import Task, TaskStatus
            t = await s.get(Task, task_id)
            if t:
                t.status = TaskStatus.failed
                t.error_message = str(exc)
                await s.commit()
        await manager.send(task_id, {"type": "failed", "error": str(exc)})


# ── Entry point ─────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
