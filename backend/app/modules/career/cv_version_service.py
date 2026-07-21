"""Business logic for CV versions (career module, Phase 5)."""

import asyncio
from typing import Any

from app.common.id_utils import generate_id
from app.core.storage import StorageAdapter
from app.modules.billing.exceptions import SubscriptionNotFoundError
from app.modules.billing.service import BillingService

from .achievement_repository import AchievementRepository
from .certification_repository import CertificationRepository
from .cv_renderer import CvRenderData, build_cv_html, render_pdf
from .cv_version_repository import CvVersionRepository
from .db_models import CvVersionDB, ProfileDB
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
    WeasyPrint generate/download pipeline."""

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
        billing_service: BillingService,
        storage: StorageAdapter,
    ):
        self.repository = repository
        self.experience_repository = experience_repository
        self.project_repository = project_repository
        self.skill_repository = skill_repository
        self.education_repository = education_repository
        self.certification_repository = certification_repository
        self.achievement_repository = achievement_repository
        self.language_repository = language_repository
        self.billing_service = billing_service
        self.storage = storage

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

    async def _collect_render_data(self, cv_version: CvVersionDB, profile: ProfileDB, user_name: str) -> CvRenderData:
        """Load the profile content this CV version selects, in display order.

        An empty id list for a section means "include everything in that section"
        rather than "include nothing" — a CV whose selection was never edited
        should still render the full profile instead of an empty page. To leave a
        section out, the CV must select a non-empty subset of the others.
        """
        sections = CvSectionsConfig.model_validate(cv_version.sections_config or {})
        profile_id = profile.id

        async def pick(repository: Any, ids: list[str], order_key: str = "display_order") -> list[Any]:
            rows = await repository.get_by_ids_and_profile(ids, profile_id) if ids else await repository.list_by_profile(profile_id)
            return sorted(rows, key=lambda row: getattr(row, order_key, 0))

        skill_rows = await self.skill_repository.list_by_profile(profile_id) if not sections.skillIds else [(skill, technology) for skill, technology in await self.skill_repository.list_by_profile(profile_id) if skill.id in set(sections.skillIds)]

        return CvRenderData(
            user_name=user_name,
            profile=profile,
            sections=sections,
            experiences=await pick(self.experience_repository, sections.experienceIds),
            projects=await pick(self.project_repository, sections.projectIds),
            skills=[(skill, technology.name) for skill, technology in skill_rows],
            education=await pick(self.education_repository, sections.educationIds),
            certifications=await pick(self.certification_repository, sections.certificationIds),
            achievements=await pick(self.achievement_repository, sections.achievementIds),
            languages=await pick(self.language_repository, sections.languageIds),
        )

    async def generate(self, cv_version: CvVersionDB, profile: ProfileDB, user_name: str) -> GenerateCvVersionResponse:
        """Render the CV to PDF and store it, synchronously.

        The digest specifies an async job (202 + jobId) for this, but WeasyPrint
        renders a CV-sized document in well under a second — a queue and a worker
        would add moving parts without shortening the request. The response keeps
        the `jobId`/`status` shape so this can move to a background job later
        without breaking clients; `status` is simply `completed` on arrival.
        """
        watermark = await self._should_watermark(profile.user_id)
        data = await self._collect_render_data(cv_version, profile, user_name)
        html = build_cv_html(data, cv_version.template, watermark)

        # WeasyPrint is synchronous and CPU-bound — keep it off the event loop.
        pdf_bytes = await asyncio.to_thread(render_pdf, html)

        destination = f"cv-versions/{profile.id}/{cv_version.id}.pdf"
        stored_path = await self.storage.upload(pdf_bytes, destination, "application/pdf")

        cv_version.pdf_url = stored_path
        await self.repository.save(cv_version)

        return GenerateCvVersionResponse(
            jobId=generate_id(),
            status="completed",
            watermark=watermark,
            pdfUrl=stored_path,
        )

    async def _should_watermark(self, user_id: str) -> bool:
        try:
            limits = await self.billing_service.get_subscription_limits(user_id)
        except SubscriptionNotFoundError:
            return True  # No subscription yet == free tier == watermarked
        return limits.pdfWatermark

    async def get_pdf_bytes(self, cv_version: CvVersionDB) -> bytes:
        """Read a previously generated PDF back out of storage."""
        if not cv_version.pdf_url:
            raise ValueError("PDF has not been generated for this CV version yet.")
        return await self.storage.download(cv_version.pdf_url)
