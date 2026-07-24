"""Migration: Create responsibilities_library table + seed data (career module, Phase 7).

Usage:
    python migrations/010_add_responsibilities_library.py upgrade
    python migrations/010_add_responsibilities_library.py downgrade
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from app.common.id_utils import generate_id
from app.core.database import engine
from app.modules.career.db_models import ResponsibilitiesLibraryDB

# (role_category, seniority_level | None, responsibility)
SEED_RESPONSIBILITIES: list[tuple[str, str | None, str]] = [
    # Backend Engineer
    ("Backend Engineer", None, "Designed and implemented RESTful APIs consumed by web and mobile clients"),
    ("Backend Engineer", None, "Optimized database queries and indexes to reduce p95 response times"),
    ("Backend Engineer", None, "Wrote and maintained automated integration and unit tests"),
    ("Backend Engineer", None, "Participated in code reviews to uphold code quality standards"),
    ("Backend Engineer", None, "Investigated and resolved production incidents and bugs"),
    ("Backend Engineer", "senior", "Designed service architecture and led technical decision-making for new features"),
    ("Backend Engineer", "senior", "Mentored junior engineers through pairing and structured code review"),
    ("Backend Engineer", "lead", "Owned the technical roadmap for a backend platform used by multiple teams"),
    # Frontend Engineer
    ("Frontend Engineer", None, "Built responsive, accessible UI components from design specifications"),
    ("Frontend Engineer", None, "Integrated frontend applications with REST/GraphQL APIs"),
    ("Frontend Engineer", None, "Improved page load performance through code splitting and lazy loading"),
    ("Frontend Engineer", None, "Collaborated with designers to translate mockups into production UI"),
    ("Frontend Engineer", None, "Wrote unit and component tests to prevent UI regressions"),
    ("Frontend Engineer", "senior", "Established frontend architecture patterns and component libraries"),
    ("Frontend Engineer", "senior", "Drove adoption of accessibility and performance best practices across teams"),
    # Full Stack Engineer
    ("Full Stack Engineer", None, "Delivered end-to-end features spanning frontend UI and backend services"),
    ("Full Stack Engineer", None, "Designed database schemas and corresponding API contracts"),
    ("Full Stack Engineer", None, "Collaborated with product managers to scope and estimate features"),
    ("Full Stack Engineer", None, "Debugged issues across the full stack, from UI to database"),
    ("Full Stack Engineer", None, "Maintained CI/CD pipelines for automated testing and deployment"),
    # DevOps Engineer
    ("DevOps Engineer", None, "Built and maintained CI/CD pipelines for automated build, test, and deploy"),
    ("DevOps Engineer", None, "Managed cloud infrastructure using infrastructure-as-code tools"),
    ("DevOps Engineer", None, "Set up monitoring, logging, and alerting for production systems"),
    ("DevOps Engineer", None, "Reduced deployment time and improved release reliability"),
    ("DevOps Engineer", None, "Implemented security best practices across infrastructure and pipelines"),
    ("DevOps Engineer", "senior", "Led migration of infrastructure to a container orchestration platform"),
    # Data Engineer
    ("Data Engineer", None, "Designed and maintained ETL/ELT pipelines for analytics and reporting"),
    ("Data Engineer", None, "Modeled data warehouses to support business intelligence needs"),
    ("Data Engineer", None, "Ensured data quality and integrity through automated validation checks"),
    ("Data Engineer", None, "Optimized large-scale data processing jobs for cost and performance"),
    ("Data Engineer", None, "Collaborated with data scientists and analysts on data availability"),
    # Product Manager
    ("Product Manager", None, "Defined product roadmap and prioritized features based on customer impact"),
    ("Product Manager", None, "Gathered and synthesized user feedback to inform product decisions"),
    ("Product Manager", None, "Wrote product requirements and user stories for engineering teams"),
    ("Product Manager", None, "Coordinated cross-functional launches with engineering, design, and marketing"),
    ("Product Manager", None, "Tracked product metrics and iterated based on data-driven insights"),
    # QA Engineer
    ("QA Engineer", None, "Designed and executed manual and automated test plans"),
    ("QA Engineer", None, "Built automated regression test suites to catch defects early"),
    ("QA Engineer", None, "Reported and tracked bugs through resolution with development teams"),
    ("QA Engineer", None, "Defined quality gates and acceptance criteria for releases"),
    ("QA Engineer", None, "Performed exploratory and performance testing on new features"),
    # Mobile Engineer
    ("Mobile Engineer", None, "Built and shipped native/cross-platform mobile application features"),
    ("Mobile Engineer", None, "Optimized app performance, startup time, and memory usage"),
    ("Mobile Engineer", None, "Integrated mobile apps with backend APIs and push notification services"),
    ("Mobile Engineer", None, "Maintained app store release processes and versioning"),
    # UI/UX Designer
    ("UI/UX Designer", None, "Designed user flows, wireframes, and high-fidelity mockups"),
    ("UI/UX Designer", None, "Conducted user research and usability testing to validate designs"),
    ("UI/UX Designer", None, "Maintained and evolved a design system and component library"),
    ("UI/UX Designer", None, "Collaborated with engineers to ensure accurate design implementation"),
    # Engineering Manager
    ("Engineering Manager", None, "Led and mentored a team of engineers, conducting regular 1:1s"),
    ("Engineering Manager", None, "Set team goals and OKRs aligned with organizational priorities"),
    ("Engineering Manager", None, "Managed hiring, onboarding, and performance reviews for the team"),
    ("Engineering Manager", None, "Facilitated sprint planning, retrospectives, and technical roadmap discussions"),
]


async def upgrade() -> None:
    """Create the responsibilities_library table and seed baseline data."""
    print("Creating responsibilities_library table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: ResponsibilitiesLibraryDB.__table__.create(sync_conn, checkfirst=True))

        existing = await conn.execute(text("SELECT COUNT(*) FROM responsibilities_library"))
        if existing.scalar_one() == 0:
            print(f"Seeding {len(SEED_RESPONSIBILITIES)} responsibilities_library rows...")
            for role_category, seniority_level, responsibility in SEED_RESPONSIBILITIES:
                await conn.execute(
                    text("INSERT INTO responsibilities_library " "(id, role_category, responsibility, seniority_level, usage_count) " "VALUES (:id, :role_category, :responsibility, :seniority_level, 0)"),
                    {
                        "id": generate_id(),
                        "role_category": role_category,
                        "responsibility": responsibility,
                        "seniority_level": seniority_level,
                    },
                )

    print("✓ responsibilities_library table created and seeded successfully")


async def downgrade() -> None:
    """Drop the responsibilities_library table."""
    print("Dropping responsibilities_library table...")

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: ResponsibilitiesLibraryDB.__table__.drop(sync_conn, checkfirst=True))

    print("✓ responsibilities_library table dropped successfully")


async def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Create responsibilities_library table")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    args = parser.parse_args()

    if args.action == "upgrade":
        await upgrade()
    elif args.action == "downgrade":
        await downgrade()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
