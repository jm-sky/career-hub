# 🚀 Auth Boilerplate Migration Plan

**Project:** CareerHub
**Source:** `~/projects/private/saas-fastapi-react-boilerplate`
**Target:** `~/projects/private/career-hub/backend`
**Date:** 2025-10-06

---

## 📊 Migration Overview

### Goals
- ✅ Integrate full JWT authentication system (access + refresh tokens)
- ✅ Add user registration, login, password reset/change
- ✅ Implement Google OAuth
- ✅ Add reCAPTCHA protection
- ✅ Setup rate limiting
- ✅ Convert in-memory user store to SQLAlchemy + PostgreSQL
- ✅ Upgrade token blacklist to Redis-based

### Key Changes
| Component | Before | After |
|-----------|--------|-------|
| User Storage | N/A | SQLAlchemy + PostgreSQL |
| Auth System | None | JWT (15min access / 30d refresh) |
| Token Blacklist | N/A | Redis-based |
| Rate Limiting | None | SlowAPI with Redis |
| Password Security | N/A | bcrypt + strength validation |
| OAuth | None | Google OAuth 2.0 |
| Bot Protection | None | reCAPTCHA v3 |

---

## 📋 Migration Checklist

### Phase 1: Core Infrastructure ⚙️

#### 1.1 Update Dependencies
- [ ] **File:** `backend/requirements.txt`
- [ ] Add: `PyJWT`, `Authlib`, `limits`, `python-ulid` (v2.7.0)
- [ ] Update: `passlib[bcrypt]` (ensure bcrypt support)
- [ ] Keep existing: SQLAlchemy, Redis, FastAPI, etc.

#### 1.2 Create Core Configuration
- [ ] **File:** `backend/app/core/config.py` (NEW)
- [ ] Port settings structure from boilerplate `core/settings.py`
- [ ] Add sections:
  - `AppSettings` (name, version, debug, environment)
  - `ServerSettings` (host, port, CORS origins)
  - `SecuritySettings` (secret_key, JWT algo, token expiry)
  - `RateLimitSettings` (per-endpoint limits)
  - `DatabaseSettings` (PostgreSQL URL)
  - `RedisSettings` (connection URL)
  - `RecaptchaSettings` (keys, min score)
  - `GoogleOAuthSettings` (client ID, secret, redirect)
- [ ] Set token expiry: **15min access / 30d refresh** (CareerHub standard)

#### 1.3 Setup Exception Handling
- [ ] **File:** `backend/app/core/exceptions.py` (NEW)
- [ ] Copy from boilerplate:
  - Base `AuthenticationError` class
  - `UserNotFoundError`, `UserAlreadyExistsError`
  - `InvalidCredentialsError`, `InvalidTokenError`, `ExpiredTokenError`
  - `InactiveUserError`, `InvalidTokenTypeError`, `InvalidResetTokenError`
  - Global exception handler `authentication_exception_handler`

#### 1.4 Create Security Utilities
- [ ] **File:** `backend/app/core/security.py` (NEW)
- [ ] Merge content from boilerplate:
  - `core/auth.py` (JWT functions, password hashing)
  - `core/token_blacklist.py` (upgrade to Redis)
- [ ] Functions to include:
  - `verify_password()`, `get_password_hash()`
  - `create_access_token()`, `create_refresh_token()`
  - `create_password_reset_token()`, `verify_token()`
- [ ] **Redis Token Blacklist:**
  ```python
  class RedisTokenBlacklist:
      def __init__(self, redis_client):
          self.redis = redis_client

      def add(self, token: str, exp_seconds: int):
          # Store in Redis with TTL = token expiry

      def is_blacklisted(self, token: str) -> bool:
          # Check if token exists in Redis
  ```

#### 1.5 Create Dependencies
- [ ] **File:** `backend/app/core/dependencies.py` (NEW)
- [ ] Copy from boilerplate:
  - `get_current_user()` - validates JWT, checks blacklist
  - `get_current_active_user()` - ensures user is active
  - Type aliases: `CurrentUser`, `CurrentActiveUser`, `BearerCredentials`

#### 1.6 Create Decorators
- [ ] **File:** `backend/app/core/decorators.py` (NEW)
- [ ] Copy from boilerplate:
  - `@rate_limit(limit)` - SlowAPI wrapper
  - `@recaptcha_protected(action)` - reCAPTCHA verification
  - `@require_auth` - authentication shortcut

#### 1.7 Setup Rate Limiting
- [ ] **File:** `backend/app/core/rate_limit.py` (NEW)
- [ ] Copy from boilerplate (SlowAPI with Redis storage)

#### 1.8 Setup reCAPTCHA
- [ ] **File:** `backend/app/core/recaptcha.py` (NEW)
- [ ] Copy from boilerplate (Google reCAPTCHA v3 verification)

#### 1.9 Setup OAuth
- [ ] **File:** `backend/app/core/oauth.py` (NEW)
- [ ] Copy from boilerplate (Authlib Google OAuth config)

---

### Phase 2: Database Layer 🗄️

#### 2.1 Create User Model
- [ ] **File:** `backend/app/models/user.py` (NEW)
- [ ] **Convert from Pydantic to SQLAlchemy:**

**Boilerplate (Pydantic):**
```python
class User(BaseModel):
    id: str  # ULID
    email: EmailStr
    name: str
    hashedPassword: str
    isActive: bool = True
    createdAt: datetime
    resetToken: Optional[str] = None
    resetTokenExpiry: Optional[datetime] = None
```

**Target (SQLAlchemy):**
```python
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from ulid import ULID
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(26), primary_key=True, default=lambda: str(ULID()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Password reset fields
    reset_token = Column(Text, nullable=True)
    reset_token_expiry = Column(DateTime(timezone=True), nullable=True)

    # Premium tier for CareerHub business model
    tier = Column(String(20), default="free", nullable=False)  # free, pro, expert

    # User settings (JSONB for flexibility)
    settings = Column(JSONB, default={}, nullable=False)

    def verify_password(self, password: str) -> bool:
        from app.core.security import verify_password
        return verify_password(password, self.hashed_password)

    def to_dict(self):
        """Convert to camelCase dict for API responses."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "isActive": self.is_active,
            "createdAt": self.created_at,
            "tier": self.tier
        }
```

#### 2.2 Setup Database Connection
- [ ] **File:** `backend/app/core/database.py` (NEW)
- [ ] SQLAlchemy engine, session, Base
- [ ] Dependency: `get_db()` for session injection

#### 2.3 Create Alembic Migration
- [ ] Run: `alembic revision --autogenerate -m "Add User model with authentication fields"`
- [ ] **Migration will create:**
  - `users` table with ULID primary key
  - Indexes: `email` (unique), `is_active`
  - Columns: id, email, name, hashed_password, is_active, created_at, updated_at, reset_token, reset_token_expiry, tier, settings
- [ ] Run: `alembic upgrade head`

---

### Phase 3: Schemas & Services 📦

#### 3.1 Create Auth Schemas
- [ ] **File:** `backend/app/schemas/auth.py` (NEW)
- [ ] Copy from boilerplate (already camelCase):
  - `UserLogin` - email, password, recaptchaToken
  - `UserRegister` - email, password (with validation), name, recaptchaToken
  - `TokenResponse` - accessToken, refreshToken, tokenType, expiresIn
  - `TokenRefresh` - refreshToken
  - `UserResponse` - id, email, name, isActive, createdAt, tier
  - `LoginResponse` - user + tokens
  - `MessageResponse` - generic message
  - `ForgotPasswordRequest` - email, recaptchaToken
  - `ResetPasswordRequest` - token, newPassword
  - `ChangePasswordRequest` - currentPassword, newPassword

#### 3.2 Create Auth Service
- [ ] **File:** `backend/app/services/auth_service.py` (NEW)
- [ ] **Adapt from boilerplate** (convert Pydantic user_store to SQLAlchemy):
  - `register_user()` - create user in DB
  - `authenticate_user()` - verify credentials
  - `refresh_tokens()` - validate refresh token, issue new pair
  - `logout_user()` - blacklist access token
  - `get_user_profile()` - return user data
  - `request_password_reset()` - generate reset token
  - `reset_password()` - validate token, update password
  - `change_password()` - verify current, set new
  - `authenticate_with_google()` - OAuth login/register

**Key Change:** Replace `user_store.*` calls with SQLAlchemy queries:
```python
# Before (Pydantic)
user = user_store.get_user_by_email(email)

# After (SQLAlchemy)
user = db.query(User).filter(User.email == email.lower()).first()
```

---

### Phase 4: API Endpoints 🌐

#### 4.1 Create Auth Router
- [ ] **File:** `backend/app/api/v1/auth.py` (NEW)
- [ ] Copy from boilerplate `api/auth.py`:
  - `POST /auth/register` - with rate limit + reCAPTCHA
  - `POST /auth/login` - with rate limit + reCAPTCHA
  - `POST /auth/refresh` - with rate limit
  - `POST /auth/logout` - requires auth
  - `GET /auth/me` - requires auth
  - `POST /auth/forgot-password` - with rate limit + reCAPTCHA
  - `POST /auth/reset-password` - with rate limit
  - `POST /auth/change-password` - requires auth + rate limit
  - `GET /auth/google/login` - OAuth initiate
  - `GET /auth/google/callback` - OAuth callback

#### 4.2 Register Router
- [ ] **File:** `backend/app/api/v1/__init__.py` (create if needed)
- [ ] Import and include auth router

---

### Phase 5: Application Setup 🏗️

#### 5.1 Update Main Application
- [ ] **File:** `backend/app/main.py`
- [ ] Add imports:
  ```python
  from app.core.config import settings
  from app.core.exceptions import AuthenticationError, authentication_exception_handler
  from app.core.rate_limit import limiter
  from app.api.v1 import auth
  from slowapi import _rate_limit_exceeded_handler
  from slowapi.errors import RateLimitExceeded
  ```
- [ ] Update app initialization:
  ```python
  app = FastAPI(
      title=settings.app.name,
      version=settings.app.version,
      debug=settings.app.debug
  )
  ```
- [ ] Add middleware:
  - CORS (update origins from settings)
  - Rate limiting state
- [ ] Register exception handlers:
  ```python
  app.add_exception_handler(AuthenticationError, authentication_exception_handler)
  app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
  ```
- [ ] Include routers:
  ```python
  app.include_router(auth.router, prefix="/api/v1")
  ```

#### 5.2 Create Environment Template
- [ ] **File:** `backend/.env.example`
- [ ] Add all required variables:
  ```env
  # App
  APP_NAME="CareerHub API"
  APP_VERSION="1.0.0"
  ENVIRONMENT=development
  DEBUG=true

  # Server
  HOST=0.0.0.0
  PORT=8000
  CORS_ORIGINS=["http://localhost:3000"]

  # Security
  SECRET_KEY=your-secret-key-min-32-chars
  JWT_ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRES_MINUTES=15
  REFRESH_TOKEN_EXPIRES_DAYS=30

  # Database
  DATABASE_URL=postgresql://user:pass@localhost:5432/careerhub

  # Redis
  REDIS_URL=redis://localhost:6379/0

  # Rate Limiting
  RATE_LIMIT_DEFAULT_PER_DAY=1000
  RATE_LIMIT_DEFAULT_PER_HOUR=100
  AUTH_REGISTER_RATE_LIMIT=5/minute
  AUTH_LOGIN_RATE_LIMIT=10/minute
  AUTH_REFRESH_RATE_LIMIT=20/minute
  AUTH_PASSWORD_CHANGE_RATE_LIMIT=3/minute

  # reCAPTCHA
  RECAPTCHA_ENABLED=false
  RECAPTCHA_SECRET_KEY=
  RECAPTCHA_SITE_KEY=
  RECAPTCHA_MIN_SCORE=0.5

  # Google OAuth
  GOOGLE_CLIENT_ID=
  GOOGLE_CLIENT_SECRET=
  GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

  # Frontend
  FRONTEND_URL=http://localhost:3000
  ```

---

### Phase 6: Testing & Validation ✅

#### 6.1 Manual Testing
- [ ] Start services: `docker-compose up -d` (PostgreSQL, Redis)
- [ ] Run migrations: `alembic upgrade head`
- [ ] Start server: `uvicorn app.main:app --reload`

**Test Flow:**
1. [ ] **Register:** `POST /api/v1/auth/register`
   - Body: `{"email": "test@example.com", "password": "Test123!@#", "name": "Test User"}`
   - Check: User created in DB, tokens returned
2. [ ] **Login:** `POST /api/v1/auth/login`
   - Body: `{"email": "test@example.com", "password": "Test123!@#"}`
   - Check: Tokens returned, same user ID
3. [ ] **Get Profile:** `GET /api/v1/auth/me`
   - Header: `Authorization: Bearer {accessToken}`
   - Check: User data returned
4. [ ] **Refresh Token:** `POST /api/v1/auth/refresh`
   - Body: `{"refreshToken": "{refreshToken}"}`
   - Check: New token pair returned
5. [ ] **Logout:** `POST /api/v1/auth/logout`
   - Header: `Authorization: Bearer {accessToken}`
   - Check: Token blacklisted
6. [ ] **Try Blacklisted Token:** `GET /api/v1/auth/me`
   - Header: `Authorization: Bearer {blacklisted_token}`
   - Check: 401 error "Token has been revoked"
7. [ ] **Forgot Password:** `POST /api/v1/auth/forgot-password`
   - Body: `{"email": "test@example.com"}`
   - Check: Success message, check logs for reset link
8. [ ] **Reset Password:** `POST /api/v1/auth/reset-password`
   - Body: `{"token": "{reset_token}", "newPassword": "NewPass123!@#"}`
   - Check: Password updated
9. [ ] **Change Password:** `POST /api/v1/auth/change-password`
   - Header: `Authorization: Bearer {accessToken}`
   - Body: `{"currentPassword": "NewPass123!@#", "newPassword": "Final123!@#"}`
   - Check: Password updated
10. [ ] **Rate Limiting:** Hit register endpoint 6 times in 1 minute
    - Check: 6th request returns 429 Too Many Requests

#### 6.2 Verify Database
- [ ] Check `users` table created
- [ ] Verify ULID format (26 chars, sortable)
- [ ] Check indexes exist (email unique)
- [ ] Verify password is hashed (bcrypt format)

#### 6.3 Verify Redis
- [ ] Check blacklisted tokens stored
- [ ] Verify TTL set correctly (token expiry)
- [ ] Check rate limit counters

---

## 🎯 Success Criteria

### Must Have ✅
- [x] User registration with strong password validation
- [x] JWT authentication (access + refresh tokens)
- [x] Token rotation on refresh
- [x] Token blacklist on logout (Redis)
- [x] Password reset flow
- [x] Password change (authenticated)
- [x] Rate limiting on all auth endpoints
- [x] Current user dependency for protected routes
- [x] Proper error handling with HTTP status codes

### Should Have 🔄
- [x] Google OAuth integration
- [x] reCAPTCHA protection
- [x] camelCase API consistency
- [x] ULID-based user IDs
- [x] User tier field (free/pro/expert)
- [x] Settings JSONB field for flexibility

### Nice to Have 🌟
- [ ] Email verification on registration
- [ ] Email notifications for password reset
- [ ] Audit log for auth events
- [ ] 2FA support

---

## 📝 Notes & Decisions

### Token Strategy
- **Access Token:** 15 minutes (CareerHub standard)
- **Refresh Token:** 30 days (CareerHub standard)
- **Reset Token:** 1 hour (security best practice)
- **Rotation:** New refresh token on each refresh (prevents reuse)

### Password Policy
- Minimum 8 characters
- Must contain: uppercase, lowercase, digit, special character
- Validated on client + server side

### Rate Limiting Strategy
| Endpoint | Limit | Reason |
|----------|-------|--------|
| Register | 5/min | Prevent spam accounts |
| Login | 10/min | Prevent brute force |
| Refresh | 20/min | Allow frequent refreshes |
| Password Change | 3/min | Security sensitive |
| Forgot Password | 5/min | Prevent email spam |

### Security Considerations
- ✅ Passwords hashed with bcrypt (cost factor 12)
- ✅ JWT tokens signed with HS256
- ✅ Token blacklist for revocation
- ✅ Secure token comparison (timing-safe)
- ✅ CORS restricted to frontend URL
- ✅ HTTPOnly cookies for refresh tokens (future enhancement)

---

## 🚨 Potential Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Token blacklist grows indefinitely** | Redis TTL auto-expires tokens |
| **Rate limit state lost on restart** | Use Redis storage (persists) |
| **Secret key not secure** | Validate length + entropy in settings |
| **Email not sent in dev** | Log reset link to console |
| **OAuth redirect mismatch** | Configure Google Console with exact URL |

---

## 📚 References

### Boilerplate Files Used
- `backend/app/core/auth.py` → Security functions
- `backend/app/core/token_blacklist.py` → Token management
- `backend/app/core/dependencies.py` → FastAPI dependencies
- `backend/app/core/exceptions.py` → Error handling
- `backend/app/core/settings.py` → Configuration
- `backend/app/models/user.py` → User model structure
- `backend/app/schemas/auth.py` → Request/response schemas
- `backend/app/services/auth_service.py` → Business logic
- `backend/app/api/auth.py` → API endpoints

### Documentation
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/
- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- Redis Python: https://redis-py.readthedocs.io/

---

## ✨ Post-Migration Tasks

After successful migration, consider:
1. [ ] Add comprehensive test suite (pytest)
2. [ ] Setup email service (SendGrid/SES) for password reset
3. [ ] Add email verification flow
4. [ ] Implement refresh token rotation in cookies
5. [ ] Add audit logging (user_id, action, timestamp, IP)
6. [ ] Setup monitoring (failed login attempts, token usage)
7. [ ] Document API with OpenAPI/Swagger examples
8. [ ] Create frontend auth integration guide

---

**Status:** 🚧 Ready to Begin
**Last Updated:** 2025-10-06
**Estimated Time:** 2-3 hours
