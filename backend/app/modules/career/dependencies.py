"""Career-module-local FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.storage import get_storage_adapter
from app.modules.ai.repositories import HistoryRepository, SettingsRepository
from app.modules.ai.services.settings_service import SettingsService as AiSettingsService
from app.modules.auth.auth_utils import verify_token
from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.modules.auth.repositories import get_user_repository
from app.modules.auth.types.repository import UserRepositoryInterface
from app.modules.billing.dependencies import get_billing_service
from app.modules.billing.exceptions import FreeTrierRequiresBYOKError
from app.modules.billing.service import BillingService

from .achievement_repository import AchievementRepository
from .achievement_service import AchievementService
from .ai_service import CareerAiService
from .certification_repository import CertificationRepository
from .certification_service import CertificationService
from .cv_version_repository import CvVersionRepository
from .cv_version_service import CvVersionService
from .db_models import ProfileDB
from .education_repository import EducationRepository
from .education_service import EducationService
from .experience_repository import ExperienceRepository, ExperienceTechnologyRepository
from .experience_service import ExperienceService
from .language_repository import LanguageRepository
from .language_service import LanguageService
from .project_repository import (
    ProjectExperienceRepository,
    ProjectRepository,
    ProjectTechnologyRepository,
)
from .project_service import ProjectService
from .repository import ProfileRepository
from .responsibilities_library_repository import ResponsibilitiesLibraryRepository
from .service import ProfileService
from .skill_repository import SkillRepository
from .skill_service import SkillService
from .technology_repository import TechnologyRepository
from .technology_service import TechnologyService

_optional_security = HTTPBearer(auto_error=False)


async def get_optional_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_optional_security)],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> str | None:
    """Best-effort viewer identification for public endpoints.

    Unlike ``get_current_user``, this never raises: a missing, expired, or invalid
    token simply means "anonymous viewer" rather than a 401. Used only to decide
    whether the requester happens to be the profile owner on the public slug
    endpoint — not a substitute for real auth on any endpoint that requires it.
    """
    if credentials is None:
        return None
    try:
        payload = verify_token(credentials.credentials, expected_type="access")
    except Exception:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    user = await user_repository.get_user_by_id(user_id)
    if user is None or not user.isActive:
        return None
    return user_id


OptionalUserId = Annotated[str | None, Depends(get_optional_user_id)]


def get_profile_service(db: AsyncSession = Depends(get_db)) -> ProfileService:
    return ProfileService(ProfileRepository(db))


async def get_current_profile(
    current_user: CurrentUser,
    profile_service: ProfileService = Depends(get_profile_service),
) -> ProfileDB:
    """The authenticated user's profile, auto-creating an empty one if needed.

    Shared by every Phase 2+ router (experiences/technologies/skills/...) so each
    doesn't have to repeat the get-or-create call itself.
    """
    return await profile_service.get_or_create_for_user(current_user.id, current_user.name)


CurrentProfile = Annotated[ProfileDB, Depends(get_current_profile)]


def get_technology_service(db: AsyncSession = Depends(get_db)) -> TechnologyService:
    return TechnologyService(TechnologyRepository(db))


def get_experience_service(db: AsyncSession = Depends(get_db)) -> ExperienceService:
    return ExperienceService(
        ExperienceRepository(db),
        ExperienceTechnologyRepository(db),
        TechnologyRepository(db),
        TechnologyService(TechnologyRepository(db)),
    )


def get_skill_service(db: AsyncSession = Depends(get_db)) -> SkillService:
    return SkillService(SkillRepository(db), TechnologyService(TechnologyRepository(db)))


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    return ProjectService(
        ProjectRepository(db),
        ProjectTechnologyRepository(db),
        ProjectExperienceRepository(db),
        TechnologyRepository(db),
        TechnologyService(TechnologyRepository(db)),
        ExperienceRepository(db),
    )


def get_education_service(db: AsyncSession = Depends(get_db)) -> EducationService:
    return EducationService(EducationRepository(db))


def get_certification_service(db: AsyncSession = Depends(get_db)) -> CertificationService:
    return CertificationService(CertificationRepository(db))


def get_achievement_service(db: AsyncSession = Depends(get_db)) -> AchievementService:
    return AchievementService(AchievementRepository(db))


def get_language_service(db: AsyncSession = Depends(get_db)) -> LanguageService:
    return LanguageService(LanguageRepository(db))


def get_cv_version_service(
    db: AsyncSession = Depends(get_db),
    billing_service: BillingService = Depends(get_billing_service),
) -> CvVersionService:
    return CvVersionService(
        CvVersionRepository(db),
        ExperienceRepository(db),
        ProjectRepository(db),
        SkillRepository(db),
        EducationRepository(db),
        CertificationRepository(db),
        AchievementRepository(db),
        LanguageRepository(db),
        billing_service,
        get_storage_adapter(),
    )


async def require_career_ai_access(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    billing_service: BillingService = Depends(get_billing_service),
) -> User:
    """Gate for the career module's AI endpoints (optimize/suggest/analyze).

    Same policy as the ``ai`` module's own chat access: paid (Pro/Expert) plans
    always have access; Free tier requires a user-configured OpenRouter token
    (BYOK). Uses ``BillingService.check_ai_access`` — the plan-tier-based check —
    rather than ``ai.dependencies.require_ai_access``, which gates on the legacy
    ``User.isPremium`` flag instead of ``billing.plan_tier``.
    """
    ai_settings_repo = SettingsRepository(db)
    ai_settings_service = AiSettingsService(ai_settings_repo)
    openrouter_token = await ai_settings_service.get_api_token(current_user.id)

    try:
        has_access = await billing_service.check_ai_access(current_user.id, openrouter_token=openrouter_token)
    except FreeTrierRequiresBYOKError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="AI features require a Pro or Expert subscription, or your own OpenRouter API token.",
        )

    return current_user


CareerAiUser = Annotated[User, Depends(require_career_ai_access)]


def get_career_ai_service(db: AsyncSession = Depends(get_db)) -> CareerAiService:
    ai_settings_service = AiSettingsService(SettingsRepository(db))
    return CareerAiService(
        ai_settings_service,
        HistoryRepository(db),
        ResponsibilitiesLibraryRepository(db),
        ExperienceRepository(db),
        ProjectRepository(db),
        SkillRepository(db),
    )
