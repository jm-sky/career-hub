"""Pydantic schemas for the career module (Phase 1: profile. Phase 2: experiences,
technologies, skills)."""

from datetime import date, datetime
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
