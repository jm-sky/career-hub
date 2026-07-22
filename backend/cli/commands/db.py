"""Database management CLI commands."""

import asyncio
import importlib.util
import sys
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from ..main import COMMAND_GROUPS, show_group_interactive_menu

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

db_app = typer.Typer(
    name="db",
    help="Database management commands",
    no_args_is_help=False,  # We handle no-args case ourselves for interactive mode
)

console = Console()


@db_app.callback(invoke_without_command=True)
def db_callback(ctx: typer.Context) -> None:
    """Callback for db command group - shows interactive menu if no subcommand provided."""
    if ctx.invoked_subcommand is None:
        # No subcommand provided, show interactive menu
        show_group_interactive_menu("db", COMMAND_GROUPS["db"])


MODEL_MODULES = [
    "app.modules.auth.db_models",
    "app.modules.users.db_models",
    "app.modules.logs.db_models",
    "app.modules.settings.db_models",
    "app.modules.tenants.db_models",
    "app.modules.two_factor.db_models",
    "app.modules.billing.db_models",
    "app.modules.feature_limits.db_models",
    "app.modules.ai.db_models",
    "app.modules.career.db_models",
]


def _import_model_modules() -> None:
    """Ensure all SQLAlchemy models are imported before create_all."""
    for module_path in MODEL_MODULES:
        try:
            import_module(module_path)
        except ModuleNotFoundError:
            console.print(f"[yellow]Skipping missing module:[/yellow] {module_path}")


@db_app.command("init")
def init_database(force: bool = typer.Option(False, "--force", "-f", help="Recreate database file if it already exists")) -> None:
    """Initialize application database (run SQLAlchemy metadata create_all)."""

    async def _init() -> None:
        _import_model_modules()

        # Import SchemaMigration model to ensure it's included in metadata
        from app.core.database import Base, engine, init_db
        from app.core.migrations import SchemaMigration  # noqa: F401

        if force:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        await init_db()

        # Mark migration 000 as applied if it wasn't already
        from app.core.migrations import ensure_schema_migrations_table, is_migration_applied, mark_migration_as_applied

        await ensure_schema_migrations_table()
        if not await is_migration_applied("000"):
            await mark_migration_as_applied("000", "create_schema_migrations")
            console.print("[green]✓ Migration 000 marked as applied[/green]")

    db_path = Path(__file__).resolve().parents[2] / "data" / "app.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if db_path.exists() and not force:
        console.print(f"[yellow]Database already exists at[/yellow] {db_path}")
        if not Confirm.ask("Re-run initialization anyway?", default=True):
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit()

    console.print("[bold green]Initializing database...[/bold green]")
    asyncio.run(_init())
    console.print(f"[bold green]✓ Database ready:[/bold green] {db_path}")


@db_app.command("init-test")
def init_test_database(
    force: bool = typer.Option(False, "--force", "-f", help="Recreate test database if it already exists"),
) -> None:
    """Initialize test database (backend_test) for integration tests.

    This command creates the test database schema in PostgreSQL.
    Requires DATABASE_URL to be set or POSTGRES_PASSWORD environment variable.
    """
    import os

    async def _init_test() -> None:
        _import_model_modules()

        # Import SchemaMigration model to ensure it's included in metadata
        from sqlalchemy.ext.asyncio import create_async_engine

        from app.core.database import Base
        from app.core.migrations import SchemaMigration  # noqa: F401

        # Get database password from environment
        db_password = os.getenv("POSTGRES_PASSWORD", "changeme")
        test_db_url = f"postgresql+asyncpg://backend:{db_password}@db:5432/backend_test"

        console.print(f"[dim]Test database URL: {test_db_url.replace(db_password, '***')}[/dim]")

        # Create engine for test database
        engine = create_async_engine(
            test_db_url,
            echo=False,
        )

        try:
            async with engine.begin() as conn:
                if force:
                    from sqlalchemy import text

                    console.print("[yellow]Dropping existing test database tables...[/yellow]")
                    # Drop all tables with CASCADE to handle foreign keys
                    await conn.execute(text("DROP SCHEMA public CASCADE"))
                    await conn.execute(text("CREATE SCHEMA public"))
                    # Grant permissions (important for PostgreSQL)
                    await conn.execute(text("GRANT ALL ON SCHEMA public TO backend"))
                    await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))

                console.print("[bold green]Creating test database schema...[/bold green]")
                await conn.run_sync(Base.metadata.create_all)

            console.print("[bold green]✓ Test database initialized successfully[/bold green]")

        finally:
            await engine.dispose()

    console.print("[bold blue]Initializing test database (backend_test)...[/bold blue]")
    asyncio.run(_init_test())


@db_app.command("migrate")
def migrate_database(
    fake: bool = typer.Option(False, "--fake", help="Mark migrations as applied without running them"),
    skip_init_check: bool = typer.Option(False, "--skip-init-check", help="Skip automatic init if database is not initialized"),
) -> None:
    """Run all pending migrations in order.

    Automatically runs 'db init' if database is not initialized.
    """

    async def _migrate() -> None:
        from app.core.migrations import (
            discover_migrations,
            ensure_schema_migrations_table,
            get_applied_migrations,
            is_database_initialized,
            is_migration_applied,
            mark_migration_as_applied,
        )

        # Check if database is initialized, if not run init first
        if not skip_init_check:
            if not await is_database_initialized():
                console.print("[yellow]Database is not initialized. Running 'db init' first...[/yellow]")
                # Run init logic
                _import_model_modules()
                from app.core.database import init_db
                from app.core.migrations import SchemaMigration  # noqa: F401

                await init_db()

                # Mark migration 000 as applied
                await ensure_schema_migrations_table()
                if not await is_migration_applied("000"):
                    await mark_migration_as_applied("000", "create_schema_migrations")
                    console.print("[green]✓ Migration 000 marked as applied[/green]")

                console.print("[bold green]✓ Database initialized[/bold green]\n")

        # Ensure schema_migrations table exists
        await ensure_schema_migrations_table()

        # Get migrations directory
        migrations_dir = Path(__file__).resolve().parents[2] / "migrations"
        if not migrations_dir.exists():
            console.print(f"[red]Migrations directory not found:[/red] {migrations_dir}")
            raise typer.Exit(1)

        # Discover all migrations
        all_migrations = discover_migrations(migrations_dir)
        if not all_migrations:
            console.print("[yellow]No migrations found[/yellow]")
            return

        # Get applied migrations
        applied_versions = set(await get_applied_migrations())

        # Find pending migrations
        pending_migrations = [(version, name, filepath) for version, name, filepath in all_migrations if version not in applied_versions]

        if not pending_migrations:
            console.print("[bold green]✓ All migrations are already applied[/bold green]")
            return

        console.print(f"[bold]Found {len(pending_migrations)} pending migration(s)[/bold]")

        # Run pending migrations in order
        for version, name, filepath in pending_migrations:
            console.print(f"\n[bold cyan]Running migration {version}: {name}[/bold cyan]")

            if fake:
                # Just mark as applied without running
                await mark_migration_as_applied(version, name)
                console.print(f"[yellow]Fake: Marked {version} as applied[/yellow]")
                continue

            try:
                # Import and run migration
                spec = importlib.util.spec_from_file_location(f"migration_{version}", filepath)
                if spec is None or spec.loader is None:
                    console.print(f"[red]Failed to load migration:[/red] {filepath}")
                    raise typer.Exit(1)

                migration_module = importlib.util.module_from_spec(spec)
                sys.modules[f"migration_{version}"] = migration_module
                spec.loader.exec_module(migration_module)

                # Run upgrade function
                if not hasattr(migration_module, "upgrade"):
                    console.print(f"[red]Migration {version} does not have upgrade() function[/red]")
                    raise typer.Exit(1)

                await migration_module.upgrade()

                # Mark as applied
                await mark_migration_as_applied(version, name)
                console.print(f"[bold green]✓ Migration {version} applied successfully[/bold green]")

            except Exception as e:
                console.print(f"[red]✗ Migration {version} failed:[/red] {e}")
                raise typer.Exit(1) from None

        console.print("\n[bold green]✓ All pending migrations completed[/bold green]")

    asyncio.run(_migrate())


@db_app.command("migrate-status")
def migrate_status() -> None:
    """Show status of all migrations."""

    async def _status() -> None:
        from app.core.migrations import (
            discover_migrations,
            ensure_schema_migrations_table,
            get_applied_migrations,
        )

        # Ensure schema_migrations table exists
        await ensure_schema_migrations_table()

        # Get migrations directory
        migrations_dir = Path(__file__).resolve().parents[2] / "migrations"
        if not migrations_dir.exists():
            console.print(f"[red]Migrations directory not found:[/red] {migrations_dir}")
            raise typer.Exit(1)

        # Discover all migrations
        all_migrations = discover_migrations(migrations_dir)
        if not all_migrations:
            console.print("[yellow]No migrations found[/yellow]")
            return

        # Get applied migrations
        applied_versions = set(await get_applied_migrations())

        # Create table
        table = Table(title="Migration Status")
        table.add_column("Version", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="green")

        pending_count = 0
        applied_count = 0

        for version, name, _ in all_migrations:
            if version in applied_versions:
                status = "[green]✓ Applied[/green]"
                applied_count += 1
            else:
                status = "[yellow]○ Pending[/yellow]"
                pending_count += 1

            table.add_row(version, name, status)

        console.print(table)
        console.print(f"\n[bold]Total: {len(all_migrations)}[/bold] | [green]Applied: {applied_count}[/green] | [yellow]Pending: {pending_count}[/yellow]")

    asyncio.run(_status())


@db_app.command("migrate-graceful")
def migrate_graceful(
    from_version: str | None = typer.Option(None, "--from", help="Start from specific migration version (e.g., '020')"),
    skip_init_check: bool = typer.Option(False, "--skip-init-check", help="Skip automatic init if database is not initialized"),
) -> None:
    """Run migrations gracefully, ignoring errors and continuing.

    This command is useful when migrations were created in wrong order or
    filenames were changed. It will attempt to run migrations but continue
    even if errors occur.

    If --from is provided, it will unmark that migration and all subsequent
    ones, then re-run them. If --from is not provided, it will run all
    pending migrations.

    Examples:
        cli db migrate-graceful                    # Run all pending migrations
        cli db migrate-graceful --from 020         # Re-run from migration 020 onwards
    """

    async def _migrate_graceful() -> None:
        from app.core.migrations import (
            discover_migrations,
            ensure_schema_migrations_table,
            get_applied_migrations,
            is_database_initialized,
            is_migration_applied,
            mark_migration_as_applied,
            unmark_migration,
        )

        # Check if database is initialized, if not run init first
        if not skip_init_check:
            if not await is_database_initialized():
                console.print("[yellow]Database is not initialized. Running 'db init' first...[/yellow]")
                # Run init logic
                _import_model_modules()
                from app.core.database import init_db
                from app.core.migrations import SchemaMigration  # noqa: F401

                await init_db()

                # Mark migration 000 as applied
                await ensure_schema_migrations_table()
                if not await is_migration_applied("000"):
                    await mark_migration_as_applied("000", "create_schema_migrations")
                    console.print("[green]✓ Migration 000 marked as applied[/green]")

                console.print("[bold green]✓ Database initialized[/bold green]\n")

        # Ensure schema_migrations table exists
        await ensure_schema_migrations_table()

        # Get migrations directory
        migrations_dir = Path(__file__).resolve().parents[2] / "migrations"
        if not migrations_dir.exists():
            console.print(f"[red]Migrations directory not found:[/red] {migrations_dir}")
            raise typer.Exit(1)

        # Discover all migrations
        all_migrations = discover_migrations(migrations_dir)
        if not all_migrations:
            console.print("[yellow]No migrations found[/yellow]")
            return

        # Get applied migrations
        applied_versions = set(await get_applied_migrations())

        # If --from is provided, unmark that migration and all subsequent ones
        if from_version:
            console.print(f"[bold yellow]Unmarking migrations from {from_version} onwards...[/bold yellow]")
            unmarked_count = 0
            for version, _, _ in all_migrations:
                try:
                    # Compare versions numerically
                    version_float = float(version)
                    from_float = float(from_version)
                    if version_float >= from_float:
                        if await is_migration_applied(version):
                            await unmark_migration(version)
                            console.print(f"[yellow]Unmarked migration {version}[/yellow]")
                            unmarked_count += 1
                            applied_versions.discard(version)
                except ValueError:
                    # If version comparison fails, use string comparison
                    if version >= from_version:
                        if await is_migration_applied(version):
                            await unmark_migration(version)
                            console.print(f"[yellow]Unmarked migration {version}[/yellow]")
                            unmarked_count += 1
                            applied_versions.discard(version)

            if unmarked_count > 0:
                console.print(f"[bold yellow]✓ Unmarked {unmarked_count} migration(s)[/bold yellow]\n")
            else:
                console.print(f"[yellow]No migrations found to unmark from version {from_version}[/yellow]\n")

        # Find migrations to run
        # If --from was provided, we want to run from that version onwards
        # Otherwise, run all pending migrations
        migrations_to_run: list[tuple[str, str, Path]] = []
        for version, name, filepath in all_migrations:
            if from_version:
                # Check if this migration should be run (>= from_version)
                try:
                    version_float = float(version)
                    from_float = float(from_version)
                    if version_float >= from_float:
                        migrations_to_run.append((version, name, filepath))
                except ValueError:
                    if version >= from_version:
                        migrations_to_run.append((version, name, filepath))
            else:
                # Run all pending migrations
                if version not in applied_versions:
                    migrations_to_run.append((version, name, filepath))

        if not migrations_to_run:
            console.print("[bold green]✓ No migrations to run[/bold green]")
            return

        console.print(f"[bold]Found {len(migrations_to_run)} migration(s) to run gracefully[/bold]")

        # Run migrations gracefully (ignore errors)
        success_count = 0
        error_count = 0
        skipped_count = 0

        for version, name, filepath in migrations_to_run:
            console.print(f"\n[bold cyan]Running migration {version}: {name}[/bold cyan]")

            try:
                # Import and run migration
                spec = importlib.util.spec_from_file_location(f"migration_{version}", filepath)
                if spec is None or spec.loader is None:
                    console.print(f"[red]Failed to load migration:[/red] {filepath}")
                    error_count += 1
                    continue

                migration_module = importlib.util.module_from_spec(spec)
                sys.modules[f"migration_{version}"] = migration_module
                spec.loader.exec_module(migration_module)

                # Run upgrade function
                if not hasattr(migration_module, "upgrade"):
                    console.print(f"[red]Migration {version} does not have upgrade() function[/red]")
                    error_count += 1
                    continue

                await migration_module.upgrade()

                # Mark as applied (even if it was already applied, this is safe)
                await mark_migration_as_applied(version, name)
                console.print(f"[bold green]✓ Migration {version} applied successfully[/bold green]")
                success_count += 1

            except Exception as e:
                console.print(f"[yellow]⚠ Migration {version} failed (continuing):[/yellow] {e}")
                error_count += 1
                # Don't mark as applied if it failed
                # But check if it was already applied before
                if await is_migration_applied(version):
                    console.print(f"[yellow]  Note: Migration {version} was already marked as applied in database[/yellow]")
                    skipped_count += 1

        console.print("\n[bold]Migration summary:[/bold]")
        console.print(f"  [green]✓ Success: {success_count}[/green]")
        if error_count > 0:
            console.print(f"  [yellow]⚠ Errors (ignored): {error_count}[/yellow]")
        if skipped_count > 0:
            console.print(f"  [yellow]○ Skipped (already applied): {skipped_count}[/yellow]")
        console.print("\n[bold green]✓ Graceful migration completed[/bold green]")

    asyncio.run(_migrate_graceful())


@db_app.command("migrate-unmark")
def migrate_unmark(
    version: str = typer.Argument(..., help="Migration version to unmark (e.g., '020')"),
) -> None:
    """Remove a migration from schema_migrations table.

    This allows re-running a migration that was already marked as applied.
    Useful when migration files were renamed or need to be re-executed.

    Example:
        cli db migrate-unmark 020
    """

    async def _unmark() -> None:
        from app.core.migrations import (
            ensure_schema_migrations_table,
            is_migration_applied,
            unmark_migration,
        )

        # Ensure schema_migrations table exists
        await ensure_schema_migrations_table()

        # Check if migration is applied
        if not await is_migration_applied(version):
            console.print(f"[yellow]Migration {version} is not marked as applied[/yellow]")
            return

        # Unmark migration
        await unmark_migration(version)
        console.print(f"[bold green]✓ Migration {version} unmarked successfully[/bold green]")
        console.print(f"[yellow]You can now re-run it with:[/yellow] cli db migrate-graceful --from {version}")

    asyncio.run(_unmark())


AVAILABLE_SEEDERS = ("career", "career-projects")


@db_app.command("seed")
def seed(
    seeder: str = typer.Argument(..., help="Seeder to run (e.g. 'career')"),
    email: str | None = typer.Option(None, "--email", help="Owner user email (find-or-create). Defaults to the seeder's built-in email, if it has one."),
    name: str | None = typer.Option(None, "--name", help="Full name, used only if the user has to be created"),
    password: str | None = typer.Option(None, "--password", help="Password, used only if the user has to be created"),
) -> None:
    """Seed the database with sample/reference data.

    Available seeders:
        career           Full Jan Madeyski profile (profile, experiences, projects, skills, …)
        career-projects  Projects only (subset of `career`)
    """
    if seeder not in AVAILABLE_SEEDERS:
        console.print(f"[red]Unknown seeder:[/red] {seeder}")
        console.print(f"[dim]Available:[/dim] {', '.join(AVAILABLE_SEEDERS)}")
        raise typer.Exit(1)

    from app.seeders.constants import SEED_USER_EMAIL, SEED_USER_NAME

    asyncio.run(
        _seed_career(
            email or SEED_USER_EMAIL,
            name or SEED_USER_NAME,
            password,
            projects_only=(seeder == "career-projects"),
            seeder_label=seeder,
        )
    )


@db_app.command("seed-remove")
def seed_remove(
    seeder: str = typer.Argument(..., help="Seeder whose data to remove (e.g. 'career')"),
    email: str | None = typer.Option(None, "--email", help="Owner user email. Defaults to the seeder's built-in email."),
) -> None:
    """Remove data previously created by a seeder (idempotent; does not delete the user).

    Available seeders:
        career           Remove profile-seeded career entities matching seed keys
        career-projects  Remove only seeded projects
    """
    if seeder not in AVAILABLE_SEEDERS:
        console.print(f"[red]Unknown seeder:[/red] {seeder}")
        console.print(f"[dim]Available:[/dim] {', '.join(AVAILABLE_SEEDERS)}")
        raise typer.Exit(1)

    from app.seeders.constants import SEED_USER_EMAIL

    asyncio.run(
        _seed_remove_career(
            email or SEED_USER_EMAIL,
            projects_only=(seeder == "career-projects"),
            seeder_label=seeder,
        )
    )


async def _resolve_seed_user(
    db: "AsyncSession",
    email: str,
    name: str | None,
    password: str | None,
    *,
    create_if_missing: bool,
):
    """Find the seed owner; optionally create when missing."""
    from app.modules.auth.repositories import UserRepository

    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(email)

    if user is not None:
        console.print(f"[dim]Using existing user {user.email} ({user.id})[/dim]")
        return user

    if not create_if_missing:
        console.print(f"[red]No user found for {email}[/red]")
        raise typer.Exit(1)

    console.print(f"[yellow]No user found for {email} — creating one.[/yellow]")
    if not name:
        name = typer.prompt("Full name")
    if not password:
        password = typer.prompt("Password", hide_input=True, confirmation_prompt=True)
    user = await user_repo.create_user(email=email, password=password, full_name=name)
    console.print(f"[green]✓ Created user {user.email} ({user.id})[/green]")
    return user


def _experience_ids_for_companies(company_to_ids: dict[str, list[str]], companies: list[str]) -> list[str]:
    """Resolve experience ids by case-insensitive company name match."""
    ids: list[str] = []
    seen: set[str] = set()
    for company in companies:
        key = company.casefold()
        for exp_id in company_to_ids.get(key, []):
            if exp_id not in seen:
                seen.add(exp_id)
                ids.append(exp_id)
    return ids


async def _seed_career(
    email: str,
    name: str | None,
    password: str | None,
    *,
    projects_only: bool,
    seeder_label: str,
) -> None:
    """Find-or-create the owning user, then idempotently seed career data on their profile."""
    from datetime import date

    from app.core.database import get_db
    from app.modules.career.achievement_repository import AchievementRepository
    from app.modules.career.certification_repository import CertificationRepository
    from app.modules.career.dependencies import (
        get_achievement_service,
        get_certification_service,
        get_education_service,
        get_experience_service,
        get_language_service,
        get_profile_service,
        get_project_service,
        get_skill_service,
    )
    from app.modules.career.education_repository import EducationRepository
    from app.modules.career.experience_repository import ExperienceRepository
    from app.modules.career.language_repository import LanguageRepository
    from app.modules.career.project_repository import ProjectRepository
    from app.modules.career.schemas import UpdateAchievementRequest, UpdateCertificationRequest, UpdateEducationRequest, UpdateProfileRequest
    from app.modules.career.skill_repository import SkillRepository
    from app.seeders.career_achievements import (
        OBSOLETE_ACHIEVEMENT_TITLES,
        RAW_ACHIEVEMENTS,
        build_create_achievement_request,
    )
    from app.seeders.career_certifications import (
        RAW_CERTIFICATIONS,
        build_create_certification_request,
        certification_key,
    )
    from app.seeders.career_education import RAW_EDUCATION, build_create_education_request, education_key
    from app.seeders.career_experiences import (
        RAW_EXPERIENCES,
        build_create_experience_request,
        build_update_experience_request,
        experience_key,
    )
    from app.seeders.career_languages import (
        RAW_LANGUAGES,
        build_create_language_request,
        build_update_language_request,
    )
    from app.seeders.career_profile import SEED_PROFILE, build_update_profile_request
    from app.seeders.career_projects import (
        RAW_PROJECTS,
        build_create_project_request,
        build_update_project_request,
    )
    from app.seeders.career_skills import RAW_SKILLS, build_create_skill_request, build_update_skill_request

    async for db in get_db():
        user = await _resolve_seed_user(db, email, name, password, create_if_missing=True)

        profile_service = get_profile_service(db)
        profile = await profile_service.get_or_create_for_user(user.id, user.name)

        counts: dict[str, tuple[int, int]] = {}

        if not projects_only:
            # Profile — always refresh from seed (source of truth for this personal seeder).
            try:
                await profile_service.update_profile(profile, build_update_profile_request(SEED_PROFILE))
                console.print("[green]✓ Profile updated[/green]")
            except ValueError as exc:
                # Slug collision: keep existing slug, still fill the rest.
                console.print(f"[yellow]Profile slug skipped:[/yellow] {exc}")
                await profile_service.update_profile(
                    profile,
                    UpdateProfileRequest(
                        headline=SEED_PROFILE.get("headline"),
                        summary=SEED_PROFILE.get("summary"),
                        location=SEED_PROFILE.get("location"),
                        visibility=SEED_PROFILE.get("visibility"),
                        contact=build_update_profile_request(SEED_PROFILE).contact,
                    ),
                )
                console.print("[green]✓ Profile updated (without slug)[/green]")

            experience_service = get_experience_service(db)
            experience_repo = ExperienceRepository(db)
            exp_rows = await experience_repo.list_by_profile(profile.id)
            existing_exps = {(e.company_name, e.position, e.start_date.isoformat()): e for e in exp_rows}
            # Fallback when position was renamed in the seeder (same company + start).
            existing_exps_by_company_start = {(e.company_name, e.start_date.isoformat()): e for e in exp_rows}
            created = updated = 0
            for raw in RAW_EXPERIENCES:
                key = experience_key(raw)
                entity = existing_exps.get(key) or existing_exps_by_company_start.get((raw["companyName"], raw["startDate"]))
                if entity is not None:
                    await experience_service.update(entity, build_update_experience_request(raw))
                    updated += 1
                else:
                    await experience_service.create(profile.id, build_create_experience_request(raw))
                    created += 1
            counts["experiences"] = (created, updated)

            skill_service = get_skill_service(db)
            skill_repo = SkillRepository(db)
            existing_skills = {technology.name.casefold(): (skill, technology) for skill, technology in await skill_repo.list_by_profile(profile.id)}
            created = updated = 0
            for raw in RAW_SKILLS:
                row = existing_skills.get(raw["technologyName"].casefold())
                if row is not None:
                    skill, technology = row
                    await skill_service.update(skill, technology, build_update_skill_request(raw))
                    updated += 1
                else:
                    await skill_service.create(profile.id, build_create_skill_request(raw))
                    created += 1
            counts["skills"] = (created, updated)

            education_service = get_education_service(db)
            education_repo = EducationRepository(db)
            existing_edu = {(e.institution, e.degree, e.start_date.isoformat()): e for e in await education_repo.list_by_profile(profile.id)}
            created = updated = 0
            for raw in RAW_EDUCATION:
                entity = existing_edu.get(education_key(raw))
                if entity is not None:
                    end = raw.get("endDate")
                    await education_service.update(
                        entity,
                        UpdateEducationRequest(
                            institution=raw["institution"],
                            degree=raw["degree"],
                            fieldOfStudy=raw.get("fieldOfStudy"),
                            startDate=date.fromisoformat(raw["startDate"]),
                            endDate=date.fromisoformat(end) if end else None,
                            grade=raw.get("grade"),
                            description=raw.get("description"),
                        ),
                    )
                    updated += 1
                else:
                    await education_service.create(profile.id, build_create_education_request(raw))
                    created += 1
            counts["education"] = (created, updated)

            certification_service = get_certification_service(db)
            certification_repo = CertificationRepository(db)
            existing_certs = {(c.name, c.issuing_organization): c for c in await certification_repo.list_by_profile(profile.id)}
            created = updated = 0
            for raw in RAW_CERTIFICATIONS:
                entity = existing_certs.get(certification_key(raw))
                if entity is not None:
                    expiry = raw.get("expiryDate")
                    await certification_service.update(
                        entity,
                        UpdateCertificationRequest(
                            name=raw["name"],
                            issuingOrganization=raw["issuingOrganization"],
                            credentialId=raw.get("credentialId"),
                            credentialUrl=raw.get("credentialUrl"),
                            issueDate=date.fromisoformat(raw["issueDate"]),
                            expiryDate=date.fromisoformat(expiry) if expiry else None,
                        ),
                    )
                    updated += 1
                else:
                    await certification_service.create(profile.id, build_create_certification_request(raw))
                    created += 1
            counts["certifications"] = (created, updated)

            achievement_service = get_achievement_service(db)
            achievement_repo = AchievementRepository(db)
            existing_achs = {a.title: a for a in await achievement_repo.list_by_profile(profile.id)}
            for obsolete_title in OBSOLETE_ACHIEVEMENT_TITLES:
                entity = existing_achs.pop(obsolete_title, None)
                if entity is not None:
                    await achievement_service.delete(entity)

            created = updated = 0
            for raw in RAW_ACHIEVEMENTS:
                entity = existing_achs.get(raw["title"])
                if entity is not None:
                    d = raw.get("date")
                    await achievement_service.update(
                        entity,
                        UpdateAchievementRequest(
                            title=raw["title"],
                            description=raw.get("description"),
                            date=date.fromisoformat(d) if d else None,
                            category=raw.get("category"),
                            url=raw.get("url"),
                        ),
                    )
                    updated += 1
                else:
                    await achievement_service.create(profile.id, build_create_achievement_request(raw))
                    created += 1
            counts["achievements"] = (created, updated)

            language_service = get_language_service(db)
            language_repo = LanguageRepository(db)
            existing_langs = {lang.name.casefold(): lang for lang in await language_repo.list_by_profile(profile.id)}
            created = updated = 0
            for raw in RAW_LANGUAGES:
                entity = existing_langs.get(raw["name"].casefold())
                if entity is not None:
                    await language_service.update(entity, build_update_language_request(raw))
                    updated += 1
                else:
                    await language_service.create(profile.id, build_create_language_request(raw))
                    created += 1
            counts["languages"] = (created, updated)

        # Experiences map for project linking (needed even on projects-only if experiences already exist)
        experience_service = get_experience_service(db)
        company_to_ids: dict[str, list[str]] = {}
        for exp in await experience_service.list_for_profile(profile.id):
            company_to_ids.setdefault(exp.companyName.casefold(), []).append(exp.id)

        project_service = get_project_service(db)
        project_repo = ProjectRepository(db)
        existing_projects = {p.name: p for p in await project_repo.list_by_profile(profile.id)}
        created = updated = 0
        for raw in RAW_PROJECTS:
            experience_ids = _experience_ids_for_companies(
                company_to_ids,
                list(raw.get("experience_companies", [])),
            )
            entity = existing_projects.get(raw["name"])
            if entity is not None:
                await project_service.update(
                    entity,
                    build_update_project_request(raw, experience_ids=experience_ids),
                )
                updated += 1
            else:
                await project_service.create(
                    profile.id,
                    build_create_project_request(raw, experience_ids=experience_ids),
                )
                created += 1
        counts["projects"] = (created, updated)

        console.print(f"\n[bold green]✓ Seed '{seeder_label}' complete:[/bold green]")
        for section, (c, s) in counts.items():
            console.print(f"  {section}: {c} created, {s} updated")
        break


async def _seed_remove_career(email: str, *, projects_only: bool, seeder_label: str) -> None:
    """Remove seeded career entities that match seed keys. Does not delete the user."""
    from app.core.database import get_db
    from app.modules.career.achievement_repository import AchievementRepository
    from app.modules.career.certification_repository import CertificationRepository
    from app.modules.career.dependencies import (
        get_achievement_service,
        get_certification_service,
        get_education_service,
        get_experience_service,
        get_language_service,
        get_profile_service,
        get_project_service,
        get_skill_service,
    )
    from app.modules.career.education_repository import EducationRepository
    from app.modules.career.experience_repository import ExperienceRepository
    from app.modules.career.language_repository import LanguageRepository
    from app.modules.career.project_repository import ProjectRepository
    from app.modules.career.skill_repository import SkillRepository
    from app.seeders.career_achievements import OBSOLETE_ACHIEVEMENT_TITLES, RAW_ACHIEVEMENTS
    from app.seeders.career_certifications import RAW_CERTIFICATIONS, certification_key
    from app.seeders.career_education import RAW_EDUCATION, education_key
    from app.seeders.career_experiences import RAW_EXPERIENCES, experience_key
    from app.seeders.career_languages import RAW_LANGUAGES
    from app.seeders.career_projects import RAW_PROJECTS
    from app.seeders.career_skills import RAW_SKILLS

    async for db in get_db():
        user = await _resolve_seed_user(db, email, None, None, create_if_missing=False)

        profile_service = get_profile_service(db)
        profile = await profile_service.get_or_create_for_user(user.id, user.name)

        removed: dict[str, int] = {}

        project_service = get_project_service(db)
        project_repo = ProjectRepository(db)
        seed_project_names = {p["name"] for p in RAW_PROJECTS}
        n = 0
        for project in await project_repo.list_by_profile(profile.id):
            if project.name in seed_project_names:
                await project_service.delete(project)
                n += 1
        removed["projects"] = n

        if not projects_only:
            experience_service = get_experience_service(db)
            experience_repo = ExperienceRepository(db)
            seed_exp_keys = {experience_key(r) for r in RAW_EXPERIENCES}
            n = 0
            for exp in await experience_repo.list_by_profile(profile.id):
                key = (exp.company_name, exp.position, exp.start_date.isoformat())
                if key in seed_exp_keys:
                    await experience_service.delete(exp)
                    n += 1
            removed["experiences"] = n

            skill_service = get_skill_service(db)
            skill_repo = SkillRepository(db)
            seed_skill_names = {s["technologyName"].casefold() for s in RAW_SKILLS}
            n = 0
            for skill, technology in await skill_repo.list_by_profile(profile.id):
                if technology.name.casefold() in seed_skill_names:
                    await skill_service.delete(skill)
                    n += 1
            removed["skills"] = n

            education_service = get_education_service(db)
            education_repo = EducationRepository(db)
            seed_edu_keys = {education_key(r) for r in RAW_EDUCATION}
            n = 0
            for edu in await education_repo.list_by_profile(profile.id):
                key = (edu.institution, edu.degree, edu.start_date.isoformat())
                if key in seed_edu_keys:
                    await education_service.delete(edu)
                    n += 1
            removed["education"] = n

            certification_service = get_certification_service(db)
            certification_repo = CertificationRepository(db)
            seed_cert_keys = {certification_key(r) for r in RAW_CERTIFICATIONS}
            n = 0
            for cert in await certification_repo.list_by_profile(profile.id):
                if (cert.name, cert.issuing_organization) in seed_cert_keys:
                    await certification_service.delete(cert)
                    n += 1
            removed["certifications"] = n

            achievement_service = get_achievement_service(db)
            achievement_repo = AchievementRepository(db)
            seed_titles = {a["title"] for a in RAW_ACHIEVEMENTS} | OBSOLETE_ACHIEVEMENT_TITLES
            n = 0
            for ach in await achievement_repo.list_by_profile(profile.id):
                if ach.title in seed_titles:
                    await achievement_service.delete(ach)
                    n += 1
            removed["achievements"] = n

            language_service = get_language_service(db)
            language_repo = LanguageRepository(db)
            seed_lang_names = {lang["name"].casefold() for lang in RAW_LANGUAGES}
            n = 0
            for lang in await language_repo.list_by_profile(profile.id):
                if lang.name.casefold() in seed_lang_names:
                    await language_service.delete(lang)
                    n += 1
            removed["languages"] = n

        console.print(f"\n[bold green]✓ Seed-remove '{seeder_label}' complete:[/bold green]")
        for section, n in removed.items():
            console.print(f"  {section}: {n} removed")
        break
