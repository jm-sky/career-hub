"""Skills seed data derived from Jan Madeyski's project/experience tech stacks.

Levels are approximate (1–5). Adjust after reviewing in the UI.
"""

from app.modules.career.schemas import CreateSkillRequest, UpdateSkillRequest

# level: 1=basic … 5=master. years / started year are rough career estimates.
RAW_SKILLS: list[dict] = [
    {"technologyName": "JavaScript", "level": 5, "yearsOfExperience": 16, "startedUsingYear": 2009, "isPrimary": True},
    {"technologyName": "TypeScript", "level": 4, "yearsOfExperience": 4, "startedUsingYear": 2022, "isPrimary": True},
    {"technologyName": "Vue.js", "level": 5, "yearsOfExperience": 8, "startedUsingYear": 2018, "isPrimary": True},
    {"technologyName": "PHP", "level": 5, "yearsOfExperience": 15, "startedUsingYear": 2009, "isPrimary": True},
    {"technologyName": "Laravel", "level": 4, "yearsOfExperience": 7, "startedUsingYear": 2018, "isPrimary": True},
    {"technologyName": "Python", "level": 4, "yearsOfExperience": 3, "startedUsingYear": 2023, "isPrimary": True},
    {"technologyName": "FastAPI", "level": 4, "yearsOfExperience": 2, "startedUsingYear": 2024, "isPrimary": True},
    {"technologyName": "PostgreSQL", "level": 4, "yearsOfExperience": 8, "startedUsingYear": 2017, "isPrimary": True},
    {"technologyName": "Microsoft SQL Server", "level": 5, "yearsOfExperience": 11, "startedUsingYear": 2014, "isPrimary": True},
    {"technologyName": "Docker", "level": 4, "yearsOfExperience": 6, "startedUsingYear": 2019, "isPrimary": False},
    {"technologyName": "Git", "level": 5, "yearsOfExperience": 12, "startedUsingYear": 2014, "isPrimary": False},
    {"technologyName": "Linux", "level": 4, "yearsOfExperience": 12, "startedUsingYear": 2014, "isPrimary": False},
    {"technologyName": "Redis", "level": 3, "yearsOfExperience": 2, "startedUsingYear": 2024, "isPrimary": False},
    {"technologyName": "TailwindCSS", "level": 4, "yearsOfExperience": 3, "startedUsingYear": 2023, "isPrimary": False},
    {"technologyName": "Nuxt", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2025, "isPrimary": False},
    {"technologyName": "React", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2025, "isPrimary": False},
    {"technologyName": "Django", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2025, "isPrimary": False},
    {"technologyName": "Asseco Softlab ERP", "level": 4, "yearsOfExperience": 7, "startedUsingYear": 2014, "isPrimary": False},
    {"technologyName": "EDI", "level": 3, "yearsOfExperience": 5, "startedUsingYear": 2015, "isPrimary": False},
    {"technologyName": "Ollama", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2026, "isPrimary": False},
    {"technologyName": "Qdrant", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2026, "isPrimary": False},
    {"technologyName": "MCP", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2026, "isPrimary": False},
    {"technologyName": "n8n", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2026, "isPrimary": False},
    {"technologyName": "WebAuthn", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2025, "isPrimary": False},
    {"technologyName": "Pinia", "level": 4, "yearsOfExperience": 2, "startedUsingYear": 2024, "isPrimary": False},
    {"technologyName": "Ruby on Rails", "level": 2, "yearsOfExperience": 1, "startedUsingYear": 2017, "isPrimary": False},
    {"technologyName": "EmberJS", "level": 2, "yearsOfExperience": 1, "startedUsingYear": 2017, "isPrimary": False},
    {"technologyName": "MySQL", "level": 3, "yearsOfExperience": 6, "startedUsingYear": 2009, "isPrimary": False},
    {"technologyName": "Astro", "level": 3, "yearsOfExperience": 1, "startedUsingYear": 2025, "isPrimary": False},
    {"technologyName": "Caddy", "level": 3, "yearsOfExperience": 2, "startedUsingYear": 2024, "isPrimary": False},
]


def build_create_skill_request(raw: dict) -> CreateSkillRequest:
    return CreateSkillRequest(
        technologyName=raw["technologyName"],
        level=raw["level"],
        yearsOfExperience=raw.get("yearsOfExperience"),
        startedUsingYear=raw.get("startedUsingYear"),
        isPrimary=bool(raw.get("isPrimary", False)),
    )


def build_update_skill_request(raw: dict) -> UpdateSkillRequest:
    return UpdateSkillRequest(
        level=raw["level"],
        yearsOfExperience=raw.get("yearsOfExperience"),
        startedUsingYear=raw.get("startedUsingYear"),
        isPrimary=bool(raw.get("isPrimary", False)),
    )
