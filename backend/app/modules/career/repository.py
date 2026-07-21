"""Repository for career module database operations (Phase 1: profiles)."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import ProfileDB


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
