# Implementation Plan

## Phase 1: Foundation (Weeks 1-2)

### Sprint 0: Project Setup
**Duration:** 1 week

#### Backend Setup
```bash
# Initialize FastAPI project
career-hub-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── core/
│   │   ├── config.py        # Settings
│   │   ├── security.py      # JWT, hashing
│   │   └── database.py      # DB connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       └── profile.py
│   └── services/            # Business logic
├── alembic/                 # Migrations
├── tests/
├── requirements.txt
├── .env.example
└── Dockerfile
```

#### Frontend Setup
```bash
# Initialize Next.js project
career-hub-frontend/
├── app/                     # App Router
│   ├── layout.tsx
│   ├── page.tsx
│   ├── auth/
│   └── profile/
├── components/
│   ├── ui/                  # shadcn/ui components
│   └── features/
├── lib/
│   ├── api/                 # API client
│   ├── hooks/               # Custom hooks
│   └── utils/
├── public/
├── package.json
└── Dockerfile
```

#### Tasks Checklist
- [ ] Initialize Git repository with .gitignore
- [ ] Setup FastAPI project structure
- [ ] Configure PostgreSQL database
- [ ] Setup Redis for caching
- [ ] Create base SQLAlchemy models
- [ ] Setup Alembic for migrations
- [ ] Initialize Next.js with TypeScript
- [ ] Install and configure Tailwind CSS
- [ ] Setup shadcn/ui components
- [ ] Configure environment variables
- [ ] Docker Compose for local development
- [ ] Setup GitHub Actions CI/CD

### Sprint 1: Authentication System
**Duration:** 1 week

#### Backend Tasks
```python
# Core authentication features to implement
- User registration with email validation
- Login with JWT tokens
- Refresh token mechanism
- Password reset flow
- Email service integration
```

#### Frontend Tasks
```typescript
// Authentication UI components
- Registration form with validation
- Login form
- Password reset flow
- Protected route wrapper
- Auth context provider
```

#### Implementation Code Samples

**Backend - User Model:**
```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from ulid import ULID
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(ULID()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    plan = Column(String(20), default="FREE")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Backend - Auth Endpoint:**
```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, auth_service: AuthService = Depends()):
    user = await auth_service.create_user(user_data)
    tokens = await auth_service.create_tokens(user)
    return tokens

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, auth_service: AuthService = Depends()):
    user = await auth_service.authenticate(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    tokens = await auth_service.create_tokens(user)
    return tokens
```

**Frontend - Auth Hook:**
```typescript
// lib/hooks/useAuth.ts
import { create } from 'zustand';
import { api } from '@/lib/api';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    const { access_token, refresh_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    
    const user = await api.get('/auth/me');
    set({ user: user.data });
  },
  
  logout: async () => {
    await api.post('/auth/logout');
    localStorage.clear();
    set({ user: null });
  },
  
  register: async (data) => {
    await api.post('/auth/register', data);
  }
}));
```

## Phase 2: Core Profile Management (Weeks 3-4)

### Sprint 2: Profile CRUD & Wizard
**Duration:** 1 week

#### Key Features
1. Profile creation wizard with draft saving
2. Step-by-step onboarding flow
3. Profile editing interface
4. Draft auto-save mechanism

#### Wizard Implementation
```typescript
// components/features/ProfileWizard/index.tsx
interface WizardStep {
  id: string;
  title: string;
  component: React.ComponentType;
  validation: ZodSchema;
}

const steps: WizardStep[] = [
  {
    id: 'basic',
    title: 'Basic Information',
    component: BasicInfoStep,
    validation: basicInfoSchema
  },
  {
    id: 'experience',
    title: 'Work Experience',
    component: ExperienceStep,
    validation: experienceSchema
  },
  {
    id: 'projects',
    title: 'Key Projects',
    component: ProjectsStep,
    validation: projectsSchema
  },
  {
    id: 'skills',
    title: 'Skills & Expertise',
    component: SkillsStep,
    validation: skillsSchema
  }
];

export function ProfileWizard() {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});
  
  // Auto-save draft every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      saveDraft(formData);
    }, 30000);
    
    return () => clearInterval(interval);
  }, [formData]);
  
  // Component implementation...
}
```

### Sprint 3: Experience Management
**Duration:** 1 week

#### Features to Implement
- Add/Edit/Delete experiences
- Rich company information
- Responsibilities management with suggestions
- Technology tags
- Drag-and-drop reordering

#### Responsibilities System
```python
# app/services/responsibilities.py
class ResponsibilitiesService:
    def __init__(self):
        self.common_responsibilities = {
            "Software Engineer": [
                "Writing clean, maintainable code",
                "Participating in code reviews",
                "Collaborating with cross-functional teams",
                "Debugging and troubleshooting issues"
            ],
            "Software Architect": [
                "Designing system architecture",
                "Making technology decisions",
                "Creating technical documentation",
                "Reviewing architectural proposals"
            ],
            # More roles...
        }
    
    async def get_suggestions(self, role: str, existing: List[str]) -> List[str]:
        """Get responsibility suggestions based on role"""
        base_suggestions = self.common_responsibilities.get(role, [])
        
        # Filter out existing responsibilities
        suggestions = [s for s in base_suggestions if s not in existing]
        
        # Add AI-powered suggestions in the future
        return suggestions[:5]
```

## Phase 3: Advanced Features (Weeks 5-6)

### Sprint 4: Projects & Skills
**Duration:** 1 week

#### Project Management Features
```typescript
// Project relationship manager
interface ProjectFormData {
  name: string;
  description: string;
  role: string;
  startDate: Date;
  endDate?: Date;
  isAnonymized: boolean;
  anonymizedCompany?: string;
  linkedExperiences: string[];
  linkedSkills: string[];
  technologies: string[];
}

// Many-to-many relationship handler
async function linkProjectRelations(
  projectId: string, 
  data: ProjectFormData
) {
  // Link to experiences
  for (const expId of data.linkedExperiences) {
    await api.post(`/projects/${projectId}/link-experience`, {
      experience_id: expId
    });
  }
  
  // Link to skills
  for (const skillId of data.linkedSkills) {
    await api.post(`/projects/${projectId}/link-skill`, {
      skill_id: skillId
    });
  }
}
```

### Sprint 5: LinkedIn Import
**Duration:** 1 week

#### Import Parser Implementation
```python
# app/services/linkedin_parser.py
from bs4 import BeautifulSoup
import json

class LinkedInParser:
    def parse_html(self, html_content: str) -> dict:
        """Parse LinkedIn HTML export"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        profile_data = {
            'basic_info': self._parse_basic_info(soup),
            'experiences': self._parse_experiences(soup),
            'education': self._parse_education(soup),
            'skills': self._parse_skills(soup)
        }
        
        return profile_data
    
    def _parse_basic_info(self, soup):
        # Extract name, headline, summary
        name = soup.find('h1', class_='top-card-layout__title')
        headline = soup.find('h2', class_='top-card-layout__headline')
        
        return {
            'name': name.text.strip() if name else '',
            'headline': headline.text.strip() if headline else ''
        }
    
    def _parse_experiences(self, soup):
        experiences = []
        exp_section = soup.find('section', {'id': 'experience'})
        
        if exp_section:
            for exp in exp_section.find_all('li'):
                experiences.append({
                    'company': exp.find('span', class_='experience-item__subtitle').text,
                    'position': exp.find('span', class_='experience-item__title').text,
                    'duration': exp.find('span', class_='experience-item__duration').text
                })
        
        return experiences
```

## Phase 4: CV Generation (Weeks 7-8)

### Sprint 6: CV Builder & PDF Generation
**Duration:** 2 weeks

#### CV Template System
```python
# app/services/cv_generator.py
from weasyprint import HTML, CSS
from jinja2 import Template

class CVGenerator:
    def __init__(self):
        self.templates = {
            'modern': 'templates/cv_modern.html',
            'classic': 'templates/cv_classic.html',
            'minimal': 'templates/cv_minimal.html'
        }
    
    async def generate_pdf(self, cv_version_id: str) -> bytes:
        """Generate PDF from CV version"""
        # Load CV version data
        cv_data = await self.get_cv_data(cv_version_id)
        
        # Load template
        template_path = self.templates[cv_data.template]
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        # Render HTML
        html_content = template.render(
            profile=cv_data.profile,
            experiences=cv_data.experiences,
            projects=cv_data.projects,
            skills=cv_data.skills
        )
        
        # Generate PDF
        pdf = HTML(string=html_content).write_pdf()
        
        # Store in S3
        pdf_url = await self.store_pdf(pdf, cv_version_id)
        
        return pdf_url
```

#### CV Template Example
```html
<!-- templates/cv_modern.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Helvetica', sans-serif;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .header {
            border-bottom: 2px solid #2563eb;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 {
            color: #1e40af;
            margin: 0;
            font-size: 32px;
        }
        .section {
            margin-bottom: 30px;
        }
        .experience-item {
            margin-bottom: 20px;
        }
        .company {
            font-weight: bold;
            color: #1e40af;
        }
        .position {
            font-size: 18px;
            font-weight: bold;
        }
        .duration {
            color: #666;
            font-size: 14px;
        }
        .responsibilities {
            list-style-type: disc;
            margin-left: 20px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ profile.name }}</h1>
        <p>{{ profile.headline }}</p>
        <p>{{ profile.location }} | {{ profile.contact.email }}</p>
    </div>
    
    <div class="section">
        <h2>Professional Summary</h2>
        <p>{{ profile.summary }}</p>
    </div>
    
    <div class="section">
        <h2>Work Experience</h2>
        {% for exp in experiences %}
        <div class="experience-item">
            <div class="position">{{ exp.position }}</div>
            <div class="company">{{ exp.company_name }}</div>
            <div class="duration">{{ exp.start_date }} - {{ exp.end_date or 'Present' }}</div>
            <ul class="responsibilities">
                {% for resp in exp.responsibilities %}
                <li>{{ resp }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </div>
    
    <!-- More sections... -->
</body>
</html>
```

## Phase 5: Public Profile & Polish (Weeks 9-10)

### Sprint 7: Public Profile
**Duration:** 1 week

#### SEO-Optimized Public Profile
```typescript
// app/profile/[slug]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const profile = await getPublicProfile(params.slug);
  
  return {
    title: `${profile.name} - ${profile.headline}`,
    description: profile.summary?.substring(0, 160),
    openGraph: {
      title: profile.name,
      description: profile.headline,
      type: 'profile',
      url: `https://careerhub.com/p/${params.slug}`,
    },
    twitter: {
      card: 'summary',
      title: profile.name,
      description: profile.headline,
    },
  };
}

export default async function PublicProfile({ params }) {
  const profile = await getPublicProfile(params.slug);
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Structured data for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Person',
            name: profile.name,
            jobTitle: profile.headline,
            description: profile.summary,
          }),
        }}
      />
      
      {/* Profile content */}
      <ProfileHeader profile={profile} />
      <ProfileExperiences experiences={profile.experiences} />
      <ProfileProjects projects={profile.projects} />
      <ProfileSkills skills={profile.skills} />
    </div>
  );
}
```

### Sprint 8: Testing & Optimization
**Duration:** 1 week

#### Testing Strategy
```python
# tests/test_profile.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers(test_user):
    """Get auth headers for test user"""
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "testpass123"
    })
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_profile(auth_headers):
    """Test profile creation"""
    response = client.post(
        "/api/v1/profile",
        json={
            "headline": "Senior Developer",
            "summary": "Test summary",
            "location": "Warsaw, Poland"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    assert response.json()["data"]["headline"] == "Senior Developer"

def test_profile_completeness(auth_headers, profile_with_data):
    """Test profile completeness calculation"""
    response = client.get("/api/v1/profile", headers=auth_headers)
    
    completeness = response.json()["data"]["completeness_score"]
    assert 0 <= completeness <= 100
```

#### Performance Optimization
```python
# Database query optimization
from sqlalchemy.orm import joinedload

class ProfileService:
    async def get_full_profile(self, profile_id: str):
        """Get profile with all related data in one query"""
        return await db.query(Profile)\
            .options(
                joinedload(Profile.experiences),
                joinedload(Profile.projects).joinedload(Project.skills),
                joinedload(Profile.skills),
                joinedload(Profile.education)
            )\
            .filter(Profile.id == profile_id)\
            .first()
```

## Deployment Strategy

### Infrastructure Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/careerhub
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"
  
  frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    ports:
      - "3000:3000"
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=careerhub
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Production Deployment
```bash
# GitHub Actions deployment workflow
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and push Docker images
      run: |
        docker build -t careerhub/backend:${{ github.sha }} ./backend
        docker build -t careerhub/frontend:${{ github.sha }} ./frontend
        docker push careerhub/backend:${{ github.sha }}
        docker push careerhub/frontend:${{ github.sha }}
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_KEY }}
        script: |
          cd /opt/careerhub
          docker-compose pull
          docker-compose up -d
          docker-compose run backend alembic upgrade head
```

## Monitoring & Maintenance

### Key Metrics to Track
```python
# app/core/monitoring.py
from prometheus_client import Counter, Histogram, Gauge

# Business metrics
user_registrations = Counter('user_registrations_total', 'Total user registrations')
cv_generations = Counter('cv_generations_total', 'Total CV generations')
profile_completeness = Gauge('profile_completeness_average', 'Average profile completeness')

# Technical metrics
api_requests = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration')
db_query_duration = Histogram('db_query_duration_seconds', 'Database query duration')

# Health checks
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": await check_database(),
        "redis": await check_redis(),
        "storage": await check_storage()
    }
```

### Backup Strategy
```bash
#!/bin/bash
# Daily backup script

# Database backup
pg_dump -U $DB_USER -h $DB_HOST $DB_NAME | gzip > backup_$(date +%Y%m%d).sql.gz

# Upload to S3
aws s3 cp backup_$(date +%Y%m%d).sql.gz s3://careerhub-backups/db/

# Clean old backups (keep 30 days)
find /backups -name "backup_*.sql.gz" -mtime +30 -delete
```

## Success Criteria

### MVP Launch Checklist
- [ ] Authentication working (register/login/logout)
- [ ] Profile wizard complete with draft saving
- [ ] Experience management CRUD
- [ ] Project management with relationships
- [ ] Skills management
- [ ] LinkedIn import functional
- [ ] CV generation (1 template)
- [ ] PDF export working
- [ ] Public profile accessible
- [ ] Mobile responsive
- [ ] Performance: <2s page load
- [ ] Security: HTTPS, rate limiting
- [ ] Monitoring: Sentry, basic metrics
- [ ] Documentation complete
- [ ] Deployed to production

### Post-Launch Priorities
1. User feedback collection
2. Bug fixes and performance optimization
3. AI features (Pro/Expert tiers)
4. Additional CV templates
5. Payment integration
6. Email notifications
7. Advanced analytics
8. API for third-party integrations