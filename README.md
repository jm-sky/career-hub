# CareerHub - Professional Profile Management Platform

## 🎯 Project Overview

CareerHub is a professional profile management platform designed specifically for senior professionals (10+ years experience) to maintain a comprehensive, configurable career profile and generate tailored CVs.

## 🚀 Key Features

### Core Functionality (MVP)
- **Rich Professional Profile** - Central repository for all career data
- **LinkedIn Import** - Quick profile setup via LinkedIn data import  
- **CV Generator** - Create multiple CV versions from single source of truth
- **Public Profile** - Share professional profile with custom URL
- **Draft System** - Save progress during profile creation wizard

### Target Audience
Primary: Senior professionals (10+ years experience) who need to:
- Manage extensive career history
- Generate tailored CVs for different opportunities
- Maintain detailed project portfolios
- Track and showcase diverse skill sets

## 💰 Business Model

**Freemium** with three tiers:

| Plan   | Price (PLN/month) | Features |
|--------|-------------------|----------|
| FREE   | 0                 | • Rich profile<br>• Basic public profile<br>• 2 CV versions<br>• PDF export (watermark)<br>• LinkedIn import |
| PRO    | 19                | • Everything in FREE<br>• Unlimited CV versions<br>• No watermark<br>• One-pager generator<br>• Basic AI suggestions<br>• Advanced privacy controls |
| EXPERT | 50                | • Everything in PRO<br>• Deep AI analysis<br>• Custom domain<br>• API access<br>• Priority support<br>• Backup & versioning |

## 🏗️ Technical Stack

### Frontend
- **Framework:** Next.js 15 (App Router)
- **UI:** Tailwind CSS v4 + shadcn/ui
- **State:** TanStack Query + Zustand
- **Forms:** React Hook Form + Zod
- **Language:** TypeScript

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL 15+
- **ORM:** SQLAlchemy + Alembic
- **Cache:** Redis
- **Queue:** Celery + Redis
- **Storage:** S3-compatible (MinIO/AWS)

### Infrastructure
- **IDs:** ULID (sortable, time-based)
- **Auth:** JWT + Refresh tokens
- **Storage:** S3-compatible (MinIO/AWS S3)
- **Package Manager:** pnpm (frontend)
- **AI:** OpenAI API / Anthropic Claude
- **PDF:** WeasyPrint / ReportLab

## 📁 Project Structure

```
career-hub/
├── frontend/              # Next.js application
│   ├── app/              # App router pages
│   ├── components/       # React components
│   ├── lib/             # Utilities
│   └── public/          # Static assets
│
├── backend/              # FastAPI application
│   ├── api/             # API endpoints
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic
│   ├── schemas/         # Pydantic schemas
│   └── core/            # Config, security
│
├── docs/                # Documentation
│   ├── README.md
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── API.md
│   └── IMPLEMENTATION.md
│
└── docker/              # Docker configurations
    ├── docker-compose.yml
    └── Dockerfile
```

## 🚀 Quick Start

For detailed development environment setup, see **[SETUP.md](docs/SETUP.md)**.

**TL;DR:**
```bash
# Automated setup
chmod +x scripts/setup.sh && ./scripts/setup.sh

# Manual setup
docker-compose up -d  # Start services
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
cd frontend && pnpm dev
```

## 📊 MVP Scope

### Phase 1 (Months 1-3)
- [ ] User authentication & authorization
- [ ] Profile wizard with draft saving
- [ ] Full CRUD for all profile sections
- [ ] LinkedIn import functionality
- [ ] CV generation (1 template)
- [ ] PDF export
- [ ] Basic public profile

### Phase 2 (Months 4-5)
- [ ] AI-powered description optimization
- [ ] Multiple CV templates
- [ ] Enhanced public profile
- [ ] CV versioning
- [ ] Recommendations system

### Phase 3 (Future)
- [ ] One-pager generator
- [ ] Deep AI career analysis
- [ ] Friends/network system
- [ ] API access
- [ ] Advanced integrations

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📄 License

[MIT](LICENSE)

## 📞 Contact

For questions about the project, please contact jan.madeyski@gmail.com