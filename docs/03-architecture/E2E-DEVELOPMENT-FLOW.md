# YatraDiscover AI - End-to-End Development Flow

**Version:** 1.0  
**Status:** In Progress  
**Created:** 2024  

## 🎯 Overview

This document outlines the complete end-to-end development flow for YatraDiscover AI, from user authentication through itinerary creation, AI processing, and payment handling.

---

## 📊 User Journey Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION FLOW                        │
└─────────────────────────────────────────────────────────────────┘

1. AUTHENTICATION PHASE
   ├── User visits website/app (yatradiscover.com)
   ├── User chooses: Sign Up OR Sign In
   │
   ├─── SIGN UP FLOW:
   │    ├── Enter: Email, Username, Full Name, Password
   │    ├── Submit to /api/v1/auth/register
   │    ├── Backend: Hash password, Create user in DB
   │    ├── Backend: Generate JWT tokens (access + refresh)
   │    └── Return: User data + tokens to client
   │
   └─── SIGN IN FLOW:
        ├── Enter: Email, Password
        ├── Submit to /api/v1/auth/login
        ├── Backend: Verify credentials
        ├── Backend: Generate JWT tokens
        └── Return: User data + tokens to client

2. DASHBOARD PHASE
   ├── Store tokens in secure storage (localStorage/Keychain)
   ├── User sees dashboard with options:
   │   ├── Create New Itinerary
   │   ├── View My Itineraries
   │   ├── View Saved Destinations
   │   ├── My Bookings
   │   └── Account Settings
   └── All requests include Authorization: Bearer {access_token}

3. ITINERARY CREATION PHASE
   ├── User clicks "Create New Itinerary"
   ├── STEP 1: Trip Details
   │   ├── Destination(s)
   │   ├── Travel Dates (Start - End)
   │   ├── Budget
   │   ├── Travel Style (Adventure, Luxury, Budget, etc.)
   │   └── Group Size
   │   └── POST /api/v1/itineraries/start
   │
   ├── STEP 2: Preferences
   │   ├── Interests (Culture, Food, Nature, History, etc.)
   │   ├── Accommodation Type
   │   ├── Transportation Preference
   │   ├── Pace (Relaxed, Moderate, Fast-paced)
   │   └── PUT /api/v1/itineraries/{id}/preferences
   │
   ├── STEP 3: Generate with AI
   │   ├── Send to OpenAI GPT-4:
   │   │   "Create a {style} itinerary for {destination} from {start} to {end}..."
   │   ├── OpenAI returns suggestions:
   │   │   - Day-by-day activities
   │   │   - Restaurant recommendations
   │   │   - Hotels/Accommodations
   │   │   - Transportation details
   │   │   - Estimated costs
   │   └── Backend stores in itinerary_activities table
   │
   └── STEP 4: Review & Customize
       ├── User views AI-generated itinerary
       ├── User can: Edit, Add, Delete activities
       ├── User can: Mark favorites
       ├── User can: Save draft OR Publish
       └── PUT /api/v1/itineraries/{id}

4. BOOKING & PAYMENT PHASE
   ├── User clicks "Book This Itinerary"
   ├── Calculate Total Cost:
   │   ├── Accommodation costs
   │   ├── Activity costs
   │   ├── Transportation costs
   │   ├── Service fees (10%)
   │   └── Total Price
   │
   ├── Stripe Payment Integration:
   │   ├── Frontend: Display Stripe payment form
   │   ├── User: Enter card details
   │   ├── POST /api/v1/payments/create-checkout
   │   ├── Backend: Create Stripe payment intent
   │   ├── User: Complete payment in Stripe modal
   │   └── Webhook: /api/v1/payments/webhook
   │
   ├── Post-Payment:
   │   ├── Create booking record
   │   ├── Send confirmation email (SendGrid)
   │   ├── Update itinerary status to "BOOKED"
   │   ├── Create invoice PDF
   │   └── Return confirmation to user
   │
   └── User receives:
       ├── Confirmation email with booking details
       ├── PDF itinerary download
       ├── Invoice
       └── Booking reference code

5. TRIP MANAGEMENT PHASE
   ├── User can view "My Bookings" dashboard
   ├── For each booking:
   │   ├── View detailed itinerary
   │   ├── View booking confirmation
   │   ├── Download as PDF
   │   ├── Share with travel companions
   │   ├── Make modifications (paid)
   │   ├── Cancel booking (with refund policy)
   │   └── Add notes/reminders
   │
   └── Mobile apps: Offline access to itinerary

6. SOCIAL & SHARING PHASE
   ├── User can share itinerary with:
   │   ├── Other users (view-only by default)
   │   ├── Make collaborative (edit permissions)
   │   └── Generate shareable link
   │
   ├── Other users can:
   │   ├── View shared itinerary
   │   ├── Create itinerary from template
   │   └── Request to join trip
   │
   └── Notification system:
       ├── Share notifications
       ├── Booking reminders
       ├── Activity reminders
       └── Payment confirmations
```

---

## 🏗️ Backend API Endpoints - Phase 1

### Authentication Endpoints
```
POST   /api/v1/auth/register          → Create new user account
POST   /api/v1/auth/login             → User login
POST   /api/v1/auth/refresh           → Refresh access token
POST   /api/v1/auth/logout            → User logout
GET    /api/v1/auth/me                → Get current user info
PUT    /api/v1/auth/profile           → Update user profile
POST   /api/v1/auth/change-password   → Change password
POST   /api/v1/auth/forgot-password   → Send password reset email
POST   /api/v1/auth/reset-password    → Reset password with token
```

### User Endpoints
```
GET    /api/v1/users/{user_id}        → Get user profile
PUT    /api/v1/users/{user_id}        → Update user profile
DELETE /api/v1/users/{user_id}        → Delete account
GET    /api/v1/users/{user_id}/preferences → Get user preferences
PUT    /api/v1/users/{user_id}/preferences → Update preferences
```

### Itinerary Endpoints
```
POST   /api/v1/itineraries            → Create new itinerary
GET    /api/v1/itineraries            → List user's itineraries
GET    /api/v1/itineraries/{id}       → Get itinerary details
PUT    /api/v1/itineraries/{id}       → Update itinerary
DELETE /api/v1/itineraries/{id}       → Delete itinerary
GET    /api/v1/itineraries/{id}/activities → Get itinerary activities
POST   /api/v1/itineraries/{id}/activities → Add activity
PUT    /api/v1/itineraries/{id}/activities/{act_id} → Update activity
DELETE /api/v1/itineraries/{id}/activities/{act_id} → Delete activity
POST   /api/v1/itineraries/{id}/generate-ai → Generate with AI
```

### Destination Endpoints
```
GET    /api/v1/destinations           → List destinations
GET    /api/v1/destinations/{id}      → Get destination details
GET    /api/v1/destinations/search    → Search destinations
POST   /api/v1/destinations/{id}/save → Save destination
GET    /api/v1/users/saved-destinations → Get user's saved destinations
```

### Booking Endpoints
```
POST   /api/v1/bookings               → Create booking
GET    /api/v1/bookings               → List user's bookings
GET    /api/v1/bookings/{id}          → Get booking details
PUT    /api/v1/bookings/{id}          → Update booking
DELETE /api/v1/bookings/{id}          → Cancel booking
GET    /api/v1/bookings/{id}/invoice  → Download invoice
```

### Payment Endpoints
```
POST   /api/v1/payments/create-checkout → Create Stripe session
GET    /api/v1/payments/session/{id}  → Get payment session
POST   /api/v1/payments/webhook       → Stripe webhook handler
GET    /api/v1/payments/history       → Payment history
GET    /api/v1/payments/refund/{id}   → Initiate refund
```

### Review Endpoints
```
POST   /api/v1/reviews                → Create review
GET    /api/v1/reviews/itinerary/{id} → Get reviews for itinerary
GET    /api/v1/reviews/destination/{id} → Get reviews for destination
PUT    /api/v1/reviews/{id}           → Update review
DELETE /api/v1/reviews/{id}           → Delete review
```

---

## 🗄️ Database Schema - Core Tables

### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    profile_picture_url VARCHAR(500),
    bio TEXT,
    phone VARCHAR(20),
    country VARCHAR(100),
    preferences JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);
```

### itineraries
```sql
CREATE TABLE itineraries (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    destination VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    travel_style VARCHAR(50),
    group_size INT,
    interests JSONB,
    status VARCHAR(20) DEFAULT 'DRAFT', -- DRAFT, PUBLISHED, BOOKED, COMPLETED
    visibility VARCHAR(20) DEFAULT 'PRIVATE', -- PRIVATE, SHARED, PUBLIC
    total_cost DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### itinerary_activities
```sql
CREATE TABLE itinerary_activities (
    id UUID PRIMARY KEY,
    itinerary_id UUID NOT NULL,
    day INT NOT NULL,
    time TIME,
    activity_name VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    category VARCHAR(50),
    duration_hours INT,
    cost DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    booking_url VARCHAR(500),
    notes TEXT,
    is_booked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id)
);
```

### bookings
```sql
CREATE TABLE bookings (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    itinerary_id UUID NOT NULL,
    booking_reference VARCHAR(50) UNIQUE NOT NULL,
    total_cost DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_status VARCHAR(20), -- PENDING, COMPLETED, FAILED, REFUNDED
    status VARCHAR(20) DEFAULT 'CONFIRMED', -- CONFIRMED, CANCELLED, COMPLETED
    travelers_count INT,
    travelers_list JSONB,
    accommodation_details JSONB,
    special_requests TEXT,
    cancellation_policy TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id)
);
```

### payments
```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY,
    booking_id UUID NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(50),
    stripe_payment_id VARCHAR(255),
    status VARCHAR(20), -- PENDING, COMPLETED, FAILED, REFUNDED
    transaction_hash VARCHAR(255),
    receipt_url VARCHAR(500),
    refund_amount DECIMAL(10, 2),
    refund_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);
```

### saved_destinations
```sql
CREATE TABLE saved_destinations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    destination_name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    description TEXT,
    image_url VARCHAR(500),
    tags JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### reviews
```sql
CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    itinerary_id UUID,
    destination_name VARCHAR(255),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    comment TEXT,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (itinerary_id) REFERENCES itineraries(id)
);
```

---

## 🔄 API Request/Response Examples

### 1. User Registration
**Request:**
```json
POST /api/v1/auth/register
{
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid-1234",
    "email": "john@example.com",
    "username": "johndoe",
    "full_name": "John Doe"
  },
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 2. Create Itinerary
**Request:**
```json
POST /api/v1/itineraries
Authorization: Bearer {access_token}
{
  "title": "Paris Trip 2024",
  "destination": "Paris, France",
  "start_date": "2024-06-01",
  "end_date": "2024-06-07",
  "budget": 3000,
  "travel_style": "Cultural",
  "group_size": 2,
  "interests": ["Art", "Food", "History"]
}
```

**Response:**
```json
{
  "id": "uuid-5678",
  "title": "Paris Trip 2024",
  "destination": "Paris, France",
  "start_date": "2024-06-01",
  "end_date": "2024-06-07",
  "budget": 3000,
  "status": "DRAFT",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 3. Generate Itinerary with AI
**Request:**
```json
POST /api/v1/itineraries/{id}/generate-ai
Authorization: Bearer {access_token}
{}
```

**Response:**
```json
{
  "id": "uuid-5678",
  "activities": [
    {
      "day": 1,
      "time": "09:00",
      "activity_name": "Arrival & Louvre Museum",
      "description": "Arrive in Paris, settle into hotel, then visit the famous Louvre Museum",
      "location": "Louvre, Paris",
      "latitude": 48.8611,
      "longitude": 2.3361,
      "cost": 50,
      "duration_hours": 4
    },
    {
      "day": 1,
      "time": "18:00",
      "activity_name": "Dinner at Michelin Star Restaurant",
      "description": "Fine dining experience",
      "location": "Le Cinq, Paris",
      "latitude": 48.8686,
      "longitude": 2.3077,
      "cost": 150,
      "duration_hours": 2
    }
  ],
  "total_estimated_cost": 2950
}
```

### 4. Create Booking & Payment
**Request:**
```json
POST /api/v1/bookings
Authorization: Bearer {access_token}
{
  "itinerary_id": "uuid-5678",
  "travelers_count": 2,
  "travelers_list": [
    {"name": "John Doe", "email": "john@example.com"},
    {"name": "Jane Doe", "email": "jane@example.com"}
  ],
  "special_requests": "Vegetarian meals preferred"
}
```

**Response:**
```json
{
  "id": "uuid-9999",
  "booking_reference": "YD-2024-001234",
  "status": "CONFIRMED",
  "total_cost": 3000,
  "payment_status": "PENDING",
  "payment_url": "https://checkout.stripe.com/pay/cs_live_..."
}
```

---

## 📱 Frontend (Next.js) Flow

### Pages Structure
```
pages/
├── index.js                    → Homepage
├── auth/
│   ├── login.js               → Login page
│   ├── register.js            → Registration page
│   ├── forgot-password.js     → Forgot password
│   └── reset-password.js      → Reset password
│
├── dashboard/
│   ├── index.js               → User dashboard
│   ├── itineraries/
│   │   ├── index.js           → List itineraries
│   │   ├── [id]/index.js      → View itinerary
│   │   ├── [id]/edit.js       → Edit itinerary
│   │   └── create.js          → Create new itinerary
│   │
│   ├── bookings/
│   │   ├── index.js           → List bookings
│   │   └── [id]/index.js      → View booking
│   │
│   └── profile/
│       └── index.js           → User profile settings
│
└── destinations/
    ├── index.js               → Browse destinations
    └── [id]/index.js          → Destination details
```

### Key Components
```
components/
├── Auth/
│   ├── LoginForm.jsx
│   ├── RegisterForm.jsx
│   └── ProtectedRoute.jsx
│
├── Itinerary/
│   ├── ItineraryForm.jsx
│   ├── ItineraryViewer.jsx
│   ├── ActivityList.jsx
│   ├── ActivityForm.jsx
│   └── AIGenerationModal.jsx
│
├── Booking/
│   ├── BookingForm.jsx
│   ├── PaymentForm.jsx (Stripe)
│   └── ConfirmationModal.jsx
│
├── Navigation/
│   ├── Header.jsx
│   ├── Sidebar.jsx
│   └── UserMenu.jsx
│
└── Layout/
    ├── MainLayout.jsx
    └── DashboardLayout.jsx
```

---

## 📲 Mobile (iOS & Android) Flow

### Core Screens
```
iOS (SwiftUI):
├── AuthenticationView
│   ├── LoginView
│   ├── RegisterView
│   └── ForgotPasswordView
│
├── DashboardView
│   ├── ItinerariesListView
│   ├── BookingsListView
│   ├── SavedDestinationsView
│   └── ProfileView
│
├── ItineraryDetail
│   ├── MapView (MapKit)
│   ├── ActivityListView
│   ├── EditActivityView
│   └── NotesView
│
└── BookingFlow
    ├── BookingDetailsView
    ├── PaymentView
    └── ConfirmationView

Android (Jetpack Compose):
├── AuthScreen
│   ├── LoginScreen
│   ├── RegisterScreen
│   └── ForgotPasswordScreen
│
├── DashboardScreen
│   ├── ItinerariesScreen
│   ├── BookingsScreen
│   ├── SavedDestinationsScreen
│   └── ProfileScreen
│
├── ItineraryDetailScreen
│   ├── MapScreen (Google Maps)
│   ├── ActivityListScreen
│   ├── EditActivityScreen
│   └── NotesScreen
│
└── BookingFlow
    ├── BookingDetailsScreen
    ├── PaymentScreen
    └── ConfirmationScreen
```

### Offline Features
- Downloaded itinerary data stored locally
- Offline maps (Maps SDK)
- Local database sync when online
- Activity reminders work offline

---

## 🔐 Security Implementation

### Authentication Flow
1. User registers/logs in
2. Backend validates credentials
3. Backend generates JWT tokens (access + refresh)
4. Frontend stores tokens securely:
   - Web: Secure HTTPOnly Cookie
   - iOS: Keychain
   - Android: EncryptedSharedPreferences
5. All API requests include `Authorization: Bearer {token}`
6. Token refresh happens automatically before expiry

### Data Protection
- All API requests over HTTPS
- Passwords hashed with bcrypt
- PII encrypted at rest
- API rate limiting enabled
- CORS properly configured
- CSRF protection on web forms

### Secrets Management
- API keys stored in environment variables
- Stripe keys never exposed to frontend
- OpenAI keys never exposed to frontend
- Database credentials only on backend
- Supabase service role keys server-side only

---

## 🧪 Testing Strategy

### Backend Testing
```
tests/
├── unit/
│   ├── test_auth_service.py
│   ├── test_itinerary_service.py
│   ├── test_booking_service.py
│   └── test_payment_service.py
│
├── integration/
│   ├── test_auth_endpoints.py
│   ├── test_itinerary_endpoints.py
│   └── test_booking_flow.py
│
└── e2e/
    ├── test_user_registration.py
    ├── test_itinerary_creation.py
    └── test_payment_flow.py
```

### Frontend Testing
- Unit tests for components (Jest)
- Integration tests for pages (React Testing Library)
- E2E tests (Cypress/Playwright)
- Visual regression tests

### Mobile Testing
- Unit tests (XCTest / JUnit)
- UI tests (XCUITest / Espresso)
- API integration tests
- Performance tests

---

## 📊 Deployment Pipeline

### CI/CD Workflow
```
git push → GitHub Actions
    ↓
Run Linters (Backend + Frontend)
    ↓
Run Tests (Backend + Frontend)
    ↓
Build Backend Docker Image
    ↓
Build Frontend (Next.js)
    ↓
Security Scanning (Snyk)
    ↓
Deploy to Staging
    ↓
Run Integration Tests
    ↓
Approval for Production
    ↓
Deploy to Production
    ↓
Health Checks & Monitoring
```

---

## ✅ Implementation Checklist - Phase 1

### Backend
- [x] Project setup with FastAPI
- [x] Environment configuration
- [x] Authentication endpoints (register, login, refresh)
- [ ] User CRUD endpoints
- [ ] Itinerary CRUD endpoints
- [ ] Itinerary activities endpoints
- [ ] AI integration with OpenAI
- [ ] Booking endpoints
- [ ] Payment integration (Stripe)
- [ ] Database migrations
- [ ] Unit & integration tests
- [ ] API documentation

### Frontend (Next.js)
- [ ] Project setup
- [ ] Design system & components
- [ ] Authentication pages (login, register)
- [ ] Dashboard layout
- [ ] Itinerary creation wizard
- [ ] Itinerary editor
- [ ] Booking flow
- [ ] Payment integration
- [ ] User profile management
- [ ] Responsive design
- [ ] Unit & integration tests

### Mobile - iOS
- [ ] Project setup (SwiftUI)
- [ ] API service layer
- [ ] Authentication flow
- [ ] Dashboard
- [ ] Itinerary views
- [ ] Booking flow
- [ ] Offline support
- [ ] Unit tests

### Mobile - Android
- [ ] Project setup (Compose)
- [ ] API service layer
- [ ] Authentication flow
- [ ] Dashboard
- [ ] Itinerary views
- [ ] Booking flow
- [ ] Offline support
- [ ] Unit tests

### Infrastructure
- [ ] Cloudflare DNS setup
- [ ] SSL/TLS configuration
- [ ] WAF rules
- [ ] Rate limiting
- [ ] CDN setup
- [ ] Monitoring & alerts
- [ ] Backup strategy

### DevOps
- [ ] CI/CD pipeline setup
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Database backups
- [ ] Log aggregation
- [ ] Performance monitoring

---

## 🚀 Next Steps

1. **Start Backend Development** - Implement remaining API endpoints
2. **Frontend Development** - Build Next.js application
3. **Database Setup** - Create Supabase instance & migrations
4. **Integration Testing** - Test end-to-end flows
5. **Mobile Development** - iOS & Android apps
6. **Deployment** - Push to staging environment
7. **QA & Testing** - Full regression testing
8. **Production Launch** - Final checklist before go-live

---

## 📞 Support & Resources

- **Backend Docs:** [BACKEND-ARCHITECTURE.md](backend/BACKEND-ARCHITECTURE.md)
- **Frontend Docs:** [WEB-ARCHITECTURE.md](frontend/WEB-ARCHITECTURE.md)
- **iOS Docs:** [IOS-ARCHITECTURE.md](mobile/IOS-ARCHITECTURE.md)
- **Android Docs:** [ANDROID-ARCHITECTURE.md](mobile/ANDROID-ARCHITECTURE.md)

