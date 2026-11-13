# YatraDiscover AI - Development Quick Start

**Purpose:** Get the development environment running quickly  
**Time:** ~30 minutes  

---

## ✅ Prerequisites

Ensure you have installed:
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ & npm ([Download](https://nodejs.org/))
- Git ([Download](https://git-scm.com/))
- PostgreSQL 14+ (or use Supabase)
- Docker (optional, for containers)
- Visual Studio Code or preferred IDE

---

## 🚀 Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/jash242214/yatradiscover.git
cd yatradiscover

# List branches
git branch -a
```

---

## 🔧 Step 2: Backend Setup

### 2.1 Create Virtual Environment
```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.3 Configure Environment Variables
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings (for development, defaults are OK)
# The file is already configured for local development
```

### 2.4 Setup Database (Local PostgreSQL)

**Option A: Use Local PostgreSQL**
```bash
# Create database
createdb yatradiscover

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/yatradiscover
```

**Option B: Use Supabase (Cloud PostgreSQL)**
```bash
# Get connection string from Supabase dashboard
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.supabase.co:5432/postgres
```

### 2.5 Run Database Migrations
```bash
# Apply all migrations
alembic upgrade head

# Check current revision
alembic current
```

### 2.6 Start Backend Server
```bash
# Option 1: Direct Python
python run.py

# Option 2: Using uvicorn directly
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Using Docker
docker-compose up -d backend
```

**✅ Backend is running:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 📦 Step 3: Frontend Setup (Next.js)

### 3.1 Navigate to Frontend
```bash
cd ../frontend/web
```

### 3.2 Install Dependencies
```bash
npm install
```

### 3.3 Configure Environment
```bash
# Copy example to .env.local
cp .env.example .env.local

# Edit .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
# NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 3.4 Start Development Server
```bash
# Development with hot reload
npm run dev

# Or build and start production build
npm run build
npm start
```

**✅ Frontend is running:** http://localhost:3000

---

## 📱 Step 4: Mobile Setup (Optional)

### iOS Setup
```bash
cd ../mobile/ios

# Install dependencies
pod install

# Open in Xcode
open YatraDiscover.xcworkspace

# Select simulator and run
```

### Android Setup
```bash
cd ../mobile/android

# Open in Android Studio
# Sync Gradle
# Run on emulator/device
```

---

## 🧪 Step 5: Test the Application

### 5.1 Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# API docs
curl http://localhost:8000/docs

# Test registration
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "TestPassword123!"
  }'

# Test login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

### 5.2 Test Frontend
1. Open http://localhost:3000
2. Click "Sign Up"
3. Register new account
4. Login
5. Create new itinerary
6. Try AI generation (if OpenAI key configured)

### 5.3 Run Tests
```bash
# Backend tests
cd backend
pytest

# Backend tests with coverage
pytest --cov=app tests/

# Frontend tests
cd ../frontend/web
npm run test

# E2E tests (optional)
npm run test:e2e
```

---

## 📊 Step 6: Verify Everything is Working

### Checklist
- [ ] Backend API is running on http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Frontend is running on http://localhost:3000
- [ ] Can register a new user
- [ ] Can login with credentials
- [ ] Can create an itinerary
- [ ] Database is connected (check logs)
- [ ] No errors in console/terminal

### Common Issues

**Port already in use**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process (if needed)
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

**Database connection error**
```bash
# Check DATABASE_URL in .env
# Make sure PostgreSQL is running
# Test connection:
psql $DATABASE_URL -c "SELECT 1;"
```

**Module not found errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# For frontend
npm install --legacy-peer-deps
```

**Python version mismatch**
```bash
# Check Python version
python --version  # Must be 3.11+

# If using pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

---

## 🔗 API Testing with Postman/Thunder Client

### 1. Import API Collection
- Download from GitHub: `backend/postman-collection.json`
- Import into Postman
- Set base URL to `http://localhost:8000`

### 2. Register & Login
1. POST `/api/v1/auth/register`
2. Copy `access_token` from response
3. Set `Authorization: Bearer {token}` in headers

### 3. Test Endpoints
- Create itinerary
- List itineraries
- Generate AI itinerary
- Create booking
- View bookings

---

## 📚 Development Tools

### Useful Commands

```bash
# Backend

# Format code
black backend/app

# Lint code
flake8 backend/app

# Type checking
mypy backend/app

# Database

# Create migration
alembic revision --autogenerate -m "Add new table"

# View migration history
alembic current
alembic history --verbose

# Rollback migration
alembic downgrade -1

# Frontend

# Format code
npm run format

# Lint code
npm run lint

# Type check
npm run type-check

# Build for production
npm run build
```

---

## 🔐 Configuration Files

### Backend .env (Already Configured)
```bash
# Application
ENVIRONMENT=development
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/yatradiscover

# Security
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
ALLOWED_ORIGINS='["http://localhost:3000","http://localhost:5173"]'

# External Services (Leave blank for now)
OPENAI_API_KEY=
STRIPE_API_KEY=
SENDGRID_API_KEY=
```

### Frontend .env.local
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_MAPBOX_TOKEN=
```

---

## 🚀 Next Steps

1. **Explore API Documentation**
   - Visit http://localhost:8000/docs
   - Try out endpoints in Swagger UI

2. **Create Test Users**
   - Register multiple users
   - Create itineraries
   - Test sharing and collaboration

3. **Read Documentation**
   - Backend: `backend/BACKEND-ARCHITECTURE.md`
   - Frontend: `frontend/WEB-ARCHITECTURE.md`
   - Overall: `E2E-DEVELOPMENT-FLOW.md`

4. **Setup IDE Debugger**
   - VS Code: Python extension
   - Add breakpoints and debug

5. **Run Full Test Suite**
   ```bash
   pytest --cov=app --cov-report=html
   npm run test -- --coverage
   ```

---

## 📞 Getting Help

### Resources
- **Backend Docs:** [BACKEND-ARCHITECTURE.md](backend/BACKEND-ARCHITECTURE.md)
- **Frontend Docs:** [WEB-ARCHITECTURE.md](frontend/WEB-ARCHITECTURE.md)
- **E2E Flow:** [E2E-DEVELOPMENT-FLOW.md](E2E-DEVELOPMENT-FLOW.md)
- **Phase 2 Guide:** [PHASE-2-IMPLEMENTATION.md](PHASE-2-IMPLEMENTATION.md)

### Common Commands Reference
```bash
# Start everything in one command
# Backend
cd backend && source venv/bin/activate && python run.py &

# Frontend (in new terminal)
cd frontend/web && npm run dev

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## ✨ You're Ready to Develop!

Start with the End-to-End Development Flow guide to understand the full architecture and begin implementing Phase 2 features.

**Happy Coding!** 🎉

