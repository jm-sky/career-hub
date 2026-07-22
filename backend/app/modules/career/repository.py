"""Repository for career module database operations (Phase 1: profiles)."""

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import (
    AchievementDB,
    CertificationDB,
    CvVersionDB,
    EducationDB,
    ExperienceDB,
    LanguageDB,
    ProfileDB,
    ProjectDB,
    SkillDB,
)


class ProfileRepository:
    """Repository for profile database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: str) -> ProfileDB | None:
        result = await self.db.execute(select(ProfileDB).where(ProfileDB.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> ProfileDB | None:
        result = await self.db.execute(select(ProfileDB).where(ProfileDB.slug == slug))
        return result.scalar_one_or_none()

    async def slug_exists(self, slug: str) -> bool:
        result = await self.db.execute(select(ProfileDB.id).where(ProfileDB.slug == slug))
        return result.scalar_one_or_none() is not None

    async def create(self, profile: ProfileDB) -> ProfileDB:
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def save(self, profile: ProfileDB) -> ProfileDB:
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def count_sections(self, profile_id: str) -> dict[str, int]:
        """Per-section item counts for one profile, in a single round-trip."""
        section_models: dict[str, Any] = {
            "experiences": ExperienceDB,
            "projects": ProjectDB,
            "skills": SkillDB,
            "education": EducationDB,
            "certifications": CertificationDB,
            "achievements": AchievementDB,
            "languages": LanguageDB,
            "cvVersions": CvVersionDB,
        }
        subqueries = {name: (select(func.count()).select_from(model).where(model.profile_id == profile_id).scalar_subquery().label(name)) for name, model in section_models.items()}
        result = await self.db.execute(select(*subqueries.values()))
        row = result.one()
        return {name: int(value) for name, value in zip(section_models, row, strict=False)}
