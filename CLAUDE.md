# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CareerHub is a Vue 3 + FastAPI application for building one master professional profile (experience, projects, skills, education, certifications) and generating multiple tailored CVs from it. It was bootstrapped from the `gear-stack` sibling project's skeleton (shared core auth/billing/2FA/feature_limits/ai infrastructure) — see `docs/plans/requirements-digest.md` for the domain spec and `docs/plans/gear-stack-keep-strip-checklist.md` / `docs/plans/rebranding-decisions.md` for what was kept, dropped, and renamed during the fork.

Unlike gear-stack, CareerHub has **no client-side/offline data layer** — all career data (profile, experiences, projects, skills, CVs) lives server-side in PostgreSQL and is fetched via the API. There is no localStorage-first module to migrate or keep in sync.

## Commands

### Development
```bash
pnpm dev              # Start development server (default port: 5176)
pnpm build            # Build for production (runs type-check + build-only)
pnpm build-only       # Build without type checking
pnpm preview          # Preview production build
```

### Code Quality
```bash
pnpm type-check       # Run TypeScript compiler check
pnpm lint             # Run ESLint with auto-fix and cache
```

### Testing
```bash
pnpm test             # Run tests in watch mode
pnpm test:ui          # Run tests with Vitest UI
pnpm test:run         # Run tests once (CI mode)
pnpm test:coverage    # Run tests with coverage report
```

### Package Manager
This project uses **pnpm** (version 10.18.3+). Always use `pnpm` instead of `npm` or `yarn`.

### Backend Development

```bash
docker compose -f backend/docker-compose.yml up    # Start backend in development mode
docker compose -f backend/docker-compose.yml down  # Stop backend
```

- Use `docker compose` (Docker Compose V2 syntax), NOT `docker-compose` (deprecated V1 syntax)
- Default host ports (see `docs/plans/rebranding-decisions.md` for why these differ from gear-stack/ops-monitor/AI-workspace, which run alongside this repo): DB `5436`, Redis `6383`, app `8004`
- In development, the backend runs in a Docker container via `docker-compose.yml`, container name `career-hub-app`. Accessible at `http://localhost:8004` (or the port in `VITE_API_PROXY_URL`).
- **Auto-reload is enabled** - FastAPI uses WatchFiles to automatically reload when Python files change. No need to restart the container after code changes during development.
- Only restart the container when changing environment variables (`.env`) or dependencies (`requirements.txt`).

### Backend Testing
The backend uses **pytest** for testing with async support via `pytest-asyncio`.

```bash
# Using Docker (recommended - ensures consistent environment)
docker exec career-hub-app python -m pytest tests/ -v

# Using venv (if dependencies are installed)
cd backend
source .venv/bin/activate
python -m pytest tests/ -v

# Run with coverage
docker exec career-hub-app python -m pytest tests/ --cov=app --cov-report=html
```

**Test Database:**
- Integration tests use PostgreSQL test database (`backend_test`)
- Use `python -m cli db init-test` to initialize test database

### Backend CLI Commands

The backend includes a Django-inspired CLI for database and user management.

```bash
# Database
docker exec career-hub-app python -m cli db init
docker exec career-hub-app python -m cli db init-test
docker exec career-hub-app python -m cli db migrate
docker exec career-hub-app python -m cli db migrate-status

# Users
docker exec career-hub-app python -m cli users create
docker exec career-hub-app python -m cli users list
docker exec career-hub-app python -m cli users set-role

# Interactive mode
docker exec -it career-hub-app python -m cli
```

## Architecture

### Module-Based Structure

The application follows a **modular architecture** where each feature is self-contained in `src/modules/`. Each module contains:

- `pages/` - Vue page components
- `components/` - Module-specific components
- `store/` - Pinia stores for state management
- `services/` - Business logic layer
- `composables/` - Reusable composition functions
- `types/` - TypeScript type definitions
- `routes.ts` - Module route definitions
- `i18n/` - Module-specific translations

Current modules (kept from gear-stack, see checklist for the full keep/drop list): `auth`, `user`, `settings`, `admin`, `billing`, `ai`. `career` is the new domain module being built (frontend + backend) per `docs/plans/requirements-digest.md` — not yet implemented as of this writing. `tenants` (backend) is kept on ice — not wired into career-hub's single-user-profile MVP.

### Core Directories

- `src/components/` - Shared UI components (`ui/` shadcn-vue, `data-table/`, `layout/`)
- `src/pages/` - Top-level/shared pages (Landing, Privacy, Terms, About, NotFound, Dashboard)
- `src/layouts/` - Layout wrappers (authenticated, guest, public)
- `src/shared/` - Shared utilities, types, composables, config, i18n infrastructure, API client
- `src/router/` - Vue Router configuration
- `src/i18n/` - Application i18n instance (merges module translations)

### State Management Pattern

- **Pinia** for client-side UI state
- **TanStack Query** (`@tanstack/vue-query`) manages server state (all career data, auth, AI, admin operations) with caching and invalidation

### Backend Modules

Backend follows FastAPI modular pattern (`backend/app/modules/<name>/`):
- `router.py` - API endpoints with rate limiting
- `service.py` - Business logic
- `repositories.py` - Database access
- `db_models.py` - SQLAlchemy models
- `schemas.py` - Request/response schemas

### Routing & Layouts

Routes are defined per-module and merged in `src/router/routes.ts`. Each route specifies a layout via `meta.layout`. Available layouts: `authenticated`, `guest`, `public`.

### Internationalization (i18n)

The app uses **vue-i18n** with a registry pattern: each module defines translations in `i18n/locales/` (en, pl), exported from `i18n/index.ts` and merged at `src/i18n/index.ts`. Locale is persisted in localStorage and synced via `useLocale()` composable.

## Tech Stack & Configuration

### Core Technologies
- **Vue 3.5+** with `<script setup>` and Composition API
- **TypeScript** (strict mode)
- **Pinia** for client-side state management
- **TanStack Query** (@tanstack/vue-query) for server state management
- **Vue Router** for navigation
- **Vite** as build tool

### UI & Styling
- **Tailwind CSS v4** (via `@tailwindcss/vite`)
- **shadcn-vue** components (based on reka-ui)
- **lucide-vue-next** for icons
- **vue-sonner** for toast notifications
- **floating-vue** for tooltips (registered as `v-tooltip` directive)

### Form Handling
- **vee-validate** + **@vee-validate/zod** for form validation
- **zod** for schema validation

### Backend & API
- **axios** for HTTP client
- **@simplewebauthn/browser** for WebAuthn/passkeys authentication
- **jwt-decode** for JWT token parsing

### PWA
- **vite-plugin-pwa** for Progressive Web App support
- Configuration in `pwa.config.ts`

### Testing
- **vitest** for unit testing with happy-dom environment
- **@playwright/test** for end-to-end testing

## Code Style & Conventions

### ESLint Configuration (eslint.config.ts)

- **No semicolons** (`semi: never`)
- **Single quotes** with escape avoidance
- **Import sorting** (Perfectionist plugin) - alphabetical order with specific groups
- **Self-closing tags** required for all HTML/SVG/Vue components
- **Max attributes per line**: 3 for single-line, 1 for multi-line
- Unused variables starting with `_` are allowed
- **No line breaks before `else`, `catch`, `finally`** - keep control flow keywords on the same line as closing brace

### TypeScript Conventions

- Use `@/` alias for absolute imports from `src/`
- Create **dedicated union types** instead of inline definitions (per global CLAUDE.md)
- Prefer interfaces for object shapes, types for unions/primitives
- All types are defined in module-specific `types/` directories

### Vue Component Patterns

- Use `<script setup lang="ts">` for all components
- Import order: external packages → internal modules (alphabetical, enforced by ESLint)
- Layouts are rendered via `<RouterView />` in App.vue

### Vue 3.5+ Best Practices

**v-model with defineModel:**
- ✅ Use: `const open = defineModel<boolean>('open', { required: true })`
- ❌ Avoid: `defineProps<{ open: boolean }>()` + `emit('update:open')`

**Reactive Destructured Props:**
- Destructured props are reactive in Vue 3.5+ (no need for `toRefs`)
- ✅ Use: `const { item } = defineProps<{ item: SomeType }>()`

**Prop Shortcuts:**
- ✅ Use: `<Dialog :open />` instead of `<Dialog :open="open" />`

**TypeScript Generics:**
- Always provide explicit types for `ref<T>`, `computed<T>`, `reactive<T>`
- ✅ Use: `const count = ref<number>(0)`
- ❌ Avoid: `const count = ref(0)` (implicit types)

**Declaration Order in `<script setup>`:**
1. Composables (e.g., `useI18n()`, `useRouter()`)
2. `defineProps()`
3. `defineModel()`
4. `defineEmits()`
5. Computed properties and reactive state
6. Functions and methods

**Routing:**
- Use route helper functions from each module's `routes.ts` instead of hardcoded paths

### Reka-ui / shadcn-vue Checkbox

**CRITICAL:** In Reka-ui (shadcn-vue), Checkbox uses standard `v-model`, **NOT** `v-model:checked`.

```vue
<!-- ✅ Correct -->
<Checkbox v-model="checked" />

<!-- ❌ Incorrect - does not work with a plain ref -->
<Checkbox v-model:checked="checked" />
```

`v-model:checked` only works with `defineModel()`. For a regular `ref`, use standard `v-model`.

## TailwindCSS Best Practices

**Sizing:**
- Prefer `size-{value}` utility class instead of separate `w-{value} h-{value}` when width and height are the same
- ✅ **Correct:** `size-4`, `size-8`, `size-12`
- ❌ **Avoid:** `w-4 h-4`, `w-8 h-8`, `w-12 h-12`

**Button Component Spacing:**
- The Button component already includes `flex` and `gap-2` classes
- Icons inside buttons do **NOT** need `mr-2` or similar margin utilities

## Responsive Design

**Always consider mobile-first responsive design:**
- Start with mobile styles (base classes)
- Add desktop variants using Tailwind breakpoint prefixes (e.g. `sm:`)
- Example: `text-sm sm:text-base lg:text-lg`
- Run `python -m black .` and `python -m mypy .` in `backend/` before committing Python code.

## Shared core with sibling projects

`backend/app/core` + `app/common` + `cli`, and frontend `src/shared` + `src/components/ui` originate from the same `gear-stack` skeleton also used by `ops-monitor` and `AI-workspace`. There is no automated sync between these repos — if you fix a bug in shared-core code here, consider whether it should be mirrored to the siblings, but do not assume it already has been.
