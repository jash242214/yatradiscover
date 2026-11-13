# Backend Architecture - Python FastAPI

## Tech Stack

```
Framework: FastAPI 0.104+
Language: Python 3.11+
Server: Uvicorn
ORM: SQLAlchemy 2.0
Database: Supabase PostgreSQL
Authentication: JWT + OAuth2
API Documentation: OpenAPI/Swagger
Validation: Pydantic v2
Async: asyncio + aiohttp
Caching: Redis
Job Queue: Celery
Email: SendGrid
Payment: Stripe API
AI: OpenAI GPT-4 API
Testing: pytest + pytest-asyncio
Database Migrations: Alembic
Logging: Python logging + Sentry
Environment: python-dotenv
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py (Application entry point)
│   ├── config.py (Environment configuration)
│   ├── dependencies.py (Dependency injection)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py (Main router)
│   │   │   │
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── itineraries.py
│   │   │   │   ├── bookings.py
│   │   │   │   ├── activities.py
│   │   │   │   ├── destinations.py
│   │   │   │   ├── reviews.py
│   │   │   │   ├── ai.py
│   │   │   │   ├── admin.py
│   │   │   │   └── health.py
│   │   │   │
│   │   │   └── models/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── user.py
│   │   │       ├── itinerary.py
│   │   │       ├── booking.py
│   │   │       ├── activity.py
│   │   │       ├── destination.py
│   │   │       ├── review.py
│   │   │       └── common.py
│   │   │
│   │   └── v2/
│   │       └── (Future API version)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py (Settings & environment)
│   │   ├── security.py (JWT, OAuth2, permissions)
│   │   ├── exceptions.py (Custom exceptions)
│   │   ├── logger.py (Logging configuration)
│   │   └── constants.py (App constants)
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py (Base model)
│   │   ├── session.py (Database session)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── itinerary.py
│   │   │   ├── activity.py
│   │   │   ├── booking.py
│   │   │   ├── destination.py
│   │   │   ├── review.py
│   │   │   └── audit_log.py
│   │   │
│   │   └── migrations/
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       ├── versions/
│   │       │   ├── 001_initial_schema.py
│   │       │   └── (future migrations)
│   │       └── alembic.ini
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── itinerary.py
│   │   ├── booking.py
│   │   ├── ai.py
│   │   ├── email.py
│   │   ├── payment.py
│   │   ├── storage.py (Cloud storage for files)
│   │   ├── cache.py (Redis caching)
│   │   └── notification.py
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py (Celery configuration)
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── email_tasks.py
│   │   │   ├── ai_tasks.py
│   │   │   ├── notification_tasks.py
│   │   │   └── sync_tasks.py
│   │   └── beat_schedule.py (Periodic tasks)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   ├── helpers.py
│   │   ├── decorators.py
│   │   └── pagination.py
│   │
│   └── middleware/
│       ├── __init__.py
│       ├── cors.py
│       ├── rate_limit.py
│       ├── error_handler.py
│       ├── request_logging.py
│       └── auth_middleware.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py (Pytest configuration & fixtures)
│   │
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── test_auth_service.py
│   │   │   ├── test_itinerary_service.py
│   │   │   ├── test_booking_service.py
│   │   │   └── test_ai_service.py
│   │   │
│   │   ├── utils/
│   │   │   └── test_validators.py
│   │   │
│   │   └── models/
│   │       └── test_database_models.py
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_auth_flow.py
│   │   ├── test_itinerary_creation.py
│   │   ├── test_booking_flow.py
│   │   ├── test_ai_suggestions.py
│   │   └── test_payment_processing.py
│   │
│   └── e2e/
│       ├── __init__.py
│       ├── test_full_user_journey.py
│       └── test_api_workflows.py
│
├── scripts/
│   ├── __init__.py
│   ├── init_db.py (Initialize database)
│   ├── seed_db.py (Seed test data)
│   ├── create_admin.py (Create admin user)
│   ├── backup_db.py (Database backup)
│   └── deploy.sh (Deployment script)
│
├── .env.example
├── .env.test
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── setup.py
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .flake8
├── .pylintrc
├── mypy.ini
├── .gitignore
├── README.md
└── ARCHITECTURE.md
```

## Database Schema (PostgreSQL)

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    profile_picture_url TEXT,
    bio TEXT,
    country VARCHAR(100),
    phone_number VARCHAR(20),
    date_of_birth DATE,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'partner')),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    email_verified_at TIMESTAMP,
    two_fa_enabled BOOLEAN DEFAULT false,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### Itineraries Table
```sql
CREATE TABLE itineraries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    destination VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget_currency VARCHAR(3) DEFAULT 'USD',
    budget_amount DECIMAL(10,2),
    is_public BOOLEAN DEFAULT false,
    is_collaborative BOOLEAN DEFAULT false,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_itineraries_user_id ON itineraries(user_id);
CREATE INDEX idx_itineraries_destination ON itineraries(destination);
```

### Activities Table
```sql
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    itinerary_id UUID NOT NULL REFERENCES itineraries(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    location VARCHAR(255),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    cost DECIMAL(10,2),
    currency VARCHAR(3),
    priority INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activities_itinerary_id ON activities(itinerary_id);
CREATE INDEX idx_activities_start_time ON activities(start_time);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    itinerary_id UUID NOT NULL REFERENCES itineraries(id),
    activity_id UUID REFERENCES activities(id),
    vendor_name VARCHAR(255),
    vendor_type VARCHAR(100),
    booking_reference VARCHAR(100) UNIQUE,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    booking_date TIMESTAMP NOT NULL,
    confirmation_date TIMESTAMP,
    check_in_date DATE,
    check_out_date DATE,
    quantity INTEGER DEFAULT 1,
    total_price DECIMAL(10,2),
    currency VARCHAR(3),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'unpaid' CHECK (payment_status IN ('unpaid', 'paid', 'refunded')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_itinerary_id ON bookings(itinerary_id);
```

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register           # Register new user
POST   /api/v1/auth/login              # Login user
POST   /api/v1/auth/logout             # Logout user
POST   /api/v1/auth/refresh            # Refresh JWT token
POST   /api/v1/auth/forgot-password    # Request password reset
POST   /api/v1/auth/reset-password     # Reset password
GET    /api/v1/auth/verify-email       # Verify email token
POST   /api/v1/auth/2fa/enable         # Enable 2FA
POST   /api/v1/auth/2fa/disable        # Disable 2FA
```

### Users
```
GET    /api/v1/users/me                # Get current user
PUT    /api/v1/users/me                # Update current user
GET    /api/v1/users/:id               # Get user by ID
PUT    /api/v1/users/:id               # Update user (admin)
DELETE /api/v1/users/:id               # Delete user (admin)
GET    /api/v1/users/:id/itineraries   # Get user's itineraries
```

### Itineraries
```
GET    /api/v1/itineraries             # List itineraries (paginated)
POST   /api/v1/itineraries             # Create itinerary
GET    /api/v1/itineraries/:id         # Get itinerary detail
PUT    /api/v1/itineraries/:id         # Update itinerary
DELETE /api/v1/itineraries/:id         # Delete itinerary
POST   /api/v1/itineraries/:id/share   # Share itinerary
GET    /api/v1/itineraries/:id/export  # Export itinerary (PDF/CSV)
```

### Activities
```
POST   /api/v1/itineraries/:id/activities         # Add activity
PUT    /api/v1/activities/:id                     # Update activity
DELETE /api/v1/activities/:id                     # Delete activity
POST   /api/v1/activities/:id/reorder             # Reorder activities
```

### Bookings
```
GET    /api/v1/bookings                # List user's bookings
POST   /api/v1/bookings                # Create booking
GET    /api/v1/bookings/:id            # Get booking detail
PUT    /api/v1/bookings/:id            # Update booking
DELETE /api/v1/bookings/:id            # Cancel booking
POST   /api/v1/bookings/:id/payment    # Process payment
```

### AI Suggestions
```
POST   /api/v1/ai/suggest              # Get AI suggestions
POST   /api/v1/ai/chat                 # Chat with AI
GET    /api/v1/ai/suggestions/:id      # Get saved suggestions
DELETE /api/v1/ai/suggestions/:id      # Delete suggestion
```

## Core Services Implementation

### Authentication Service

```python
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"])
    
    async def register_user(self, email: str, password: str, username: str) -> User:
        # Check if user exists
        existing = await User.get(email=email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = User(
            email=email,
            username=username,
            password_hash=self.pwd_context.hash(password)
        )
        await user.save()
        return user
    
    async def authenticate(self, email: str, password: str) -> User:
        user = await User.get(email=email)
        if not user or not self.pwd_context.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        return user
    
    def create_access_token(self, user_id: str, expires_delta: timedelta = None):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode = {"sub": str(user_id), "exp": expire}
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
```

### AI Service

```python
import openai
from functools import lru_cache

class AIService:
    def __init__(self, api_key: str):
        openai.api_key = api_key
    
    async def generate_itinerary_suggestions(
        self,
        destination: str,
        duration: int,
        budget: float,
        interests: List[str]
    ) -> Dict:
        prompt = f"""
        Create a {duration}-day travel itinerary for {destination}
        with a budget of ${budget}.
        Interests: {', '.join(interests)}
        
        Return as JSON with activities, costs, and recommendations.
        """
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    async def chat_with_user(self, user_id: str, message: str) -> str:
        # Get user's itinerary context
        user = await User.get(id=user_id)
        context = f"User: {user.username}, Recent trips: {user.recent_trips}"
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a helpful travel advisor. {context}"},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
```

## FastAPI Application Setup

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.api.v1 import router as v1_router

app = FastAPI(
    title="YatraDiscover AI API",
    description="AI-powered travel planning platform",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include routers
app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

## Security Best Practices

✓ **Implemented:**
- JWT tokens with expiration
- Password hashing with bcrypt
- CORS configuration
- Rate limiting
- Input validation with Pydantic
- SQL injection prevention (ORM)
- HTTPS enforcement
- Secure headers
- API key rotation

✗ **Never:**
- Store secrets in code
- Log sensitive data
- Expose stack traces to clients
- Use default credentials
- Disable HTTPS in production

---

**Last Updated:** 2026-11-13
**Status:** Ready for development
