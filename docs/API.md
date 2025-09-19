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
        "code": "VALIDATION_ERROR", // Error code
        "message": "Validation failed", // Human-readable error message
        "details": [ // Optional field-specific errors
            {"field": "email", "message": "Invalid email format"},
            {"field": "password", "message": "Password must be at least 8 characters"}
        ]
    }
}

// Error Response (Simple)
{
    "error": {
        "code": "NOT_FOUND",
        "message": "Resource not found"
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
    "passwordConfirm": "SecurePassword123!"
}

Response: 201 Created
{
    "data": {
        "id": "01HKQW3F5D3QJXZB5XYQ3VWZJM",
        "email": "user@example.com",
        "plan": "FREE",
        "createdAt": "2024-01-15T10:30:00Z"
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
        "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "tokenType": "Bearer",
        "expiresIn": 900  // 15 minutes
    }
}
```

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
    "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
    "data": {
        "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "tokenType": "Bearer",
        "expiresIn": 900
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
        "planExpiresAt": "2024-02-15T00:00:00Z",
        "profileId": "01HKQW3F5D3QJXZB5XYQ3VWZJN"
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
        "completenessScore": 85,
        "createdAt": "2024-01-15T10:30:00Z",
        "updatedAt": "2024-01-15T10:30:00Z"
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
        "companyName": "Tech Corp",
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
            "companyName": "Tech Corp",
            "companyWebsite": "https://techcorp.com",
            "companySize": "1000-5000",
            "industry": "Software Development",
            "companyLocation": "Warsaw, Poland",
            "position": "Senior Software Architect",
            "employmentType": "FULL_TIME",
            "startDate": "2020-01-15",
            "endDate": null,
            "isCurrent": true,
            "responsibilities": [
                "Designing scalable microservices architecture",
                "Leading team of 8 developers",
                "Code review and mentoring"
            ],
            "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis"],
            "displayOrder": 0
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
    "companyName": "New Company",
    "companyWebsite": "https://newcompany.com",
    "companySize": "50-200",
    "industry": "FinTech",
    "companyLocation": "Warsaw, Poland",
    "position": "Lead Developer",
    "employmentType": "FULL_TIME",
    "startDate": "2018-03-01",
    "endDate": "2019-12-31",
    "isCurrent": false,
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
            "startDate": "2023-01-01",
            "endDate": "2023-12-31",
            "isOngoing": false,
            "isAnonymized": false,
            "visibility": "PUBLIC",
            "technologies": ["React", "Node.js", "PostgreSQL"],
            "linkedExperiences": ["01HKQW3F5D3QJXZB5XYQ3VWZJP"],
            "linkedSkills": ["01HKQW3F5D3QJXZB5XYQ3VWZJT"]
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
    "startDate": "2022-06-01",
    "endDate": "2023-05-31",
    "isAnonymized": true,
    "anonymizedCompany": "Major European Bank",
    "technologies": ["AWS", "Kubernetes", "Terraform"]
}

Response: 201 Created
{
    "data": { ... }  // Created project
}
```

### Link Experience to Project
```http
POST /projects/{projectId}/link-experience
Authorization: Bearer <token>
Content-Type: application/json

{
    "experienceId": "01HKQW3F5D3QJXZB5XYQ3VWZJP"
}

Response: 200 OK
{
    "message": "Experience linked successfully"
}
```

### Link Skill to Project
```http
POST /projects/{projectId}/link-skill
Authorization: Bearer <token>
Content-Type: application/json

{
    "skillId": "01HKQW3F5D3QJXZB5XYQ3VWZJT"
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
            "yearsOfExperience": 15,
            "isPrimary": true
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
            "yearsOfExperience": 3
        },
        {
            "name": "Docker",
            "category": "TOOLS",
            "level": 4,
            "yearsOfExperience": 7
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
            "isDefault": true,
            "createdAt": "2024-01-15T10:30:00Z",
            "pdfUrl": "https://storage.careerhub.com/cvs/..."
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
    "sectionsConfig": {
        "includePhoto": false,
        "includeSummary": true,
        "experiences": [
            "01HKQW3F5D3QJXZB5XYQ3VWZJP",
            "01HKQW3F5D3QJXZB5XYQ3VWZJQ"
        ],
        "projects": ["01HKQW3F5D3QJXZB5XYQ3VWZJS"],
        "skills": ["01HKQW3F5D3QJXZB5XYQ3VWZJT"],
        "customSummary": "Experienced architect focused on cloud solutions..."
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
        "jobId": "01HKQW3F5D3QJXZB5XYQ3VWZJV",
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
        "importId": "01HKQW3F5D3QJXZB5XYQ3VWZJW",
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
    "exportDate": "2024-01-15T10:30:00Z"
}
```

## Health Check Endpoints

### System Health
```http
GET /health

Response: 200 OK
{
    "data": {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2024-01-15T10:30:00Z",
        "services": {
            "database": "healthy",
            "redis": "healthy",
            "minio": "healthy"
        }
    }
}
```

## Subscription Management Endpoints

### Get Current Plan
```http
GET /subscription
Authorization: Bearer <token>

Response: 200 OK
{
    "data": {
        "plan": "PRO",
        "planExpiresAt": "2024-02-15T00:00:00Z",
        "features": {
            "unlimitedCvVersions": true,
            "noWatermark": true,
            "aiSuggestions": true
        },
        "usage": {
            "cvVersionsCreated": 15,
            "aiRequestsUsed": 45
        }
    }
}
```

### Upgrade Plan
```http
POST /subscription/upgrade
Authorization: Bearer <token>
Content-Type: application/json

{
    "plan": "EXPERT",
    "paymentMethod": "stripe_pm_123456"
}

Response: 200 OK
{
    "data": {
        "subscriptionId": "sub_123456",
        "plan": "EXPERT",
        "planExpiresAt": "2025-01-15T00:00:00Z",
        "paymentStatus": "succeeded"
    }
}
```

### Cancel Subscription
```http
DELETE /subscription
Authorization: Bearer <token>

Response: 200 OK
{
    "message": "Subscription cancelled. Access will continue until plan expiration."
}
```

## Audit Log Endpoints

### Get Audit Log
```http
GET /audit-log
Authorization: Bearer <token>

Response: 200 OK
{
    "data": [
        {
            "id": "01HKQW3F5D3QJXZB5XYQ3VWZJX",
            "action": "PROFILE_UPDATE",
            "entityType": "profile",
            "entityId": "01HKQW3F5D3QJXZB5XYQ3VWZJN",
            "changes": {
                "headline": {
                    "old": "Software Engineer",
                    "new": "Senior Software Engineer"
                }
            },
            "ipAddress": "192.168.1.1",
            "userAgent": "Mozilla/5.0...",
            "createdAt": "2024-01-15T10:30:00Z"
        }
    ],
    "pagination": {
        "page": 1,
        "size": 20,
        "total": 45,
        "pages": 3
    }
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
    "targetRole": "Cloud Solutions Architect"
}

Response: 200 OK
{
    "data": {
        "matchScore": 78,
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

| Code               | Description    | HTTP Status |
|--------------------|----------------|-------------|
| `UNAUTHORIZED`     | Missing or invalid authentication | 401 |
| `FORBIDDEN`        | Insufficient permissions | 403 |
| `NOT_FOUND`        | Resource not found   | 404 |
| `VALIDATION_ERROR` | Invalid input data   | 400 |
| `DUPLICATE_ENTRY`  | Resource already exists | 409 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `INTERNAL_ERROR`   | Server error         | 500 |
| `SERVICE_UNAVAILABLE` | Service temporarily unavailable | 503 |

## Rate Limiting

| Endpoint Category | Free       | Pro        | Expert     |
|-------------------|------------|------------|------------|
| Auth endpoints    | 100/hour   | 500/hour   | 2000/hour  |
| Profile read      | 1000/hour  | 5000/hour  | Unlimited  |
| Profile write     | 200/hour   | 1000/hour  | 5000/hour  |
| AI endpoints      | 50/hour    | 500/hour   | 2000/hour  |
| PDF generation    | 20/day     | 200/day    | 1000/day   |
| Import/Export     | 10/day     | 100/day    | 500/day    |

## Pagination

All list endpoints support pagination:
```
GET /experiences?page=1&size=20&sort=startDate:desc
```

Parameters:
- `page`: Page number (default: 1)
- `size`: Items per page (default: 20, max: 100)
- `sort`: Field and direction (format: `field:asc|desc`)

## Filtering

List endpoints support filtering:
```
GET /projects?isAnonymized=true&startDate_gte=2020-01-01
```

Common filters:
- `fieldEq`: Exact match
- `fieldNe`: Not equal
- `fieldGt`: Greater than
- `fieldGte`: Greater than or equal
- `fieldLt`: Less than
- `fieldLte`: Less than or equal
- `fieldLike`: Partial match
- `fieldIn`: In list (comma-separated)