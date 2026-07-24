"""Skill endpoints for the career module (Phase 2)."""

from fastapi import APIRouter, Depends, HTTPException, status

from .ai_service import CareerAiService
from .dependencies import CareerAiUser, CurrentProfile, get_career_ai_service, get_skill_service
from .schemas import (
    BulkSkillsRequest,
    CreateSkillRequest,
    SkillResponse,
    UpdateSkillRequest,
)
from .skill_service import SkillService

router = APIRouter(prefix="/career", tags=["Career", "Skills"])


@router.get("/skills", response_model=list[SkillResponse])
async def list_skills(
    *,
    profile: CurrentProfile,
    service: SkillService = Depends(get_skill_service),
) -> list[SkillResponse]:
    """List the authenticated user's skills, ordered by technology name."""
    return await service.list_for_profile(profile.id)


@router.get("/skills/suggestions", response_model=list[str])
async def suggest_skills(
    *,
    user: CareerAiUser,
    role: str,
    seniorityLevel: str | None = None,
    ai_service: CareerAiService = Depends(get_career_ai_service),
) -> list[str]:
    """AI-backed skill suggestions for the given role (Pro/Expert or BYOK Free)."""
    return await ai_service.suggest_skills(user.id, role, seniorityLevel)


@router.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    *,
    payload: CreateSkillRequest,
    profile: CurrentProfile,
    service: SkillService = Depends(get_skill_service),
) -> SkillResponse:
    """Add a skill. Fails if the profile already has a skill for this technology —
    use ``PUT /skills/{id}`` to update it instead."""
    try:
        return await service.create(profile.id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/skills/bulk", response_model=list[SkillResponse])
async def bulk_upsert_skills(
    *,
    payload: BulkSkillsRequest,
    profile: CurrentProfile,
    service: SkillService = Depends(get_skill_service),
) -> list[SkillResponse]:
    """Add or update many skills at once, upserted by technology (no conflict errors)."""
    return await service.bulk_upsert(profile.id, payload)


@router.put("/skills/{id}", response_model=SkillResponse)
async def update_skill(
    *,
    id: str,
    payload: UpdateSkillRequest,
    profile: CurrentProfile,
    service: SkillService = Depends(get_skill_service),
) -> SkillResponse:
    """Partially update a skill owned by the authenticated user."""
    row = await service.get_entity_for_profile(id, profile.id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    skill, technology = row
    return await service.update(skill, technology, payload)


@router.delete("/skills/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    *,
    id: str,
    profile: CurrentProfile,
    service: SkillService = Depends(get_skill_service),
) -> None:
    """Delete a skill owned by the authenticated user."""
    row = await service.get_entity_for_profile(id, profile.id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    skill, _technology = row
    await service.delete(skill)
