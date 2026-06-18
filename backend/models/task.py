import enum
import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TaskStatus(str, enum.Enum):
    pending = "pending"
    storyboarding = "storyboarding"
    generating_images = "generating_images"
    generating_videos = "generating_videos"
    upscaling = "upscaling"
    generating_audio = "generating_audio"
    compositing = "compositing"
    packaging = "packaging"
    completed = "completed"
    failed = "failed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    type: Mapped[str] = mapped_column(String(20), default="generate")  # "text" or "generate"
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus), default=TaskStatus.pending)
    input_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    storyboard_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    output_dir: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution: Mapped[str] = mapped_column(String(20), default="1080p")
    fps: Mapped[int] = mapped_column(Integer, default=24)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @property
    def storyboard(self) -> Optional[list]:
        import json
        if self.storyboard_json:
            return json.loads(self.storyboard_json)
        return None


class Shot(Base):
    __tablename__ = "shots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[str] = mapped_column(String(36), ForeignKey("tasks.id"))
    shot_index: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dialogue: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mood: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    duration_sec: Mapped[float] = mapped_column(Float, default=3.0)
    keyframe_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    video_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    audio_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    first_frame_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    last_frame_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
