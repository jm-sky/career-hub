# backend

CareerHub's FastAPI backend.

## Setup

### Prerequisites

- Python 3.12+
- pip or a virtualenv tool

### Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and update with your configuration
```

### Environment Variables

#### Sentry Error Monitoring (Optional)

Sentry integration is **optional** and disabled by default. To enable:

```bash
SENTRY_ENABLED=true
SENTRY_DSN=https://your-key@your-org.ingest.sentry.io/project-id
SENTRY_ENVIRONMENT=production
SENTRY_RELEASE=v0.1.0
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_PROFILES_SAMPLE_RATE=1.0
```

4. Initialize the database:
```bash
python -m cli db init
python -m cli db migrate
```

### Running the Application

Development mode with auto-reload:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive docs (Swagger): http://localhost:8000/docs
- Alternative docs (ReDoc): http://localhost:8000/redoc

(When running via `docker-compose.yml`, the host-forwarded port is `8004` by default — see `../CLAUDE.md`.)

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── app/
│   ├── core/               # Core utilities (config, database, storage, security headers)
│   ├── common/             # Shared cross-module utilities
│   └── modules/            # Feature modules (auth, two_factor, users, settings, admin,
│                            # billing, feature_limits, ai, logs, career)
├── cli/                    # Django-inspired management CLI
├── migrations/             # Database migrations
├── requirements.txt        # Python dependencies
├── docker-compose.yml
└── README.md
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

```bash
pytest                # Run tests
python -m black .     # Format
python -m mypy .      # Type-check
ruff check .          # Lint
```

## Environment Variables

Key environment variables (see `.env.example` for the full list):

- `PROJECT_NAME`: Application name
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for security (change in production!)
- `CORS_ORIGINS`: Allowed CORS origins (JSON array format)
- `ENVIRONMENT`: Environment (development/production)

### Storage Configuration

- `STORAGE_TYPE`: Storage backend type (`local` or `s3`, default: `local`)
- `STORAGE_BASE_URL`: Base URL for serving uploaded files (e.g., `https://api.careerhub.com`)
- `STORAGE_LOCAL_PATH`: Local storage base path (default: `./uploads`)

**S3 Storage Configuration** (if `STORAGE_TYPE=s3`):
- `STORAGE_S3_BUCKET`, `STORAGE_S3_ACCESS_KEY`, `STORAGE_S3_SECRET_KEY`, `STORAGE_S3_REGION`
- `STORAGE_S3_ENDPOINT_URL` (internal), `STORAGE_S3_PUBLIC_ENDPOINT_URL` (browser-accessible)

**RustFS:** Run RustFS separately and ensure the external Docker network `rustfs-network` exists. `docker-compose.yml` attaches the app service to that network when using S3 storage.

### Email Configuration

Two adapters are supported:

**1. File Adapter (Development - Default)**
```bash
EMAIL_ENABLED=true
EMAIL_ADAPTER=file
EMAIL_FILE_PATH=./emails
```
Emails are saved in `./emails/YYYY-MM-DD/` as HTML + JSON metadata.

**2. SMTP Adapter (Production)**
```bash
EMAIL_ENABLED=true
EMAIL_ADAPTER=smtp
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-password
SMTP_FROM=noreply@careerhub.com
SMTP_USE_TLS=true
```

## License

MIT — see [../LICENSE](../LICENSE).
