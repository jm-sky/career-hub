"""Seed data transcribed from madeyski.org/src/data/projects.ts (Jan Madeyski's project history).

`ProjectDB` has no `company` column, so company names are folded into `clients`
here already (deduplicated). `team` (colleague names) and `subProjects`
(`{name,url}[]`, only on "DEV Made IT Template") have no equivalent field at all
and are intentionally omitted — see
docs/issues/2026-07-21--001--project-team-and-subprojects-fields.md.

Optional ``experience_companies`` lists company names used to link projects to
seeded experiences after both are created (case-insensitive match).
"""

from app.modules.career.schemas import (
    CreateProjectRequest,
    ProjectCategory,
    ProjectLinks,
    ProjectStatus,
    UpdateProjectRequest,
)

STATUS_MAP: dict[str, ProjectStatus] = {
    "Live": "ACTIVE",
    "Staging": "STAGING",
    "Retired": "ARCHIVED",
}

CATEGORY_MAP: dict[str, ProjectCategory] = {
    "Production": "PRODUCTION",
    "Internal": "INTERNAL",
    "Demo": "DEMO",
}

# scale.teamSize / scale.users are qualitative in the source data (no exact
# numbers were ever recorded) — approximated to a representative value per bucket.
TEAM_SIZE_MAP = {
    "solo": 1,
    "small": 3,
    "medium": 8,
    "large": 20,
}

USERS_MAP = {
    "dozens": 24,
    "hundreds": 150,
    "thousands": 1500,
}

RAW_PROJECTS: list[dict] = [
    {
        "name": "Implicit Association Test (IAT)",
        "category": "Production",
        "status": "Retired",
        "clients": ["University of Warsaw"],
        "experience_companies": ["Wider-Group s.c."],
        "date_start": "2010-12-01",
        "date_end": "2011-08-01",
        "description": (
            "Development of a web application for conducting the Implicit Association Test (IAT), "
            "used in psychological research to measure unconscious biases. The tool was created on "
            "request for a postgraduate research project at the University of Warsaw."
        ),
        "role": "Full Stack Developer",
        "achievements": [
            "Delivered a research-ready IAT web app for University of Warsaw postgraduate work",
        ],
        "technologies": ["PHP", "MySQL", "JavaScript", "ActionScript", "Flash", "HTML"],
    },
    {
        "name": "Logistics Center",
        "category": "Production",
        "status": "Live",
        "clients": ["Home décor group (3 companies)", "Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2015-06-01",
        "date_end": "2015-09-01",
        "description": (
            "Contributed to the development and implementation of a centralized logistics platform "
            "to coordinate and synchronize operations between the ERP systems of three separate "
            "companies. The integration relied on database-level synchronization resembling event "
            "sourcing. The project aimed to unify key business processes such as order and inventory "
            "management."
        ),
        "role": "ERP Developer & Implementation Specialist",
        "achievements": [
            "Synchronized logistics workflows across three companies' ERP systems",
        ],
        "technologies": ["Microsoft SQL Server", "Asseco Softlab ERP"],
    },
    {
        "name": "Production planning",
        "category": "Production",
        "status": "Retired",
        "clients": ["Furniture manufacturer", "Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2015-11-01",
        "date_end": "2016-06-01",
        "description": (
            "A production scheduling interface based on a Gantt chart integrated with Asseco Softlab "
            "ERP. The solution allowed users to visualize and manage production plans using a "
            "commercial JavaScript component. It included integration of production data through "
            "Microsoft SQL Server and customization of the frontend within the ERP environment."
        ),
        "role": "ERP Developer & Implementation Specialist",
        "technologies": ["JavaScript", "Microsoft SQL Server", "Asseco Softlab ERP"],
    },
    {
        "name": "Warehouse Management System (WMS)",
        "category": "Production",
        "status": "Live",
        "clients": ["Home décor group (3 companies)", "Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2015-02-01",
        "date_end": "2016-07-01",
        "description": (
            "Contributed to the development and implementation of a custom WMS module within Asseco "
            "Softlab ERP, adapted to the operational needs of three different companies."
        ),
        "role": "ERP Developer & Implementation Specialist",
        "technologies": ["Microsoft SQL Server", "Asseco Softlab ERP"],
    },
    {
        "name": "EDI",
        "category": "Production",
        "status": "Live",
        "clients": ["Home décor group (3 companies)", "Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2015-01-01",
        "date_end": "2018-01-01",
        "description": (
            "EDI integration between a major international retailer and their suppliers, integrated "
            "with Asseco Softlab ERP."
        ),
        "role": "Integration Support Developer",
        "achievements": [
            "Integrated supplier EDI flows with Asseco Softlab ERP for a major retailer chain",
        ],
        "technologies": ["Asseco Softlab ERP", "Microsoft SQL Server", "Scala", "XML", "EDI"],
    },
    {
        "name": "LiteMES",
        "category": "Production",
        "status": "Retired",
        "clients": ["Furniture manufacturer", "Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2016-02-01",
        "date_end": "2017-02-01",
        "description": (
            "A manufacturing execution system tailored to production floor operations, integrated "
            "with ERP, and extended with modules for service tracking and time & attendance (RCP). "
            "Supported RFID and barcode-based workflows."
        ),
        "role": "Lead Developer & System Architect",
        "achievements": [
            "Led design of a custom MES with RFID/barcode shop-floor workflows",
            "Extended the system with service tracking and RCP (time & attendance)",
        ],
        "challenges": [
            "Fitting real-time floor operations into ERP constraints and offline-prone environments",
        ],
        "technologies": ["PHP", "Microsoft SQL Server", "JavaScript", "jQuery", "Bootstrap", "HTML"],
    },
    {
        "name": "Tax Order",
        "category": "Production",
        "status": "Retired",
        "clients": ["Tax Order", "Skłodowscy Sp. z o.o."],
        "experience_companies": ["Tax Order", "Skłodowscy Sp. z o.o."],
        "date_start": "2017-07-01",
        "date_end": "2018-02-01",
        "description": "Tax Order is a web application for managing the tax order of a company.",
        "role": "Full Stack Developer",
        "technologies": ["EmberJS", "JavaScript", "Ruby", "Ruby on Rails", "PostgreSQL", "HTML"],
    },
    {
        "name": "Portal Klienta",
        "category": "Production",
        "status": "Live",
        "clients": ["Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o.", "Tax Order"],
        "date_start": "2018-01-01",
        "date_end": None,
        "description": (
            "A comprehensive client portal enabling customers to access and manage their financial "
            "documents, invoices, and account information. The system integrates with ERP systems to "
            "provide real-time data synchronization and automated document generation. Features "
            "include role-based access control, document search and filtering, payment tracking, and "
            "automated notifications."
        ),
        "role": "Team Lead & System Architect",
        "scale": {"budget": "large", "duration": 84, "team_size": "medium", "users": "hundreds"},
        "achievements": [
            "Architected a multi-year client portal serving hundreds of users",
            "Integrated ERP data with RBAC, document search, and payment tracking",
        ],
        "challenges": [
            "Keeping ERP sync reliable while evolving the portal over many years and team members",
        ],
        "technologies": [
            "PHP",
            "Laravel",
            "Microsoft SQL Server",
            "Vue.js",
            "JavaScript",
            "HTML",
            "Docker",
            "Apache",
            "Nginx",
            "Git",
        ],
        "links": {"demo": "https://portal-klienta.sklodowscy.pl"},
    },
    {
        "name": "KSeF integration for Portal Klienta",
        "category": "Internal",
        "status": "Retired",
        "clients": ["Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2022-06-01",
        "date_end": "2023-05-26",
        "description": (
            "Developed a comprehensive microservice to integrate Poland's KSeF (National System of "
            "e-Invoices) with our existing client portal. The system handles XML invoice processing, "
            "validation, and automated submission to government services, ensuring compliance with "
            "Polish e-invoicing regulations while providing seamless user experience."
        ),
        "role": "Full Stack Developer",
        "achievements": [
            "Shipped KSeF XML validation and submission integrated into Portal Klienta",
        ],
        "challenges": [
            "Tracking evolving government KSeF schemas and submission rules",
        ],
        "technologies": ["PHP", "Laravel", "PostgreSQL", "XML", "Git", "Docker"],
    },
    {
        "name": "e-doręczenia",
        "category": "Internal",
        "status": "Retired",
        "clients": ["Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2025-03-01",
        "date_end": "2025-04-01",
        "description": (
            "Built a modern web portal that integrates with Poland's official e-Doręczenia "
            "(electronic delivery) system, enabling secure digital document delivery and receipt "
            "confirmation. The application features a responsive Vue.js frontend and a robust Django "
            "backend handling API communications with government services."
        ),
        "role": "Full Stack Developer",
        "technologies": [
            "Python",
            "Django",
            "Vue.js",
            "TypeScript",
            "TailwindCSS",
            "HTML",
            "CSS",
            "Git",
            "Docker",
        ],
    },
    {
        "name": "JIRA Integration",
        "category": "Internal",
        "status": "Live",
        "clients": ["Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2025-05-01",
        "date_end": "2025-07-01",
        "description": (
            "Developed a comprehensive JIRA Connect App and microservice to seamlessly integrate "
            "project management workflows with our internal systems. The solution synchronizes "
            "issues, worklogs, and project data bidirectionally, enabling automated time tracking, "
            "project reporting, and workflow management while maintaining data consistency across "
            "platforms."
        ),
        "role": "Full Stack Developer & System Architect",
        "achievements": [
            "Built bidirectional Jira sync for issues, worklogs, and project reporting",
        ],
        "technologies": ["Python", "Flask", "Jira", "Docker", "Git", "Linux", "Connect App"],
    },
    {
        "name": "Documents Generator",
        "category": "Internal",
        "status": "Live",
        "clients": ["Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2025-05-01",
        "date_end": "2025-07-01",
        "description": (
            "Built a flexible document generation microservice that creates professional business "
            "documents from templates. The system handles dynamic content injection, formatting, and "
            "supports various output formats for generating contracts, agreements, and other business "
            "documentation with consistent branding and legal compliance."
        ),
        "role": "Full Stack Developer & System Architect",
        "technologies": ["Python", "Flask", "TypeScript", "Vue.js", "HTML", "CSS", "Git"],
    },
    {
        "name": "Azure OCR Service",
        "category": "Internal",
        "status": "Live",
        "clients": ["Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2025-05-01",
        "date_end": "2025-07-01",
        "description": (
            "Implemented an intelligent document processing microservice leveraging Azure Computer "
            "Vision API to extract and digitize text from scanned documents, invoices, and forms. The "
            "service includes preprocessing capabilities, confidence scoring, and structured data "
            "extraction to automate document digitization workflows and reduce manual data entry."
        ),
        "role": "Full Stack Developer & System Architect",
        "achievements": [
            "Automated invoice/form digitization via Azure Computer Vision with confidence scoring",
        ],
        "technologies": [
            "Python",
            "Django",
            "Azure",
            "Vue.js",
            "TypeScript",
            "TailwindCSS",
            "Docker",
            "Git",
            "Linux",
        ],
    },
    {
        "name": "SaasBase",
        "category": "Demo",
        "status": "Staging",
        "clients": ["DEV Made IT"],
        "experience_companies": ["DEV Made IT"],
        "date_start": "2025-04-01",
        "date_end": "2025-07-30",
        "description": (
            "A comprehensive multi-tenant SaaS platform designed for small to medium businesses to "
            "manage their operations. Features include company management, financial document "
            "handling, task management, and team collaboration. The system integrates with multiple "
            "external APIs including Polish REGON database for company verification, Ministry of "
            "Finance APIs, EU VIES for VAT validation, and IBAN verification services. Includes Stripe "
            "integration for subscription payments and comprehensive admin dashboard."
        ),
        "role": "Independent Full Stack Developer",
        "scale": {"budget": "small", "duration": 4, "team_size": "solo", "users": "dozens"},
        "achievements": [
            "Integrated REGON, MF, VIES, IBAN, and Stripe into a multi-tenant SaaS skeleton",
        ],
        "technologies": [
            "PHP",
            "Laravel",
            "PostgreSQL",
            "HTML",
            "CSS",
            "TypeScript",
            "Vue.js",
            "TailwindCSS",
            "XML",
            "Docker",
            "Git",
            "Linux",
            "Caddy",
        ],
        "links": {"demo": "https://saasbase.ovh"},
    },
    {
        "name": "Company Hub",
        "category": "Demo",
        "status": "Staging",
        "clients": ["DEV Made IT"],
        "experience_companies": ["DEV Made IT"],
        "date_start": "2025-07-01",
        "date_end": "2025-07-30",
        "description": "Api service integrating company data from REGON, MF, VIES and IBAN APIs.",
        "role": "Independent Full Stack Developer",
        "technologies": [
            "Python",
            "FastAPI",
            "TypeScript",
            "React",
            "Next.js",
            "HTML",
            "TailwindCSS",
            "PostgreSQL",
            "Docker",
            "Git",
            "Linux",
        ],
        "links": {"demo": "https://company-hub.dev-made.it"},
    },
    {
        "name": "Madeyski.org",
        "category": "Production",
        "status": "Live",
        "clients": ["Jan Madeyski", "DEV Made IT"],
        "experience_companies": ["DEV Made IT"],
        "date_start": "2025-07-01",
        "date_end": "2025-07-30",
        "description": "Development of a personal website for a software engineer.",
        "role": "Frontend Developer",
        "technologies": ["TypeScript", "Astro", "TailwindCSS", "HTML", "CSS", "Git", "Caddy"],
        "links": {
            "demo": "https://madeyski.org",
            "github": "https://github.com/jm-sky/madeyski.org",
        },
    },
    {
        "name": "Gear Stack",
        "category": "Production",
        "status": "Live",
        "clients": ["DEV Made IT"],
        "experience_companies": ["DEV Made IT"],
        "date_start": "2025-11-18",
        "date_end": None,
        "description": (
            "A full-stack web application for managing survival gear, bug-out bags, and outdoor "
            "equipment, combining offline-first localStorage storage with a synchronized backend for "
            "multi-user, multi-device use. Features hierarchical gear containers with nested items, "
            "weight and readiness tracking, rich item metadata (category, priority, expiration, shelf "
            "life), and AI-ready JSON/Markdown/CSV import-export. The backend provides JWT "
            "authentication with OAuth and WebAuthn/passkey-based 2FA, a role system (Owner, Premium, "
            "Admin, User), and Stripe-powered subscription billing (Free/Pro/Pro Plus tiers) alongside "
            "AI-assisted gear recommendations, a public container gallery, and an admin dashboard."
        ),
        "role": "Independent Full Stack Developer",
        "achievements": [
            "Shipped offline-first gear management with sync, WebAuthn 2FA, and Stripe billing",
        ],
        "technologies": [
            "Vue.js",
            "TypeScript",
            "Pinia",
            "TailwindCSS",
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Redis",
            "WebAuthn",
            "Docker",
            "Git",
            "Linux",
            "Caddy",
        ],
        "links": {
            "demo": "https://gear-stack.ovh",
            "github": "https://github.com/jm-sky/gear-stack",
        },
    },
    {
        "name": "DEV Made IT Template",
        "category": "Production",
        "status": "Live",
        "clients": ["DEV Made IT", "WIARBUD", "SAVA GROUP", "Kraina Snów"],
        "experience_companies": ["DEV Made IT"],
        "date_start": "2025-07-01",
        "date_end": None,
        "description": (
            "A reusable template for building company websites with modern technologies. Multiple "
            "client websites have been built using this template, featuring responsive design, "
            "performance optimization, and SEO-friendly structure."
        ),
        "role": "Frontend Developer",
        "achievements": [
            "Reused one Nuxt template across multiple client sites (WIARBUD, SAVA GROUP, Kraina Snów)",
        ],
        "technologies": ["TypeScript", "Nuxt", "TailwindCSS", "HTML", "CSS", "Git", "Caddy"],
    },
    {
        "name": "Ops Monitor",
        "category": "Internal",
        "status": "Live",
        "clients": ["Skłodowscy Sp. z o.o.", "DEV Made IT"],
        "experience_companies": ["Skłodowscy Sp. z o.o.", "DEV Made IT"],
        "date_start": "2025-10-30",
        "date_end": None,
        "description": (
            "Central operations monitoring system that polls remote servers and applications for "
            "health and system metrics, stores historical snapshots in PostgreSQL, and presents them "
            "on a Vue 3 dashboard. Sends deduplicated alerts via MS Teams webhooks with per-channel "
            "routing, quiet hours, and severity thresholds. A lightweight standalone Python agent runs "
            "on each monitored server to report system metrics (CPU, memory, disk, pending updates, "
            "reboot status)."
        ),
        "role": "Full Stack Developer & System Architect",
        "achievements": [
            "Built fleet monitoring with historical metrics and deduplicated MS Teams alerts",
        ],
        "technologies": [
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Redis",
            "Vue.js",
            "TypeScript",
            "Pinia",
            "TailwindCSS",
            "WebAuthn",
            "Docker",
            "Git",
            "Linux",
        ],
    },
    {
        "name": "AI Kancelaria",
        "category": "Internal",
        "status": "Staging",
        "clients": ["Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2026-06-05",
        "date_end": None,
        "description": (
            "Internal proof-of-concept for an AI assistant layered over the firm's back-office "
            "systems: a chat agent that lets employees query business data in natural language and "
            "get answers with source citations. Explores a range of AI techniques — a prompt router "
            "for query classification, RAG over a knowledge base (Qdrant + bge-m3 embeddings), "
            "persistent facts memory injected into context, and a growing set of MCP (Model Context "
            "Protocol) tool servers integrating multiple internal systems for read-only data access. "
            "Ships as both a web app and a Windows desktop client (Tauri), running on a self-hosted "
            "LLM (Ollama)."
        ),
        "role": "Full Stack Developer & System Architect",
        "achievements": [
            "Prototyped RAG + MCP tool servers over internal systems with a Tauri desktop client",
        ],
        "technologies": [
            "Python",
            "FastAPI",
            "React",
            "TypeScript",
            "Tauri",
            "Rust",
            "Ollama",
            "Qdrant",
            "PostgreSQL",
            "MCP",
            "Docker",
            "Git",
        ],
    },
    {
        "name": "Wymiary AI",
        "category": "Internal",
        "status": "Staging",
        "clients": ["Corporate accounting client", "Skłodowscy Sp. z o.o."],
        "experience_companies": ["Skłodowscy Sp. z o.o."],
        "date_start": "2026-04-22",
        "date_end": None,
        "description": (
            "An AI-powered classifier that automatically assigns accounting dimension codes to "
            "invoice line items, supporting the bookkeeping process — a decision-support tool "
            "reviewed by accountants. Uses a two-stage RAG + LLM pipeline (semantic search with "
            "Qdrant + classification with Ollama) orchestrated in n8n, with a dedicated dashboard for "
            "monitoring classification quality and throughput. Currently being rolled out to "
            "production."
        ),
        "role": "Lead Developer & System Architect",
        "achievements": [
            "Designed two-stage RAG + LLM dimension classification reviewed by accountants",
        ],
        "technologies": [
            "n8n",
            "Qdrant",
            "Ollama",
            "PostgreSQL",
            "Redis",
            "React",
            "TypeScript",
            "Hono",
            "Python",
            "Docker",
            "Git",
        ],
    },
    {
        "name": "Zbory CHWZ",
        "category": "Production",
        "status": "Live",
        "clients": ["CHWZ", "DEV Made IT"],
        "experience_companies": ["DEV Made IT"],
        "date_start": "2025-12-28",
        "date_end": None,
        "description": (
            "A public congregation directory and multi-tenant management platform for CHWZ "
            "(Chrześcijańska Wspólnota Wolnych Zielonoświątkowców). Visitors can search congregations, "
            "view public profiles, and browse locations on an interactive Leaflet map with distance "
            "filtering. Authorized users manage congregation data with per-congregation roles; "
            "sensitive contact and GPS fields are encrypted at rest. Supports AI-assisted "
            "address/contact import from pasted text, Google Contacts sync, and an IMAP clergy e-mail "
            "import pipeline with admin review."
        ),
        "role": "Independent Full Stack Developer",
        "scale": {"budget": "small", "team_size": "solo"},
        "achievements": [
            "Shipped encrypted multi-tenant congregation directory with map search and import pipelines",
        ],
        "technologies": [
            "Vue.js",
            "TypeScript",
            "Pinia",
            "TailwindCSS",
            "Leaflet",
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Redis",
            "Docker",
            "Git",
            "Linux",
            "Nginx",
        ],
        "links": {
            "demo": "https://zbory.chwz.waw.pl",
            "github": "https://github.com/jm-sky/zbory-chwz",
        },
    },
    {
        "name": "CareerHub",
        "category": "Production",
        "status": "Staging",
        "clients": ["DEV Made IT"],
        "experience_companies": ["DEV Made IT"],
        "date_start": "2026-06-01",
        "date_end": None,
        "description": (
            "A Vue 3 + FastAPI application for building one master professional profile "
            "(experience, projects, skills, education, certifications) and generating multiple "
            "tailored CVs from it. Server-side career data in PostgreSQL with JWT auth, WebAuthn "
            "2FA, Stripe billing, and AI infrastructure reused from the gear-stack skeleton."
        ),
        "role": "Independent Full Stack Developer",
        "scale": {"budget": "small", "team_size": "solo"},
        "achievements": [
            "Forked gear-stack into a career-domain app with profile, experiences, projects, and CV-ready structure",
        ],
        "technologies": [
            "Vue.js",
            "TypeScript",
            "Pinia",
            "TailwindCSS",
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Redis",
            "WebAuthn",
            "Docker",
            "Git",
            "Linux",
        ],
        "links": {
            "github": "https://github.com/jm-sky/career-hub",
        },
    },
]


def build_create_project_request(
    raw: dict,
    *,
    experience_ids: list[str] | None = None,
) -> CreateProjectRequest:
    """Map one `RAW_PROJECTS` entry onto the API's `CreateProjectRequest` shape."""
    scale = raw.get("scale", {})
    links = raw.get("links", {})
    team_size = scale.get("team_size")
    users = scale.get("users")

    return CreateProjectRequest(
        name=raw["name"],
        description=raw.get("description"),
        role=raw.get("role"),
        startDate=raw["date_start"],
        endDate=raw.get("date_end"),
        isOngoing=raw.get("date_end") is None,
        status=STATUS_MAP[raw["status"]],
        category=CATEGORY_MAP[raw["category"]],
        achievements=list(raw.get("achievements", [])),
        challenges=list(raw.get("challenges", [])),
        clients=list(raw.get("clients", [])),
        teamSize=TEAM_SIZE_MAP.get(team_size) if team_size else None,
        durationMonths=scale.get("duration"),
        usersCount=USERS_MAP.get(users) if users else None,
        budgetRange=scale.get("budget"),
        links=ProjectLinks(demo=links.get("demo"), github=links.get("github")),
        technologies=list(raw.get("technologies", [])),
        experienceIds=list(experience_ids or []),
    )


def build_update_project_request(
    raw: dict,
    *,
    experience_ids: list[str] | None = None,
) -> UpdateProjectRequest:
    """Full replace payload for an existing seeded project."""
    create = build_create_project_request(raw, experience_ids=experience_ids)
    return UpdateProjectRequest(
        name=create.name,
        description=create.description,
        role=create.role,
        startDate=create.startDate,
        endDate=create.endDate,
        isOngoing=create.isOngoing,
        isAnonymized=create.isAnonymized,
        anonymizedCompany=create.anonymizedCompany,
        status=create.status,
        category=create.category,
        achievements=create.achievements,
        challenges=create.challenges,
        clients=create.clients,
        teamSize=create.teamSize,
        durationMonths=create.durationMonths,
        usersCount=create.usersCount,
        budgetRange=create.budgetRange,
        links=create.links,
        visibility=create.visibility,
        technologies=create.technologies,
        experienceIds=create.experienceIds,
    )
