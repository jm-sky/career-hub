"""Work experience seed data transcribed from LinkedIn (Jan Madeyski).

Dates use the first day of the month from LinkedIn ranges. DEV Made IT is the
personal brand for independent work (not a registered company) — kept as a
freelance experience so portfolio projects can link to it.
"""

from datetime import date

from app.modules.career.schemas import CreateExperienceRequest, UpdateExperienceRequest

RAW_EXPERIENCES: list[dict] = [
    {
        "companyName": "Skłodowscy Sp. z o.o.",
        "position": "Head of the Programming Team",
        "employmentType": "full_time",
        "startDate": "2021-11-01",
        "endDate": None,
        "isCurrent": True,
        "description": (
            "Lead the programming team delivering internal products, client-facing portals, "
            "ERP integrations, and AI-assisted back-office tools. Hybrid work, Poland."
        ),
        "responsibilities": [
            "Own technical direction and delivery for the programming team",
            "Architect and ship full-stack products (Vue, Python/PHP, SQL Server/Postgres)",
            "Mentor developers and coordinate with implementation / consulting",
        ],
        "technologies": [
            "JavaScript",
            "TypeScript",
            "Vue.js",
            "Python",
            "FastAPI",
            "PHP",
            "Laravel",
            "Kafka",
            "Microsoft SQL Server",
            "PostgreSQL",
            "Docker",
            "Git",
            "Linux",
        ],
    },
    {
        # Personal brand / solo practice — not a registered company.
        "companyName": "DEV Made IT",
        "position": "Independent Full Stack Developer",
        "employmentType": "freelance",
        "startDate": "2025-04-01",
        "endDate": None,
        "isCurrent": True,
        "description": (
            "Personal brand for independent product and client work (not a registered company): "
            "SaaS prototypes, company websites, ops tooling, and full-stack apps shipped under "
            "the DEV Made IT name."
        ),
        "responsibilities": [
            "Design and build end-to-end web products (Vue/Nuxt/Astro + FastAPI/Laravel)",
            "Ship multi-tenant and AI-assisted tools for niche domains",
            "Own hosting, CI, and production operations",
        ],
        "technologies": [
            "Vue.js",
            "TypeScript",
            "Nuxt",
            "Astro",
            "Python",
            "FastAPI",
            "PHP",
            "Laravel",
            "PostgreSQL",
            "Redis",
            "Docker",
            "Caddy",
            "Git",
            "Linux",
        ],
    },
    {
        "companyName": "Tax Order",
        "position": "Full Stack Developer",
        "employmentType": "full_time",
        "startDate": "2019-11-01",
        "endDate": "2024-10-01",
        "isCurrent": False,
        "description": (
            "Creating a microERP application — PHP 8 + Laravel 10 + Vue.js 3 + PostgreSQL. "
            "Hybrid work, Warsaw, Mazowieckie."
        ),
        "responsibilities": [
            "Design and develop microERP features end-to-end",
            "Build Vue.js 3 frontends and Laravel/PHP 8 backends",
            "Work with PostgreSQL and Microsoft SQL Server data layers",
        ],
        "technologies": [
            "PHP",
            "Laravel",
            "Vue.js",
            "JavaScript",
            "PostgreSQL",
            "Microsoft SQL Server",
            "Git",
        ],
    },
    {
        "companyName": "Skłodowscy Sp. z o.o.",
        "position": "Full Stack Developer",
        "employmentType": "full_time",
        "startDate": "2018-03-01",
        "endDate": "2019-10-01",
        "isCurrent": False,
        "description": (
            "PHP/JavaScript/SQL development. Projecting, designing, programming, developing, "
            "training, reviewing, consulting, presenting. Vue.js, T-SQL, security, financial documents."
        ),
        "responsibilities": [
            "Full-stack development of financial and portal features",
            "Security-conscious handling of financial documents",
            "Training, code review, consulting, and product presentations",
        ],
        "technologies": [
            "PHP",
            "JavaScript",
            "Vue.js",
            "Microsoft SQL Server",
            "T-SQL",
            "Git",
        ],
    },
    {
        "companyName": "Skłodowscy Sp. z o.o.",
        "position": "Implementation Consultant / Developer",
        "employmentType": "full_time",
        "startDate": "2016-01-01",
        "endDate": "2021-11-01",
        "isCurrent": False,
        "description": (
            "Creating original MES application. Developing and implementing original ERP features. "
            "Product presentations, training, customer support, international arrangements."
        ),
        "responsibilities": [
            "Build and implement original MES / ERP features",
            "Deliver product presentations, training, and customer support",
            "Coordinate international arrangements with partners and clients",
        ],
        "technologies": [
            "Microsoft SQL Server",
            "PHP",
            "JavaScript",
            "EDI",
            "Linux",
            "Asseco Softlab ERP",
        ],
    },
    {
        "companyName": "Tax Order",
        "position": "Developer",
        "employmentType": "full_time",
        "startDate": "2017-06-01",
        "endDate": "2018-06-01",
        "isCurrent": False,
        "description": "Application development with Ruby on Rails and Ember.js.",
        "responsibilities": [
            "Develop web application features in Ruby on Rails",
            "Build Ember.js frontends",
        ],
        "technologies": ["Ruby", "Ruby on Rails", "EmberJS", "JavaScript", "Git", "PostgreSQL"],
    },
    {
        "companyName": "Skłodowscy Sp. z o.o.",
        "position": "Junior Implementation Consultant",
        "employmentType": "full_time",
        "startDate": "2014-12-01",
        "endDate": "2015-12-01",
        "isCurrent": False,
        "description": (
            "Implementation of original ERP features. SQL Server, PHP, JavaScript, EDI. "
            "Based in Marki, Poland."
        ),
        "responsibilities": [
            "Implement ERP customizations for client operations",
            "Support EDI and SQL Server–based integrations",
        ],
        "technologies": ["Microsoft SQL Server", "SQL", "PHP", "JavaScript", "EDI"],
    },
    {
        "companyName": "Powiślańska Fundacja Społeczna",
        "position": "Wychowawca",
        "employmentType": "full_time",
        "startDate": "2011-05-01",
        "endDate": "2014-09-01",
        "isCurrent": False,
        "description": (
            "Praca z dziećmi i rodzinami marginalizowanymi społecznie oraz współpraca ze szkołami "
            "i urzędami w środowiskowej świetlicy terapeutyczno-opiekuńczej. Warszawa, praca stacjonarna."
        ),
        "responsibilities": [
            "Prowadzenie zajęć i opieki w świetlicy terapeutyczno-opiekuńczej",
            "Współpraca ze szkołami i urzędami",
            "Wsparcie rodzin marginalizowanych społecznie",
        ],
        "technologies": [],
    },
    {
        "companyName": "Wider-Group s.c.",
        "position": "IT Specialist",
        "employmentType": "part_time",
        "startDate": "2009-06-01",
        "endDate": "2014-05-01",
        "isCurrent": False,
        "description": (
            "Web development with PHP, JavaScript, MySQL, and Visual Basic. "
            "Hybrid work, Warsaw, Mazowieckie."
        ),
        "responsibilities": [
            "Build and maintain web applications",
            "Work with PHP, JavaScript, MySQL, and Visual Basic",
        ],
        "technologies": ["PHP", "JavaScript", "MySQL", "Visual Basic", "HTML"],
    },
]


def experience_key(raw: dict) -> tuple[str, str, str]:
    """Idempotency key: company + position + start date."""
    return (raw["companyName"], raw["position"], raw["startDate"])


def build_create_experience_request(raw: dict) -> CreateExperienceRequest:
    end = raw.get("endDate")
    return CreateExperienceRequest(
        companyName=raw["companyName"],
        position=raw["position"],
        employmentType=raw.get("employmentType"),
        startDate=date.fromisoformat(raw["startDate"]),
        endDate=date.fromisoformat(end) if end else None,
        isCurrent=bool(raw.get("isCurrent", end is None)),
        description=raw.get("description"),
        responsibilities=list(raw.get("responsibilities", [])),
        technologies=list(raw.get("technologies", [])),
    )


def build_update_experience_request(raw: dict) -> UpdateExperienceRequest:
    create = build_create_experience_request(raw)
    return UpdateExperienceRequest(
        companyName=create.companyName,
        position=create.position,
        employmentType=create.employmentType,
        startDate=create.startDate,
        endDate=create.endDate,
        isCurrent=create.isCurrent,
        description=create.description,
        responsibilities=create.responsibilities,
        technologies=create.technologies,
    )
