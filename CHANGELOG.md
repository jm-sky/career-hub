# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [2.52.0] - 2026-07-23

### Added
- **Career module**: profile CRUD + public view + draft autosave; experiences, technologies, skills; projects (incl. team / sub-project fields); education, certifications, achievements; languages; CV versions
- **CV**: PDF generation with WeasyPrint; overview dashboard (completeness score, section counts, suggestions)
- **Health**: `GET /api/health/details` for Ops Monitor
- **CLI**: `users change-password`
- Configurable footer GitHub link via `config.app.githubUrl`
- Bootstrapped from `gear-stack` skeleton (gear domain stripped); CareerHub rebrand

### Changed
- Billing tier `pro_plus` → `expert`; redesigned limits and watermark gating
- UI: glassmorphism / design tokens (Dimension.dev), floating sidebar dock, brand teal file-user icons
- Docker Compose at repo root; Compose-managed Postgres volume; shared compose auto-detect

### Fixed
- Mobile sidebar glass/backdrop blur; `glass-surface` backdrop-filter; AppSidebar responsiveness
- UserNav dropdown glass styling

### Security
- Path-safe storage and OAuth state cleanup; unified OAuth callback `/auth/callback/:provider`
- OAuth state store and login hardening; WebAuthn / users-router / rate-limiter backport
- `tv`/`jti` on 2FA login/refresh; TOTP `verified`/`method`; pnpm Dependabot overrides
