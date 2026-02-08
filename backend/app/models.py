from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, Text, Boolean, Integer, Float, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Generation(Base):
    """SQLAlchemy model for music generations."""

    __tablename__ = "generations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    task_type: Mapped[str] = mapped_column(String(50), default="text2music")
    mode: Mapped[str] = mapped_column(String(50), default="simple")
    model_variant: Mapped[str] = mapped_column(String(50), default="turbo")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Input fields
    prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    lyrics: Mapped[str | None] = mapped_column(Text, nullable=True)
    instrumental: Mapped[bool] = mapped_column(Boolean, default=False)
    cover_strength: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_audio_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    reference_audio_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    source_audio_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    reference_audio_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Musical parameters
    bpm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    key: Mapped[str | None] = mapped_column(String(20), nullable=True)
    time_signature: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Output
    output_audio_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Cover/theme
    cover_color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cover_icon: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cover_image_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Metadata
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
