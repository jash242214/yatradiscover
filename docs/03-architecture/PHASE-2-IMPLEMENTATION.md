# YatraDiscover AI - Phase 2 Implementation Guide

**Status:** Ready for Development  
**Priority:** HIGH  
**Timeline:** Weeks 2-4  

---

## 🎯 Phase 2 Goals

Complete the full end-to-end flow from user registration through AI-powered itinerary generation and booking/payment processing.

### Deliverables
1. ✅ Authentication system (already done)
2. User management endpoints
3. Itinerary CRUD operations
4. OpenAI AI integration
5. Booking system
6. Stripe payment processing
7. Email notifications
8. Comprehensive testing

---

## 📋 Implementation Order

### Week 1: User & Itinerary Management

#### Task 1.1: User Endpoints
**File:** `backend/app/api/v1/endpoints/users.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.user import UserProfile, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserProfile)
async def get_current_user(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    user = UserService.get_user(db, current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserProfile)
async def update_current_user(
    user_data: UserUpdate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    user = UserService.update_user(db, current_user_id, user_data)
    return user

@router.post("/preferences")
async def set_user_preferences(
    preferences: dict,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save user travel preferences"""
    user = UserService.set_preferences(db, current_user_id, preferences)
    return {"message": "Preferences saved", "user": user}
```

#### Task 1.2: Itinerary CRUD Endpoints
**File:** `backend/app/api/v1/endpoints/itineraries.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.base import get_db
from app.schemas.itinerary import (
    ItineraryCreate, ItineraryUpdate, ItineraryResponse
)
from app.services.itinerary_service import ItineraryService

router = APIRouter(prefix="/itineraries", tags=["itineraries"])

@router.post("", response_model=ItineraryResponse, status_code=201)
async def create_itinerary(
    itinerary_data: ItineraryCreate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new itinerary"""
    itinerary = ItineraryService.create(db, current_user_id, itinerary_data)
    return itinerary

@router.get("", response_model=list[ItineraryResponse])
async def list_itineraries(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's itineraries"""
    itineraries = ItineraryService.list_by_user(
        db, current_user_id, skip, limit, status
    )
    return itineraries

@router.get("/{itinerary_id}", response_model=ItineraryResponse)
async def get_itinerary(
    itinerary_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get itinerary details"""
    itinerary = ItineraryService.get(db, itinerary_id, current_user_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary

@router.put("/{itinerary_id}", response_model=ItineraryResponse)
async def update_itinerary(
    itinerary_id: str,
    itinerary_data: ItineraryUpdate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update itinerary"""
    itinerary = ItineraryService.update(
        db, itinerary_id, current_user_id, itinerary_data
    )
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary

@router.delete("/{itinerary_id}", status_code=204)
async def delete_itinerary(
    itinerary_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete itinerary"""
    success = ItineraryService.delete(db, itinerary_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return None
```

#### Task 1.3: Activity Endpoints
**File:** `backend/app/api/v1/endpoints/activities.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
from app.services.activity_service import ActivityService

router = APIRouter(prefix="/itineraries/{itinerary_id}/activities", tags=["activities"])

@router.post("", response_model=ActivityResponse, status_code=201)
async def create_activity(
    itinerary_id: str,
    activity_data: ActivityCreate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add activity to itinerary"""
    activity = ActivityService.create(
        db, itinerary_id, current_user_id, activity_data
    )
    return activity

@router.get("", response_model=list[ActivityResponse])
async def list_activities(
    itinerary_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all activities for itinerary"""
    activities = ActivityService.list_by_itinerary(
        db, itinerary_id, current_user_id
    )
    return activities

@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    itinerary_id: str,
    activity_id: str,
    activity_data: ActivityUpdate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update activity"""
    activity = ActivityService.update(
        db, activity_id, itinerary_id, current_user_id, activity_data
    )
    return activity

@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    itinerary_id: str,
    activity_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete activity"""
    success = ActivityService.delete(
        db, activity_id, itinerary_id, current_user_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return None
```

---

### Week 2: AI Integration & Booking

#### Task 2.1: OpenAI AI Integration
**File:** `backend/app/services/ai_service.py`

```python
import openai
from app.core.config import settings
from app.schemas.itinerary import ItineraryCreate
import json

class AIService:
    
    @staticmethod
    def generate_itinerary(itinerary_data: ItineraryCreate) -> dict:
        """Generate itinerary using OpenAI GPT-4"""
        
        prompt = f"""
        Create a detailed {itinerary_data.travel_style} travel itinerary for {itinerary_data.destination}
        from {itinerary_data.start_date} to {itinerary_data.end_date}.
        
        Budget: ${itinerary_data.budget}
        Group Size: {itinerary_data.group_size}
        Interests: {', '.join(itinerary_data.interests)}
        Travel Style: {itinerary_data.travel_style}
        
        Please provide:
        1. Day-by-day activities with times
        2. Restaurant recommendations with estimated costs
        3. Hotel/Accommodation suggestions
        4. Transportation details
        5. Estimated costs for each activity
        
        Format the response as JSON with the following structure:
        {{
            "activities": [
                {{
                    "day": 1,
                    "time": "09:00",
                    "activity_name": "...",
                    "description": "...",
                    "location": "...",
                    "cost": 50,
                    "duration_hours": 4
                }}
            ],
            "accommodations": [...],
            "restaurants": [...],
            "total_estimated_cost": 3000
        }}
        """
        
        response = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a expert travel planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS
        )
        
        # Parse response
        content = response.choices[0].message.content
        itinerary_data = json.loads(content)
        
        return itinerary_data
    
    @staticmethod
    async def refine_itinerary(
        itinerary_id: str,
        feedback: str,
        db: Session
    ) -> dict:
        """Refine itinerary based on user feedback"""
        # Implementation for iterative refinement
        pass
```

#### Task 2.2: Booking Endpoints
**File:** `backend/app/api/v1/endpoints/bookings.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("", response_model=BookingResponse, status_code=201)
async def create_booking(
    booking_data: BookingCreate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a booking for an itinerary"""
    booking = BookingService.create(db, current_user_id, booking_data)
    return booking

@router.get("", response_model=list[BookingResponse])
async def list_bookings(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's bookings"""
    bookings = BookingService.list_by_user(db, current_user_id)
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get booking details"""
    booking = BookingService.get(db, booking_id, current_user_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/{booking_id}/cancel", status_code=200)
async def cancel_booking(
    booking_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    booking = BookingService.cancel(db, booking_id, current_user_id)
    return booking
```

---

### Week 3: Payment & Notifications

#### Task 3.1: Stripe Payment Integration
**File:** `backend/app/services/payment_service.py`

```python
import stripe
from app.core.config import settings
from app.schemas.payment import CheckoutCreate
from sqlalchemy.orm import Session

stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    
    @staticmethod
    async def create_checkout_session(
        booking_id: str,
        amount: float,
        currency: str = "usd",
        success_url: str = None,
        cancel_url: str = None
    ) -> dict:
        """Create Stripe checkout session"""
        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "unit_amount": int(amount * 100),
                        "product_data": {
                            "name": f"Travel Booking - {booking_id}",
                            "description": "YatraDiscover AI Travel Itinerary Booking"
                        }
                    },
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url=success_url or f"{settings.FRONTEND_URL}/booking/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=cancel_url or f"{settings.FRONTEND_URL}/booking/cancel",
            metadata={
                "booking_id": booking_id
            }
        )
        
        return {
            "session_id": session.id,
            "payment_url": session.url,
            "client_secret": session.client_secret
        }
    
    @staticmethod
    async def verify_payment(session_id: str, db: Session) -> dict:
        """Verify payment completion"""
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == "paid":
            booking_id = session.metadata["booking_id"]
            # Update booking status
            # Create payment record
            return {
                "status": "success",
                "booking_id": booking_id,
                "amount": session.amount_total / 100,
                "currency": session.currency
            }
        
        return {"status": "failed"}
    
    @staticmethod
    async def process_webhook(event: dict, db: Session):
        """Process Stripe webhook events"""
        
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            booking_id = session.metadata["booking_id"]
            amount = session.amount_total / 100
            
            # Update payment & booking status
            # Send confirmation email
            await PaymentService.send_confirmation_email(booking_id)
        
        elif event["type"] == "charge.refunded":
            # Handle refund
            pass
```

#### Task 3.2: Email Notifications
**File:** `backend/app/services/email_service.py`

```python
import sendgrid
from sendgrid.helpers.mail import Mail
from app.core.config import settings
import jinja2

class EmailService:
    
    sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
    
    @staticmethod
    async def send_registration_email(email: str, username: str):
        """Send welcome email"""
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=email,
            subject="Welcome to YatraDiscover AI!",
            html_content=f"""
            <h1>Welcome, {username}!</h1>
            <p>Thank you for joining YatraDiscover AI.</p>
            <p>Start creating your personalized itineraries today!</p>
            """
        )
        EmailService.sg.send(message)
    
    @staticmethod
    async def send_booking_confirmation(email: str, booking_ref: str, itinerary_title: str):
        """Send booking confirmation"""
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=email,
            subject=f"Booking Confirmed - {booking_ref}",
            html_content=f"""
            <h1>Your booking is confirmed!</h1>
            <p>Booking Reference: {booking_ref}</p>
            <p>Trip: {itinerary_title}</p>
            <p>Download your itinerary: <a href="...">Download PDF</a></p>
            """
        )
        EmailService.sg.send(message)
    
    @staticmethod
    async def send_itinerary_ready(email: str, itinerary_title: str, view_url: str):
        """Send email when AI itinerary is ready"""
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=email,
            subject=f"Your AI Itinerary is Ready - {itinerary_title}",
            html_content=f"""
            <h1>Your itinerary has been generated!</h1>
            <p>Itinerary: {itinerary_title}</p>
            <p><a href="{view_url}">View Your Itinerary</a></p>
            """
        )
        EmailService.sg.send(message)
```

---

### Week 4: Testing & Documentation

#### Task 4.1: Unit Tests
**File:** `backend/tests/unit/test_itinerary_service.py`

```python
import pytest
from app.services.itinerary_service import ItineraryService
from app.schemas.itinerary import ItineraryCreate
from datetime import date

def test_create_itinerary(db_session):
    """Test itinerary creation"""
    data = ItineraryCreate(
        title="Paris Trip",
        destination="Paris, France",
        start_date=date(2024, 6, 1),
        end_date=date(2024, 6, 7),
        budget=3000,
        travel_style="Cultural",
        group_size=2,
        interests=["Art", "Food"]
    )
    
    itinerary = ItineraryService.create(
        db_session, "user-123", data
    )
    
    assert itinerary.id
    assert itinerary.title == "Paris Trip"
    assert itinerary.status == "DRAFT"

def test_list_user_itineraries(db_session):
    """Test listing user itineraries"""
    itineraries = ItineraryService.list_by_user(
        db_session, "user-123", skip=0, limit=10
    )
    assert isinstance(itineraries, list)

def test_update_itinerary(db_session, sample_itinerary):
    """Test updating itinerary"""
    from app.schemas.itinerary import ItineraryUpdate
    
    update_data = ItineraryUpdate(
        title="Updated Title",
        status="PUBLISHED"
    )
    
    updated = ItineraryService.update(
        db_session, sample_itinerary.id, "user-123", update_data
    )
    
    assert updated.title == "Updated Title"
    assert updated.status == "PUBLISHED"
```

#### Task 4.2: Integration Tests
**File:** `backend/tests/integration/test_itinerary_flow.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_complete_itinerary_flow(auth_token):
    """Test complete itinerary creation flow"""
    
    # 1. Create itinerary
    response = client.post(
        "/api/v1/itineraries",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "Paris Trip",
            "destination": "Paris, France",
            "start_date": "2024-06-01",
            "end_date": "2024-06-07",
            "budget": 3000,
            "travel_style": "Cultural",
            "group_size": 2,
            "interests": ["Art", "Food"]
        }
    )
    assert response.status_code == 201
    itinerary_id = response.json()["id"]
    
    # 2. Generate AI itinerary
    response = client.post(
        f"/api/v1/itineraries/{itinerary_id}/generate-ai",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    activities = response.json()["activities"]
    assert len(activities) > 0
    
    # 3. Create booking
    response = client.post(
        "/api/v1/bookings",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "itinerary_id": itinerary_id,
            "travelers_count": 2,
            "travelers_list": [
                {"name": "John", "email": "john@example.com"}
            ]
        }
    )
    assert response.status_code == 201
    booking_id = response.json()["id"]
    
    # 4. Verify booking
    response = client.get(
        f"/api/v1/bookings/{booking_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
```

---

## 📁 Updated Backend File Structure

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py ........................ ✅ DONE
│   │   │   ├── users.py ....................... NEW
│   │   │   ├── itineraries.py ................ NEW
│   │   │   ├── activities.py ................. NEW
│   │   │   ├── bookings.py ................... NEW
│   │   │   ├── payments.py ................... NEW
│   │   │   ├── reviews.py .................... NEW
│   │   │   └── destinations.py ............... NEW
│   │   └── router.py
│   │
│   ├── schemas/
│   │   ├── user.py ............................ ✅ DONE
│   │   ├── itinerary.py ...................... NEW
│   │   ├── activity.py ....................... NEW
│   │   ├── booking.py ........................ NEW
│   │   ├── payment.py ........................ NEW
│   │   └── review.py ......................... NEW
│   │
│   ├── services/
│   │   ├── auth_service.py ................... ✅ DONE
│   │   ├── user_service.py .................. NEW
│   │   ├── itinerary_service.py ............ NEW
│   │   ├── activity_service.py ............ NEW
│   │   ├── booking_service.py ............ NEW
│   │   ├── payment_service.py ............ NEW
│   │   ├── email_service.py ............... NEW
│   │   ├── ai_service.py .................. NEW
│   │   └── notification_service.py ....... NEW
│   │
│   ├── db/
│   │   ├── models/
│   │   │   ├── user.py ...................... ✅ DONE
│   │   │   ├── itinerary.py ................ NEW
│   │   │   ├── activity.py ................. NEW
│   │   │   ├── booking.py .................. NEW
│   │   │   ├── payment.py .................. NEW
│   │   │   └── review.py ................... NEW
│   │   └── base.py .......................... ✅ DONE
│   │
│   └── core/
│       ├── config.py ........................ ✅ DONE
│       ├── security.py ..................... ✅ DONE
│       └── constants.py .................... NEW
│
├── tests/
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   ├── test_itinerary_service.py
│   │   ├── test_booking_service.py
│   │   └── test_payment_service.py
│   │
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   ├── test_itinerary_flow.py
│   │   └── test_booking_payment_flow.py
│   │
│   ├── e2e/
│   │   ├── test_user_journey.py
│   │   └── test_complete_flow.py
│   │
│   └── conftest.py .......................... pytest fixtures
│
├── alembic/
│   ├── versions/
│   │   ├── 001_initial_schema.py ........... ✅ DONE
│   │   ├── 002_add_itinerary_tables.py .... NEW
│   │   ├── 003_add_booking_tables.py ...... NEW
│   │   └── 004_add_payment_tables.py ...... NEW
│   └── env.py
│
├── .env.example ............................ ✅ UPDATED
├── requirements.txt ........................ ✅ UPDATED
├── run.py ................................. ✅ DONE
├── Dockerfile ............................. ✅ DONE
└── docker-compose.yml ..................... ✅ DONE
```

---

## 🧪 Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/unit/test_itinerary_service.py -v

# Run integration tests only
pytest tests/integration/ -v

# Run with markers
pytest -m "not slow" -v
```

---

## 🚀 Deployment Checklist

- [ ] All endpoints tested
- [ ] Documentation updated
- [ ] Database migrations run
- [ ] Environment variables configured
- [ ] SSL certificates valid
- [ ] Rate limiting configured
- [ ] Error logging setup
- [ ] Monitoring alerts configured
- [ ] Backup strategy verified
- [ ] Security audit passed

---

## 📞 Support

For questions or issues:
1. Check the Backend Architecture guide
2. Review test examples
3. Check API documentation at `/docs`

