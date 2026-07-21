"""Education endpoints for the career module (Phase 4)."""

from fastapi import APIRouter, Depends, HTTPException, status

from .dependencies import CurrentProfile, get_education_service
from .education_service import EducationService
from .schemas import (
    CreateEducationRequest,
    EducationResponse,
    ReorderRequest,
    UpdateEducationRequest,
)

router = APIRouter(prefix="/career", tags=["Career", "Education"])


@router.get("/education", response_model=list[EducationResponse])
async def list_education(
    *,
    profile: CurrentProfile,
    service: EducationService = Depends(get_education_service),
) -> list[EducationResponse]:
    """List the authenticated user's education entries, ordered by display_order."""
    return await service.list_for_profile(profile.id)


@router.post("/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def create_education(
    *,
    payload: CreateEducationRequest,
    profile: CurrentProfile,
    service: EducationService = Depends(get_education_service),
) -> EducationResponse:
    """Create an education entry, appended to the end of the display order."""
    try:
        return await service.create(profile.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/education/reorder", response_model=list[EducationResponse])
async def reorder_education(
    *,
    payload: ReorderRequest,
    profile: CurrentProfile,
    service: EducationService = Depends(get_education_service),
) -> list[EducationResponse]:
    """Batch-reorder all of the authenticated user's education entries."""
    try:
        return await service.reorder(profile.id, payload.orderedIds)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/education/{id}", response_model=EducationResponse)
async def update_education(
    *,
    id: str,
    payload: UpdateEducationRequest,
    profile: CurrentProfile,
    service: EducationService = Depends(get_education_service),
) -> EducationResponse:
    """Partially update an education entry owned by the authenticated user."""
    education = await service.get_entity_for_profile(id, profile.id)
    if education is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education entry not found")
    try:
        return await service.update(education, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/education/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    *,
    id: str,
    profile: CurrentProfile,
    service: EducationService = Depends(get_education_service),
) -> None:
    """Delete an education entry owned by the authenticated user."""
    education = await service.get_entity_for_profile(id, profile.id)
    if education is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education entry not found")
    await service.delete(education)
