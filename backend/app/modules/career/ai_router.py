"""AI endpoints for the career module (Phase 7, Pro/Expert or BYOK Free).

Distinct from the ``ai`` module's own ``/ai/chat`` endpoint — these are one-shot,
domain-specific completions (optimize a description, suggest responsibilities,
gap-analyze a profile against a target role), not a chat/conversation UI.
"""

from fastapi import APIRouter, Depends

from .ai_service import CareerAiService
from .dependencies import CareerAiUser, CurrentProfile, get_career_ai_service
from .schemas import (
    AnalyzeProfileRequest,
    AnalyzeProfileResponse,
    OptimizeDescriptionRequest,
    OptimizeDescriptionResponse,
    SuggestResponsibilitiesRequest,
    SuggestResponsibilitiesResponse,
)

router = APIRouter(prefix="/career/ai", tags=["Career", "AI"])


@router.post("/optimize-description", response_model=OptimizeDescriptionResponse)
async def optimize_description(
    *,
    payload: OptimizeDescriptionRequest,
    user: CareerAiUser,
    service: CareerAiService = Depends(get_career_ai_service),
) -> OptimizeDescriptionResponse:
    """Rewrite a responsibility/description into a stronger, achievement-oriented version."""
    return await service.optimize_description(user.id, payload)


@router.post("/suggest-responsibilities", response_model=SuggestResponsibilitiesResponse)
async def suggest_responsibilities(
    *,
    payload: SuggestResponsibilitiesRequest,
    user: CareerAiUser,
    service: CareerAiService = Depends(get_career_ai_service),
) -> SuggestResponsibilitiesResponse:
    """Suggest responsibilities for a role/seniority, from the shared library or AI."""
    return await service.suggest_responsibilities(user.id, payload)


@router.post("/analyze-profile", response_model=AnalyzeProfileResponse)
async def analyze_profile(
    *,
    payload: AnalyzeProfileRequest,
    user: CareerAiUser,
    profile: CurrentProfile,
    service: CareerAiService = Depends(get_career_ai_service),
) -> AnalyzeProfileResponse:
    """Gap analysis (match score + strengths/gaps/recommendations) of the
    authenticated user's profile against a target role."""
    return await service.analyze_profile(user.id, profile.id, payload.targetRole)
