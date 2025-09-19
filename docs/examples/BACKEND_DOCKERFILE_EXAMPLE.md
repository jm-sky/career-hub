# backend/Dockerfile.dev

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

# backend/requirements.txt

```txt
# FastAPI and Server
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Redis
redis==5.0.1
hiredis==2.2.3

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Data Validation
pydantic==2.5.2
pydantic-settings==2.1.0
email-validator==2.1.0

# ULID
python-ulid==2.2.0

# Storage
minio==7.2.0
pillow==10.1.0

# AI (optional for now)
openai==1.3.8
anthropic==0.8.1

# PDF Generation
weasyprint==60.1
jinja2==3.1.2

# HTML Parsing (for LinkedIn import)
beautifulsoup4==4.12.2
lxml==4.9.3

# Background Tasks
celery==5.3.4
flower==2.0.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
faker==20.1.0

# Development
black==23.12.0
ruff==0.1.7
mypy==1.7.1
ipython==8.18.1

# Monitoring
sentry-sdk[fastapi]==1.38.0
prometheus-client==0.19.0

# CORS and Security
python-multipart==0.0.6
slowapi==0.1.9

# Date handling
python-dateutil==2.8.2
pytz==2023.3
```

---

# backend/.env.example

```env
# Database
DB_USER=careerhub
DB_PASSWORD=careerhub_pass
DB_NAME=careerhub
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL=postgresql://careerhub:careerhub_pass@localhost:5432/careerhub

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30

# MinIO (S3-compatible storage)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=careerhub
MINIO_SECURE=false

# Email (SendGrid/AWS SES)
EMAIL_ENABLED=false
EMAIL_FROM=noreply@careerhub.com
SENDGRID_API_KEY=your-sendgrid-api-key

# AI Services (optional)
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
DEBUG=true

# Sentry (optional)
SENTRY_DSN=

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
```