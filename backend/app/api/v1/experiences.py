"""Experience API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.experience import (
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse,
    ExperienceSummaryResponse,
    ExperienceReorderRequest,
)
from app.services.experience_service import (
    ExperienceService,
    ExperienceNotFoundError,
)

router = APIRouter(prefix="/experiences", tags=["experiences"])


@router.post("/", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
def create_experience(
    experience_data: ExperienceCreate,
    profile_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new experience for a profile."""
    service = ExperienceService(db)

    experience = service.create_experience(profile_id, current_user.id, experience_data)
    return experience.to_dict()


@router.get("/{experience_id}", response_model=ExperienceResponse)
def get_experience(
    experience_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get an experience by ID."""
    service = ExperienceService(db)

    experience = service.get_experience_by_id(experience_id)
    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")

    # Check if user can view this experience through profile ownership
    from app.services.profile_service import ProfileService

    profile_service = ProfileService(db)
    profile = profile_service.get_profile_by_id(experience.profile_id)

    if not profile or not profile.can_view(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to view this experience"
        )

    return experience.to_dict()


@router.put("/{experience_id}", response_model=ExperienceResponse)
def update_experience(
    experience_id: str,
    experience_data: ExperienceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update an experience."""
    service = ExperienceService(db)

    try:
        experience = service.update_experience(experience_id, current_user.id, experience_data)
        return experience.to_dict()
    except ExperienceNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(
    experience_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete an experience."""
    service = ExperienceService(db)

    deleted = service.delete_experience(experience_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")


@router.get("/profile/{profile_id}", response_model=List[ExperienceSummaryResponse])
def get_profile_experiences(
    profile_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all experiences for a profile."""
    service = ExperienceService(db)

    experiences = service.get_experiences_by_profile(profile_id, current_user.id)
    return [experience.to_summary_dict() for experience in experiences]


@router.post("/profile/{profile_id}/reorder", response_model=List[ExperienceSummaryResponse])
def reorder_experiences(
    profile_id: str,
    reorder_data: ExperienceReorderRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Reorder experiences for a profile."""
    service = ExperienceService(db)

    experiences = service.reorder_experiences(profile_id, current_user.id, reorder_data.experience_ids)
    return [experience.to_summary_dict() for experience in experiences]


@router.post("/{experience_id}/responsibilities", response_model=ExperienceResponse)
def add_responsibility(
    experience_id: str,
    responsibility: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Add a responsibility to an experience."""
    service = ExperienceService(db)

    try:
        experience = service.add_responsibility(experience_id, current_user.id, responsibility)
        return experience.to_dict()
    except ExperienceNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")


@router.delete("/{experience_id}/responsibilities", response_model=ExperienceResponse)
def remove_responsibility(
    experience_id: str,
    responsibility: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Remove a responsibility from an experience."""
    service = ExperienceService(db)

    try:
        experience = service.remove_responsibility(experience_id, current_user.id, responsibility)
        return experience.to_dict()
    except ExperienceNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")


@router.post("/{experience_id}/technologies", response_model=ExperienceResponse)
def add_technology(
    experience_id: str,
    technology: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Add a technology to an experience."""
    service = ExperienceService(db)

    try:
        experience = service.add_technology(experience_id, current_user.id, technology)
        return experience.to_dict()
    except ExperienceNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")


@router.delete("/{experience_id}/technologies", response_model=ExperienceResponse)
def remove_technology(
    experience_id: str,
    technology: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Remove a technology from an experience."""
    service = ExperienceService(db)

    try:
        experience = service.remove_technology(experience_id, current_user.id, technology)
        return experience.to_dict()
    except ExperienceNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
