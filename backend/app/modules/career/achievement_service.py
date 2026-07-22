"""Business logic for achievements (career module, Phase 4)."""

from typing import cast

from app.common.id_utils import generate_id

from .achievement_repository import AchievementRepository
from .db_models import AchievementDB
from .schemas import (
    AchievementCategory,
    AchievementResponse,
    CreateAchievementRequest,
    UpdateAchievementRequest,
)


def _build_response(achievement: AchievementDB) -> AchievementResponse:
    return AchievementResponse(
        id=achievement.id,
        profile_id=achievement.profile_id,
        title=achievement.title,
        description=achievement.description,
        date=achievement.date,
        category=cast(AchievementCategory | None, achievement.category),
        url=achievement.url,
        display_order=achievement.display_order,
        created_at=achievement.created_at,
        updated_at=achievement.updated_at,
    )


class AchievementService:
    """Business logic for achievement CRUD and reordering."""

    def __init__(self, repository: AchievementRepository):
        self.repository = repository

    async def list_for_profile(self, profile_id: str) -> list[AchievementResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        return [_build_response(entry) for entry in entries]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> AchievementDB | None:
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def create(self, profile_id: str, payload: CreateAchievementRequest) -> AchievementResponse:
        display_order = await self.repository.get_next_display_order(profile_id)
        achievement = AchievementDB(
            id=generate_id(),
            profile_id=profile_id,
            title=payload.title,
            description=payload.description,
            date=payload.date,
            category=payload.category,
            url=payload.url,
            display_order=display_order,
        )
        achievement = await self.repository.create(achievement)
        return _build_response(achievement)

    async def update(self, achievement: AchievementDB, payload: UpdateAchievementRequest) -> AchievementResponse:
        if payload.title is not None:
            achievement.title = payload.title
        if payload.description is not None:
            achievement.description = payload.description
        if payload.date is not None:
            achievement.date = payload.date
        if payload.category is not None:
            achievement.category = payload.category
        if payload.url is not None:
            achievement.url = payload.url

        achievement = await self.repository.save(achievement)
        return _build_response(achievement)

    async def delete(self, achievement: AchievementDB) -> None:
        await self.repository.delete(achievement)

    async def reorder(self, profile_id: str, ordered_ids: list[str]) -> list[AchievementResponse]:
        entries = await self.repository.list_by_profile(profile_id)
        if {e.id for e in entries} != set(ordered_ids) or len(ordered_ids) != len(entries):
            raise ValueError("orderedIds must contain exactly the profile's existing achievement ids.")

        await self.repository.reorder(entries, ordered_ids)
        return await self.list_for_profile(profile_id)
