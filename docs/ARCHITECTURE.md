# Technical Architecture Document

## 1. Architecture Overview

### High-Level Architecture
```
┌─────────────────────────────────────────┐
│           FRONTEND (SPA)                │
│         Next.js + React                  │
└────────────────┬────────────────────────┘
                 │ HTTPS/REST
┌────────────────▼────────────────────────┐
│           API GATEWAY                   │
│         FastAPI + Nginx                 │
├─────────────────────────────────────────┤
│           BACKEND SERVICES              │
│         FastAPI + Python                │
│  ┌────────────┐  ┌──────────────┐      │
│  │   Auth     │  │   Profile    │      │
│  │  Service   │  │   Service    │      │
│  └────────────┘  └──────────────┘      │
│  ┌────────────┐  ┌──────────────┐      │
│  │    CV      │  │   Import     │      │
│  │ Generator  │  │   Service    │      │
│  └────────────┘  └──────────────┘      │
│  ┌────────────┐  ┌──────────────┐      │
│  │    AI      │  │   Export     │      │
│  │  Service   │  │   Service    │      │
│  └────────────┘  └──────────────┘      │
└────────────────┬────────────────────────┘
                 │
    ┌────────────▼──────────┐
    │     PostgreSQL        │
    │   (Primary DB)        │
    └───────────────────────┘
    ┌───────────────────────┐
    │      Redis            │
    │  (Cache & Queue)      │
    └───────────────────────┘
    ┌───────────────────────┐
    │    S3 / MinIO         │
    │   (File Storage)      │
    └───────────────────────┘
```

### Architecture Principles
1. **API-First Design** - Backend and frontend completely decoupled
2. **Monolith First** - Start with modular monolith, prepare for microservices
3. **Database Per Service** - Logical separation, physical separation later
4. **Event-Driven** - Use events for async operations
5. **Cache Everything** - Redis for performance
6. **Security by Default** - Auth, encryption, validation everywhere

## 2. Technology Stack

### Frontend Stack
```yaml
Core:
  - Framework: Next.js 14 (App Router)
  - Language: TypeScript 5.x
  - Runtime: Node.js 20 LTS

UI & Styling:
  - CSS Framework: Tailwind CSS 3.x
  - Component Library: shadcn/ui
  - Icons: Lucide React
  - Animations: Framer Motion

State & Data:
  - Server State: TanStack Query v5
  - Client State: Zustand
  - Forms: React Hook Form + Zod
  - Router: Next.js App Router

Development:
  - Build Tool: Turbo (if monorepo)
  - Linting: ESLint + Prettier
  - Testing: Vitest + Testing Library
```

### Backend Stack
```yaml
Core:
  - Framework: FastAPI 0.104+
  - Language: Python 3.11+
  - ASGI Server: Uvicorn + Gunicorn

Database:
  - Primary: PostgreSQL 15+
  - ORM: SQLAlchemy 2.0
  - Migrations: Alembic
  - Cache: Redis 7+

Security:
  - Authentication: JWT (PyJWT)
  - Password Hashing: Passlib + bcrypt
  - CORS: FastAPI middleware
  - Rate Limiting: slowapi

AI & Processing:
  - AI SDK: OpenAI Python SDK / Anthropic SDK
  - PDF Generation: WeasyPrint / ReportLab
  - Task Queue: Celery + Redis
  - File Processing: Python-Multipart

Development:
  - Type Checking: Pydantic v2
  - Testing: Pytest + Pytest-asyncio
  - Linting: Ruff + Black
  - API Docs: FastAPI built-in (Swagger/ReDoc)
```

### Infrastructure
```yaml
Deployment:
  - Containerization: Docker + Docker Compose
  - Orchestration: Kubernetes (future)
  - CI/CD: GitHub Actions
  - Hosting: AWS/GCP/DigitalOcean

Monitoring:
  - APM: Sentry
  - Logs: ELK Stack / CloudWatch
  - Metrics: Prometheus + Grafana
  - Uptime: UptimeRobot / Pingdom

Storage:
  - Object Storage: S3 / MinIO
  - CDN: CloudFlare / CloudFront
  - Backups: Automated daily
```

## 3. Key Design Decisions

### ID Generation Strategy
**Decision: Use ULID instead of UUID**
```python
# Why ULID?
- Lexicographically sortable
- Timestamp embedded
- Shorter than UUID
- Better index performance

from ulid import ULID
user_id = str(ULID())  # 01ARZ3NDEKTSV4RRFFQ69G5FAV
```

### Authentication Strategy
**Decision: JWT with Refresh Tokens**
```python
# Token Structure
access_token: 15 minutes TTL
refresh_token: 30 days TTL
storage: httpOnly cookies + localStorage (access only)

# Security measures
- Token rotation on refresh
- Blacklist for logout
- Rate limiting on auth endpoints
- Account lockout after failed attempts
```

### Data Storage Strategy
```python
# Structured Data: PostgreSQL
- User profiles
- Experiences, projects
- Relationships

# Cache Layer: Redis
- Session data
- Public profiles (TTL: 1h)
- PDF cache (TTL: 7d)
- API rate limiting

# File Storage: S3/MinIO
- Generated PDFs
- Profile images
- Export archives
```

### AI Integration Pattern
```python
# Abstract AI Provider
from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    async def optimize_text(self, text: str) -> str:
        pass
    
    @abstractmethod
    async def suggest_skills(self, role: str) -> List[str]:
        pass

class OpenAIProvider(AIProvider):
    # Implementation
    pass

class AnthropicProvider(AIProvider):
    # Implementation
    pass

# Usage with dependency injection
ai_provider = get_ai_provider()  # Based on config
```

### Responsibilities Storage
**Decision: JSONB Array in PostgreSQL**
```sql
-- Simple, flexible, performant for our use case
CREATE TABLE experiences (
    id TEXT PRIMARY KEY,
    responsibilities JSONB DEFAULT '[]'::jsonb,
    -- Create GIN index for search
    CREATE INDEX idx_responsibilities ON experiences 
    USING gin(responsibilities);
);
```

## 4. Service Architecture

### Service Boundaries
```python
# Auth Service
- User registration/login
- Token management
- Password reset
- Session management

# Profile Service
- Profile CRUD
- Experience management
- Skills management
- Education/achievements

# Project Service
- Project CRUD
- Project-Experience relations
- Project-Skill relations
- Anonymization logic

# CV Service
- CV version management
- Template selection
- Section configuration
- Generation orchestration

# Import Service
- LinkedIn parsing
- Data mapping
- Conflict resolution
- Batch imports

# Export Service
- PDF generation
- JSON export
- Public profile rendering
- One-pager generation

# AI Service
- Text optimization
- Skill suggestions
- Gap analysis
- Summary generation
```

### API Design Principles
```python
# RESTful with consistent patterns
GET    /api/v1/profiles/{id}      # Get single
GET    /api/v1/profiles           # List with pagination
POST   /api/v1/profiles           # Create
PUT    /api/v1/profiles/{id}      # Full update
PATCH  /api/v1/profiles/{id}      # Partial update
DELETE /api/v1/profiles/{id}      # Delete

# Consistent error responses
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": [
            {
                "field": "email",
                "message": "Invalid email format"
            }
        ]
    }
}

# Pagination
GET /api/v1/experiences?page=1&size=20&sort=start_date:desc
{
    "data": [...],
    "pagination": {
        "page": 1,
        "size": 20,
        "total": 45,
        "pages": 3
    }
}
```

## 5. Database Design Principles

### Normalization Strategy
- 3NF for core entities
- Denormalization for read-heavy data
- JSONB for flexible/evolving data

### Indexing Strategy
```sql
-- Primary keys use ULID
-- Foreign key indexes
-- Composite indexes for common queries
CREATE INDEX idx_experiences_profile_dates 
ON experiences(profile_id, start_date DESC);

-- Partial indexes for filtered queries
CREATE INDEX idx_public_profiles 
ON profiles(slug) 
WHERE visibility = 'PUBLIC';

-- Full-text search
CREATE INDEX idx_projects_search 
ON projects 
USING gin(to_tsvector('english', name || ' ' || description));
```

### Data Integrity
```python
# Application-level constraints
- Business logic validation in services
- Pydantic models for type safety
- Database constraints as last defense

# Database-level constraints
- Foreign key constraints with CASCADE
- Check constraints for enums
- Unique constraints for business keys
```

## 6. Security Architecture

### Defense in Depth
```
1. Network Level
   - HTTPS only
   - Rate limiting
   - DDoS protection (CloudFlare)

2. Application Level
   - Input validation (Pydantic)
   - SQL injection prevention (ORM)
   - XSS prevention (React)
   - CSRF tokens

3. Data Level
   - Encryption at rest
   - Encryption in transit
   - PII data masking
   - Secure password storage

4. Access Control
   - JWT authentication
   - Role-based access (future)
   - Resource-level permissions
   - API key management (Expert tier)
```

### Privacy & Compliance
```python
# GDPR Compliance
- Right to be forgotten (data deletion)
- Data portability (JSON export)
- Consent management
- Privacy policy versioning

# Data Retention
- Active accounts: Indefinite
- Inactive accounts: 2 years
- Deleted accounts: 30 days soft delete
- Logs: 90 days
```

## 7. Performance Optimization

### Caching Strategy
```python
# Cache Layers
1. Browser Cache
   - Static assets: 1 year
   - API responses: varies

2. CDN Cache (CloudFlare)
   - Static files
   - Public profiles

3. Application Cache (Redis)
   - Session data: 24h
   - Public profiles: 1h
   - Generated PDFs: 7d
   - AI suggestions: 24h

4. Database Cache
   - Query result cache
   - Prepared statements
```

### Query Optimization
```python
# N+1 Prevention
- Eager loading with SQLAlchemy
- DataLoader pattern for GraphQL (future)
- Batch operations where possible

# Pagination
- Cursor-based for infinite scroll
- Offset-based for page navigation
- Limit max page size to 100
```

### Async Processing
```python
# Background Jobs (Celery)
- PDF generation
- Email sending
- Import processing
- AI analysis
- Data exports

# Event-Driven Updates
- Profile completeness calculation
- Cache invalidation
- Search index updates
```

## 8. Development Workflow

### Git Strategy
```bash
main           # Production-ready code
├── develop    # Integration branch
    ├── feature/profile-wizard
    ├── feature/linkedin-import
    └── fix/pdf-generation

# Commit convention
feat: Add LinkedIn import
fix: Resolve PDF generation timeout
docs: Update API documentation
chore: Update dependencies
```

### Environment Management
```yaml
Development:
  - Local PostgreSQL + Redis
  - MinIO for S3
  - Mock AI responses
  - Hot reload

Staging:
  - Production-like environment
  - Real AI integration
  - Full monitoring
  - Load testing

Production:
  - High availability
  - Auto-scaling
  - Full monitoring
  - Automated backups
```

## 9. Testing Strategy

### Testing Pyramid
```
         /\
        /  \    E2E Tests (10%)
       /----\   - Critical user journeys
      /      \  Integration Tests (30%)
     /--------\ - API endpoints, DB queries
    /          \Unit Tests (60%)
   /____________\- Business logic, utilities
```

### Test Coverage Goals
- Overall: 80%
- Critical paths: 95%
- AI integrations: Mocked in tests
- Performance tests: Load testing with k6

## 10. Scalability Plan

### Horizontal Scaling Path
```
Phase 1 (MVP): Single server
- 1 server (4 CPU, 8GB RAM)
- PostgreSQL on same server
- Local Redis

Phase 2 (Growth): Separated services
- 2 app servers (load balanced)
- Dedicated DB server
- Managed Redis

Phase 3 (Scale): Microservices
- Service mesh (Istio)
- Kubernetes orchestration
- Multi-region deployment
```

### Database Scaling
```
1. Vertical scaling (bigger server)
2. Read replicas
3. Connection pooling (PgBouncer)
4. Partitioning by user_id
5. Sharding (if needed)
```

## 11. Monitoring & Observability

### Key Metrics
```yaml
Business Metrics:
  - User registrations
  - Profile completion rate
  - CV generations
  - Conversion to paid

Technical Metrics:
  - API response time (p50, p95, p99)
  - Error rate
  - Database query time
  - Cache hit rate
  - Background job success rate

Infrastructure Metrics:
  - CPU/Memory usage
  - Disk I/O
  - Network throughput
  - Container health
```

### Alerting Rules
- API response time > 2s
- Error rate > 1%
- Database CPU > 80%
- Disk space < 20%
- Failed logins spike

## 12. Disaster Recovery

### Backup Strategy
- Database: Daily automated backups, 30-day retention
- Files: S3 versioning enabled
- Code: Git repository
- Configuration: Encrypted in vault

### RTO/RPO Targets
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 24 hours

### Incident Response
1. Alert triggered
2. On-call engineer notified
3. Assess severity
4. Execute runbook
5. Post-mortem