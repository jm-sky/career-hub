"""CareerHub API - Professional Profile Management Platform."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1 import api_router
from app.core.config import settings
from app.core.exceptions import AuthenticationError, authentication_exception_handler
from app.core.rate_limit import limiter, rate_limit_handler

# Create FastAPI application
app = FastAPI(
    title=settings.app.name,
    description="Professional Profile Management Platform",
    version=settings.app.version,
    debug=settings.app.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.server.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting state
app.state.limiter = limiter

# Register exception handlers
app.add_exception_handler(AuthenticationError, authentication_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Welcome to CareerHub API",
        "version": settings.app.version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.app.environment,
        "version": settings.app.version
    }
