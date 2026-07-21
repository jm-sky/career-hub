"""Work-experience endpoints for the career module (Phase 2)."""

from fastapi import APIRouter, Depends, HTTPException, status

from .dependencies import CurrentProfile, get_experience_service
from .experience_service import ExperienceService
from .schemas import (
    CreateExperienceRequest,
    ExperienceResponse,
    ReorderRequest,
    UpdateExperienceRequest,
)

router = APIRouter(prefix="/career", tags=["Career", "Experiences"])


@router.get("/experiences", response_model=list[ExperienceResponse])
async def list_experiences(
    *,
    profile: CurrentProfile,
    service: ExperienceService = Depends(get_experience_service),
) -> list[ExperienceResponse]:
    """List the authenticated user's work experiences, ordered by display_order."""
    return await service.list_for_profile(profile.id)


@router.post("/experiences", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def create_experience(
    *,
    payload: CreateExperienceRequest,
    profile: CurrentProfile,
    service: ExperienceService = Depends(get_experience_service),
) -> ExperienceResponse:
    """Create a work-experience entry, appended to the end of the display order."""
    try:
        return await service.create(profile.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/experiences/reorder", response_model=list[ExperienceResponse])
async def reorder_experiences(
    *,
    payload: ReorderRequest,
    profile: CurrentProfile,
    service: ExperienceService = Depends(get_experience_service),
) -> list[ExperienceResponse]:
    """Batch-reorder all of the authenticated user's experiences.

    ``orderedIds`` must be exactly the full set of the profile's existing
    experience ids — partial reorders are rejected rather than silently dropped.
    """
    try:
        return await service.reorder(profile.id, payload.orderedIds)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/experiences/{id}", response_model=ExperienceResponse)
async def update_experience(
    *,
    id: str,
    payload: UpdateExperienceRequest,
    profile: CurrentProfile,
    service: ExperienceService = Depends(get_experience_service),
) -> ExperienceResponse:
    """Partially update a work-experience entry owned by the authenticated user."""
    experience = await service.get_entity_for_profile(id, profile.id)
    if experience is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    try:
        return await service.update(experience, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/experiences/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    *,
    id: str,
    profile: CurrentProfile,
    service: ExperienceService = Depends(get_experience_service),
) -> None:
    """Delete a work-experience entry owned by the authenticated user."""
    experience = await service.get_entity_for_profile(id, profile.id)
    if experience is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    await service.delete(experience)
