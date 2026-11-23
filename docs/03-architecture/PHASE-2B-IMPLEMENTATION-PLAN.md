# Phase 2B - API Implementation Plan

**Status**: 🚀 IN PROGRESS  
**Duration**: 2-3 weeks  
**Start Date**: 2026-11-19  
**Target Completion**: 2026-12-03 to 2026-12-10

---

## 🎯 Objectives

- [ ] Implement 12-15 FastAPI endpoints
- [ ] Wire services to endpoints
- [ ] Add authentication/authorization (JWT)
- [ ] Add request validation & error handling
- [ ] Run database migrations
- [ ] Seed sample data
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Generate API documentation (Swagger)
- [ ] Deploy locally and test

---

## 📋 Endpoint Implementation Roadmap

### **Week 1: Hotels (Phase 2B-1)**
- [ ] POST `/api/v2/hotels/search` - Search hotels with filters
- [ ] GET `/api/v2/hotels/{id}` - Get hotel details
- [ ] GET `/api/v2/hotels/best-value` - Best value recommendations
- [ ] GET `/api/v2/hotels/budget` - Budget-friendly hotels
- [ ] POST `/api/v2/hotels/{id}/preferences` - Save user preferences
- [ ] GET `/api/v2/hotels/trending` - Trending hotels

**Tests**: Unit tests for HotelSearchService + integration tests for endpoints

### **Week 2: Restaurants (Phase 2B-2)**
- [ ] POST `/api/v2/restaurants/search` - Search restaurants
- [ ] GET `/api/v2/restaurants/{id}` - Get restaurant details
- [ ] GET `/api/v2/restaurants/michelin` - Michelin-starred
- [ ] GET `/api/v2/restaurants/best-value` - Best value restaurants
- [ ] POST `/api/v2/restaurants/{id}/preferences` - Save user preferences
- [ ] GET `/api/v2/restaurants/occasion/{occasion}` - Occasion-based

**Tests**: Unit tests for RestaurantSearchService + integration tests

### **Week 2-3: Attractions (Phase 2B-3)**
- [ ] POST `/api/v2/attractions/search` - Search attractions
- [ ] GET `/api/v2/attractions/{id}` - Get attraction details
- [ ] GET `/api/v2/attractions/hidden-gems` - Hidden gems
- [ ] GET `/api/v2/attractions/quick-visit` - Quick visit attractions
- [ ] POST `/api/v2/attractions/{id}/preferences` - Save user preferences
- [ ] GET `/api/v2/attractions/nearby` - Geospatial search

**Tests**: Unit tests for AttractionSearchService + integration tests

---

## 🔧 Technical Implementation Steps

### Phase 2B-1: Project Setup
```
1. Create FastAPI application structure
2. Set up main.py with app initialization
3. Configure CORS, middleware
4. Set up environment variables
5. Create routers for each feature
```

### Phase 2B-2: Database Setup
```
1. Run: alembic upgrade head
2. Create sample data seeds
3. Verify tables created
4. Test PostGIS queries
```

### Phase 2B-3: Endpoint Implementation
```
1. Create routers: api/v2/hotels.py, restaurants.py, attractions.py
2. Wire services to endpoints
3. Add request/response serialization
4. Add error handling
5. Add pagination support
```

### Phase 2B-4: Authentication
```
1. Create JWT token generation
2. Add dependency for auth check
3. Add user_id extraction from token
4. Secure endpoints with @auth_required
```

### Phase 2B-5: Testing
```
1. Unit tests for services
2. Integration tests for endpoints
3. Test error cases
4. Test authentication/authorization
5. Test pagination and filtering
```

### Phase 2B-6: Documentation
```
1. Generate Swagger/OpenAPI docs
2. Create endpoint documentation
3. Document error codes
4. Create postman collection
```

---

## 📂 File Structure (Phase 2B)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    (NEW - FastAPI app)
│   ├── config.py                  (EXISTS - env config)
│   ├── auth.py                    (NEW - JWT auth)
│   ├── dependencies.py            (NEW - dependency injection)
│   ├── exceptions.py              (NEW - custom exceptions)
│   ├── db/
│   │   ├── models/
│   │   │   ├── hotel.py          (EXISTS)
│   │   │   ├── restaurant.py      (EXISTS)
│   │   │   └── attraction.py      (EXISTS)
│   │   └── session.py            (EXISTS - DB session)
│   ├── schemas/
│   │   ├── hotel.py              (EXISTS)
│   │   ├── restaurant.py          (EXISTS)
│   │   └── attraction.py          (EXISTS)
│   ├── services/
│   │   ├── hotel_service.py       (EXISTS)
│   │   ├── restaurant_service.py  (EXISTS)
│   │   └── attraction_service.py  (EXISTS)
│   └── api/
│       ├── __init__.py            (NEW)
│       └── v2/
│           ├── __init__.py        (NEW)
│           ├── hotels.py          (NEW - hotel endpoints)
│           ├── restaurants.py     (NEW - restaurant endpoints)
│           └── attractions.py     (NEW - attraction endpoints)
├── tests/
│   ├── __init__.py                (NEW)
│   ├── test_hotels.py             (NEW)
│   ├── test_restaurants.py        (NEW)
│   └── test_attractions.py        (NEW)
├── alembic/
│   ├── versions/
│   │   ├── 001_initial_hotel_tables.py (EXISTS)
│   │   ├── 002_restaurant_tables.py (EXISTS)
│   │   └── 003_attraction_tables.py (EXISTS)
│   └── env.py                     (EXISTS)
├── requirements.txt               (UPDATE - add FastAPI, pytest)
└── .env.example                   (NEW - example env vars)
```

---

## 🚀 Implementation Strategy

### **Approach: Incremental (Hotels → Restaurants → Attractions)**

**Why this approach?**
- ✅ Faster feedback loop
- ✅ Test as we build
- ✅ Learn patterns from hotels, apply to restaurants/attractions
- ✅ Easier to debug and iterate

**Benefits:**
1. Hotels foundation → establish patterns
2. Restaurants → apply patterns with variations
3. Attractions → leverage established patterns

---

## ✅ Success Criteria for Phase 2B

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| Endpoints | 12-15 | All endpoints working |
| Tests | 80%+ coverage | Unit + integration tests |
| Documentation | Complete | Swagger/OpenAPI docs |
| Sample Data | Realistic | 20-30 per category |
| Performance | <500ms | API response time |
| Error Handling | Comprehensive | All edge cases covered |

---

## 📊 Estimated Effort Breakdown

| Task | Duration | Status |
|------|----------|--------|
| Project setup + main.py | 2 hours | Pending |
| Database migrations + seeds | 2 hours | Pending |
| Hotel endpoints (6) | 6 hours | Pending |
| Hotel tests | 4 hours | Pending |
| Restaurant endpoints (6) | 6 hours | Pending |
| Restaurant tests | 4 hours | Pending |
| Attraction endpoints (6) | 6 hours | Pending |
| Attraction tests | 4 hours | Pending |
| Auth + middleware | 3 hours | Pending |
| API documentation | 2 hours | Pending |
| Integration testing | 4 hours | Pending |
| **Total** | **~43 hours** | **~1 week** |

---

## 🔐 Security Checklist for Phase 2B

- [ ] JWT authentication on all endpoints
- [ ] Rate limiting on login/search endpoints
- [ ] Input validation (Pydantic handles this)
- [ ] Error messages don't leak sensitive info
- [ ] CORS configuration restricted
- [ ] NO booking payment processing (affiliate only)
- [ ] User data encryption ready
- [ ] Audit logging setup
- [ ] API key management for external services

---

## 📝 Next Immediate Steps

1. Create FastAPI main.py
2. Set up routers and endpoints
3. Run database migrations
4. Create sample data seeds
5. Test first hotel endpoint
6. Build from there incrementally

---

## 🎯 Phase 2B Completion Criteria

✅ All 12-15 endpoints implemented and working  
✅ All endpoints tested (unit + integration)  
✅ Database migrations run successfully  
✅ Sample data seeded  
✅ API documentation generated  
✅ Error handling comprehensive  
✅ Performance optimized  
✅ All code committed to GitHub  

---

**Ready to start? Let's build! 🚀**

Generated: 2026-11-19  
Phase: Phase 2B - API Implementation  
Status: Ready to Begin
