"""Business logic for the career module (Phase 1: profiles)."""

import re
import secrets
from typing import cast

from app.common.id_utils import generate_id

from .db_models import ProfileDB
from .repository import ProfileRepository
from .schemas import (
    CareerOverviewResponse,
    CareerSectionCounts,
    ProfileDraftRequest,
    ProfileVisibility,
    UpdateProfileRequest,
)


def slugify(value: str) -> str:
    """Turn a display name into a URL-safe, lowercase, hyphenated slug."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "user"


def compute_completeness_score(profile: ProfileDB) -> int:
    """Weighted completeness score over Phase 1 profile-level fields only.

    NOTE: once experiences/projects/skills/education (Phase 2+) exist, this must be
    extended to weigh in section counts (e.g. "has at least one experience", "has at
    least 3 skills") — right now it can only see what's on the profiles table itself.
    """
    weights = {
        "headline": 20,
        "summary": 25,
        "location": 15,
        "contact": 20,
        "profile_photo_url": 20,
    }
    score = 0
    if profile.headline:
        score += weights["headline"]
    if profile.summary:
        score += weights["summary"]
    if profile.location:
        score += weights["location"]
    if profile.contact and any(profile.contact.get(k) for k in ("email", "phone", "linkedin", "website")):
        score += weights["contact"]
    if profile.profile_photo_url:
        score += weights["profile_photo_url"]
    return score


def compute_overall_completeness(profile_score: int, counts: dict[str, int]) -> int:
    """Overall completeness (0-100): profile-table fields count for half, the
    other half comes from actually having career content in the sections.

    This intentionally lives outside the stored ``profiles.completeness_score``
    (which is recomputed only on profile writes and can't see other tables) —
    section counts change on every section CRUD, so the combined score is
    derived per-read instead of persisted.
    """
    section_points = 0
    if counts.get("experiences", 0) >= 1:
        section_points += 15
    skills = counts.get("skills", 0)
    if skills >= 3:
        section_points += 10
    elif skills >= 1:
        section_points += 5
    if counts.get("projects", 0) >= 1:
        section_points += 10
    if counts.get("education", 0) >= 1:
        section_points += 5
    if counts.get("languages", 0) >= 1:
        section_points += 5
    if counts.get("cvVersions", 0) >= 1:
        section_points += 5
    return round(profile_score / 2) + section_points


def build_suggestions(profile: ProfileDB, counts: dict[str, int], limit: int = 4) -> list[str]:
    """Prioritized next-step suggestion keys (most impactful first) for the
    dashboard. Values are i18n keys under ``career.overview.suggestions.*``."""
    candidates: list[tuple[bool, str]] = [
        (not profile.headline, "addHeadline"),
        (counts.get("experiences", 0) == 0, "addExperience"),
        (not profile.summary, "addSummary"),
        (counts.get("skills", 0) < 3, "addSkills"),
        (counts.get("projects", 0) == 0, "addProject"),
        (counts.get("education", 0) == 0, "addEducation"),
        (counts.get("languages", 0) == 0, "addLanguage"),
        (counts.get("cvVersions", 0) == 0, "createCv"),
        (not profile.profile_photo_url, "addPhoto"),
        (profile.visibility != "PUBLIC", "makePublic"),
    ]
    return [key for applies, key in candidates if applies][:limit]


class ProfileService:
    """Business logic for profile CRUD, draft autosave, and public visibility."""

    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    async def _generate_unique_slug(self, base_name: str) -> str:
        base = slugify(base_name)
        candidate = base
        while await self.repository.slug_exists(candidate):
            candidate = f"{base}-{secrets.token_hex(3)}"
        return candidate

    async def get_or_create_for_user(self, user_id: str, user_name: str) -> ProfileDB:
        """Return the user's profile, auto-creating an empty one on first access."""
        profile = await self.repository.get_by_user_id(user_id)
        if profile is not None:
            return profile

        slug = await self._generate_unique_slug(user_name)
        profile = ProfileDB(
            id=generate_id(),
            user_id=user_id,
            slug=slug,
            visibility="PRIVATE",
            contact={},
            draft_data={},
            completeness_score=0,
        )
        return await self.repository.create(profile)

    async def update_profile(self, profile: ProfileDB, payload: UpdateProfileRequest) -> ProfileDB:
        """Apply a partial update, then recompute the completeness score."""
        if payload.headline is not None:
            profile.headline = payload.headline
        if payload.summary is not None:
            profile.summary = payload.summary
        if payload.location is not None:
            profile.location = payload.location
        if payload.visibility is not None:
            profile.visibility = payload.visibility
        if payload.contact is not None:
            profile.contact = payload.contact.model_dump(exclude_none=True)
        if payload.profilePhotoUrl is not None:
            profile.profile_photo_url = payload.profilePhotoUrl
        if payload.slug is not None and payload.slug != profile.slug:
            new_slug = slugify(payload.slug)
            if await self.repository.slug_exists(new_slug):
                raise ValueError(f"Slug '{new_slug}' is already taken.")
            profile.slug = new_slug

        profile.completeness_score = compute_completeness_score(profile)
        return await self.repository.save(profile)

    async def save_draft(self, profile: ProfileDB, payload: ProfileDraftRequest) -> ProfileDB:
        """Step-scoped autosave — merges into draft_data[step], leaves other steps intact."""
        draft = dict(profile.draft_data or {})
        draft[payload.step] = payload.data
        profile.draft_data = draft
        return await self.repository.save(profile)

    async def get_overview(self, profile: ProfileDB) -> CareerOverviewResponse:
        """One-call dashboard summary: counts, overall completeness, suggestions."""
        counts = await self.repository.count_sections(profile.id)
        return CareerOverviewResponse(
            slug=profile.slug,
            headline=profile.headline,
            visibility=cast(ProfileVisibility, profile.visibility),
            profileCompleteness=profile.completeness_score,
            completenessScore=compute_overall_completeness(profile.completeness_score, counts),
            counts=CareerSectionCounts(**counts),
            suggestions=build_suggestions(profile, counts),
        )

    async def get_public_profile(self, slug: str, viewer_user_id: str | None) -> ProfileDB | None:
        """Return a profile for public/slug-based viewing, applying visibility rules.

        - PUBLIC: visible to anyone.
        - PRIVATE: visible only to the owner.
        - FRIENDS: no friends/connections system exists yet (Phase 1) — treated
          identically to PRIVATE (owner-only) until that's built.
        """
        profile = await self.repository.get_by_slug(slug)
        if profile is None:
            return None

        is_owner = viewer_user_id is not None and viewer_user_id == profile.user_id
        if profile.visibility == "PUBLIC" or is_owner:
            return profile
        return None
