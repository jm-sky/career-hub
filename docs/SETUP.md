# Development Environment Setup Guide

## Overview

This guide walks you through setting up the CareerHub development environment on your local machine.

## Prerequisites

### Required Software
- **Python 3.11+** - Backend runtime
- **Node.js 20+** - Frontend runtime  
- **Docker & Docker Compose** - For database and services
- **Git** - Version control

### Recommended Tools
- **VS Code** - IDE with Python and TypeScript extensions
- **PostgreSQL Client** - For database management (optional, can use Adminer)
- **Postman** - For API testing

## Quick Setup

### Option 1: Automated Setup (Recommended)

Use the provided setup script for automatic project initialization:

```bash
# Clone or download the project
git clone <repository-url>
cd career-hub

# Run the automated setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Copy environment configuration
cp .env.example .env
# Edit .env with your custom settings if needed
```

The script will:
- Check prerequisites
- Create project structure
- Set up Python virtual environment
- Install dependencies
- Create configuration files
- Initialize database migrations

### Option 2: Manual Setup

If you prefer manual setup or need to customize the process:

#### 1. Project Structure

Create the basic project structure:

```bash
mkdir career-hub && cd career-hub

# Backend structure
mkdir -p backend/{app,alembic,tests,scripts}
mkdir -p backend/app/{api/v1,core,models,schemas,services,middleware}

# Frontend structure
mkdir -p frontend/{app,components,lib,public}
mkdir -p frontend/app/{auth,profile,dashboard}
mkdir -p frontend/components/{ui,features}
mkdir -p frontend/lib/{api,hooks,utils}

# Documentation
mkdir -p docs
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
# Edit .env with your settings

# Initialize database migrations
alembic init alembic
alembic upgrade head
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment configuration
cp .env.example .env.local
# Edit .env.local with your settings

# Generate Tailwind CSS configuration
npx tailwindcss init -p
```

#### 4. Services Setup

```bash
# Start database and supporting services
docker-compose up -d db redis minio

# Verify services are running
docker-compose ps
```

## Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://careerhub:careerhub_pass@localhost:5432/careerhub

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30

# Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=careerhub
MINIO_SECURE=false

# Email (optional for development)
EMAIL_ENABLED=false
EMAIL_FROM=noreply@careerhub.com

# Environment
ENVIRONMENT=development
DEBUG=true
```

#### Frontend (.env.local)
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Features
NEXT_PUBLIC_ENABLE_AI_FEATURES=false
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

### Database Setup

1. **Start PostgreSQL:**
   ```bash
   docker-compose up -d db
   ```

2. **Run migrations:**
   ```bash
   cd backend
   source venv/bin/activate
   alembic upgrade head
   ```

3. **Verify connection:**
   ```bash
   python -c "from app.core.database import engine; print('Database connected!')"
   ```

## Running the Application

### Development Mode

1. **Start services:**
   ```bash
   docker-compose up -d
   ```

2. **Start backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

### Access Points

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API Alternative Docs:** http://localhost:8000/redoc
- **MinIO Console:** http://localhost:9001 (minioadmin/minioadmin)
- **Database Admin:** http://localhost:8080 (if Adminer is enabled)

## Development Workflow

### 1. Code Structure

Follow the established patterns:
- **Backend:** Service layer pattern with dependency injection
- **Frontend:** Component-based architecture with custom hooks
- **Database:** Migration-first approach

### 2. Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests  
cd frontend
npm test
```

### 3. Code Quality

```bash
# Backend linting
cd backend
ruff check .
black .

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

## Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check if PostgreSQL is running
docker-compose ps db

# Check logs
docker-compose logs db

# Reset database
docker-compose down
docker volume rm career-hub_postgres_data
docker-compose up -d db
```

#### Python Dependencies Conflict
```bash
# Clear virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Node Modules Issues
```bash
# Clear node modules
rm -rf node_modules package-lock.json
npm install
```

#### Port Already in Use
```bash
# Find process using port
lsof -i :8000  # or :3000, :5432

# Kill process
kill -9 <PID>
```

### Health Checks

Verify everything is working:

```bash
# Check backend health
curl http://localhost:8000/health

# Check database connection
docker-compose exec db psql -U careerhub -d careerhub -c "SELECT 1;"

# Check Redis
docker-compose exec redis redis-cli ping

# Check MinIO
curl http://localhost:9000/minio/health/live
```

## Next Steps

After successful setup:

1. **Review Documentation:** Read through `/docs` folder
2. **Explore API:** Visit http://localhost:8000/docs
3. **Run Tests:** Ensure everything works
4. **Start Development:** Follow the implementation plan

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review Docker Compose logs: `docker-compose logs`
3. Check application logs
4. Consult the detailed documentation in `/docs`

---

## File Structure After Setup

```
career-hub/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Core functionality
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── alembic/             # Database migrations
│   ├── tests/               # Test files
│   ├── venv/                # Virtual environment
│   ├── .env                 # Environment variables
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities and hooks
│   ├── node_modules/        # NPM dependencies
│   ├── .env.local           # Environment variables
│   └── package.json         # NPM configuration
├── docs/                    # Documentation
├── scripts/                 # Setup and utility scripts
├── docker-compose.yml       # Services configuration
└── README.md               # Project overview
```