# Phase 2A Developer Quick Start Guide

## Overview
This guide shows developers how to use the discovery services for hotels, restaurants, and attractions with smart budget recommendations.

## Key Principle: Budget-First Recommendations

✅ **DO**: Show users best value options (high rating, low price)  
✅ **DO**: Filter by minimum quality threshold (3.5+ stars)  
✅ **DO**: Include external booking links (Booking.com, Google Hotels, etc.)  
❌ **DON'T**: Manage bookings directly  
❌ **DON'T**: Process payments or cancellations  
❌ **DON'T**: Store sensitive booking information  

---

## 1. Hotel Discovery

### Setup
```python
from sqlalchemy.orm import Session
from app.services.hotel_service import HotelSearchService, HotelRecommendationService
from app.schemas.hotel import HotelSearchRequest

async def search_hotels(db: Session, user_id: str = None):
    service = HotelSearchService(db)
    # ... use service methods
```

### Search Hotels with Budget Filter
```python
request = HotelSearchRequest(
    city="Mumbai",
    country="India",
    min_price=50,
    max_price=150,
    min_rating=3.5,
    category="budget",  # budget, midrange, upscale, luxury
    sort_by="rating",   # rating, price, distance, review_count
    limit=10
)

results, total = service.search_hotels(request, user_id)

# Each result includes:
# - id, name, address, city, country
# - overall_rating, review_count, avg_price, lowest_price
# - category, amenities, booking_url
# - booking_links: {"booking.com": "...", "agoda": "...", ...}
```

### Get Best Value Hotels (Smart Recommendation)
```python
# Algorithm: rating/price ratio (highest value first)
best_value = service.get_best_value_hotels(
    city="Mumbai",
    country="India",
    limit=5,
    min_rating=3.5  # Quality threshold
)

# Returns top 5 hotels with best rating-to-price ratio
for hotel in best_value:
    print(f"{hotel.name}: ⭐{hotel.overall_rating} @ ${hotel.avg_price}/night")
    print(f"Book: {hotel.booking_links['booking.com']}")
```

### Get Budget-Friendly Hotels
```python
# High-rated hotels within user's budget
budget_options = service.get_budget_friendly_hotels(
    city="Mumbai",
    country="India",
    max_price=100,  # User's budget
    min_rating=3.5,
    limit=10
)
```

### Get Luxury Recommendations
```python
# For premium travelers
luxury = service.get_luxury_recommendations(
    city="Paris",
    country="France",
    min_stars=4,  # 4+ star hotels
    limit=5
)
```

### Get Price Trends (Price Predictions)
```python
# Check if prices are increasing or stable
trends = service.get_price_trends(
    hotel_id="uuid-here",
    days_back=30
)

# Returns:
# {
#   "current_price": 120.50,
#   "min_price_7days": 95.00,
#   "max_price_7days": 150.00,
#   "avg_price_7days": 120.00,
#   "trend": "stable"  # or "increasing", "decreasing"
# }

# Get booking recommendation
prediction = service.get_price_prediction(
    hotel_id="uuid-here",
    check_in_date=datetime.now(),
    check_out_date=datetime.now() + timedelta(days=3)
)

# Returns:
# {
#   "estimated_price": 120.50,
#   "price_trend": "stable",
#   "recommendation": "book_now",  # or "wait"
#   "booking_links": {
#       "booking.com": "https://...",
#       "google_hotels": "https://...",
#       ...
#   }
# }
```

---

## 2. Restaurant Discovery

### Setup
```python
from app.services.restaurant_service import RestaurantSearchService, RestaurantRecommendationService
from app.schemas.restaurant import RestaurantSearchRequest
```

### Search Restaurants
```python
request = RestaurantSearchRequest(
    city="Barcelona",
    country="Spain",
    cuisines=["Spanish", "Catalan"],
    price_levels=["$$", "$$$"],  # Filter by price level
    min_rating=3.5,
    sort_by="rating",
    limit=10
)

results, total = service.search_restaurants(request)
```

### Get Best Value Restaurants
```python
# Algorithm: rating / price_level (highest value first)
# Price levels: "$" (1), "$$" (2), "$$$" (3), "$$$$" (4)
best_value = service.get_best_value_restaurants(
    city="Barcelona",
    country="Spain",
    limit=5,
    min_rating=3.5
)

# Returns restaurants with best rating-to-price ratio
for restaurant in best_value:
    print(f"{restaurant.name}: ⭐{restaurant.overall_rating} ({restaurant.price_level})")
```

### Get Michelin Restaurants
```python
# For special occasions
michelin = service.get_michelin_restaurants(
    city="Paris",
    country="France",
    min_stars=1,  # 1, 2, or 3 stars
    limit=5
)
```

### Get Budget-Friendly Restaurants
```python
# Good food at affordable prices
budget = service.get_budget_friendly_restaurants(
    city="Bangkok",
    country="Thailand",
    price_levels=["$", "$$"],  # Budget range
    min_rating=3.5,
    limit=10
)
```

### Get Restaurant by Occasion
```python
# Recommendation service with occasion awareness
rec_service = RestaurantRecommendationService(db)

recommendations = rec_service.get_personalized_recommendations(
    user_id="user-uuid",
    city="London",
    country="United Kingdom",
    occasion="date"  # casual, date, business, family
)

# For date night: Fine dining, romantic atmosphere
# For casual: Budget-friendly, relaxed atmosphere
# For business: Upscale, professional atmosphere
# For family: Family-friendly, diverse menus
```

### Get Signature Dishes
```python
# Most popular dishes at a restaurant
dishes = service.get_signature_dishes(restaurant_id="uuid-here")

for dish in dishes:
    print(f"{dish['name']}: {dish['popularity_score']}/10")
    print(f"Mentioned {dish['reviewer_mentions']} times in reviews")
    print(f"Vegetarian: {'Yes' if 'vegetarian' in dish.get('dietary_info', []) else 'No'}")
```

---

## 3. Attraction Discovery

### Setup
```python
from app.services.attraction_service import AttractionSearchService, AttractionRecommendationService
from app.schemas.attraction import AttractionSearchRequest
```

### Search Attractions
```python
request = AttractionSearchRequest(
    city="Rome",
    country="Italy",
    categories=["museum", "monument"],
    max_entry_fee=20,  # Budget constraint
    min_rating=3.5,
    max_visit_duration_hours=4,  # Time constraint
    sort_by="rating",
    limit=10
)

results, total = service.search_attractions(request)
```

### Get Budget-Friendly Attractions
```python
# Free attractions first, then low-cost
budget = service.get_budget_friendly_attractions(
    city="New York",
    country="USA",
    max_entry_fee=15,
    min_rating=3.5,
    limit=10
)

# Returns free attractions first, then affordable paid attractions
```

### Get Hidden Gems
```python
# Highly-rated but less-visited attractions
gems = service.get_hidden_gems(
    city="Prague",
    country="Czech Republic",
    min_rating=4.0,
    max_visitors_rank=20,  # Less than top 20 most visited
    limit=10
)
```

### Get Quick Visit Attractions
```python
# Perfect for travelers with limited time
quick = service.get_quick_visit_attractions(
    city="Amsterdam",
    country="Netherlands",
    max_duration_hours=2,  # Can be visited in 2 hours
    limit=10
)
```

### Get Attractions by Type
```python
# Indoor (museums, galleries)
indoor = service.get_indoor_attractions(
    city="London",
    country="United Kingdom",
    limit=10
)

# Outdoor (parks, monuments)
outdoor = service.get_outdoor_attractions(
    city="Barcelona",
    country="Spain",
    limit=10
)
```

### Get Visitor Tips
```python
# Crowdsourced advice (timing, money, planning, experience)
tips = service.get_visitor_tips(
    attraction_id="uuid-here",
    tip_type="timing"  # timing, money, planning, experience
)

for tip in tips:
    print(f"💡 {tip['title']}")
    print(f"   {tip['content']}")
    print(f"   Helpful: {tip['helpful_count']} people")
    if tip['is_official']:
        print("   ✓ Official")
```

### Get Personalized Recommendations
```python
# Trip duration-aware suggestions
rec_service = AttractionRecommendationService(db)

recommendations = rec_service.get_personalized_recommendations(
    user_id="user-uuid",
    city="Barcelona",
    country="Spain",
    trip_duration_hours=6,  # Half-day trip
    limit=5
)

# Returns 5 attractions that fit in 6 hours
```

---

## 4. User Preferences Management

### Set Hotel Preferences
```python
from app.schemas.hotel import UserHotelPreferenceRequest

pref_request = UserHotelPreferenceRequest(
    min_budget=50,
    max_budget=200,
    currency="USD",
    preferred_categories=["budget", "midrange"],
    min_star_rating=3.5,
    preferred_amenities=["wifi", "gym", "pool"],
    preferred_chains=["Marriott", "IHG"],
    max_distance_km=5
)

# Save to database
preference = UserHotelPreference(
    user_id=user_id,
    **pref_request.dict()
)
db.add(preference)
db.commit()
```

### Set Restaurant Preferences
```python
from app.schemas.restaurant import UserRestaurantPreferenceRequest

pref_request = UserRestaurantPreferenceRequest(
    preferred_price_levels=["$", "$$"],
    max_cost_per_person=50,
    currency="USD",
    preferred_cuisines=["Italian", "Indian"],
    dietary_options=["vegetarian"],
    preferred_dining_style=["casual"],
    atmosphere_preferences=["family-friendly"],
    max_distance_km=5
)

# Save to database
```

### Set Attraction Preferences
```python
from app.schemas.attraction import UserAttractionPreferenceRequest

pref_request = UserAttractionPreferenceRequest(
    preferred_categories=["museum", "park"],
    preferred_activity_type="indoor",
    max_visit_duration_hours=2,
    wheelchair_required=True,
    parking_required=False,
    max_ticket_price=15,
    currency="USD",
    max_distance_km=10
)

# Save to database
```

---

## 5. API Response Structure

### Hotel Response Example
```json
{
  "id": "uuid-123",
  "name": "Budget Inn Mumbai",
  "city": "Mumbai",
  "country": "India",
  "overall_rating": 4.2,
  "review_count": 156,
  "avg_price": 65.00,
  "lowest_price": 45.00,
  "currency": "USD",
  "category": "budget",
  "star_rating": 3.0,
  "amenities": ["wifi", "ac", "tv"],
  "booking_url": "https://booking.com/...",
  "booking_links": {
    "booking.com": "https://www.booking.com/hotel/...",
    "agoda": "https://www.agoda.com/hotel/...",
    "google_hotels": "https://www.google.com/travel/hotels/...",
    "hotel_direct": "https://budgetinn-mumbai.com/"
  },
  "is_featured": false
}
```

### Restaurant Response Example
```json
{
  "id": "uuid-456",
  "name": "Tapas Bar Barcelona",
  "city": "Barcelona",
  "country": "Spain",
  "primary_cuisine": "Spanish",
  "cuisines": ["Spanish", "Catalan"],
  "price_level": "$$",
  "avg_cost_per_person": 25.00,
  "currency": "USD",
  "overall_rating": 4.3,
  "review_count": 342,
  "michelin_stars": 0,
  "dining_style": "casual",
  "accepts_reservations": true,
  "reservation_url": "https://resy.com/...",
  "is_trending": true,
  "booking_links": {
    "resy": "https://resy.com/...",
    "tripadvisor": "https://tripadvisor.com/..."
  }
}
```

### Attraction Response Example
```json
{
  "id": "uuid-789",
  "name": "Colosseum",
  "city": "Rome",
  "country": "Italy",
  "category": "monument",
  "attraction_type": "outdoor",
  "has_entry_fee": true,
  "entry_fee": 18.00,
  "currency": "USD",
  "overall_rating": 4.6,
  "review_count": 5234,
  "popularity_rank": 1,
  "typical_visit_duration_minutes": 120,
  "wheelchair_accessible": true,
  "parking_available": true,
  "opening_hours": {
    "monday": "08:30-19:00",
    "tuesday": "08:30-19:00"
  },
  "is_featured": true,
  "ticket_url": "https://colosseumtickets.com/"
}
```

---

## 6. Common Usage Patterns

### Pattern 1: Budget Traveler
```python
# 1. Get best value hotels
hotels = service.get_best_value_hotels("Bangkok", "Thailand", limit=5)

# 2. Get budget-friendly restaurants
restaurants = rest_service.get_budget_friendly_restaurants(
    "Bangkok", "Thailand", 
    price_levels=["$", "$$"], 
    limit=5
)

# 3. Get free/cheap attractions
attractions = attr_service.get_budget_friendly_attractions(
    "Bangkok", "Thailand",
    max_entry_fee=10,
    limit=10
)
```

### Pattern 2: Special Occasion (Date Night)
```python
# 1. Get fine dining restaurants
restaurants = rest_service.get_fine_dining_restaurants(
    "Paris", "France", 
    price_levels=["$$$", "$$$$"],
    limit=5
)

# 2. Get luxury hotels
hotels = hotel_service.get_luxury_recommendations(
    "Paris", "France",
    min_stars=4,
    limit=3
)

# 3. Get trending attractions
attractions = attr_service.get_trending_attractions(
    "Paris", "France",
    limit=5
)
```

### Pattern 3: Quick City Visit (4 Hours)
```python
# 1. Get quick-visit attractions
attractions = attr_service.get_quick_visit_attractions(
    "Rome", "Italy",
    max_duration_hours=2,  # Multiple attractions
    limit=5
)

# 2. Get nearby restaurants
restaurants = rest_service.search_restaurants(
    RestaurantSearchRequest(
        city="Rome",
        latitude=41.9028,  # Colosseum location
        longitude=12.4964,
        distance_km=1,
        price_levels=["$", "$$"],
        limit=3
    )
)

# 3. Plan itinerary based on recommendations
```

---

## 7. Error Handling

```python
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

try:
    results, total = service.search_hotels(request, user_id)
except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail="Database error")
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 8. Database Setup

Before using services, ensure database is ready:

```bash
# 1. Apply migrations
cd backend
alembic upgrade head

# 2. Seed sample data (Week 5)
python scripts/seed_data.py

# 3. Verify data
psql yatradiscover -c "SELECT COUNT(*) FROM hotels;"
```

---

## Summary

| Feature | Method | Use Case |
|---------|--------|----------|
| Best Value | `get_best_value_hotels()` | Smart recommendations |
| Budget | `get_budget_friendly_hotels()` | Limited budget |
| Luxury | `get_luxury_recommendations()` | Premium travelers |
| Trending | `get_trending_hotels()` | Popular choices |
| Price Trends | `get_price_trends()` | Booking decisions |
| Search | `search_hotels()` | Custom filters |

Next: Implement API endpoints using these services!
