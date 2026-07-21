"""Achievement endpoints for the career module (Phase 4)."""

from fastapi import APIRouter, Depends, HTTPException, status

from .achievement_service import AchievementService
from .dependencies import CurrentProfile, get_achievement_service
from .schemas import (
    AchievementResponse,
    CreateAchievementRequest,
    ReorderRequest,
    UpdateAchievementRequest,
)

router = APIRouter(prefix="/career", tags=["Career", "Achievements"])


@router.get("/achievements", response_model=list[AchievementResponse])
async def list_achievements(
    *,
    profile: CurrentProfile,
    service: AchievementService = Depends(get_achievement_service),
) -> list[AchievementResponse]:
    """List the authenticated user's achievements, ordered by display_order."""
    return await service.list_for_profile(profile.id)


@router.post("/achievements", response_model=AchievementResponse, status_code=status.HTTP_201_CREATED)
async def create_achievement(
    *,
    payload: CreateAchievementRequest,
    profile: CurrentProfile,
    service: AchievementService = Depends(get_achievement_service),
) -> AchievementResponse:
    """Create an achievement, appended to the end of the display order."""
    return await service.create(profile.id, payload)


@router.put("/achievements/reorder", response_model=list[AchievementResponse])
async def reorder_achievements(
    *,
    payload: ReorderRequest,
    profile: CurrentProfile,
    service: AchievementService = Depends(get_achievement_service),
) -> list[AchievementResponse]:
    """Batch-reorder all of the authenticated user's achievements."""
    try:
        return await service.reorder(profile.id, payload.orderedIds)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/achievements/{id}", response_model=AchievementResponse)
async def update_achievement(
    *,
    id: str,
    payload: UpdateAchievementRequest,
    profile: CurrentProfile,
    service: AchievementService = Depends(get_achievement_service),
) -> AchievementResponse:
    """Partially update an achievement owned by the authenticated user."""
    achievement = await service.get_entity_for_profile(id, profile.id)
    if achievement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")
    return await service.update(achievement, payload)


@router.delete("/achievements/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_achievement(
    *,
    id: str,
    profile: CurrentProfile,
    service: AchievementService = Depends(get_achievement_service),
) -> None:
    """Delete an achievement owned by the authenticated user."""
    achievement = await service.get_entity_for_profile(id, profile.id)
    if achievement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Achievement not found")
    await service.delete(achievement)
