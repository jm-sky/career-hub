"""Profile API endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
    ProfilePublicResponse,
    ProfileSummaryResponse,
)
from app.services.profile_service import (
    ProfileService,
    ProfileNotFoundError,
    ProfileAlreadyExistsError,
    SlugAlreadyExistsError,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new profile for the current user."""
    service = ProfileService(db)

    try:
        profile = service.create_profile(current_user.id, profile_data)
        return profile.to_dict(include_private=True)
    except ProfileAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already has a profile")
    except SlugAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug is already taken")


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get the current user's profile."""
    service = ProfileService(db)

    profile = service.get_profile_by_user_id(current_user.id, include_relations=True)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return profile.to_dict(include_private=True)


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: str,
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a profile by ID."""
    service = ProfileService(db)

    profile = service.get_profile_by_id(profile_id, include_relations=True)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    # Check if user can view this profile
    user_id = current_user.id if current_user else None
    if not profile.can_view(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to view this profile"
        )

    # Return appropriate response based on ownership
    include_private = bool(current_user and profile.user_id == current_user.id)
    return profile.to_dict(include_private=include_private)


@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: str,
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a profile."""
    service = ProfileService(db)

    try:
        profile = service.update_profile(profile_id, current_user.id, profile_data)
        return profile.to_dict(include_private=True)
    except ProfileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    except SlugAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug is already taken")


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a profile."""
    service = ProfileService(db)

    deleted = service.delete_profile(profile_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


@router.get("/", response_model=List[ProfileSummaryResponse])
def get_public_profiles(
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
    offset: int = Query(0, ge=0, description="Number of profiles to skip"),
    db: Session = Depends(get_db),
):
    """Get public profiles."""
    service = ProfileService(db)

    profiles = service.get_public_profiles(limit=limit, offset=offset)
    return [
        {
            "id": profile.id,
            "headline": profile.headline,
            "location": profile.location,
            "completenessScore": profile.completeness_score,
            "visibility": profile.visibility,
        }
        for profile in profiles
    ]


@router.get("/search/", response_model=List[ProfileSummaryResponse])
def search_profiles(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of profiles to return"),
    offset: int = Query(0, ge=0, description="Number of profiles to skip"),
    db: Session = Depends(get_db),
):
    """Search public profiles."""
    service = ProfileService(db)

    profiles = service.search_profiles(q, limit=limit, offset=offset)
    return [
        {
            "id": profile.id,
            "headline": profile.headline,
            "location": profile.location,
            "completenessScore": profile.completeness_score,
            "visibility": profile.visibility,
        }
        for profile in profiles
    ]


@router.get("/slug/{slug}", response_model=ProfilePublicResponse)
def get_profile_by_slug(
    slug: str,
    db: Session = Depends(get_db),
):
    """Get a public profile by slug."""
    service = ProfileService(db)

    profile = service.get_profile_by_slug(slug, include_relations=True)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    if not profile.is_public():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return profile.to_public_dict()


@router.post("/{profile_id}/completeness", response_model=dict)
def update_completeness_score(
    profile_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update profile completeness score."""
    service = ProfileService(db)

    # Check if user owns the profile
    profile = service.get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    if profile.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this profile"
        )

    try:
        score = service.update_completeness_score(profile_id)
        return {"completenessScore": score}
    except ProfileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


@router.get("/slug-available/{slug}", response_model=dict)
def check_slug_availability(
    slug: str,
    profile_id: Optional[str] = Query(None, description="Profile ID to exclude from check"),
    db: Session = Depends(get_db),
):
    """Check if a slug is available."""
    service = ProfileService(db)

    available = service.is_slug_available(slug, exclude_profile_id=profile_id)
    return {"available": available}
