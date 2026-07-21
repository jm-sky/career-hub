"""Business logic for CV versions (career module, Phase 5)."""

from app.common.id_utils import generate_id

from .achievement_repository import AchievementRepository
from .certification_repository import CertificationRepository
from .cv_version_repository import CvVersionRepository
from .db_models import CvVersionDB
from .education_repository import EducationRepository
from .experience_repository import ExperienceRepository
from .language_repository import LanguageRepository
from .project_repository import ProjectRepository
from .schemas import (
    CreateCvVersionRequest,
    CvSectionsConfig,
    CvVersionResponse,
    GenerateCvVersionResponse,
    UpdateCvVersionRequest,
)
from .skill_repository import SkillRepository


class CvVersionService:
    """Business logic for CV version CRUD, single-default enforcement, and the
    (stubbed) generate/download pipeline."""

    def __init__(
        self,
        repository: CvVersionRepository,
        experience_repository: ExperienceRepository,
        project_repository: ProjectRepository,
        skill_repository: SkillRepository,
        education_repository: EducationRepository,
        certification_repository: CertificationRepository,
        achievement_repository: AchievementRepository,
        language_repository: LanguageRepository,
    ):
        self.repository = repository
        self.experience_repository = experience_repository
        self.project_repository = project_repository
        self.skill_repository = skill_repository
        self.education_repository = education_repository
        self.certification_repository = certification_repository
        self.achievement_repository = achievement_repository
        self.language_repository = language_repository

    async def _validate_sections_config(self, profile_id: str, sections: CvSectionsConfig) -> None:
        checks = (
            (self.experience_repository, sections.experienceIds, "experienceIds"),
            (self.project_repository, sections.projectIds, "projectIds"),
            (self.skill_repository, sections.skillIds, "skillIds"),
            (self.education_repository, sections.educationIds, "educationIds"),
            (self.certification_repository, sections.certificationIds, "certificationIds"),
            (self.achievement_repository, sections.achievementIds, "achievementIds"),
            (self.language_repository, sections.languageIds, "languageIds"),
        )
        for repository, ids, field_name in checks:
            if not ids:
                continue
            owned = await repository.get_by_ids_and_profile(ids, profile_id)
            if len(owned) != len(set(ids)):
                raise ValueError(f"One or more {field_name} do not belong to this profile.")

    async def list_for_profile(self, profile_id: str) -> list[CvVersionResponse]:
        cv_versions = await self.repository.list_by_profile(profile_id)
        return [CvVersionResponse.model_validate(cv) for cv in cv_versions]

    async def get_entity_for_profile(self, id_: str, profile_id: str) -> CvVersionDB | None:
        return await self.repository.get_by_id_and_profile(id_, profile_id)

    async def create(self, profile_id: str, payload: CreateCvVersionRequest) -> CvVersionResponse:
        await self._validate_sections_config(profile_id, payload.sectionsConfig)

        if payload.isDefault:
            await self.repository.clear_default(profile_id)

        cv_version = CvVersionDB(
            id=generate_id(),
            profile_id=profile_id,
            name=payload.name,
            template=payload.template,
            sections_config=payload.sectionsConfig.model_dump(),
            is_default=payload.isDefault,
        )
        cv_version = await self.repository.create(cv_version)
        return CvVersionResponse.model_validate(cv_version)

    async def update(self, cv_version: CvVersionDB, payload: UpdateCvVersionRequest) -> CvVersionResponse:
        if payload.sectionsConfig is not None:
            await self._validate_sections_config(cv_version.profile_id, payload.sectionsConfig)
            cv_version.sections_config = payload.sectionsConfig.model_dump()
        if payload.name is not None:
            cv_version.name = payload.name
        if payload.template is not None:
            cv_version.template = payload.template
        if payload.isDefault is not None:
            if payload.isDefault:
                await self.repository.clear_default(cv_version.profile_id, except_id=cv_version.id)
            cv_version.is_default = payload.isDefault

        cv_version = await self.repository.save(cv_version)
        return CvVersionResponse.model_validate(cv_version)

    async def delete(self, cv_version: CvVersionDB) -> None:
        await self.repository.delete(cv_version)

    async def generate(self, cv_version: CvVersionDB) -> GenerateCvVersionResponse:
        """Stub — accepts the request but does not render a PDF. No PDF rendering
        engine has been chosen yet (open question in career-module-plan.md Phase 5);
        this only confirms the request shape and hands back a job id."""
        return GenerateCvVersionResponse(jobId=generate_id(), status="queued")

    async def get_pdf_url(self, cv_version: CvVersionDB) -> str:
        if not cv_version.pdf_url:
            raise ValueError("PDF has not been generated for this CV version yet.")
        return cv_version.pdf_url
