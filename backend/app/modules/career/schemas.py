"""Pydantic schemas for the career module (Phase 1: profile endpoints)."""

from datetime import datetime
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
    visibility: ProfileVisibility = Field(
        alias="visibility", serialization_alias="visibility"
    )
    contact: ContactInfo = Field(
        default_factory=ContactInfo, alias="contact", serialization_alias="contact"
    )
    draftData: dict[str, Any] = Field(
        default_factory=dict, alias="draft_data", serialization_alias="draftData"
    )
    profilePhotoUrl: str | None = Field(
        None, alias="profile_photo_url", serialization_alias="profilePhotoUrl"
    )
    completenessScore: int = Field(
        alias="completeness_score", serialization_alias="completenessScore"
    )
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
    profilePhotoUrl: str | None = Field(
        None, alias="profile_photo_url", serialization_alias="profilePhotoUrl"
    )

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
