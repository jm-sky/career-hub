"""Pydantic schemas for the career module (Phase 1: profile. Phase 2: experiences,
technologies, skills. Phase 3: projects. Phase 4: education, certifications,
achievements. Phase 5: cv_versions)."""

from datetime import date, datetime
from datetime import date as _Date
from typing import Any, Literal

from pydantic import BaseModel, Field

ProfileVisibility = Literal["PRIVATE", "FRIENDS", "PUBLIC"]


class ContactInfo(BaseModel):
    """Profile contact details. Never returned on the public slug endpoint."""

    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    website: str | None = None


class ProfileResponse(BaseModel):
    """Full profile representation — returned to the profile's own owner."""

    id: str = Field(alias="id", serialization_alias="id")
    userId: str = Field(alias="user_id", serialization_alias="userId")
    slug: str = Field(alias="slug", serialization_alias="slug")
    headline: str | None = Field(None, alias="headline", serialization_alias="headline")
    summary: str | None = Field(None, alias="summary", serialization_alias="summary")
    location: str | None = Field(None, alias="location", serialization_alias="location")
    visibility: ProfileVisibility = Field(alias="visibility", serialization_alias="visibility")
    contact: ContactInfo = Field(default_factory=ContactInfo, alias="contact", serialization_alias="contact")
    draftData: dict[str, Any] = Field(default_factory=dict, alias="draft_data", serialization_alias="draftData")
    profilePhotoUrl: str | None = Field(None, alias="profile_photo_url", serialization_alias="profilePhotoUrl")
    completenessScore: int = Field(alias="completeness_score", serialization_alias="completenessScore")
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class PublicProfileResponse(BaseModel):
    """Public-safe profile view — no contact info, no draft data, ever."""

    slug: str = Field(alias="slug", serialization_alias="slug")
    headline: str | None = Field(None, alias="headline", serialization_alias="headline")
    summary: str | None = Field(None, alias="summary", serialization_alias="summary")
    location: str | None = Field(None, alias="location", serialization_alias="location")
    profilePhotoUrl: str | None = Field(None, alias="profile_photo_url", serialization_alias="profilePhotoUrl")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class UpdateProfileRequest(BaseModel):
    """Partial update — only provided fields change."""

    headline: str | None = Field(default=None, max_length=200)
    summary: str | None = Field(default=None)
    location: str | None = Field(default=None, max_length=120)
    visibility: ProfileVisibility | None = Field(default=None)
    contact: ContactInfo | None = Field(default=None)
    profilePhotoUrl: str | None = Field(default=None, max_length=500)
    slug: str | None = Field(default=None, min_length=3, max_length=80)


class ProfileDraftRequest(BaseModel):
    """Step-scoped autosave payload — merges into draft_data[step], doesn't touch other steps."""

    step: str = Field(..., min_length=1, max_length=50)
    data: dict[str, Any] = Field(default_factory=dict)


# --- Phase 2: technologies, experiences, skills ---------------------------------


class TechnologyResponse(BaseModel):
    """A global technology reference, as attached to an experience or skill."""

    id: str = Field(alias="id", serialization_alias="id")
    name: str = Field(alias="name", serialization_alias="name")
    category: str | None = Field(None, alias="category", serialization_alias="category")
    layer: str | None = Field(None, alias="layer", serialization_alias="layer")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class ExperienceResponse(BaseModel):
    """Full work-experience representation, incl. its linked technologies."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    companyName: str = Field(alias="company_name", serialization_alias="companyName")
    position: str = Field(alias="position", serialization_alias="position")
    employmentType: str | None = Field(None, alias="employment_type", serialization_alias="employmentType")
    startDate: date = Field(alias="start_date", serialization_alias="startDate")
    endDate: date | None = Field(None, alias="end_date", serialization_alias="endDate")
    isCurrent: bool = Field(alias="is_current", serialization_alias="isCurrent")
    description: str | None = Field(None, alias="description", serialization_alias="description")
    responsibilities: list[str] = Field(default_factory=list, alias="responsibilities", serialization_alias="responsibilities")
    displayOrder: int = Field(alias="display_order", serialization_alias="displayOrder")
    technologies: list[TechnologyResponse] = Field(default_factory=list)
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CreateExperienceRequest(BaseModel):
    """Payload to create a work-experience entry.

    ``technologies`` is a free-form list of technology names — unknown names are
    created on the fly (get-or-create), matching the frontend's tag-input UX.
    """

    companyName: str = Field(..., min_length=1, max_length=200)
    position: str = Field(..., min_length=1, max_length=200)
    employmentType: str | None = Field(default=None, max_length=30)
    startDate: date
    endDate: date | None = Field(default=None)
    isCurrent: bool = Field(default=False)
    description: str | None = Field(default=None)
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)


class UpdateExperienceRequest(BaseModel):
    """Partial update for a work-experience entry — only provided fields change.

    ``technologies``, when provided, fully replaces the experience's technology set.
    """

    companyName: str | None = Field(default=None, min_length=1, max_length=200)
    position: str | None = Field(default=None, min_length=1, max_length=200)
    employmentType: str | None = Field(default=None, max_length=30)
    startDate: date | None = Field(default=None)
    endDate: date | None = Field(default=None)
    isCurrent: bool | None = Field(default=None)
    description: str | None = Field(default=None)
    responsibilities: list[str] | None = Field(default=None)
    technologies: list[str] | None = Field(default=None)


class ReorderRequest(BaseModel):
    """Batch reorder payload — the full, ordered list of ids for the owning profile.

    Reused across every orderable career entity (experiences now; education/
    projects later), so it stays generic rather than experience-specific.
    """

    orderedIds: list[str] = Field(..., min_length=1)


class CreateSkillRequest(BaseModel):
    """Payload to add a skill.

    ``technologyName`` is get-or-create, same as experience technologies.
    """

    technologyName: str = Field(..., min_length=1, max_length=100)
    level: int = Field(..., ge=1, le=5)
    yearsOfExperience: float | None = Field(default=None, ge=0)
    startedUsingYear: int | None = Field(default=None)
    isPrimary: bool = Field(default=False)


class UpdateSkillRequest(BaseModel):
    """Partial update for a skill — only provided fields change. Technology is fixed
    at creation time; delete + recreate to change which technology a skill tracks."""

    level: int | None = Field(default=None, ge=1, le=5)
    yearsOfExperience: float | None = Field(default=None, ge=0)
    startedUsingYear: int | None = Field(default=None)
    isPrimary: bool | None = Field(default=None)


class BulkSkillsRequest(BaseModel):
    """Bulk add/update payload — each entry is upserted by (profile, technology)."""

    skills: list[CreateSkillRequest] = Field(..., min_length=1)


class SkillResponse(BaseModel):
    """Full skill representation, incl. its linked technology."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    technology: TechnologyResponse
    level: int = Field(alias="level", serialization_alias="level")
    yearsOfExperience: float | None = Field(None, alias="years_of_experience", serialization_alias="yearsOfExperience")
    startedUsingYear: int | None = Field(None, alias="started_using_year", serialization_alias="startedUsingYear")
    isPrimary: bool = Field(alias="is_primary", serialization_alias="isPrimary")
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --- Phase 3: projects -----------------------------------------------------------

ProjectStatus = Literal["ACTIVE", "STAGING", "ARCHIVED"]
ProjectCategory = Literal["DEMO", "INTERNAL", "PRODUCTION"]


class ProjectLinks(BaseModel):
    """External links for a project. Never required — a project can exist with none."""

    demo: str | None = None
    github: str | None = None
    docs: str | None = None


class SubProject(BaseModel):
    """A client site/instance of a template project (issue 001) — e.g. one
    deployed customization of a reusable platform."""

    name: str = Field(..., min_length=1, max_length=200)
    url: str | None = Field(default=None, max_length=500)


class ProjectResponse(BaseModel):
    """Full project representation, incl. linked technologies and experience ids."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    name: str = Field(alias="name", serialization_alias="name")
    description: str | None = Field(None, alias="description", serialization_alias="description")
    role: str | None = Field(None, alias="role", serialization_alias="role")
    startDate: date = Field(alias="start_date", serialization_alias="startDate")
    endDate: date | None = Field(None, alias="end_date", serialization_alias="endDate")
    isOngoing: bool = Field(alias="is_ongoing", serialization_alias="isOngoing")
    isAnonymized: bool = Field(alias="is_anonymized", serialization_alias="isAnonymized")
    anonymizedCompany: str | None = Field(None, alias="anonymized_company", serialization_alias="anonymizedCompany")
    status: ProjectStatus = Field(alias="status", serialization_alias="status")
    category: ProjectCategory | None = Field(None, alias="category", serialization_alias="category")
    achievements: list[str] = Field(default_factory=list)
    challenges: list[str] = Field(default_factory=list)
    clients: list[str] = Field(default_factory=list)
    team: list[str] = Field(default_factory=list)
    subProjects: list[SubProject] = Field(default_factory=list, alias="sub_projects", serialization_alias="subProjects")
    teamSize: int | None = Field(None, alias="team_size", serialization_alias="teamSize")
    durationMonths: int | None = Field(None, alias="duration_months", serialization_alias="durationMonths")
    usersCount: int | None = Field(None, alias="users_count", serialization_alias="usersCount")
    budgetRange: str | None = Field(None, alias="budget_range", serialization_alias="budgetRange")
    links: ProjectLinks = Field(default_factory=ProjectLinks, alias="links", serialization_alias="links")
    visibility: ProfileVisibility = Field(alias="visibility", serialization_alias="visibility")
    displayOrder: int = Field(alias="display_order", serialization_alias="displayOrder")
    technologies: list[TechnologyResponse] = Field(default_factory=list)
    experienceIds: list[str] = Field(default_factory=list)
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CreateProjectRequest(BaseModel):
    """Payload to create a project.

    ``technologies`` is get-or-create by name, same as experiences. ``experienceIds``
    links this project to one or more of the profile's own existing experiences
    (cross-company/portfolio projects) — ids not owned by the profile are rejected.
    """

    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None)
    role: str | None = Field(default=None, max_length=200)
    startDate: date
    endDate: date | None = Field(default=None)
    isOngoing: bool = Field(default=False)
    isAnonymized: bool = Field(default=False)
    anonymizedCompany: str | None = Field(default=None, max_length=200)
    status: ProjectStatus = Field(default="ACTIVE")
    category: ProjectCategory | None = Field(default=None)
    achievements: list[str] = Field(default_factory=list)
    challenges: list[str] = Field(default_factory=list)
    clients: list[str] = Field(default_factory=list)
    team: list[str] = Field(default_factory=list)
    subProjects: list[SubProject] = Field(default_factory=list)
    teamSize: int | None = Field(default=None, ge=0)
    durationMonths: int | None = Field(default=None, ge=0)
    usersCount: int | None = Field(default=None, ge=0)
    budgetRange: str | None = Field(default=None, max_length=50)
    links: ProjectLinks = Field(default_factory=ProjectLinks)
    visibility: ProfileVisibility = Field(default="PRIVATE")
    technologies: list[str] = Field(default_factory=list)
    experienceIds: list[str] = Field(default_factory=list)


class UpdateProjectRequest(BaseModel):
    """Partial update for a project — only provided fields change.

    ``technologies``/``experienceIds``, when provided, fully replace the current set.
    """

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None)
    role: str | None = Field(default=None, max_length=200)
    startDate: date | None = Field(default=None)
    endDate: date | None = Field(default=None)
    isOngoing: bool | None = Field(default=None)
    isAnonymized: bool | None = Field(default=None)
    anonymizedCompany: str | None = Field(default=None, max_length=200)
    status: ProjectStatus | None = Field(default=None)
    category: ProjectCategory | None = Field(default=None)
    achievements: list[str] | None = Field(default=None)
    challenges: list[str] | None = Field(default=None)
    clients: list[str] | None = Field(default=None)
    team: list[str] | None = Field(default=None)
    subProjects: list[SubProject] | None = Field(default=None)
    teamSize: int | None = Field(default=None, ge=0)
    durationMonths: int | None = Field(default=None, ge=0)
    usersCount: int | None = Field(default=None, ge=0)
    budgetRange: str | None = Field(default=None, max_length=50)
    links: ProjectLinks | None = Field(default=None)
    visibility: ProfileVisibility | None = Field(default=None)
    technologies: list[str] | None = Field(default=None)
    experienceIds: list[str] | None = Field(default=None)


# --- Phase 4: education, certifications, achievements ----------------------------

AchievementCategory = Literal["AWARD", "PUBLICATION", "SPEAKING", "OTHER"]


class EducationResponse(BaseModel):
    """Full education entry representation."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    institution: str = Field(alias="institution", serialization_alias="institution")
    degree: str = Field(alias="degree", serialization_alias="degree")
    fieldOfStudy: str | None = Field(None, alias="field_of_study", serialization_alias="fieldOfStudy")
    startDate: date = Field(alias="start_date", serialization_alias="startDate")
    endDate: date | None = Field(None, alias="end_date", serialization_alias="endDate")
    grade: str | None = Field(None, alias="grade", serialization_alias="grade")
    description: str | None = Field(None, alias="description", serialization_alias="description")
    displayOrder: int = Field(alias="display_order", serialization_alias="displayOrder")
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CreateEducationRequest(BaseModel):
    institution: str = Field(..., min_length=1, max_length=200)
    degree: str = Field(..., min_length=1, max_length=200)
    fieldOfStudy: str | None = Field(default=None, max_length=200)
    startDate: date
    endDate: date | None = Field(default=None)
    grade: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None)


class UpdateEducationRequest(BaseModel):
    """Partial update — only provided fields change."""

    institution: str | None = Field(default=None, min_length=1, max_length=200)
    degree: str | None = Field(default=None, min_length=1, max_length=200)
    fieldOfStudy: str | None = Field(default=None, max_length=200)
    startDate: date | None = Field(default=None)
    endDate: date | None = Field(default=None)
    grade: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None)


class CertificationResponse(BaseModel):
    """Full certification representation. ``isExpired`` is computed relative to the
    current date at request time — never stored."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    name: str = Field(alias="name", serialization_alias="name")
    issuingOrganization: str = Field(alias="issuing_organization", serialization_alias="issuingOrganization")
    credentialId: str | None = Field(None, alias="credential_id", serialization_alias="credentialId")
    credentialUrl: str | None = Field(None, alias="credential_url", serialization_alias="credentialUrl")
    issueDate: date = Field(alias="issue_date", serialization_alias="issueDate")
    expiryDate: date | None = Field(None, alias="expiry_date", serialization_alias="expiryDate")
    isExpired: bool = Field(default=False)
    displayOrder: int = Field(alias="display_order", serialization_alias="displayOrder")
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CreateCertificationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    issuingOrganization: str = Field(..., min_length=1, max_length=200)
    credentialId: str | None = Field(default=None, max_length=100)
    credentialUrl: str | None = Field(default=None, max_length=500)
    issueDate: date
    expiryDate: date | None = Field(default=None)


class UpdateCertificationRequest(BaseModel):
    """Partial update — only provided fields change."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    issuingOrganization: str | None = Field(default=None, min_length=1, max_length=200)
    credentialId: str | None = Field(default=None, max_length=100)
    credentialUrl: str | None = Field(default=None, max_length=500)
    issueDate: date | None = Field(default=None)
    expiryDate: date | None = Field(default=None)


class AchievementResponse(BaseModel):
    """Full achievement representation."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    title: str = Field(alias="title", serialization_alias="title")
    description: str | None = Field(None, alias="description", serialization_alias="description")
    # Annotated as `_Date`, not `date` — a field literally named `date` self-shadows the
    # `date` type mid-statement (the value binds to the name before its own annotation
    # is evaluated), which raises `TypeError: unsupported operand type(s) for |: 'FieldInfo' and 'NoneType'`.
    date: _Date | None = Field(None, alias="date", serialization_alias="date")
    category: AchievementCategory | None = Field(None, alias="category", serialization_alias="category")
    url: str | None = Field(None, alias="url", serialization_alias="url")
    displayOrder: int = Field(alias="display_order", serialization_alias="displayOrder")
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CreateAchievementRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None)
    date: _Date | None = Field(default=None)
    category: AchievementCategory | None = Field(default=None)
    url: str | None = Field(default=None, max_length=500)


class UpdateAchievementRequest(BaseModel):
    """Partial update — only provided fields change."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None)
    date: _Date | None = Field(default=None)
    category: AchievementCategory | None = Field(default=None)
    url: str | None = Field(default=None, max_length=500)


# --- Languages -------------------------------------------------------------------

LanguageLevel = Literal["NATIVE", "C2", "C1", "B2", "B1", "A2", "A1"]


class LanguageResponse(BaseModel):
    """A spoken/written language on the profile."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    name: str = Field(alias="name", serialization_alias="name")
    level: LanguageLevel = Field(alias="level", serialization_alias="level")
    description: str | None = Field(None, alias="description", serialization_alias="description")
    displayOrder: int = Field(alias="display_order", serialization_alias="displayOrder")
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CreateLanguageRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    level: LanguageLevel
    description: str | None = Field(default=None)


class UpdateLanguageRequest(BaseModel):
    """Partial update — only provided fields change."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    level: LanguageLevel | None = Field(default=None)
    description: str | None = Field(default=None)


# --- Phase 5: cv_versions ---------------------------------------------------------


class CvSectionsConfig(BaseModel):
    """Which profile-section items to include in a CV export, plus a few overrides.

    Ids reference the profile's own experiences/projects/skills/education/
    certifications/achievements/languages — ownership is validated at the service layer
    (this schema has no DB access), same as Project's ``experienceIds``.
    """

    experienceIds: list[str] = Field(default_factory=list)
    projectIds: list[str] = Field(default_factory=list)
    skillIds: list[str] = Field(default_factory=list)
    educationIds: list[str] = Field(default_factory=list)
    certificationIds: list[str] = Field(default_factory=list)
    achievementIds: list[str] = Field(default_factory=list)
    languageIds: list[str] = Field(default_factory=list)
    customSummary: str | None = Field(default=None)
    includePhoto: bool = Field(default=True)
    includeSummary: bool = Field(default=True)


class CvVersionResponse(BaseModel):
    """Full CV version representation. ``pdfUrl`` is null until Phase 5's follow-up
    (PDF render pipeline) actually generates one."""

    id: str = Field(alias="id", serialization_alias="id")
    profileId: str = Field(alias="profile_id", serialization_alias="profileId")
    name: str = Field(alias="name", serialization_alias="name")
    template: str = Field(alias="template", serialization_alias="template")
    sectionsConfig: CvSectionsConfig = Field(default_factory=CvSectionsConfig, alias="sections_config", serialization_alias="sectionsConfig")
    pdfUrl: str | None = Field(None, alias="pdf_url", serialization_alias="pdfUrl")
    isDefault: bool = Field(alias="is_default", serialization_alias="isDefault")
    createdAt: datetime = Field(alias="created_at", serialization_alias="createdAt")
    updatedAt: datetime = Field(alias="updated_at", serialization_alias="updatedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CreateCvVersionRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    template: str = Field(default="default", max_length=50)
    sectionsConfig: CvSectionsConfig = Field(default_factory=CvSectionsConfig)
    isDefault: bool = Field(default=False)


class UpdateCvVersionRequest(BaseModel):
    """Partial update — only provided fields change. ``sectionsConfig``, when
    provided, fully replaces the existing selection."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    template: str | None = Field(default=None, max_length=50)
    sectionsConfig: CvSectionsConfig | None = Field(default=None)
    isDefault: bool | None = Field(default=None)


class GenerateCvVersionResponse(BaseModel):
    """Result of a PDF generation request. Rendering is synchronous (WeasyPrint
    is fast for CV-sized documents), so the normal outcome is ``completed`` with
    the PDF stored and downloadable; ``queued`` is kept in the contract for a
    future move to a background job without breaking clients."""

    jobId: str
    status: Literal["queued", "completed"]
    watermark: bool = Field(description="Whether the PDF carries a watermark, per the requester's subscription tier (Free tier only)")
    pdfUrl: str | None = Field(default=None, description="Storage path of the rendered PDF once completed — download via the download endpoint, not directly")


# --- Career overview (dashboard) -------------------------------------------------


class CareerSectionCounts(BaseModel):
    """Item counts per career section — powers the dashboard cards."""

    experiences: int = 0
    projects: int = 0
    skills: int = 0
    education: int = 0
    certifications: int = 0
    achievements: int = 0
    languages: int = 0
    cvVersions: int = 0


class CareerOverviewResponse(BaseModel):
    """One-call dashboard summary: profile essentials, per-section counts, an
    overall completeness score that (unlike ``profiles.completeness_score``)
    also weighs in section contents, and prioritized next-step suggestion keys
    the frontend translates."""

    slug: str
    headline: str | None = None
    visibility: ProfileVisibility
    profileCompleteness: int = Field(description="Profile-table-only score (0-100), as stored")
    completenessScore: int = Field(description="Overall score (0-100): profile fields + section contents")
    counts: CareerSectionCounts
    suggestions: list[str] = Field(default_factory=list, description="Ordered i18n suggestion keys, most impactful first")
