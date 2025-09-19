# setup.sh - Project Initialization Script

```bash
#!/bin/bash

# CareerHub Project Setup Script
# This script initializes the complete project structure

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
╚═══════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "Starting CareerHub project setup..."
echo ""

# Check prerequisites
print_status "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1,2)
    print_status "Python 3 found: $(python3 --version)"
else
    print_error "Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    print_status "Node.js found: $(node --version)"
else
    print_error "Node.js is not installed. Please install Node.js 20+"
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    print_status "Docker found: $(docker --version)"
else
    print_warning "Docker is not installed. You'll need it for database and services."
fi

# Create project structure
print_status "Creating project structure..."

mkdir -p career-hub
cd career-hub

# Create backend structure
print_status "Setting up backend..."
mkdir -p backend/{app,alembic,tests,scripts}
mkdir -p backend/app/{api/v1,core,models,schemas,services,middleware}

# Create frontend structure  
print_status "Setting up frontend..."
mkdir -p frontend/{app,components,lib,public}
mkdir -p frontend/app/{auth,profile,dashboard}
mkdir -p frontend/components/{ui,features}
mkdir -p frontend/lib/{api,hooks,utils}

# Create documentation
mkdir -p docs

# Copy environment files
print_status "Creating environment files..."

# Backend .env
cat > backend/.env << 'EOL'
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

# Environment
ENVIRONMENT=development
DEBUG=true
EOL

# Frontend .env.local
cat > frontend/.env.local << 'EOL'
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Features
NEXT_PUBLIC_ENABLE_AI_FEATURES=false
NEXT_PUBLIC_ENABLE_ANALYTICS=false
EOL

# Create Python virtual environment
print_status "Creating Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary redis passlib python-jose python-multipart python-ulid minio beautifulsoup4 pydantic pydantic-settings email-validator python-dotenv

# Initialize Alembic
print_status "Initializing database migrations..."
alembic init alembic
cat > alembic.ini << 'EOL'
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql://careerhub:careerhub_pass@localhost:5432/careerhub

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
EOL

cd ..

# Setup frontend
print_status "Setting up frontend..."
cd frontend
npm init -y
npm install next@14 react react-dom typescript @types/react @types/react-dom @types/node
npm install tailwindcss postcss autoprefixer @tanstack/react-query zustand axios
npm install @radix-ui/react-dialog @radix-ui/react-label @radix-ui/react-select
npm install react-hook-form zod @hookform/resolvers
npm install lucide-react class-variance-authority clsx tailwind-merge
npx tailwindcss init -p

cd ..

# Create docker-compose.yml at root
print_status "Creating Docker configuration..."
cat > docker-compose.yml << 'EOL'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: careerhub-db
    environment:
      POSTGRES_USER: careerhub
      POSTGRES_PASSWORD: careerhub_pass
      POSTGRES_DB: careerhub
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: careerhub-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio:latest
    container_name: careerhub-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  redis_data:
  minio_data:
EOL

# Create .gitignore
print_status "Creating .gitignore..."
cat > .gitignore << 'EOL'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Node
node_modules/
.next/
out/
dist/
*.log
npm-debug.log*

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

# Docker
docker-compose.override.yml
EOL

# Create README
print_status "Creating README..."
cat > README.md << 'EOL'
# CareerHub - Professional Profile Management Platform

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)

### Setup

1. **Start services with Docker:**
   ```bash
   docker-compose up -d
   ```

2. **Backend setup:**
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

3. **Frontend setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs
   - MinIO Console: http://localhost:9001 (minioadmin/minioadmin)

## Development

See `/docs` folder for detailed documentation.

## License

MIT
EOL

print_status "Creating initial backend application file..."
cat > backend/app/__init__.py << 'EOL'
"""CareerHub Backend Application"""

__version__ = "1.0.0"
EOL

cat > backend/app/main.py << 'EOL'
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

# Final instructions
echo ""
echo "═══════════════════════════════════════════════════════════════"
print_status "Setup completed successfully!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the database and services:"
echo "   ${GREEN}docker-compose up -d${NC}"
echo ""
echo "2. Start the backend:"
echo "   ${GREEN}cd backend${NC}"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo "   ${GREEN}uvicorn app.main:app --reload${NC}"
echo ""
echo "3. Start the frontend:"
echo "   ${GREEN}cd frontend${NC}"
echo "   ${GREEN}npm run dev${NC}"
echo ""
echo "4. Access the application:"
echo "   - Frontend: ${GREEN}http://localhost:3000${NC}"
echo "   - API Docs: ${GREEN}http://localhost:8000/api/docs${NC}"
echo ""
echo "5. Copy the documentation files from /docs to get started"
echo ""
print_warning "Remember to change SECRET_KEY in production!"
echo ""
echo "Happy coding! 🚀"
```

Make the script executable:
```bash
chmod +x setup.sh
```