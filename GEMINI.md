# GEMINI.md

This file provides guidance to Gemini when working with code in this repository.

## Development Commands

### Backend (FastAPI)
```bash
# Development server
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Code quality
black .
ruff check . --fix
mypy .

# Testing
pytest
pytest -v tests/specific_test.py
pytest --cov=app

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "Description"
```

### Frontend (Next.js)
```bash
# Development server
cd frontend
pnpm dev

# Build and type checking
pnpm build
pnpm run type-check
```

### Services
```bash
# Start all services (PostgreSQL, Redis, MinIO)
docker-compose up -d

# Individual services
docker-compose up -d db redis minio

# Logs and cleanup
docker-compose logs -f
docker-compose down
```

## Architecture Overview

### Tech Stack
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL + Redis + MinIO
- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS v4 + shadcn/ui
- **State**: TanStack Query (server) + Zustand (client)
- **Forms**: React Hook Form + Zod validation
- **IDs**: ULID (lexicographically sortable)

### Service Architecture
The backend follows a service layer pattern with clear boundaries:

```
Auth Service      → User management, JWT tokens, sessions
Profile Service   → Core profile data, experiences, skills
Project Service   → Project management and relationships
CV Service        → CV generation, templates, versions
Import Service    → LinkedIn data import and mapping
Export Service    → PDF generation, public profiles
AI Service        → Text optimization, suggestions
```

### Key Design Patterns
- **API-First**: Complete frontend/backend decoupling via REST APIs
- **Service Layer**: Business logic isolated in service classes
- **Repository Pattern**: Data access through SQLAlchemy models
- **Component Architecture**: Reusable UI with shadcn/ui components
- **Event-Driven**: Async processing with Celery + Redis

### Database Strategy
- **Primary Storage**: PostgreSQL with ULID primary keys
- **Flexible Data**: JSONB for responsibilities, configurations
- **Caching**: Redis for sessions, public profiles, generated PDFs
- **Files**: MinIO (S3-compatible) for uploads and generated documents
- **Search**: GIN indexes for JSONB full-text search

### Authentication Flow
- JWT access tokens (15min) + refresh tokens (30 days)
- Token rotation on refresh
- httpOnly cookies for refresh tokens
- Rate limiting on auth endpoints

### Performance Optimizations
- **Caching Layers**: Browser → CDN → Redis → Database
- **Query Optimization**: Eager loading, proper indexing, pagination
- **Background Jobs**: PDF generation, imports, AI processing via Celery

## Development Environment

### Quick Setup
```bash
# Automated setup
chmod +x scripts/setup.sh && ./scripts/setup.sh

# Manual setup
docker-compose up -d
cd backend && source .venv/bin/activate && pip install -r requirements.txt
cd frontend && pnpm install
```

### Environment Configuration
- **Backend**: `.env` (database, security, storage, AI API keys)
- **Frontend**: `.env.local` (API URLs, feature flags)

### Project Structure
```
backend/app/
├── api/v1/          # REST API endpoints
├── core/            # Configuration, database, security
├── models/          # SQLAlchemy database models
├── schemas/         # Pydantic request/response schemas
├── services/        # Business logic layer
└── middleware/      # Custom middleware

frontend/src/
├── app/             # Next.js App Router pages
├── components/ui/   # shadcn/ui base components
├── components/      # Feature components
└── lib/             # Utilities, hooks, API clients
```

## API Design

### RESTful Conventions
```
GET    /api/v1/profiles/{id}    # Single resource
GET    /api/v1/profiles         # List with pagination
POST   /api/v1/profiles         # Create
PUT    /api/v1/profiles/{id}    # Full update
PATCH  /api/v1/profiles/{id}    # Partial update
DELETE /api/v1/profiles/{id}    # Delete
```

### Response Patterns
- Consistent error format with RFC 7807 problem details
- Pagination with cursor-based (infinite scroll) or offset-based (pages)
- ISO 8601 timestamps with timezone information

## Testing Strategy

### Backend Testing
```bash
# Unit tests for services and models
pytest tests/unit/

# Integration tests for API endpoints
pytest tests/integration/

# Single test file or function
pytest tests/test_auth.py::test_login_success
```

### Test Database
- Separate test database automatically created/cleaned
- Fixtures for common test data
- AI services mocked in tests

## Business Model Context

CareerHub targets senior professionals (10+ years experience) with a freemium model:
- **FREE**: Basic profile, 2 CV versions, PDF with watermark
- **PRO** (19 PLN/month): Unlimited CVs, no watermark, AI suggestions
- **EXPERT** (50 PLN/month): Advanced AI, custom domain, API access

This context drives feature prioritization and user experience decisions.
- API responses should use camelCase
- API requests should expect camelCase params