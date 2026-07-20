"""Database models for the career module (Phase 1: profiles only)."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProfileDB(Base):
    """A user's professional profile — 1:1 with users.id.

    Anchor table for the career module: experiences/projects/skills/education/
    certifications/achievements/cv_versions (Phase 2+) all belong to a profile.
    """

    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), unique=True, nullable=False, index=True
    )
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    headline: Mapped[str | None] = mapped_column(String(200), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(120), nullable=True)
    visibility: Mapped[str] = mapped_column(
        String(10), nullable=False, default="PRIVATE"
    )
    # Shape: {email?, phone?, linkedin?, website?}
    contact: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # Wizard-in-progress storage, keyed by step name: {stepName: {...}}
    draft_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    profile_photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    completeness_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
