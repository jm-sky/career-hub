"""Unit tests for the career overview scoring/suggestion helpers (pure functions)."""

from app.modules.career.db_models import ProfileDB
from app.modules.career.service import build_suggestions, compute_overall_completeness


def make_profile(**overrides: object) -> ProfileDB:
    defaults: dict[str, object] = {
        "id": "01TESTPROFILE0000000000000",
        "user_id": "01TESTUSER000000000000000",
        "slug": "test-user",
        "visibility": "PRIVATE",
        "contact": {},
        "draft_data": {},
        "completeness_score": 0,
    }
    defaults.update(overrides)
    return ProfileDB(**defaults)


EMPTY_COUNTS = {
    "experiences": 0,
    "projects": 0,
    "skills": 0,
    "education": 0,
    "certifications": 0,
    "achievements": 0,
    "languages": 0,
    "cvVersions": 0,
}

FULL_COUNTS = {
    "experiences": 3,
    "projects": 2,
    "skills": 5,
    "education": 1,
    "certifications": 1,
    "achievements": 1,
    "languages": 2,
    "cvVersions": 1,
}


class TestComputeOverallCompleteness:
    def test_empty_profile_scores_zero(self) -> None:
        assert compute_overall_completeness(0, EMPTY_COUNTS) == 0

    def test_full_profile_scores_hundred(self) -> None:
        assert compute_overall_completeness(100, FULL_COUNTS) == 100

    def test_profile_fields_alone_cap_at_fifty(self) -> None:
        assert compute_overall_completeness(100, EMPTY_COUNTS) == 50

    def test_sections_alone_cap_at_fifty(self) -> None:
        assert compute_overall_completeness(0, FULL_COUNTS) == 50

    def test_partial_skills_score(self) -> None:
        one_skill = {**EMPTY_COUNTS, "skills": 1}
        three_skills = {**EMPTY_COUNTS, "skills": 3}
        assert compute_overall_completeness(0, one_skill) == 5
        assert compute_overall_completeness(0, three_skills) == 10


class TestBuildSuggestions:
    def test_empty_profile_gets_most_impactful_first(self) -> None:
        suggestions = build_suggestions(make_profile(), EMPTY_COUNTS)
        assert suggestions == ["addHeadline", "addExperience", "addSummary", "addSkills"]

    def test_limit_respected(self) -> None:
        assert len(build_suggestions(make_profile(), EMPTY_COUNTS, limit=2)) == 2

    def test_complete_public_profile_has_no_suggestions(self) -> None:
        profile = make_profile(
            headline="Senior Engineer",
            summary="A summary.",
            profile_photo_url="https://example.com/photo.jpg",
            visibility="PUBLIC",
        )
        assert build_suggestions(profile, FULL_COUNTS) == []

    def test_private_complete_profile_suggests_going_public(self) -> None:
        profile = make_profile(
            headline="Senior Engineer",
            summary="A summary.",
            profile_photo_url="https://example.com/photo.jpg",
        )
        assert build_suggestions(profile, FULL_COUNTS) == ["makePublic"]
