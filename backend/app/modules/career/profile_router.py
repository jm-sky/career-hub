"""Profile endpoints for the career module (Phase 1)."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.auth.dependencies import CurrentUser

from .dependencies import OptionalUserId, get_profile_service
from .schemas import (
    ProfileDraftRequest,
    ProfileResponse,
    PublicProfileResponse,
    UpdateProfileRequest,
)
from .service import ProfileService

router = APIRouter(prefix="/career", tags=["Career"])


@router.get("/profile", response_model=ProfileResponse)
async def get_my_profile(
    *,
    current_user: CurrentUser,
    service: ProfileService = Depends(get_profile_service),
) -> ProfileResponse:
    """Return the authenticated user's profile, auto-creating an empty one if needed."""
    profile = await service.get_or_create_for_user(current_user.id, current_user.name)
    return ProfileResponse.model_validate(profile)


@router.put("/profile", response_model=ProfileResponse)
async def update_my_profile(
    *,
    payload: UpdateProfileRequest,
    current_user: CurrentUser,
    service: ProfileService = Depends(get_profile_service),
) -> ProfileResponse:
    """Partially update the authenticated user's profile."""
    profile = await service.get_or_create_for_user(current_user.id, current_user.name)
    try:
        profile = await service.update_profile(profile, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return ProfileResponse.model_validate(profile)


@router.post("/profile/draft", response_model=ProfileResponse)
async def save_profile_draft(
    *,
    payload: ProfileDraftRequest,
    current_user: CurrentUser,
    service: ProfileService = Depends(get_profile_service),
) -> ProfileResponse:
    """Step-scoped autosave for the profile wizard — does not touch other steps."""
    profile = await service.get_or_create_for_user(current_user.id, current_user.name)
    profile = await service.save_draft(profile, payload)
    return ProfileResponse.model_validate(profile)


@router.get("/profile/{slug}", response_model=PublicProfileResponse)
async def get_public_profile(
    *,
    slug: str,
    viewer_user_id: OptionalUserId,
    service: ProfileService = Depends(get_profile_service),
) -> PublicProfileResponse:
    """Public profile view, filtered by visibility. 404s for anything not visible
    to the current (possibly anonymous) viewer, rather than leaking existence."""
    profile = await service.get_public_profile(slug, viewer_user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return PublicProfileResponse.model_validate(profile)
