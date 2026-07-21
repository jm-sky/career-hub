"""Certification endpoints for the career module (Phase 4)."""

from fastapi import APIRouter, Depends, HTTPException, status

from .certification_service import CertificationService
from .dependencies import CurrentProfile, get_certification_service
from .schemas import (
    CertificationResponse,
    CreateCertificationRequest,
    ReorderRequest,
    UpdateCertificationRequest,
)

router = APIRouter(prefix="/career", tags=["Career", "Certifications"])


@router.get("/certifications", response_model=list[CertificationResponse])
async def list_certifications(
    *,
    profile: CurrentProfile,
    service: CertificationService = Depends(get_certification_service),
) -> list[CertificationResponse]:
    """List the authenticated user's certifications, ordered by display_order."""
    return await service.list_for_profile(profile.id)


@router.post("/certifications", response_model=CertificationResponse, status_code=status.HTTP_201_CREATED)
async def create_certification(
    *,
    payload: CreateCertificationRequest,
    profile: CurrentProfile,
    service: CertificationService = Depends(get_certification_service),
) -> CertificationResponse:
    """Create a certification, appended to the end of the display order."""
    try:
        return await service.create(profile.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/certifications/reorder", response_model=list[CertificationResponse])
async def reorder_certifications(
    *,
    payload: ReorderRequest,
    profile: CurrentProfile,
    service: CertificationService = Depends(get_certification_service),
) -> list[CertificationResponse]:
    """Batch-reorder all of the authenticated user's certifications."""
    try:
        return await service.reorder(profile.id, payload.orderedIds)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/certifications/{id}", response_model=CertificationResponse)
async def update_certification(
    *,
    id: str,
    payload: UpdateCertificationRequest,
    profile: CurrentProfile,
    service: CertificationService = Depends(get_certification_service),
) -> CertificationResponse:
    """Partially update a certification owned by the authenticated user."""
    certification = await service.get_entity_for_profile(id, profile.id)
    if certification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")
    try:
        return await service.update(certification, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/certifications/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certification(
    *,
    id: str,
    profile: CurrentProfile,
    service: CertificationService = Depends(get_certification_service),
) -> None:
    """Delete a certification owned by the authenticated user."""
    certification = await service.get_entity_for_profile(id, profile.id)
    if certification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")
    await service.delete(certification)
