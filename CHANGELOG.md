# Changelog

## [Unreleased]

### Added
- CLI `users change-password` command to set a user's password by email or ID (admin override; invalidates existing sessions via token version bump).
- Bootstrapped repository from the `gear-stack` skeleton (auth, two-factor, users, settings, admin, billing, feature_limits, ai, logs modules kept; gear/gear_settings/stats dropped as gear-domain-specific).
- Rebranded configuration, docker-compose, CLI, and UI copy from Gear Stack to CareerHub (see `docs/plans/rebranding-decisions.md`).

### Planned
- New `career` domain module (profiles, experiences, projects, skills, education, certifications, CV generation) per `docs/plans/requirements-digest.md`.
