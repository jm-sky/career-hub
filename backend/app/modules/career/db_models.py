"""Database models for the career module (Phase 1: profiles. Phase 2: experiences,
technologies, skills. Phase 3: projects. Phase 4: education, certifications,
achievements. Phase 5: cv_versions)."""

from datetime import UTC, date, datetime
from datetime import date as _Date

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProfileDB(Base):
    """A user's professional profile — 1:1 with users.id.

    Anchor table for the career module: experiences/projects/skills/education/
    certifications/achievements/cv_versions (Phase 2+) all belong to a profile.
    """

    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    headline: Mapped[str | None] = mapped_column(String(200), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(120), nullable=True)
    visibility: Mapped[str] = mapped_column(String(10), nullable=False, default="PRIVATE")
    # Shape: {email?, phone?, linkedin?, website?}
    contact: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # Wizard-in-progress storage, keyed by step name: {stepName: {...}}
    draft_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    profile_photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    completeness_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class TechnologyDB(Base):
    """A global, de-duplicated reference to a technology/tool/skill name.

    Shared across all profiles' experiences/skills — not owned by any one profile.
    """

    __tablename__ = "technologies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    layer: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class ExperienceDB(Base):
    """A profile's work experience entry."""

    __tablename__ = "experiences"
    __table_args__ = (CheckConstraint("end_date IS NULL OR end_date > start_date", name="ck_experiences_end_after_start"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    employment_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(default=False, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsibilities: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class ExperienceTechnologyDB(Base):
    """M:N junction between experiences and technologies.

    ``experience_id`` cascades on delete — removing an experience should drop its
    junction rows automatically. ``technology_id`` does not — technologies are
    shared reference data, never deleted as a side effect of unlinking one experience.
    """

    __tablename__ = "experience_technologies"

    experience_id: Mapped[str] = mapped_column(String(36), ForeignKey("experiences.id", ondelete="CASCADE"), primary_key=True)
    technology_id: Mapped[str] = mapped_column(String(36), ForeignKey("technologies.id"), primary_key=True)


class ProjectDB(Base):
    """A profile's portfolio project — documented independently of any one experience,
    then optionally linked to the experience(s) and technologies it came from.

    ``is_anonymized``/``anonymized_company`` is a deliberately separate concern from
    ``visibility``: an NDA-restricted project can still be shown publicly with the
    company name redacted, which is not the same thing as hiding the project entirely.
    """

    __tablename__ = "projects"
    __table_args__ = (CheckConstraint("end_date IS NULL OR end_date > start_date", name="ck_projects_end_after_start"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    role: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_anonymized: Mapped[bool] = mapped_column(default=False, nullable=False)
    anonymized_company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ACTIVE")
    category: Mapped[str | None] = mapped_column(String(20), nullable=True)
    achievements: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    challenges: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    clients: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # Colleague names who worked on the project (issue 001)
    team: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # Shape: [{name, url?}] — client sites/instances of a template project (issue 001)
    sub_projects: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    team_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    users_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    budget_range: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # Shape: {demo?, github?, docs?}
    links: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    visibility: Mapped[str] = mapped_column(String(10), nullable=False, default="PRIVATE")
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class ProjectExperienceDB(Base):
    """M:N junction between projects and experiences — both sides are profile-owned,
    deletable entities, so both cascade on delete (unlike *_technologies junctions,
    where the technology side is shared reference data and never cascades)."""

    __tablename__ = "project_experiences"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    experience_id: Mapped[str] = mapped_column(String(36), ForeignKey("experiences.id", ondelete="CASCADE"), primary_key=True)


class ProjectTechnologyDB(Base):
    """M:N junction between projects and technologies. ``project_id`` cascades on
    delete; ``technology_id`` does not (shared reference data)."""

    __tablename__ = "project_technologies"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    technology_id: Mapped[str] = mapped_column(String(36), ForeignKey("technologies.id"), primary_key=True)


class SkillDB(Base):
    """A profile's self-rated proficiency in a technology.

    Unique per (profile_id, technology_id) — a profile has at most one skill
    entry per technology.
    """

    __tablename__ = "skills"
    __table_args__ = (
        UniqueConstraint("profile_id", "technology_id", name="uq_skills_profile_technology"),
        CheckConstraint("level >= 1 AND level <= 5", name="ck_skills_level_range"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    technology_id: Mapped[str] = mapped_column(String(36), ForeignKey("technologies.id"), nullable=False, index=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    years_of_experience: Mapped[float | None] = mapped_column(Float, nullable=True)
    started_using_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_primary: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class EducationDB(Base):
    """A profile's education entry. Nullable ``end_date`` means "still studying" —
    same convention as experiences, no separate is-ongoing flag needed."""

    __tablename__ = "education"
    __table_args__ = (CheckConstraint("end_date IS NULL OR end_date > start_date", name="ck_education_end_after_start"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    institution: Mapped[str] = mapped_column(String(200), nullable=False)
    degree: Mapped[str] = mapped_column(String(200), nullable=False)
    field_of_study: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    grade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class CertificationDB(Base):
    """A profile's certification. ``is_expired`` is deliberately not a DB column —
    computed at the service/response layer instead, so it's always correct relative
    to "now" without needing a scheduled job or DB-specific generated column."""

    __tablename__ = "certifications"
    __table_args__ = (CheckConstraint("expiry_date IS NULL OR expiry_date > issue_date", name="ck_certifications_expiry_after_issue"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    issuing_organization: Mapped[str] = mapped_column(String(200), nullable=False)
    credential_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    credential_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class AchievementDB(Base):
    """A profile's standalone achievement (award, publication, speaking engagement, ...)."""

    __tablename__ = "achievements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Annotated as `_Date`, not `date` — a column literally named `date` self-shadows
    # the `date` type mid-statement (the value binds to the name before its own
    # annotation is evaluated). Harmless here only because `MappedColumn` happens to
    # define `__or__` (for SQL OR-expressions); Pydantic's `FieldInfo` does not, which
    # is exactly what turned the same pattern into a hard crash in schemas.py.
    date: Mapped[_Date | None] = mapped_column(Date, nullable=True)
    category: Mapped[str | None] = mapped_column(String(20), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class LanguageDB(Base):
    """A spoken/written language on a profile, with a CEFR (or native) proficiency level."""

    __tablename__ = "languages"
    __table_args__ = (UniqueConstraint("profile_id", "name", name="uq_languages_profile_name"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class CvVersionDB(Base):
    """A named, curated selection of a profile's data for CV export.

    ``sections_config`` holds the actual curation (which experience/project/skill/
    education/certification/achievement/language ids to include, plus summary/photo overrides)
    as JSONB rather than relational rows — it's a snapshot of *which ids to select at
    render time*, not a copy of the underlying data, so it stays accurate as the
    profile changes.

    ``pdf_url`` is null until a PDF has actually been generated — Phase 5 ships CRUD
    only; the render pipeline (PDF engine choice still open) lands in a later pass.
    """

    __tablename__ = "cv_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    profile_id: Mapped[str] = mapped_column(String(36), ForeignKey("profiles.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    template: Mapped[str] = mapped_column(String(50), nullable=False, default="default")
    accent_color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    sections_config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    pdf_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
