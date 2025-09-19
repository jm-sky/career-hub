# API Documentation

## Base Configuration

### Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.careerhub.com/api/v1
```

### Authentication
All authenticated endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

### Response Format
```json
// Success Response
{
    "data": { ... },
    "message": "Success message (optional)"
}

// Error Response
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": [ ... ]  // Optional field-specific errors
    }
}

// Paginated Response
{
    "data": [ ... ],
    "pagination": {
        "page": 1,
        "size": 20,
        "total": 100,
        "pages": 5
    }
}
```

## Authentication Endpoints

### Register User
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "password_confirm": "SecurePassword123!"
}

Response: 201 Created
{
    "data": {
        "id": "01HKQW3F5D3QJXZB5XYQ3VWZJM",
        "email": "user@example.com",
        "plan": "FREE",
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "SecurePassword123!"
}

Response: 200 OK
{
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "token_type": "Bearer",
        "expires_in": 900  // 15 minutes
    }
}
```

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "token_type": "Bearer",
        "expires_in": 900
    }
}
```

### Logout
```http
POST /auth/logout
Authorization: Bearer <token>

Response: 200 OK
{
    "message": "Successfully logged out"
}
```

### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>

Response: 200 OK
{
    "data": {
        "id": "01HKQW3F5D3QJXZB5XYQ3VWZJM",
        "email": "user@example.com",
        "plan": "PRO",
        "plan_expires_at": "2024-02-15T00:00:00Z",
        "profile_id": "01HKQW3F5D3QJXZB5XYQ3VWZJN"
    }
}
```

## Profile Endpoints

### Get My Profile
```http
GET /profile
Authorization: Bearer <token>

Response: 200 OK
{
    "data": {
        "id": "01HKQW3F5D3QJXZB5XYQ3VWZJN",
        "slug": "john-doe",
        "headline": "Senior Software Architect",
        "summary": "20+ years of experience...",
        "location": "Warsaw, Poland",
        "visibility": "PUBLIC",
        "contact": {
            "email": "john@example.com",
            "phone": "+48 123 456 789",
            "linkedin": "https://linkedin.com/in/johndoe",
            "website": "https://johndoe.com"
        },
        "completeness_score": 85,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

### Update Profile
```http
PUT /profile
Authorization: Bearer <token>
Content-Type: application/json

{
    "headline": "Senior Software Architect & Tech Lead",
    "summary": "Updated summary...",
    "location": "Warsaw, Poland",
    "visibility": "PUBLIC",
    "contact": {
        "email": "john@example.com",
        "linkedin": "https://linkedin.com/in/johndoe"
    }
}

Response: 200 OK
{
    "data": { ... }  // Updated profile
}
```

### Get Public Profile
```http
GET /profile/{slug}

Response: 200 OK
{
    "data": {
        "slug": "john-doe",
        "headline": "Senior Software Architect",
        "summary": "20+ years of experience...",
        "location": "Warsaw, Poland",
        "experiences": [ ... ],  // Only public data
        "projects": [ ... ],
        "skills": [ ... ]
    }
}
```

### Save Draft
```http
POST /profile/draft
Authorization: Bearer <token>
Content-Type: application/json

{
    "step": "experience",
    "data": {
        "company_name": "Tech Corp",
        "position": "Software Engineer"
    }
}

Response: 200 OK
{
    "message": "Draft saved successfully"
}
```

## Experience Endpoints

### List Experiences
```http
GET /experiences
Authorization: Bearer <token>

Response: 200 OK
{
    "data": [
        {
            "id": "01HKQW3F5D3QJXZB5XYQ3VWZJP",
            "company_name": "Tech Corp",
            "company_website": "https://techcorp.com",
            "company_size": "1000-5000",
            "industry": "Software Development",
            "company_location": "Warsaw, Poland",
            "position": "Senior Software Architect",
            "employment_type": "FULL_TIME",
            "start_date": "2020-01-15",
            "end_date": null,
            "is_current": true,
            "responsibilities": [
                "Designing scalable microservices architecture",
                "Leading team of 8 developers",
                "Code review and mentoring"
            ],
            "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis"],
            "display_order": 0
        }
    ]
}
```

### Create Experience
```http
POST /experiences
Authorization: Bearer <token>
Content-Type: application/json

{
    "company_name": "New Company",
    "company_website": "https://newcompany.com",
    "company_size": "50-200",
    "industry": "FinTech",
    "company_location": "Warsaw, Poland",
    "position": "Lead Developer",
    "employment_type": "FULL_TIME",
    "start_date": "2018-03-01",
    "end_date": "2019-12-31",
    "is_current": false,
    "responsibilities": [
        "Building payment processing system",
        "Team leadership"
    ],
    "technologies": ["Java", "Spring Boot", "MySQL"]
}

Response: 201 Created
{
    "data": { ... }  // Created experience
}
```

### Update Experience
```http
PUT /experiences/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "position": "Senior Lead Developer",
    "responsibilities": [
        "Building payment processing system",
        "Team leadership",
        "Architecture decisions"
    ]
}

Response: 200 OK
{
    "data": { ... }  // Updated experience
}
```

### Delete Experience
```http
DELETE /experiences/{id}
Authorization: Bearer <token>

Response: 204 No Content
```

### Reorder Experiences
```http
PUT /experiences/reorder
Authorization: Bearer <token>
Content-Type: application/json

{
    "order": [
        "01HKQW3F5D3QJXZB5XYQ3VWZJP",
        "01HKQW3F5D3QJXZB5XYQ3VWZJQ",
        "01HKQW3F5D3QJXZB5XYQ3VWZJR"
    ]
}

Response: 200 OK
{
    "message": "Experiences reordered successfully"
}
```

## Project Endpoints

### List Projects
```http
GET /projects
Authorization: Bearer <token>

Response: 200 OK
{
    "data": [
        {
            "id": "01HKQW3F5D3QJXZB5XYQ3VWZJS",
            "name": "E-commerce Platform Redesign",
            "description": "Complete redesign of legacy e-commerce system...",
            "role": "Technical Lead",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "is_ongoing": false,
            "is_anonymized": false,
            "visibility": "PUBLIC",
            "technologies": ["React", "Node.js", "PostgreSQL"],
            "linked_experiences": ["01HKQW3F5D3QJXZB5XYQ3VWZJP"],
            "linked_skills": ["01HKQW3F5D3QJXZB5XYQ3VWZJT"]
        }
    ]
}
```

### Create Project
```http
POST /projects
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Banking System Migration",
    "description": "Led migration of core banking system to cloud...",
    "role": "Solution Architect",
    "start_date": "2022-06-01",
    "end_date": "2023-05-31",
    "is_anonymized": true,
    "anonymized_company": "Major European Bank",
    "technologies": ["AWS", "Kubernetes", "Terraform"]
}

Response: 201 Created
{
    "data": { ... }  // Created project
}
```

### Link Experience to Project
```http
POST /projects/{project_id}/link-experience
Authorization: Bearer <token>
Content-Type: application/json

{
    "experience_id": "01HKQW3F5D3QJXZB5XYQ3VWZJP"
}

Response: 200 OK
{
    "message": "Experience linked successfully"
}
```

### Link Skill to Project
```http
POST /projects/{project_id}/link-skill
Authorization: Bearer <token>
Content-Type: application/json

{
    "skill_id": "01HKQW3F5D3QJXZB5XYQ3VWZJT"
}

Response: 200 OK
{
    "message": "Skill linked successfully"
}
```

## Skills Endpoints

### List Skills
```http
GET /skills
Authorization: Bearer <token>

Response: 200 OK
{
    "data": [
        {
            "id": "01HKQW3F5D3QJXZB5XYQ3VWZJT",
            "name": "Python",
            "category": "TECHNICAL",
            "level": 5,
            "years_of_experience": 15,
            "is_primary": true
        }
    ]
}
```

### Add Skills (Bulk)
```http
POST /skills/bulk
Authorization: Bearer <token>
Content-Type: application/json

{
    "skills": [
        {
            "name": "FastAPI",
            "category": "TECHNICAL",
            "level": 5,
            "years_of_experience": 3
        },
        {
            "name": "Docker",
            "category": "TOOLS",
            "level": 4,
            "years_of_experience": 7
        }
    ]
}

Response: 201 Created
{
    "data": {
        "created": 2,
        "skipped": 0,
        "skills": [ ... ]
    }
}
```

### Get Skill Suggestions
```http
GET /skills/suggestions?role=Software%20Architect
Authorization: Bearer <token>

Response: 200 OK
{
    "data": {
        "suggestions": [
            "System Design",
            "Microservices",
            "Cloud Architecture",
            "API Design",
            "Database Design"
        ]
    }
}
```

## CV Generation Endpoints

### List CV Versions
```http
GET /cv-versions
Authorization: Bearer <token>

Response: 200 OK
{
    "data": [
        {
            "id": "01HKQW3F5D3QJXZB5XYQ3VWZJU",
            "name": "Technical Lead - Full Stack",
            "template": "modern",
            "is_default": true,
            "created_at": "2024-01-15T10:30:00Z",
            "pdf_url": "https://storage.careerhub.com/cvs/..."
        }
    ]
}
```

### Create CV Version
```http
POST /cv-versions
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Solution Architect - Cloud",
    "template": "modern",
    "sections_config": {
        "include_photo": false,
        "include_summary": true,
        "experiences": [
            "01HKQW3F5D3QJXZB5XYQ3VWZJP",
            "01HKQW3F5D3QJXZB5XYQ3VWZJQ"
        ],
        "projects": ["01HKQW3F5D3QJXZB5XYQ3VWZJS"],
        "skills": ["01HKQW3F5D3QJXZB5XYQ3VWZJT"],
        "custom_summary": "Experienced architect focused on cloud solutions..."
    }
}

Response: 201 Created
{
    "data": { ... }  // Created CV version
}
```

### Generate PDF
```http
POST /cv-versions/{id}/generate
Authorization: Bearer <token>

Response: 202 Accepted
{
    "data": {
        "job_id": "01HKQW3F5D3QJXZB5XYQ3VWZJV",
        "status": "processing",
        "message": "PDF generation started"
    }
}
```

### Download CV PDF
```http
GET /cv-versions/{id}/download
Authorization: Bearer <token>

Response: 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="cv-john-doe.pdf"
[Binary PDF data]
```

## Import/Export Endpoints

### Import from LinkedIn
```http
POST /import/linkedin
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
    "file": <linkedin_profile.html>
}

Response: 202 Accepted
{
    "data": {
        "import_id": "01HKQW3F5D3QJXZB5XYQ3VWZJW",
        "status": "processing",
        "message": "Import started, check status for progress"
    }
}
```

### Parse Copy-Paste Text
```http
POST /import/parse-text
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "John Doe\nSenior Software Architect at Tech Corp\n..."
}

Response: 200 OK
{
    "data": {
        "parsed": {
            "name": "John Doe",
            "headline": "Senior Software Architect at Tech Corp",
            "experiences": [ ... ]
        }
    }
}
```

### Export Profile as JSON
```http
GET /export/json
Authorization: Bearer <token>

Response: 200 OK
Content-Type: application/json
Content-Disposition: attachment; filename="profile-export.json"
{
    "profile": { ... },
    "experiences": [ ... ],
    "projects": [ ... ],
    "skills": [ ... ],
    "export_date": "2024-01-15T10:30:00Z"
}
```

## AI Enhancement Endpoints

### Optimize Description
```http
POST /ai/optimize-description
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "I worked on building software and managing team",
    "context": "Senior Developer role"
}

Response: 200 OK
{
    "data": {
        "original": "I worked on building software and managing team",
        "optimized": "Led cross-functional team of 8 engineers in designing and implementing scalable software solutions, resulting in 40% improvement in system performance",
        "suggestions": [
            "Add specific metrics",
            "Mention technologies used",
            "Include business impact"
        ]
    }
}
```

### Suggest Responsibilities
```http
POST /ai/suggest-responsibilities
Authorization: Bearer <token>
Content-Type: application/json

{
    "role": "Software Architect",
    "seniority": "SENIOR",
    "existing": [
        "System design",
        "Code reviews"
    ]
}

Response: 200 OK
{
    "data": {
        "suggestions": [
            "Define and enforce architectural standards and best practices",
            "Collaborate with product owners to translate business requirements into technical solutions",
            "Conduct architectural reviews and provide recommendations",
            "Mentor development teams on architectural patterns",
            "Evaluate and recommend new technologies and tools"
        ]
    }
}
```

### Analyze Profile
```http
POST /ai/analyze-profile
Authorization: Bearer <token>
Content-Type: application/json

{
    "target_role": "Cloud Solutions Architect"
}

Response: 200 OK
{
    "data": {
        "match_score": 78,
        "strengths": [
            "Strong experience with microservices",
            "AWS certifications",
            "Leadership experience"
        ],
        "gaps": [
            "Limited Kubernetes experience",
            "No Azure/GCP experience mentioned",
            "Consider adding DevOps practices"
        ],
        "recommendations": [
            "Highlight your AWS Lambda experience",
            "Add specific cloud migration projects",
            "Get Kubernetes certification"
        ]
    }
}
```

## Error Codes

| Code | Description | HTTP Status |
|------|------------|-------------|
| `UNAUTHORIZED` | Missing or invalid authentication | 401 |
| `FORBIDDEN` | Insufficient permissions | 403 |
| `NOT_FOUND` | Resource not found | 404 |
| `VALIDATION_ERROR` | Invalid input data | 400 |
| `DUPLICATE_ENTRY` | Resource already exists | 409 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `INTERNAL_ERROR` | Server error | 500 |
| `SERVICE_UNAVAILABLE` | Service temporarily unavailable | 503 |

## Rate Limiting

| Endpoint Category | Free | Pro | Expert |
|------------------|------|-----|---------|
| Auth endpoints | 10/hour | 20/hour | 50/hour |
| Profile read | 100/hour | 500/hour | Unlimited |
| Profile write | 20/hour | 100/hour | 500/hour |
| AI endpoints | 5/hour | 50/hour | 200/hour |
| PDF generation | 5/day | 50/day | 200/day |
| Import/Export | 3/day | 20/day | 100/day |

## Pagination

All list endpoints support pagination:
```
GET /experiences?page=1&size=20&sort=start_date:desc
```

Parameters:
- `page`: Page number (default: 1)
- `size`: Items per page (default: 20, max: 100)
- `sort`: Field and direction (format: `field:asc|desc`)

## Filtering

List endpoints support filtering:
```
GET /projects?is_anonymized=true&start_date_gte=2020-01-01
```

Common filters:
- `field_eq`: Exact match
- `field_ne`: Not equal
- `field_gt`: Greater than
- `field_gte`: Greater than or equal
- `field_lt`: Less than
- `field_lte`: Less than or equal
- `field_like`: Partial match
- `field_in`: In list (comma-separated)