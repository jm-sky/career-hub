# Business Requirements Document

## 1. Executive Summary

CareerHub addresses the problem of fragmented career data management for senior professionals. It provides a centralized platform for maintaining comprehensive professional profiles and generating tailored CVs.

## 2. User Problems Being Solved

### Primary Pain Points
1. **Data Fragmentation** - Career information scattered across LinkedIn, CVs, portfolios, certificates
2. **Lack of Continuity** - Difficulty tracking career progression over time
3. **Reactive Applications** - CVs created hastily when opportunities arise
4. **Generic Applications** - Same CV sent to all employers
5. **Competency Blind Spots** - Unaware of skill gaps
6. **Data Loss** - No backup of achievements, references, projects

### Target User: Senior Professional (10+ years experience)
- Multiple roles across different companies
- Extensive project portfolio
- Complex skill sets requiring detailed documentation
- Need for different CV versions (technical vs management)
- Transitioning between IC, leadership, advisory roles

## 3. Core User Stories

### Profile Management
```
As a senior professional,
I want to maintain a comprehensive career profile in one place
So that I have a single source of truth for my professional history
```

```
As a senior professional,
I want to import my LinkedIn profile
So that I can quickly bootstrap my profile without manual entry
```

```
As a senior professional,
I want to add detailed responsibilities for each role
So that I can capture the full scope of my experience
```

### Project Documentation
```
As a senior professional,
I want to document projects separately from roles
So that I can showcase cross-company initiatives
```

```
As a senior professional,
I want to anonymize certain projects
So that I can share my experience while respecting NDAs
```

### CV Generation
```
As a senior professional,
I want to generate different CV versions
So that I can tailor applications to specific opportunities
```

```
As a senior professional,
I want to select which experiences/projects to include
So that my CV is relevant to the position
```

### Public Sharing
```
As a senior professional,
I want a public profile with granular privacy controls
So that I can share my experience while protecting sensitive information
```

## 4. Functional Requirements

### 4.1 User Management
- **FR-001**: User registration with email verification
- **FR-002**: Secure authentication (JWT + refresh tokens)
- **FR-003**: Password reset functionality
- **FR-004**: Profile settings management
- **FR-005**: Subscription management (Free/Pro/Expert)

### 4.2 Profile Creation & Management
- **FR-010**: Profile creation wizard with draft saving
- **FR-011**: Import data from LinkedIn
- **FR-012**: Copy-paste parser for LinkedIn data (fallback)
- **FR-013**: Manual profile data entry
- **FR-014**: Edit all profile sections
- **FR-015**: Profile completeness indicator

### 4.3 Experience Section
- **FR-020**: Add/edit/delete work experiences
- **FR-021**: Rich company information (name, website, size, industry, location)
- **FR-022**: Multiple responsibilities per role
- **FR-023**: Technology/tool tags per role
- **FR-024**: Date range with "current" option
- **FR-025**: Reorder experiences

### 4.4 Projects Section
- **FR-030**: Add/edit/delete projects
- **FR-031**: Link projects to multiple experiences
- **FR-032**: Link projects to multiple skills
- **FR-033**: Project anonymization (hide company name)
- **FR-034**: Rich project description (challenge, solution, results)
- **FR-035**: Project visibility controls

### 4.5 Skills Management
- **FR-040**: Add/edit/delete skills
- **FR-041**: Skill categorization (Technical/Tools/Soft)
- **FR-042**: Skill level assessment (1-5)
- **FR-043**: Years of experience per skill
- **FR-044**: Link skills to projects
- **FR-045**: AI skill suggestions

### 4.6 Education & Achievements
- **FR-050**: Add/edit/delete education entries
- **FR-051**: Add/edit/delete certifications
- **FR-052**: Certification expiry tracking
- **FR-053**: Add/edit/delete achievements
- **FR-054**: Achievement categorization

### 4.7 CV Generation
- **FR-060**: Create multiple CV versions
- **FR-061**: Select sections to include in CV
- **FR-062**: Select specific experiences/projects
- **FR-063**: CV preview before generation
- **FR-064**: PDF export with templates
- **FR-065**: Watermark for free users

### 4.8 Public Profile
- **FR-070**: Generate public profile URL
- **FR-071**: Privacy controls (Private/Friends/Public)
- **FR-072**: Granular section visibility
- **FR-073**: SEO-optimized public pages
- **FR-074**: Share via link/QR code

### 4.9 AI Features (Pro/Expert)
- **FR-080**: Optimize responsibility descriptions
- **FR-081**: Suggest missing responsibilities
- **FR-082**: Generate executive summary
- **FR-083**: Career gap analysis
- **FR-084**: Role-specific CV optimization

## 5. Non-Functional Requirements

### Performance
- **NFR-001**: Page load time < 2 seconds
- **NFR-002**: PDF generation < 5 seconds
- **NFR-003**: Support 10,000 concurrent users
- **NFR-004**: 99.9% uptime

### Security
- **NFR-010**: HTTPS everywhere
- **NFR-011**: OWASP Top 10 compliance
- **NFR-012**: GDPR compliance
- **NFR-013**: Regular security audits
- **NFR-014**: Encrypted data at rest

### Usability
- **NFR-020**: Mobile responsive design
- **NFR-021**: WCAG 2.1 AA accessibility
- **NFR-022**: Support latest 2 versions of major browsers
- **NFR-023**: Intuitive navigation (user testing)

### Scalability
- **NFR-030**: Horizontal scaling capability
- **NFR-031**: Database sharding ready
- **NFR-032**: CDN for static assets
- **NFR-033**: Microservices-ready architecture

## 6. Data Requirements

### Profile Data Complexity
- Support 20+ years of experience entries
- Up to 100 projects per profile
- Up to 200 skills per profile
- Up to 50 achievements
- Up to 20 CV versions

### Storage Requirements
- Text data: ~500KB per complete profile
- Generated PDFs: ~200KB per CV
- Profile images: max 5MB
- Total per user: ~10MB average

## 7. Integration Requirements

### Phase 1 (MVP)
- LinkedIn import (HTML/data parsing)
- Email service (SendGrid/AWS SES)
- Payment processing (Stripe)

### Phase 2
- GitHub integration (projects)
- Google Scholar (publications)
- Calendar integration (reminders)

### Phase 3
- Slack/Teams notifications
- Zapier/Make webhooks
- Public API

## 8. Constraints & Assumptions

### Constraints
- Budget: Bootstrap/self-funded initially
- Team: 1-2 developers
- Timeline: 3 months to MVP
- Technology: Use open-source where possible

### Assumptions
- Users have stable internet connection
- Users understand basic profile concepts
- LinkedIn remains accessible for import
- AI APIs remain available and affordable

## 9. Success Metrics

### MVP Success Criteria
- 100 registered users in first month
- 50% create complete profiles
- 30% generate at least one CV
- 20% upgrade to Pro

### Long-term Goals (Year 1)
- 10,000 registered users
- 2,000 paying customers
- 4.5+ app store rating
- < 5% churn rate

## 10. Out of Scope (MVP)

- Mobile applications (iOS/Android)
- Team collaboration features
- Advanced analytics dashboard
- White-label solutions
- Multi-language support
- Video introductions
- Interview preparation tools
- Salary negotiation tools