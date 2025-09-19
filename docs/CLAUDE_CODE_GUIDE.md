# Using CareerHub with Claude Code CLI

## Overview

This guide explains how to use the CareerHub project documentation with Claude Code CLI to build your professional profile management platform.

## Prerequisites

1. **Install Claude Code CLI**
   ```bash
   # Install Claude Code globally
   npm install -g @anthropic/claude-code
   
   # Or use with npx
   npx @anthropic/claude-code
   ```

2. **Setup API Key**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Project Structure Setup

### Step 1: Initialize Project

```bash
# Create project directory
mkdir career-hub
cd career-hub

# Copy all documentation files to docs/ folder
mkdir docs
# Copy all the .md files from our artifacts to this folder:
# - README.md
# - REQUIREMENTS.md
# - ARCHITECTURE.md
# - DATABASE.md
# - API.md
# - IMPLEMENTATION.md
# - CLAUDE_CODE_GUIDE.md

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Step 2: Prepare Context for Claude Code

Create a `.claude-code.json` configuration file:

```json
{
  "name": "CareerHub",
  "description": "Professional Profile Management Platform",
  "context": {
    "include": [
      "docs/**/*.md",
      "backend/app/**/*.py",
      "frontend/app/**/*.tsx",
      "frontend/components/**/*.tsx",
      "docker-compose.yml",
      "backend/requirements.txt",
      "frontend/package.json"
    ],
    "exclude": [
      "**/node_modules/**",
      "**/venv/**",
      "**/__pycache__/**",
      "**/.next/**",
      "**/dist/**"
    ]
  },
  "instructions": {
    "primary": "You are building a professional profile management platform for senior professionals. Follow the architecture and requirements defined in the docs/ folder.",
    "style": "Use clean, maintainable code with proper error handling and type safety.",
    "testing": "Include unit tests for critical business logic.",
    "security": "Implement proper authentication, authorization, and data validation."
  }
}
```

## Working with Claude Code CLI

### Phase 1: Backend Implementation

```bash
# Navigate to backend
cd backend

# Ask Claude to implement the authentication system
claude-code "Implement the complete authentication system based on docs/API.md and docs/DATABASE.md. Include user registration, login, JWT tokens, and password reset functionality."

# Implement profile management
claude-code "Create the profile management endpoints and services based on the requirements. Include the wizard functionality with draft saving."

# Implement experience CRUD
claude-code "Implement the experience management system with full CRUD operations and the responsibilities system as described in the documentation."
```

### Phase 2: Frontend Implementation

```bash
# Navigate to frontend
cd frontend

# Create authentication UI
claude-code "Create the authentication UI components including login, register, and password reset forms using the shadcn/ui components."

# Build profile wizard
claude-code "Implement the profile creation wizard with step-by-step flow and draft saving as described in the requirements."

# Create profile dashboard
claude-code "Build the profile dashboard showing all user data with edit capabilities."
```

### Phase 3: Integration & Features

```bash
# LinkedIn import feature
claude-code "Implement the LinkedIn import functionality with HTML parsing and data mapping to our profile structure."

# CV generation
claude-code "Create the CV generation system with PDF export using the template system described in the documentation."

# AI features
claude-code "Add AI-powered features for optimizing descriptions and suggesting responsibilities."
```

## Specific Implementation Tasks

### Task 1: Database Models

```bash
claude-code "Based on docs/DATABASE.md, create all SQLAlchemy models in backend/app/models/ with proper relationships and constraints."
```

### Task 2: API Endpoints

```bash
claude-code "Implement all API endpoints defined in docs/API.md for the profile module, including proper error handling and validation."
```

### Task 3: Frontend Components

```bash
claude-code "Create the ProfileWizard component with all steps, validation, and draft saving functionality as described in IMPLEMENTATION.md"
```

### Task 4: Testing

```bash
claude-code "Write comprehensive tests for the authentication service and profile management endpoints."
```

## Tips for Better Results

### 1. Provide Clear Context

Always reference the specific documentation section:
```bash
claude-code "Following the schema in docs/DATABASE.md section 2, implement the Experience model with all fields and relationships."
```

### 2. Break Down Complex Tasks

Instead of asking for everything at once, break it down:
```bash
# First, create the models
claude-code "Create the User and Profile models based on DATABASE.md"

# Then, create the schemas
claude-code "Create Pydantic schemas for User and Profile models"

# Finally, create the endpoints
claude-code "Implement the profile CRUD endpoints using the models and schemas"
```

### 3. Use Iterative Development

```bash
# Start with basic functionality
claude-code "Create a basic working authentication system with register and login"

# Then add features
claude-code "Add JWT refresh token functionality to the existing auth system"

# Add error handling
claude-code "Improve error handling in the auth endpoints with proper status codes"
```

### 4. Debugging and Fixes

```bash
# When you encounter errors
claude-code "I'm getting this error: [paste error]. Fix it based on our architecture."

# For optimization
claude-code "Optimize the profile query to include all related data in one query using SQLAlchemy eager loading"
```

## Common Commands

### Backend Development

```bash
# Create a new feature
claude-code "Add the skills management feature with bulk operations as specified in the requirements"

# Fix or improve existing code
claude-code "Refactor the experience service to use proper async/await patterns"

# Add validation
claude-code "Add comprehensive input validation for all profile-related endpoints"
```

### Frontend Development

```bash
# Create new pages
claude-code "Create the public profile page with SEO optimization as described in the implementation plan"

# Build components
claude-code "Build the ExperienceCard component with edit and delete functionality"

# Add interactivity
claude-code "Add drag-and-drop reordering for experiences using react-dnd"
```

### DevOps & Deployment

```bash
# Docker setup
claude-code "Create production Dockerfiles for both backend and frontend with multi-stage builds"

# CI/CD
claude-code "Create GitHub Actions workflows for testing and deployment"

# Monitoring
claude-code "Add Sentry error tracking and Prometheus metrics to the backend"
```

## Project Milestones Checklist

Use this checklist to track progress:

### MVP Phase 1 (Authentication & Profile)
- [ ] User registration and login
- [ ] JWT authentication
- [ ] Profile CRUD operations
- [ ] Profile wizard with drafts
- [ ] Basic profile dashboard

### MVP Phase 2 (Core Features)
- [ ] Experience management
- [ ] Project management with relationships
- [ ] Skills management
- [ ] Education and certifications
- [ ] Achievements section

### MVP Phase 3 (Import & Export)
- [ ] LinkedIn import
- [ ] CV generation (1 template)
- [ ] PDF export
- [ ] Public profile pages
- [ ] Profile completeness scoring

### Post-MVP Enhancements
- [ ] AI-powered optimizations
- [ ] Multiple CV templates
- [ ] Advanced privacy controls
- [ ] Payment integration
- [ ] Email notifications

## Troubleshooting

### Issue: Claude Code doesn't understand the context

**Solution:** Make sure all documentation files are in the docs/ folder and reference them explicitly:
```bash
claude-code "Using the database schema from docs/DATABASE.md, create the models"
```

### Issue: Generated code doesn't match requirements

**Solution:** Be more specific and reference exact sections:
```bash
claude-code "Implement the profile visibility system exactly as described in REQUIREMENTS.md section 4.8"
```

### Issue: Complex features need multiple iterations

**Solution:** Break down into smaller tasks:
```bash
# Instead of: "Build the complete CV generation system"
# Do:
claude-code "Step 1: Create the CVVersion model and schema"
claude-code "Step 2: Create the CV template system"
claude-code "Step 3: Implement PDF generation with WeasyPrint"
claude-code "Step 4: Add the download endpoint"
```

## Best Practices

1. **Always test incrementally** - Don't wait until everything is built
2. **Keep documentation updated** - Update docs as requirements change
3. **Use version control** - Commit working versions before major changes
4. **Follow the architecture** - Stick to the patterns defined in ARCHITECTURE.md
5. **Maintain consistency** - Use the same patterns throughout the codebase

## Getting Help

If Claude Code needs more context, you can:

1. **Add more details to the prompt**
2. **Reference specific documentation sections**
3. **Provide example code patterns**
4. **Share error messages for debugging**

## Example Session

Here's a complete example session for building the authentication system:

```bash
# 1. Create the User model
claude-code "Create the User model in backend/app/models/user.py based on docs/DATABASE.md with all fields and using ULID for IDs"

# 2. Create authentication schemas
claude-code "Create Pydantic schemas for user registration, login, and token responses in backend/app/schemas/auth.py"

# 3. Create security utilities
claude-code "Implement password hashing and JWT token creation/validation in backend/app/core/security.py"

# 4. Create auth service
claude-code "Create the authentication service with register, login, and token refresh methods in backend/app/services/auth.py"

# 5. Create auth endpoints
claude-code "Implement the authentication API endpoints in backend/app/api/v1/auth.py as specified in docs/API.md"

# 6. Add tests
claude-code "Write tests for the authentication endpoints in backend/tests/test_auth.py"

# 7. Create frontend auth forms
claude-code "Create login and registration forms using React Hook Form and Zod in frontend/components/auth/"

# 8. Create auth context
claude-code "Implement authentication state management using Zustand in frontend/lib/stores/auth.ts"
```

## Final Notes

Remember that Claude Code CLI is a tool to help you build faster, but you should:
- Review all generated code
- Test thoroughly
- Adjust based on your specific needs
- Keep security best practices in mind
- Follow your organization's coding standards

Happy coding with CareerHub! 🚀