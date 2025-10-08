"""Profile model for user professional profiles."""

from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ulid import ULID

from app.core.database import Base

if TYPE_CHECKING:
    pass


class Profile(Base):
    """Profile model for user professional information."""

    __tablename__ = "profiles"

    # Primary fields
    id = Column(String(26), primary_key=True, default=lambda: str(ULID()))
    user_id = Column(String(26), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Public profile fields
    slug = Column(String(100), unique=True, nullable=True, index=True)  # for public URL
    headline = Column(String(200), nullable=True)
    summary = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)

    # Privacy and visibility
    visibility = Column(String(20), default="PRIVATE", nullable=False)  # PRIVATE, FRIENDS, PUBLIC

    # Contact information (JSONB for flexibility)
    # Example: {"email": "user@example.com", "phone": "+1234567890",
    # "linkedin": "linkedin.com/in/user", "website": "user.com"}
    contact = Column(JSONB, default={}, nullable=False, server_default="{}")

    # Draft data for wizard progress
    draft_data = Column(JSONB, nullable=True)

    # Profile photo
    profile_photo_url = Column(Text, nullable=True)

    # Completeness score (0-100)
    completeness_score = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")
    # TODO: Add relationships when models are implemented:
    # skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    # education = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    # certifications = relationship("Certification", back_populates="profile", cascade="all, delete-orphan")
    # achievements = relationship("Achievement", back_populates="profile", cascade="all, delete-orphan")
    # cv_versions = relationship("CVVersion", back_populates="profile", cascade="all, delete-orphan")

    def generate_slug(self) -> str:
        """Generate URL-friendly slug from user name."""
        if not self.user or not self.user.name:
            return str(self.id).lower()

        # Create slug from name
        import re

        slug = re.sub(r"[^a-zA-Z0-9\s-]", "", self.user.name.lower())
        slug = re.sub(r"\s+", "-", slug.strip())

        # Add random suffix to ensure uniqueness
        import secrets

        suffix = secrets.token_hex(3)
        return f"{slug}-{suffix}"

    def calculate_completeness(self) -> int:
        """Calculate profile completeness score (0-100)."""
        score = 0

        # Basic info (30%)
        if self.headline and self.headline.strip():
            score += 10
        if self.summary and len(self.summary.strip()) > 100:
            score += 20

        # Experiences (30%)
        experience_count = len(self.experiences) if self.experiences else 0
        score += min(experience_count * 10, 30)

        # TODO: Add when models are implemented
        # Projects (15%)
        # project_count = len(self.projects) if self.projects else 0
        # score += min(project_count * 5, 15)

        # Skills (15%)
        # skill_count = len(self.skills) if self.skills else 0
        # score += min(skill_count * 3, 15)

        # Education (10%)
        # education_count = len(self.education) if self.education else 0
        # score += min(education_count * 10, 10)

        # For now, max score is 60% (basic info + experiences)
        return min(score, 100)

    def update_completeness(self) -> None:
        """Update completeness score."""
        self.completeness_score = self.calculate_completeness()  # type: ignore[assignment]

    def is_public(self) -> bool:
        """Check if profile is publicly visible."""
        return self.visibility == "PUBLIC"  # type: ignore[return-value]

    def can_view(self, viewer_user_id: Optional[str] = None) -> bool:
        """Check if profile can be viewed by given user."""
        if self.visibility == "PUBLIC":
            return True
        if self.visibility == "PRIVATE":
            return viewer_user_id == self.user_id
        # FRIENDS visibility would require friendship model
        return viewer_user_id == self.user_id

    def to_dict(self, include_private: bool = False) -> Dict[str, Any]:
        """
        Convert to camelCase dict for API responses.

        Args:
            include_private: Whether to include private fields like draft_data
        """
        result = {
            "id": self.id,
            "userId": self.user_id,
            "slug": self.slug,
            "headline": self.headline,
            "summary": self.summary,
            "location": self.location,
            "visibility": self.visibility,
            "contact": self.contact,
            "profilePhotoUrl": self.profile_photo_url,
            "completenessScore": self.completeness_score,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

        if include_private:
            result["draftData"] = self.draft_data

        return result

    def to_public_dict(self) -> Dict[str, Any]:
        """Convert to public-safe dict (no private information)."""
        return {
            "id": self.id,
            "slug": self.slug,
            "headline": self.headline,
            "summary": self.summary,
            "location": self.location,
            "profilePhotoUrl": self.profile_photo_url,
            "createdAt": self.created_at,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Profile(id={self.id}, user_id={self.user_id}, slug={self.slug})>"
