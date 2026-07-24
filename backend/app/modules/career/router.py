"""API router for the career module — aggregates the per-entity sub-routers.

Split out once Phase 2 added experiences/technologies/skills alongside the
Phase 1 profile endpoints; keeps each entity's endpoints in its own file as the
module keeps growing (projects, education, cv_versions, ... in later phases).
"""

from fastapi import APIRouter

from .achievement_router import router as achievement_router
from .ai_router import router as ai_router
from .certification_router import router as certification_router
from .cv_version_router import router as cv_version_router
from .education_router import router as education_router
from .experience_router import router as experience_router
from .language_router import router as language_router
from .profile_router import router as profile_router
from .project_router import router as project_router
from .skill_router import router as skill_router
from .technology_router import router as technology_router

router = APIRouter()
router.include_router(profile_router)
router.include_router(experience_router)
router.include_router(technology_router)
router.include_router(skill_router)
router.include_router(project_router)
router.include_router(education_router)
router.include_router(certification_router)
router.include_router(achievement_router)
router.include_router(language_router)
router.include_router(cv_version_router)
router.include_router(ai_router)
