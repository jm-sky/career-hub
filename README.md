# CareerHub

A single professional profile that generates as many tailored CVs as you need — with LinkedIn import, curated CV versions, and AI-assisted content optimization.

## Overview

CareerHub is a full-stack application for building one master professional profile — experience, projects, skills, education, certifications, achievements — and generating multiple named CV versions from it, each a curated selection over the master data rather than a separate document. It's aimed at professionals who need to tailor their CV per application without maintaining N duplicate files by hand.

**Key Capabilities:**
- **Multi-User Platform** - Secure user accounts with authentication and authorization
- **Freemium Plans** - Free, Pro, and Expert tiers with Stripe payment integration
- **Curated CV Generation** - Named CV versions select which experiences, projects, skills, and education to include, with an optional custom summary override
- **Public Profile** - Shareable profile page at a unique slug with Private/Friends/Public visibility
- **Data Portability** - LinkedIn import, copy-paste text import fallback, full JSON export

> 📋 **[Zobacz pełną listę funkcjonalności w języku polskim →](./FEATURES.md)**

---

### Core Features
- Build one master profile: experience, projects, skills, education, certifications, achievements.
- Rich per-role experience data: company, position, employment type, dates, responsibilities, technologies.
- Projects documented independently of experiences, then explicitly linked to one or more experiences and skills.
- Anonymization for NDA-restricted work — hide the real company/client name behind a placeholder.
- Generate multiple named CV versions, each a curated selection over the master profile, with async PDF generation.

---

### Technical Stack

**Frontend:**
- Vue 3.5+ with TypeScript & Composition API
- Pinia for state management
- Vue Router for navigation
- TailwindCSS v4 + shadcn-vue components
- VeeValidate + Zod for form validation
- TanStack Query for server state management
- vue-i18n for internationalization

**Backend:**
- FastAPI (Python) with async/await
- PostgreSQL database, ULID primary keys
- SQLAlchemy ORM with async support
- JWT authentication with refresh tokens
- Stripe payment integration for subscriptions
- Rate limiting and reCAPTCHA protection
- Modular architecture (auth, billing, two-factor, career, ai)

**Infrastructure:**
- Docker containerization
- Nginx/Caddy reverse proxy
- Development and production configurations

---

## Business Features

### 🔐 User Management & Security
- **User Registration & Login** - Email/password authentication with secure password hashing
- **OAuth Social Login** - Sign in with Google, Facebook, or GitHub
- **Email Verification** - Confirm email addresses for account security
- **Two-Factor Authentication (2FA)** - TOTP (authenticator apps) and WebAuthn (passkeys/security keys)
- **Password Management** - Reset forgotten passwords, change password for authenticated users
- **reCAPTCHA v3 Protection** - Invisible bot protection on login, registration, and password reset
- **Session Management** - JWT tokens with automatic refresh, secure logout
- **Token Blacklist** - Server-side token invalidation using Redis (prevents token reuse after logout)
- **Account Deletion** - GDPR-compliant soft delete with confirmation

### 👤 User Profile
- **Profile Management** - Update name, email, and preferences
- **Avatar Support** - OAuth providers automatically provide profile pictures
- **Preferred Settings** - Language, theme preferences
- **Security Settings** - Manage 2FA methods, view security status

### 🌐 Multi-Language Support
- English and Polish fully supported
- Automatic locale detection from browser
- Manual language switching in settings
- All UI text, validation messages, and emails localized

### 🎨 Theming
- **Dark Mode** - Full dark theme support with system preference detection
- **Theme Persistence** - Settings saved per user account

---

## 💳 Subscription Plans

CareerHub offers flexible subscription plans powered by **Stripe** for secure payment processing:

| Plan | Price | Features |
|------|-------|----------|
| **Free** | 0 PLN/month | Rich profile, basic public profile, 2 CV versions, watermarked PDF export, LinkedIn import |
| **Pro** | 19 PLN/month | Everything in Free + unlimited CV versions, no watermark, one-pager generator, basic AI suggestions, advanced privacy controls |
| **Expert** | 50 PLN/month | Everything in Pro + deep AI analysis, custom domain, API access, priority support, backup & versioning |

**Payment Features:**
- Secure checkout powered by Stripe
- Monthly and annual billing
- Customer self-service portal for subscription management
- Automatic subscription renewal
- Easy plan switching and cancellation

---

## Career Profile Features

### 👔 Profile
- Multi-step profile wizard with per-step draft autosave
- Completeness score to nudge users toward a fuller profile
- Three-level visibility: Private, Friends, Public
- Public profile page at a shareable slug, SEO-friendly

### 💼 Experience & Projects
- Rich per-role data: company, position, employment type, dates, responsibilities, technologies
- Projects documented independently of experiences, then explicitly linked to one or more experiences and skills — supports cross-company/portfolio work
- Anonymization — hide the real company/client name behind a placeholder for NDA-restricted work
- User-orderable sections (drag-and-drop reordering)

### 🧠 Skills
- Categorized skills (Technical/Tools/Soft) with 1-5 proficiency level and years of experience
- Linkable to specific projects
- AI-suggested skills for a target role (Pro/Expert)

### 📄 CV Generation
- Multiple named CV versions per profile, each an explicit curated selection over the master profile
- Optional custom summary override and template choice per CV version
- Asynchronous PDF generation (background job); Free tier PDFs are watermarked

### 🤖 AI Features (Pro/Expert)
- Optimize responsibility/description text
- Suggest missing responsibilities for a role + seniority level
- Gap analysis against a target role (match score, strengths, gaps, recommendations)

### 🚀 Import/Export
- LinkedIn import (async job)
- Copy-paste text fallback parser
- Full JSON export of profile data

---

## Development

### Prerequisites
- Node.js ^20.19.0 or >=22.12.0
- pnpm 10.18.3+
- Python 3.12+
- PostgreSQL 15+
- Docker & Docker Compose (for containerized development)

### Quick Start

**Frontend Development:**
```bash
pnpm install
pnpm dev              # Start dev server (http://localhost:5176)
pnpm build            # Build for production
pnpm type-check       # Run TypeScript checks
pnpm lint             # Run ESLint with auto-fix
```

**Backend Development:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Docker (Backend stack):**
```bash
# From repo root
docker compose up -d
```

`compose.yaml` includes `docker-compose.dev.yml` and loads `backend/.env` for interpolation.

### Environment Variables

**Frontend (.env):**
```env
VITE_API_PROXY_URL=http://localhost:8004
VITE_GOOGLE_RECAPTCHA_SITE_KEY=your_recaptcha_site_key
VITE_GOOGLE_OAUTH_CLIENT_ID=your_google_oauth_client_id
# Stripe (optional - for subscription features)
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

**Backend (backend/.env):**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5436/careerhub
JWT_SECRET_KEY=your-secret-key
RECAPTCHA_ENABLED=true
RECAPTCHA_SECRET_KEY=your_recaptcha_secret
GOOGLE_OAUTH_CLIENT_ID=your_oauth_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_oauth_client_secret
# Stripe (optional - for subscription features)
STRIPE_ENABLED=true
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

See `.env.example` and `backend/.env.example` for complete configuration options.

---

## Project Structure

```
career-hub/
├── src/                      # Frontend source code
│   ├── modules/              # Feature modules
│   │   ├── auth/             # Authentication module
│   │   ├── career/           # Career profile/CV module (in progress)
│   │   ├── settings/         # Settings module
│   │   └── user/             # User profile module
│   ├── components/           # Shared components
│   │   └── ui/               # shadcn-vue components
│   ├── layouts/              # Layout wrappers
│   ├── router/                # Vue Router config
│   ├── shared/                # Shared utilities
│   └── i18n/                  # Internationalization
├── backend/                  # Backend source code
│   ├── app/
│   │   ├── core/             # Core functionality (config, DB, email)
│   │   ├── modules/          # Feature modules
│   │   │   ├── auth/         # Auth module
│   │   │   ├── billing/      # Stripe subscription module
│   │   │   ├── career/       # Career profile/CV module (in progress)
│   │   │   └── two_factor/   # 2FA module
│   │   └── main.py           # FastAPI app entry
│   └── migrations/           # Database migrations
├── docs/
│   └── plans/                 # Requirements digest, rebrand/module decisions
├── compose.yaml              # Compose entry (include + backend/.env)
├── docker-compose.dev.yml    # Backend stack
```

---

## Architecture

### Module-Based Frontend

Each feature is self-contained in `src/modules/`:
- `pages/` - Vue page components
- `components/` - Module-specific components
- `store/` - Pinia stores for state
- `services/` - Business logic layer
- `composables/` - Reusable composition functions
- `types/` - TypeScript definitions
- `routes.ts` - Module routes
- `i18n/` - Module translations

### Backend Modules

Backend follows FastAPI modular pattern:
- `router.py` - API endpoints with rate limiting
- `service.py` - Business logic
- `repositories.py` - Database access
- `db_models.py` - SQLAlchemy models
- `schemas.py` - Request/response schemas

### Data Model

- ULID primary keys throughout.
- JSONB for flexible/evolving fields (responsibilities, achievements, CV section selection).
- Async job pattern for long operations (PDF generation, LinkedIn import) — 202 + job id, polled for status.

---

## Security Features

- ✅ **JWT Authentication** - Secure token-based auth with refresh tokens
- ✅ **Password Hashing** - bcrypt with configurable rounds
- ✅ **Rate Limiting** - Protection against brute force attacks
- ✅ **reCAPTCHA v3** - Bot protection (score-based, invisible)
- ✅ **OAuth 2.0** - CSRF protection via state parameter
- ✅ **Two-Factor Authentication** - TOTP and WebAuthn support
- ✅ **Email Verification** - Confirm user email addresses
- ✅ **CORS Configuration** - Secure cross-origin requests
- ✅ **SQL Injection Prevention** - Parameterized queries via SQLAlchemy
- ✅ **XSS Protection** - Input validation and sanitization

---

## License

MIT — see [LICENSE](./LICENSE).

---

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
