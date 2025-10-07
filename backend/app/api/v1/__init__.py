"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1 import auth, profiles, experiences

# Create main API v1 router
api_router = APIRouter()

# Include all v1 sub-routers
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(profiles.router, tags=["profiles"])
api_router.include_router(experiences.router, tags=["experiences"])
