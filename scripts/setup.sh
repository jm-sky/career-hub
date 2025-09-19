#!/bin/bash

# CareerHub Project Setup Script
# This script sets up the development environment for existing project structure

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# ASCII Art Header
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ █████╗ ██████╗ ███████╗███████╗██████╗            ║
║  ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗           ║
║  ██║     ███████║██████╔╝█████╗  █████╗  ██████╔╝           ║
║  ██║     ██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗           ║
║  ╚██████╗██║  ██║██║  ██║███████╗███████╗██║  ██║           ║
║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝           ║
║                                                               ║
║              ██╗  ██╗██╗   ██╗██████╗                        ║
║              ██║  ██║██║   ██║██╔══██╗                       ║
║              ███████║██║   ██║██████╔╝                       ║
║              ██╔══██║██║   ██║██╔══██╗                       ║
║              ██║  ██║╚██████╔╝██████╔╝                       ║
║              ╚═╝  ╚═╝ ╚═════╝ ╚═════╝                        ║
║                                                               ║
║           Professional Profile Management Platform            ║
║                     Development Setup                         ║
╚═══════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "Setting up CareerHub development environment..."
echo ""

# Check prerequisites
print_status "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1,2)
    print_status "Python 3 found: $(python3 --version)"
else
    print_error "Python 3 is not installed. Please install Python 3.12+"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    print_status "Node.js found: $(node --version)"
else
    print_error "Node.js is not installed. Please install Node.js 20+"
    exit 1
fi

# Check pnpm
if command -v pnpm &> /dev/null; then
    print_status "pnpm found: $(pnpm --version)"
else
    print_error "pnpm is not installed. Please install pnpm: npm install -g pnpm"
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    print_status "Docker found: $(docker --version)"
else
    print_warning "Docker is not installed. You'll need it for database and services."
fi

# Check if we're in the project root
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the CareerHub project root directory"
    exit 1
fi

print_status "Project structure detected"

# Backend setup
print_status "Setting up backend environment..."

cd backend

# Create virtual environment in .venv
if [ ! -d ".venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv .venv
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Verify we're in virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    print_status "Virtual environment activated: $VIRTUAL_ENV"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    print_status "Creating requirements.txt..."
    cat > requirements.txt << 'EOL'
# FastAPI and ASGI
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Cache and Queue
redis==5.0.1
celery==5.3.4

# Authentication and Security
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6

# Validation and Settings
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0

# Utilities
python-ulid==1.1.0
python-dotenv==1.0.0

# File Processing and PDF
beautifulsoup4==4.12.2
lxml==4.9.3
weasyprint==60.2
reportlab==4.0.7

# Storage
minio==7.2.0

# Rate Limiting
slowapi==0.1.9

# Monitoring and Logging
sentry-sdk[fastapi]==1.38.0

# Development dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
black==23.11.0
ruff==0.1.6
EOL
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating backend .env file..."
    cat > .env << 'EOL'
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

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=careerhub
MINIO_SECURE=false

# Email
EMAIL_ENABLED=false
EMAIL_FROM=noreply@careerhub.com

# Frontend
FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# Environment
ENVIRONMENT=development
DEBUG=true

# Features
RATE_LIMIT_ENABLED=true
METRICS_ENABLED=false

# AI (optional for development)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
EOL
    print_warning "Remember to change SECRET_KEY and add AI API keys if needed!"
else
    print_status "Backend .env file already exists"
fi

# Initialize Alembic if not already done
if [ ! -d "alembic" ]; then
    print_status "Initializing database migrations..."
    alembic init alembic
    
    # Update alembic.ini with correct database URL
    sed -i 's|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = postgresql://careerhub:careerhub_pass@localhost:5432/careerhub|' alembic.ini
else
    print_status "Alembic already initialized"
fi

# Create basic app structure if it doesn't exist
if [ ! -f "app/__init__.py" ]; then
    print_status "Creating basic app structure..."
    mkdir -p app/{api/v1,core,models,schemas,services,middleware}
    
    cat > app/__init__.py << 'EOL'
"""CareerHub Backend Application"""

__version__ = "1.0.0"
EOL

    cat > app/main.py << 'EOL'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CareerHub API",
    description="Professional Profile Management Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to CareerHub API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOL
else
    print_status "App structure already exists"
fi

cd ..

# Frontend setup
print_status "Setting up frontend environment..."

cd frontend

# Install frontend dependencies
if [ -f "package.json" ]; then
    print_status "Installing frontend dependencies with pnpm..."
    pnpm install
    
    # Add CareerHub specific dependencies if not already present
    print_status "Adding CareerHub specific dependencies..."
    pnpm add @tanstack/react-query zustand axios react-hook-form zod @hookform/resolvers
    pnpm add @radix-ui/react-dialog @radix-ui/react-label @radix-ui/react-select @radix-ui/react-toast
    pnpm add lucide-react class-variance-authority clsx tailwind-merge date-fns
    pnpm add -D @types/node
else
    print_error "Frontend package.json not found. Please ensure Next.js is properly set up."
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f ".env.local" ]; then
    print_status "Creating frontend .env.local file..."
    cat > .env.local << 'EOL'
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Features
NEXT_PUBLIC_ENABLE_AI_FEATURES=false
NEXT_PUBLIC_ENABLE_ANALYTICS=false

# Sentry (optional)
NEXT_PUBLIC_SENTRY_DSN=
EOL
else
    print_status "Frontend .env.local file already exists"
fi

cd ..

# Docker setup
if [ ! -f "docker-compose.yml" ]; then
    print_status "Creating Docker configuration..."
    cat > docker-compose.yml << 'EOL'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: careerhub-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER:-careerhub}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-careerhub_pass}
      POSTGRES_DB: ${DB_NAME:-careerhub}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-careerhub}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: careerhub-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  minio:
    image: minio/minio:latest
    container_name: careerhub-minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

volumes:
  postgres_data:
  redis_data:
  minio_data:

networks:
  default:
    name: careerhub-network
EOL
else
    print_status "Docker configuration already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_status "Creating .gitignore..."
    cat > .gitignore << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
ENV/

# Node
node_modules/
.next/
out/
dist/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Database
*.db
*.sqlite3

# Uploads
uploads/
media/
static/

# Testing
coverage/
.coverage
.pytest_cache/
htmlcov/
.nyc_output

# Docker
docker-compose.override.yml

# Logs
logs/
*.log

# Build artifacts
build/
dist/

# Temporary files
tmp/
temp/
EOL
else
    print_status "Gitignore already exists"
fi

# Final instructions
echo ""
echo "═══════════════════════════════════════════════════════════════"
print_status "Development environment setup completed!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the database and services:"
echo -e "   ${GREEN}docker-compose up -d${NC}"
echo ""
echo "2. Start the backend:"
echo -e "   ${GREEN}cd backend${NC}"
echo -e "   ${GREEN}source .venv/bin/activate${NC}"
echo -e "   ${GREEN}uvicorn app.main:app --reload${NC}"
echo ""
echo "3. Start the frontend (in a new terminal):"
echo -e "   ${GREEN}cd frontend${NC}"
echo -e "   ${GREEN}pnpm dev${NC}"
echo ""
echo "4. Access the application:"
echo -e "   - Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "   - API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   - MinIO Console: ${GREEN}http://localhost:9001${NC} (minioadmin/minioadmin)"
echo ""
echo "5. Review the documentation in /docs folder"
echo ""
print_warning "Remember to:"
print_warning "- Change SECRET_KEY in production"
print_warning "- Add AI API keys if you plan to use AI features"
print_warning "- Review and customize environment variables"
echo ""
echo "Happy coding! 🚀"