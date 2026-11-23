# Phase 2B Part 2 - Quick Start Guide

## 🚀 Starting Phase 2B Part 2

This guide will get you started with database setup, testing, and production readiness.

---

## ✅ Prerequisites

Before starting Part 2, verify you have:

- [x] All 19 API endpoints implemented (Part 1 complete)
- [x] PostgreSQL 15+ running locally
- [x] PostGIS extension enabled
- [x] Python dependencies installed
- [x] Alembic migrations ready

**Check PostgreSQL:**
```bash
psql --version
psql -U postgres -d yatradiscover -c "SELECT PostGIS_Version();"
```

---

## 📋 Phase 2B Part 2 Tasks (Estimated: 2-3 weeks)

### TASK 1: Database Migrations (1-2 hours) 🔴 BLOCKER
**Status**: Ready to execute  
**Effort**: 1-2 hours  
**Files Involved**: 
- `backend/alembic/versions/` (existing migrations)
- `backend/app/db/models.py` (Phase 2A models)

**Commands:**
```bash
cd backend

# Run all migrations
python -m alembic upgrade head

# Verify tables created
psql -U postgres -d yatradiscover -c "\dt"

# Check PostGIS geometry columns
psql -U postgres -d yatradiscover -c "SELECT table_name, column_name, udt_name FROM information_schema.columns WHERE udt_name = 'geometry' OR udt_name = 'geography';"
```

**Expected Outcome:**
- 15 tables created (hotels, restaurants, attractions, users, etc.)
- PostGIS geometry columns enabled
- Indexes created for performance
- Foreign key relationships established

---

### TASK 2: Seed Sample Data (1-2 hours) 🟡 HIGH
**Status**: Design ready, implementation pending  
**Effort**: 1-2 hours  
**Files to Create**:
- `backend/scripts/seed_data.py` (NEW)

**What to seed:**
```python
# Cities to seed
CITIES = ["New York", "Paris", "Tokyo", "Barcelona", "Dubai"]

# Per city:
# - 20-30 Hotels (various price ranges, ratings)
# - 15-20 Restaurants (cuisines, price levels, Michelin stars)
# - 15-20 Attractions (categories, fees, durations)
# - Total: ~350-400 records across all categories
```

**Data points to include:**
- Realistic coordinates (latitude/longitude)
- Price variations and historical trends
- Ratings and review counts
- Cuisines and dietary preferences
- Amenities and facilities
- Opening hours and accessibility

**Script Structure:**
```python
from sqlalchemy.orm import Session
from app.db.models import Hotel, Restaurant, Attraction
from app.db.session import get_db

def seed_hotels(db: Session):
    hotels = [
        Hotel(
            name="Hotel Name",
            city="New York",
            price_per_night=150,
            rating=4.5,
            review_count=250,
            # ... other fields
        ),
        # ... more hotels
    ]
    db.add_all(hotels)
    db.commit()

def seed_restaurants(db: Session):
    # Similar structure
    pass

def seed_attractions(db: Session):
    # Similar structure
    pass

if __name__ == "__main__":
    db = next(get_db())
    seed_hotels(db)
    seed_restaurants(db)
    seed_attractions(db)
    print("✅ Sample data seeded successfully!")
```

**Run seeding:**
```bash
cd backend
python scripts/seed_data.py
```

---

### TASK 3: Integrate with Main App (30 mins) 🟢 QUICK
**Status**: Code ready, integration pending  
**Effort**: 30 minutes  
**File to Update**: `backend/app/main.py`

**Add these imports:**
```python
from app.api.v2 import hotels, restaurants, attractions
```

**Add these routes (after existing routes):**
```python
# V2 API Routers
app.include_router(
    hotels.router,
    prefix="/api/v2/hotels",
    tags=["Hotels V2"]
)

app.include_router(
    restaurants.router,
    prefix="/api/v2/restaurants",
    tags=["Restaurants V2"]
)

app.include_router(
    attractions.router,
    prefix="/api/v2/attractions",
    tags=["Attractions V2"]
)
```

**Verify integration:**
```bash
cd backend
python -m uvicorn app.main:app --reload

# Open http://localhost:8000/api/docs
# Should see all 19 endpoints listed
```

---

### TASK 4: Write Unit Tests (4-6 hours) 🟡 HIGH
**Status**: Test framework ready, test cases pending  
**Effort**: 4-6 hours  
**Files to Create**:
- `backend/tests/services/test_hotel_search.py`
- `backend/tests/services/test_restaurant_search.py`
- `backend/tests/services/test_attraction_search.py`

**Test Services:**
```python
# Example: test_hotel_search.py
import pytest
from app.services.hotel import HotelSearchService
from app.db.models import Hotel

@pytest.fixture
def hotel_service(db_session):
    return HotelSearchService(db_session)

def test_search_hotels_by_city(hotel_service):
    results = hotel_service.search(city="Paris", limit=10)
    assert len(results) > 0
    assert all(h.city == "Paris" for h in results)

def test_get_budget_hotels(hotel_service):
    results = hotel_service.get_budget_hotels(limit=10)
    assert all(h.price_per_night < 50 for h in results)

def test_get_best_value_hotels(hotel_service):
    results = hotel_service.get_best_value_hotels(limit=10)
    # Best value = high rating / low price
    for h in results:
        value_score = (h.rating / h.price_per_night) * 100
        assert value_score > 0

def test_search_pagination(hotel_service):
    page1 = hotel_service.search(limit=10, offset=0)
    page2 = hotel_service.search(limit=10, offset=10)
    assert all(h not in page2 for h in page1)
```

**Run tests:**
```bash
cd backend
pytest tests/services/ -v
pytest tests/services/ -v --cov=app.services
```

**Coverage Target**: 80%+ for service layer

---

### TASK 5: Write Integration Tests (4-6 hours) 🟡 HIGH
**Status**: Test framework ready, test cases pending  
**Effort**: 4-6 hours  
**Files to Create**:
- `backend/tests/api/v2/test_hotels.py`
- `backend/tests/api/v2/test_restaurants.py`
- `backend/tests/api/v2/test_attractions.py`

**Test Endpoints:**
```python
# Example: test_hotels.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_hotels():
    response = client.post("/api/v2/hotels/search", json={
        "city": "Paris",
        "min_price": 50,
        "max_price": 200
    })
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "data" in response.json()

def test_search_hotels_invalid_price():
    response = client.post("/api/v2/hotels/search", json={
        "city": "Paris",
        "min_price": 200,
        "max_price": 50  # min > max
    })
    assert response.status_code == 400

def test_get_hotel_details():
    response = client.get("/api/v2/hotels/1")
    if response.status_code == 200:
        assert response.json()["success"] == True
        assert "data" in response.json()

def test_get_hotel_not_found():
    response = client.get("/api/v2/hotels/999999")
    assert response.status_code == 404

def test_pagination():
    response1 = client.get("/api/v2/hotels/best-value?limit=5&offset=0")
    response2 = client.get("/api/v2/hotels/best-value?limit=5&offset=5")
    
    data1 = response1.json()["data"]
    data2 = response2.json()["data"]
    
    assert len(data1) == 5
    assert len(data2) == 5
    assert data1 != data2
```

**Run tests:**
```bash
cd backend
pytest tests/api/v2/ -v
pytest tests/api/v2/ -v --cov=app.api
```

**Coverage Target**: 70%+ for API layer

---

### TASK 6: Add Authentication (2-3 hours) 🟡 MEDIUM
**Status**: Design ready, implementation pending  
**Effort**: 2-3 hours  
**Files to Create**:
- `backend/app/auth.py` (JWT authentication)

**JWT Implementation:**
```python
# backend/app/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

# Configuration
SECRET_KEY = "your-secret-key-here"  # Use environment variable!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"user_id": user_id}
```

**Use in endpoints:**
```python
@router.get("/api/v2/hotels/{id}")
async def get_hotel(id: int, current_user = Depends(get_current_user)):
    # Only authenticated users can access
    hotel = HotelSearchService().get_hotel(id)
    if not hotel:
        raise HTTPException(status_code=404)
    return {"success": True, "data": hotel}
```

---

### TASK 7: Generate API Documentation (1 hour) 🟢 QUICK
**Status**: Automatic via FastAPI, manual verification pending  
**Effort**: 1 hour  

**Run the app:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Access documentation:**
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

**Verify:**
- [ ] All 19 endpoints appear in /api/docs
- [ ] Request/response schemas are correct
- [ ] Error responses documented
- [ ] Parameters documented with descriptions
- [ ] Example requests/responses shown

**Export OpenAPI spec:**
```bash
curl http://localhost:8000/openapi.json > openapi.json
```

---

## 🎯 Completion Checklist for Phase 2B Part 2

- [ ] Database migrations executed successfully
- [ ] All 15 tables created with PostGIS support
- [ ] Sample data seeded (350+ records)
- [ ] Endpoints integrated with main.py
- [ ] Endpoints responding with sample data
- [ ] Unit tests written (80%+ coverage)
- [ ] Integration tests written (70%+ coverage)
- [ ] All tests passing
- [ ] Authentication implemented
- [ ] API documentation generated (/api/docs working)
- [ ] Swagger UI shows all 19 endpoints
- [ ] Error handling verified
- [ ] Pagination working correctly
- [ ] No critical bugs or errors

---

## 📊 Testing Commands

**Run all tests:**
```bash
cd backend
pytest -v
pytest -v --cov=app
```

**Run specific test file:**
```bash
pytest tests/services/test_hotel_search.py -v
pytest tests/api/v2/test_hotels.py -v
```

**Run with coverage:**
```bash
pytest --cov=app --cov-report=html
```

---

## 🔍 Manual Testing

**Using curl:**
```bash
# Search hotels
curl -X POST http://localhost:8000/api/v2/hotels/search \
  -H "Content-Type: application/json" \
  -d '{"city": "Paris", "min_price": 50, "max_price": 200}'

# Get best value hotels
curl http://localhost:8000/api/v2/hotels/best-value?limit=10

# Search restaurants
curl -X POST http://localhost:8000/api/v2/restaurants/search \
  -H "Content-Type: application/json" \
  -d '{"city": "Tokyo", "cuisine": "Japanese"}'

# Get nearby attractions (geospatial)
curl "http://localhost:8000/api/v2/attractions/nearby?latitude=35.6762&longitude=139.6503&radius_km=5"
```

**Using Postman:**
1. Import OpenAPI spec: http://localhost:8000/openapi.json
2. Create requests for each endpoint
3. Test valid and invalid inputs
4. Verify error handling

---

## 📈 Success Metrics

**Phase 2B Part 2 is complete when:**

✅ All 19 endpoints tested and working  
✅ Database has 350+ sample records  
✅ Unit test coverage ≥ 80%  
✅ Integration test coverage ≥ 70%  
✅ All tests passing (0 failures)  
✅ Authentication implemented  
✅ API documentation complete  
✅ No critical bugs  
✅ Response times < 500ms (most queries)  
✅ Error handling verified  

---

## 🚨 Common Issues & Solutions

**Issue**: "ModuleNotFoundError: No module named 'app'"
```bash
# Solution: Run from backend directory
cd backend
python -m pytest
```

**Issue**: "FATAL: Ident authentication failed for user 'postgres'"
```bash
# Solution: Configure PostgreSQL authentication
# Edit pg_hba.conf to use password authentication
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'your_password';"
```

**Issue**: "PostGIS extension not found"
```bash
# Solution: Enable PostGIS in database
psql -U postgres -d yatradiscover -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

**Issue**: "Alembic migrations failed"
```bash
# Solution: Check migration status and history
alembic current
alembic history
alembic upgrade head
```

---

## 📚 References

- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [JWT Authentication](https://fastapi.tiangolo.com/advanced/security/oauth2-jwt/)

---

**Next Phase**: Phase 2B Part 3 - Performance Optimization (1 week)
- Load testing
- Query optimization
- Caching strategy
- Database indexing

---

Generated: 2026-11-19  
Phase: 2B Part 2 - Database, Tests, Auth, Docs  
Status: Ready to Execute
