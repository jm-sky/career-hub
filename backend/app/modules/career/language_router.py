"""Language endpoints for the career module."""

from fastapi import APIRouter, Depends, HTTPException, status

from .dependencies import CurrentProfile, get_language_service
from .language_service import LanguageService
from .schemas import (
    CreateLanguageRequest,
    LanguageResponse,
    ReorderRequest,
    UpdateLanguageRequest,
)

router = APIRouter(prefix="/career", tags=["Career", "Languages"])


@router.get("/languages", response_model=list[LanguageResponse])
async def list_languages(
    *,
    profile: CurrentProfile,
    service: LanguageService = Depends(get_language_service),
) -> list[LanguageResponse]:
    """List the authenticated user's languages, ordered by display_order."""
    return await service.list_for_profile(profile.id)


@router.post("/languages", response_model=LanguageResponse, status_code=status.HTTP_201_CREATED)
async def create_language(
    *,
    payload: CreateLanguageRequest,
    profile: CurrentProfile,
    service: LanguageService = Depends(get_language_service),
) -> LanguageResponse:
    """Create a language entry, appended to the end of the display order."""
    try:
        return await service.create(profile.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/languages/reorder", response_model=list[LanguageResponse])
async def reorder_languages(
    *,
    payload: ReorderRequest,
    profile: CurrentProfile,
    service: LanguageService = Depends(get_language_service),
) -> list[LanguageResponse]:
    """Batch-reorder all of the authenticated user's languages."""
    try:
        return await service.reorder(profile.id, payload.orderedIds)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/languages/{id}", response_model=LanguageResponse)
async def update_language(
    *,
    id: str,
    payload: UpdateLanguageRequest,
    profile: CurrentProfile,
    service: LanguageService = Depends(get_language_service),
) -> LanguageResponse:
    """Partially update a language entry owned by the authenticated user."""
    language = await service.get_entity_for_profile(id, profile.id)
    if language is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language entry not found")
    try:
        return await service.update(language, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/languages/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_language(
    *,
    id: str,
    profile: CurrentProfile,
    service: LanguageService = Depends(get_language_service),
) -> None:
    """Delete a language entry owned by the authenticated user."""
    language = await service.get_entity_for_profile(id, profile.id)
    if language is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language entry not found")
    await service.delete(language)
