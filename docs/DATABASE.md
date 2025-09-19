# Database Schema Documentation

## 1. Database Overview

- **Database Engine**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Migration Tool**: Alembic
- **ID Strategy**: ULID (Universally Unique Lexicographically Sortable Identifier)

## 2. Core Schema Design

### Users & Authentication

```sql
-- users table
CREATE TABLE users (
    id TEXT PRIMARY KEY,  -- ULID
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    verification_token TEXT,
    reset_token TEXT,
    reset_token_expires TIMESTAMP,
    plan VARCHAR(20) DEFAULT 'FREE',  -- FREE, PRO, EXPERT
    plan_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    CONSTRAINT check_plan CHECK (plan IN ('FREE', 'PRO', 'EXPERT'))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_reset_token ON users(reset_token) WHERE reset_token IS NOT NULL;
```

### Profiles

```sql
-- profiles table
CREATE TABLE profiles (
    id TEXT PRIMARY KEY,  -- ULID
    user_id TEXT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    slug VARCHAR(100) UNIQUE,  -- for public URL
    headline VARCHAR(200),
    summary TEXT,
    location VARCHAR(100),
    visibility VARCHAR(20) DEFAULT 'PRIVATE',  -- PRIVATE, FRIENDS, PUBLIC
    contact JSONB DEFAULT '{}',  -- {email, phone, linkedin, website}
    draft_data JSONB,  -- wizard progress storage
    profile_photo_url TEXT,
    completeness_score INTEGER DEFAULT 0,  -- 0-100
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_visibility CHECK (visibility IN ('PRIVATE', 'FRIENDS', 'PUBLIC'))
);

CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_profiles_slug ON profiles(slug) WHERE slug IS NOT NULL;
CREATE INDEX idx_profiles_visibility ON profiles(visibility) WHERE visibility = 'PUBLIC';
```

### Experiences

```sql
-- experiences table
CREATE TABLE experiences (
    id TEXT PRIMARY KEY,  -- ULID
    profile_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    company_name VARCHAR(200) NOT NULL,
    company_website VARCHAR(500),
    company_size VARCHAR(50),  -- 1-10, 11-50, 51-200, etc.
    industry VARCHAR(100),
    company_location VARCHAR(100),
    position VARCHAR(200) NOT NULL,
    employment_type VARCHAR(50),  -- FULL_TIME, PART_TIME, CONTRACT, etc.
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT false,
    description TEXT,
    responsibilities JSONB DEFAULT '[]',  -- Array of responsibility strings
    technologies TEXT[],  -- PostgreSQL array
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_dates CHECK (end_date IS NULL OR end_date > start_date)
);

CREATE INDEX idx_experiences_profile_id ON experiences(profile_id);
CREATE INDEX idx_experiences_dates ON experiences(profile_id, start_date DESC);
CREATE INDEX idx_responsibilities_gin ON experiences USING gin(responsibilities);
```

### Projects

```sql
-- projects table
CREATE TABLE projects (
    id TEXT PRIMARY KEY,  -- ULID
    profile_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    role VARCHAR(100),  -- myRole from JS model
    start_date DATE,
    end_date DATE,
    is_ongoing BOOLEAN DEFAULT false,
    is_anonymized BOOLEAN DEFAULT false,
    anonymized_company VARCHAR(200),  -- "Fortune 500 Bank"

    -- Enhanced fields from proven JS model
    status VARCHAR(20) DEFAULT 'Active',  -- Active, Staging, Archived
    category VARCHAR(20) DEFAULT 'Production',  -- Demo, Internal, Production
    achievements JSONB DEFAULT '[]',  -- Array of achievement strings
    challenges JSONB DEFAULT '[]',  -- Array of challenge strings
    clients JSONB DEFAULT '[]',  -- Array of client strings

    -- Project scale/scope
    team_size INTEGER,
    duration_months INTEGER,
    users_count INTEGER,
    budget_range VARCHAR(20),  -- small, medium, large

    -- Links
    demo_url VARCHAR(500),
    github_url VARCHAR(500),
    documentation_url VARCHAR(500),

    visibility VARCHAR(20) DEFAULT 'PUBLIC',  -- PUBLIC, ANONYMOUS
    technologies TEXT[],  -- Will be replaced with technology relationships
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_visibility CHECK (visibility IN ('PUBLIC', 'ANONYMOUS')),
    CONSTRAINT check_status CHECK (status IN ('Active', 'Staging', 'Archived')),
    CONSTRAINT check_category CHECK (category IN ('Demo', 'Internal', 'Production')),
    CONSTRAINT check_budget CHECK (budget_range IS NULL OR budget_range IN ('small', 'medium', 'large'))
);

CREATE INDEX idx_projects_profile_id ON projects(profile_id);
CREATE INDEX idx_projects_dates ON projects(start_date DESC);
```

### Project-Experience Relations

```sql
-- project_experiences junction table
CREATE TABLE project_experiences (
    project_id TEXT REFERENCES projects(id) ON DELETE CASCADE,
    experience_id TEXT REFERENCES experiences(id) ON DELETE CASCADE,
    PRIMARY KEY (project_id, experience_id)
);

CREATE INDEX idx_project_exp_project ON project_experiences(project_id);
CREATE INDEX idx_project_exp_experience ON project_experiences(experience_id);
```

### Technologies (Global Reference)

```sql
-- technologies table - global reference for all technologies
CREATE TABLE technologies (
    id TEXT PRIMARY KEY,  -- ULID
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,  -- Framework, Library, Platform, Service, System
    layer VARCHAR(50) NOT NULL,  -- Backend, Database, DevOps, Frontend, Language, Tools
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_category CHECK (category IN ('Framework', 'Library', 'Platform', 'Service', 'System')),
    CONSTRAINT check_layer CHECK (layer IN ('Backend', 'Database', 'DevOps', 'Frontend', 'Language', 'Tools'))
);

CREATE INDEX idx_technologies_name ON technologies(name);
CREATE INDEX idx_technologies_category ON technologies(category);
CREATE INDEX idx_technologies_layer ON technologies(layer);
```

### Skills (User-specific technology usage)

```sql
-- skills table - user's relationship with technologies
CREATE TABLE skills (
    id TEXT PRIMARY KEY,  -- ULID
    profile_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    technology_id TEXT NOT NULL REFERENCES technologies(id) ON DELETE CASCADE,
    level INTEGER CHECK (level >= 1 AND level <= 5),  -- 1=Basic, 2=Intermediate, 3=Advanced, 4=Expert, 5=Master
    years_of_experience INTEGER,
    started_using_year INTEGER,  -- Year when user started using this technology
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_profile_technology UNIQUE (profile_id, technology_id)
);

CREATE INDEX idx_skills_profile_id ON skills(profile_id);
CREATE INDEX idx_skills_technology_id ON skills(technology_id);
CREATE INDEX idx_skills_level ON skills(profile_id, level DESC);
```

### Technology Relationships

```sql
-- project_technologies junction table - which technologies were used in each project
CREATE TABLE project_technologies (
    project_id TEXT REFERENCES projects(id) ON DELETE CASCADE,
    technology_id TEXT REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (project_id, technology_id)
);

CREATE INDEX idx_project_tech_project ON project_technologies(project_id);
CREATE INDEX idx_project_tech_technology ON project_technologies(technology_id);

-- experience_technologies junction table - which technologies were used in each role
CREATE TABLE experience_technologies (
    experience_id TEXT REFERENCES experiences(id) ON DELETE CASCADE,
    technology_id TEXT REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (experience_id, technology_id)
);

CREATE INDEX idx_exp_tech_experience ON experience_technologies(experience_id);
CREATE INDEX idx_exp_tech_technology ON experience_technologies(technology_id);
```

### Education

```sql
-- education table
CREATE TABLE education (
    id TEXT PRIMARY KEY,  -- ULID
    profile_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    institution VARCHAR(200) NOT NULL,
    degree VARCHAR(100),
    field_of_study VARCHAR(200),
    start_date DATE,
    end_date DATE,
    grade VARCHAR(50),
    description TEXT,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_education_profile_id ON education(profile_id);
```

### Certifications

```sql
-- certifications table
CREATE TABLE certifications (
    id TEXT PRIMARY KEY,  -- ULID
    profile_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    issuing_organization VARCHAR(200),
    credential_id VARCHAR(100),
    credential_url VARCHAR(500),
    issue_date DATE,
    expiry_date DATE,
    is_expired BOOLEAN GENERATED ALWAYS AS (expiry_date < CURRENT_DATE) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_certifications_profile_id ON certifications(profile_id);
CREATE INDEX idx_certifications_expiry ON certifications(expiry_date) 
    WHERE expiry_date IS NOT NULL;
```

### Achievements

```sql
-- achievements table
CREATE TABLE achievements (
    id TEXT PRIMARY KEY,  -- ULID
    profile_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    date DATE,
    category VARCHAR(50),  -- AWARD, PUBLICATION, SPEAKING, OTHER
    url VARCHAR(500),
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_achievements_profile_id ON achievements(profile_id);
```

### CV Versions

```sql
-- cv_versions table
CREATE TABLE cv_versions (
    id TEXT PRIMARY KEY,  -- ULID
    profile_id TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    template VARCHAR(50) DEFAULT 'modern',
    sections_config JSONB NOT NULL,  -- Configuration for what to include
    /*
    Example sections_config:
    {
        "include_photo": false,
        "include_summary": true,
        "experiences": ["exp_id1", "exp_id2"],  -- specific IDs to include
        "projects": ["proj_id1"],
        "skills": ["skill_id1", "skill_id2"],
        "education": ["edu_id1"],
        "certifications": ["cert_id1"],
        "achievements": ["ach_id1"],
        "custom_summary": "Optional override summary text"
    }
    */
    pdf_url TEXT,  -- S3/storage URL
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cv_versions_profile_id ON cv_versions(profile_id);
CREATE INDEX idx_cv_versions_default ON cv_versions(profile_id, is_default) 
    WHERE is_default = true;
```

### Import History

```sql
-- import_history table
CREATE TABLE import_history (
    id TEXT PRIMARY KEY,  -- ULID
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source VARCHAR(50) NOT NULL,  -- LINKEDIN, GITHUB, etc.
    status VARCHAR(50) DEFAULT 'PENDING',  -- PENDING, PROCESSING, COMPLETED, FAILED
    items_imported INTEGER DEFAULT 0,
    error_message TEXT,
    import_data JSONB,  -- Store raw imported data for debugging
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_import_history_user_id ON import_history(user_id);
CREATE INDEX idx_import_history_status ON import_history(status);
```

## 3. Supporting Tables

### Responsibilities Suggestions

```sql
-- responsibilities_library table (for AI suggestions)
CREATE TABLE responsibilities_library (
    id TEXT PRIMARY KEY,  -- ULID
    role_category VARCHAR(100),  -- "Software Engineer", "Product Manager", etc.
    responsibility TEXT NOT NULL,
    seniority_level VARCHAR(50),  -- JUNIOR, MID, SENIOR, LEAD, EXECUTIVE
    usage_count INTEGER DEFAULT 0,  -- Track popularity
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resp_library_role ON responsibilities_library(role_category);
CREATE INDEX idx_resp_library_usage ON responsibilities_library(usage_count DESC);
```

### Audit Log

```sql
-- audit_log table
CREATE TABLE audit_log (
    id TEXT PRIMARY KEY,  -- ULID
    user_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,  -- CREATE_PROFILE, UPDATE_EXPERIENCE, etc.
    entity_type VARCHAR(50),  -- PROFILE, EXPERIENCE, PROJECT, etc.
    entity_id TEXT,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_log_created ON audit_log(created_at DESC);
```

## 4. Database Functions & Triggers

### Updated Timestamp Trigger

```sql
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Repeat for all tables with updated_at column
```

### Profile Completeness Calculator

```sql
-- Function to calculate profile completeness
CREATE OR REPLACE FUNCTION calculate_profile_completeness(p_profile_id TEXT)
RETURNS INTEGER AS $$
DECLARE
    completeness INTEGER := 0;
    has_headline BOOLEAN;
    has_summary BOOLEAN;
    experience_count INTEGER;
    project_count INTEGER;
    skill_count INTEGER;
    education_count INTEGER;
BEGIN
    -- Check basic info (30%)
    SELECT 
        (headline IS NOT NULL AND headline != ''),
        (summary IS NOT NULL AND LENGTH(summary) > 100)
    INTO has_headline, has_summary
    FROM profiles WHERE id = p_profile_id;
    
    IF has_headline THEN completeness := completeness + 10; END IF;
    IF has_summary THEN completeness := completeness + 20; END IF;
    
    -- Check experiences (30%)
    SELECT COUNT(*) INTO experience_count 
    FROM experiences WHERE profile_id = p_profile_id;
    completeness := completeness + LEAST(experience_count * 10, 30);
    
    -- Check projects (15%)
    SELECT COUNT(*) INTO project_count 
    FROM projects WHERE profile_id = p_profile_id;
    completeness := completeness + LEAST(project_count * 5, 15);
    
    -- Check skills (15%)
    SELECT COUNT(*) INTO skill_count 
    FROM skills WHERE profile_id = p_profile_id;
    completeness := completeness + LEAST(skill_count * 3, 15);
    
    -- Check education (10%)
    SELECT COUNT(*) INTO education_count 
    FROM education WHERE profile_id = p_profile_id;
    completeness := completeness + LEAST(education_count * 10, 10);
    
    RETURN completeness;
END;
$$ LANGUAGE plpgsql;
```

## 5. Indexes Strategy

### Performance Indexes

```sql
-- Frequently queried columns
CREATE INDEX idx_users_plan ON users(plan) WHERE plan != 'FREE';
CREATE INDEX idx_profiles_completeness ON profiles(completeness_score);

-- Full-text search indexes
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- For fuzzy search

CREATE INDEX idx_experiences_search ON experiences 
    USING gin(to_tsvector('english', company_name || ' ' || position));

CREATE INDEX idx_projects_search ON projects 
    USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '')));

CREATE INDEX idx_skills_search ON skills 
    USING gin(name gin_trgm_ops);  -- Fuzzy search on skill names

-- Composite indexes for common queries
CREATE INDEX idx_exp_profile_current ON experiences(profile_id, is_current) 
    WHERE is_current = true;

CREATE INDEX idx_projects_profile_public ON projects(profile_id, visibility) 
    WHERE visibility = 'PUBLIC';
```

## 6. Data Partitioning Strategy (Future)

```sql
-- When we reach scale, partition large tables by user_id
-- Example for experiences table:

CREATE TABLE experiences_partitioned (
    LIKE experiences INCLUDING ALL
) PARTITION BY HASH (profile_id);

-- Create 10 partitions
CREATE TABLE experiences_p0 PARTITION OF experiences_partitioned
    FOR VALUES WITH (modulus 10, remainder 0);
CREATE TABLE experiences_p1 PARTITION OF experiences_partitioned
    FOR VALUES WITH (modulus 10, remainder 1);
-- ... continue for p2 through p9
```

## 7. Migration Strategy

### Initial Migration (V1)

```python
"""Initial schema migration

Revision ID: 001
Create Date: 2024-01-01
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        # ... rest of columns
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create other tables...
    # Add indexes...
    # Add triggers...

def downgrade():
    # Drop in reverse order due to foreign keys
    op.drop_table('users')
```

## 8. Backup & Recovery Procedures

### Backup Strategy

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="career_hub"

# Full backup
pg_dump -U postgres -d $DB_NAME -Fc -f "$BACKUP_DIR/full_backup_$TIMESTAMP.dump"

# Keep last 30 days
find $BACKUP_DIR -name "full_backup_*.dump" -mtime +30 -delete

# Upload to S3
aws s3 cp "$BACKUP_DIR/full_backup_$TIMESTAMP.dump" s3://backups/postgres/
```

### Recovery Procedures

```bash
# Restore from backup
pg_restore -U postgres -d career_hub_restore -Fc backup_file.dump

# Point-in-time recovery using WAL
# Requires WAL archiving to be configured
```

## 9. Performance Monitoring Queries

```sql
-- Find slow queries
SELECT 
    query,
    calls,
    mean_exec_time,
    total_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- queries taking > 100ms
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Table size monitoring
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Cache hit ratio (should be > 99%)
SELECT 
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_ratio
FROM pg_statio_user_tables;
```

## 10. Security Considerations

### Row-Level Security (Future)

```sql
-- Enable RLS for multi-tenant security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own profile
CREATE POLICY profiles_owner_policy ON profiles
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::TEXT);
```

### Data Encryption

```sql
-- Sensitive data encryption using pgcrypto
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Example: Encrypt contact information
UPDATE profiles 
SET contact = pgp_sym_encrypt(contact::text, 'encryption_key')::jsonb
WHERE visibility = 'PRIVATE';
```