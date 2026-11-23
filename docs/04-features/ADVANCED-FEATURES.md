# YatraDiscover AI - Advanced Discovery Features

**Version:** 1.0  
**Status:** Ready for Phase 2 Development  
**Priority:** HIGH  

---

## 🎯 Overview

Advanced features for intelligent travel discovery:
- 🏨 Smart hotel recommendations with price filtering
- 🍽️ Food discoveries and restaurant recommendations
- 🎯 Attractions and famous places
- ⭐ Review aggregation system
- 💡 Smart recommendations engine
- 📍 Location-based discovery
- 🔍 Advanced search and filtering

---

## 1. 🏨 SMART HOTEL DISCOVERY

### Features
- **Price-based filtering** - Sort by budget range
- **Review aggregation** - Rating from multiple sources
- **Amenities filtering** - WiFi, Pool, Gym, etc.
- **Location proximity** - Distance from attractions
- **Best value ranking** - Rating/price ratio
- **Photo gallery** - High-quality images
- **Guest reviews** - Authentic feedback

### Data Model

```sql
CREATE TABLE hotels (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Pricing
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    price_per_night DECIMAL(10, 2),
    
    -- Rating
    average_rating DECIMAL(3, 2), -- 0-5
    total_reviews INT DEFAULT 0,
    rating_breakdown JSONB, -- {5: 100, 4: 50, 3: 20, 2: 5, 1: 2}
    
    -- Details
    description TEXT,
    hotel_type VARCHAR(50), -- LUXURY, MIDRANGE, BUDGET, BOUTIQUE
    star_rating INT, -- 1-5 stars
    amenities JSONB, -- ["WiFi", "Pool", "Gym", "Restaurant"]
    
    -- Contact
    phone VARCHAR(20),
    website VARCHAR(500),
    email VARCHAR(255),
    booking_url VARCHAR(500),
    
    -- Metadata
    images_count INT,
    verified BOOLEAN DEFAULT FALSE,
    source VARCHAR(50), -- BOOKING, TRIPADVISOR, GOOGLE, MANUAL
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE hotel_reviews (
    id UUID PRIMARY KEY,
    hotel_id UUID NOT NULL,
    user_id UUID,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    comment TEXT,
    verified_booking BOOLEAN,
    helpful_count INT DEFAULT 0,
    source VARCHAR(50), -- BOOKING, TRIPADVISOR, GOOGLE, APP
    review_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE hotel_images (
    id UUID PRIMARY KEY,
    hotel_id UUID NOT NULL,
    image_url VARCHAR(500),
    image_type VARCHAR(50), -- MAIN, ROOM, LOBBY, POOL, etc.
    display_order INT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id)
);

CREATE TABLE hotel_amenities (
    id UUID PRIMARY KEY,
    hotel_id UUID NOT NULL,
    amenity_name VARCHAR(100),
    category VARCHAR(50), -- FACILITIES, SERVICES, WELLNESS, etc.
    availability BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id)
);
```

### API Endpoints

```
# Hotel Discovery
GET    /api/v1/hotels/search
       ?destination=Paris
       &check_in=2024-06-01
       &check_out=2024-06-07
       &min_price=50
       &max_price=300
       &rating_min=4.0
       &amenities=WiFi,Pool,Restaurant
       &sort_by=best_value (rating/price)
       &limit=20

GET    /api/v1/hotels/{id}
       - Full hotel details
       - Reviews with pagination
       - Images gallery
       - Booking options

POST   /api/v1/hotels/{id}/reviews
       - Add guest review
       - Only for verified bookings

GET    /api/v1/hotels/{id}/reviews
       ?sort_by=helpful,recent,rating
       &rating_filter=5,4  (show only 5 and 4 star reviews)

GET    /api/v1/destinations/{destination}/hotels
       - All hotels in destination
       - Sorted by rating/price ratio
```

### Smart Filtering Logic

```python
# backend/app/services/hotel_service.py

class HotelService:
    
    @staticmethod
    def search_hotels(
        destination: str,
        check_in: date,
        check_out: date,
        min_price: float = None,
        max_price: float = None,
        min_rating: float = None,
        amenities: list = None,
        sort_by: str = "best_value",
        limit: int = 20
    ) -> list:
        """Search hotels with smart filtering"""
        
        query = db.query(Hotel).filter(
            Hotel.destination == destination
        )
        
        # Price filtering
        if min_price:
            query = query.filter(Hotel.price_per_night >= min_price)
        if max_price:
            query = query.filter(Hotel.price_per_night <= max_price)
        
        # Rating filtering
        if min_rating:
            query = query.filter(Hotel.average_rating >= min_rating)
        
        # Amenities filtering
        if amenities:
            for amenity in amenities:
                query = query.filter(
                    Hotel.amenities.contains([amenity])
                )
        
        # Sorting logic
        if sort_by == "best_value":
            # Highest rating for lowest price
            query = query.order_by(
                (Hotel.average_rating / Hotel.price_per_night).desc()
            )
        elif sort_by == "price_low":
            query = query.order_by(Hotel.price_per_night.asc())
        elif sort_by == "rating":
            query = query.order_by(Hotel.average_rating.desc())
        elif sort_by == "newest":
            query = query.order_by(Hotel.last_updated.desc())
        
        return query.limit(limit).all()
    
    @staticmethod
    def get_hotel_details(hotel_id: str) -> dict:
        """Get detailed hotel information"""
        hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
        
        return {
            "id": hotel.id,
            "name": hotel.name,
            "description": hotel.description,
            "location": {
                "latitude": hotel.latitude,
                "longitude": hotel.longitude,
                "address": hotel.address
            },
            "pricing": {
                "min_price": hotel.min_price,
                "max_price": hotel.max_price,
                "currency": hotel.currency,
                "per_night": hotel.price_per_night
            },
            "rating": {
                "average": hotel.average_rating,
                "total_reviews": hotel.total_reviews,
                "breakdown": hotel.rating_breakdown
            },
            "amenities": hotel.amenities,
            "images": [img.image_url for img in hotel.images],
            "booking_url": hotel.booking_url,
            "reviews": get_top_reviews(hotel_id)
        }
```

---

## 2. 🍽️ RESTAURANT & FOOD DISCOVERY

### Features
- **Cuisine filtering** - Italian, Indian, Chinese, etc.
- **Price categorization** - Budget, Mid, Fine dining
- **Specialties** - Local dishes, trending items
- **Food review aggregation**
- **Best food recommendations**
- **Dietary preferences** - Vegan, Vegetarian, Gluten-free
- **Michelin guide integration** (where available)

### Data Model

```sql
CREATE TABLE restaurants (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255),
    city VARCHAR(100),
    cuisine_type VARCHAR(100), -- Italian, Indian, Japanese, etc.
    sub_cuisine VARCHAR(100), -- Fine dining, Street food, Casual
    
    -- Location
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Pricing
    price_level INT, -- 1-4 ($, $$, $$$, $$$$)
    average_cost DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Rating & Reviews
    average_rating DECIMAL(3, 2),
    total_reviews INT,
    rating_breakdown JSONB,
    
    -- Details
    description TEXT,
    specialties JSONB, -- ["Pasta", "Risotto", "Pizza"]
    dietary_options JSONB, -- ["Vegan", "Vegetarian", "Gluten-free"]
    seating_capacity INT,
    reservation_required BOOLEAN,
    has_wifi BOOLEAN,
    
    -- Contact
    phone VARCHAR(20),
    website VARCHAR(500),
    reservation_url VARCHAR(500),
    
    -- Status
    is_open BOOLEAN DEFAULT TRUE,
    michelin_stars INT, -- 0-3
    popular_dishes JSONB,
    best_time_to_visit VARCHAR(100), -- e.g., "Lunch 12-2pm"
    
    source VARCHAR(50), -- GOOGLE, TRIPADVISOR, MICHELIN, MANUAL
    verified BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE restaurant_dishes (
    id UUID PRIMARY KEY,
    restaurant_id UUID NOT NULL,
    dish_name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    is_signature BOOLEAN,
    is_trending BOOLEAN,
    popularity_score INT DEFAULT 0,
    dietary_tags JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE food_reviews (
    id UUID PRIMARY KEY,
    restaurant_id UUID NOT NULL,
    user_id UUID,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    food_quality INT CHECK (food_quality >= 1 AND food_quality <= 5),
    service_quality INT CHECK (service_quality >= 1 AND service_quality <= 5),
    atmosphere INT CHECK (atmosphere >= 1 AND atmosphere <= 5),
    comment TEXT,
    dishes_tried JSONB,
    would_recommend BOOLEAN,
    visit_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### API Endpoints

```
# Restaurant Discovery
GET    /api/v1/restaurants/search
       ?destination=Paris
       &cuisine=Italian,French
       &price_level=1,2
       &rating_min=4.0
       &dietary=Vegan
       &special=Michelin
       &sort_by=rating,popular,trending
       &limit=20

GET    /api/v1/restaurants/{id}
       - Full restaurant details
       - Signature dishes
       - Reviews with ratings
       - Photos gallery
       - Reservation link

GET    /api/v1/restaurants/{id}/dishes
       - Menu with prices
       - Signature items
       - Trending dishes
       - Dietary information

POST   /api/v1/restaurants/{id}/reviews
       - Food rating
       - Service rating
       - Atmosphere rating
       - Dish recommendations

GET    /api/v1/destinations/{destination}/food-guide
       - Best restaurants by category
       - Top-rated dishes
       - Local specialties
       - Budget options
```

### Smart Recommendations

```python
# backend/app/services/food_service.py

class FoodService:
    
    @staticmethod
    def get_best_food_experiences(
        destination: str,
        preferences: dict = None,
        budget: str = "moderate"
    ) -> dict:
        """Get curated food experiences"""
        
        budget_mapping = {
            "budget": (1, 2),      # $ to $$
            "moderate": (2, 3),    # $$ to $$$
            "luxury": (3, 4)       # $$$ to $$$$
        }
        
        price_range = budget_mapping.get(budget, (2, 3))
        
        restaurants = db.query(Restaurant).filter(
            Restaurant.destination == destination,
            Restaurant.price_level.between(*price_range),
            Restaurant.average_rating >= 4.0
        ).all()
        
        return {
            "top_rated": sorted(
                restaurants, 
                key=lambda x: x.average_rating, 
                reverse=True
            )[:5],
            "trending": sorted(
                restaurants,
                key=lambda x: x.popularity_score,
                reverse=True
            )[:5],
            "signature_dishes": get_signature_dishes(destination),
            "local_favorites": get_local_specialties(destination),
            "michelin_options": get_michelin_restaurants(destination),
            "budget_friendly": sorted(
                restaurants,
                key=lambda x: x.average_cost
            )[:5]
        }
    
    @staticmethod
    def get_signature_dishes(destination: str) -> list:
        """Get must-try dishes in a destination"""
        
        dishes = db.query(RestaurantDish).join(
            Restaurant
        ).filter(
            Restaurant.destination == destination,
            RestaurantDish.is_signature == True
        ).order_by(
            RestaurantDish.popularity_score.desc()
        ).limit(10).all()
        
        return dishes
```

---

## 3. 🎯 ATTRACTIONS & FAMOUS PLACES

### Features
- **Category-based discovery** - Museums, Parks, Monuments
- **Popularity rankings**
- **Visitor reviews and ratings**
- **Operating hours and tickets**
- **Best time to visit**
- **Nearby facilities** - Cafes, restrooms, parking
- **Accessibility information**

### Data Model

```sql
CREATE TABLE attractions (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255),
    city VARCHAR(100),
    category VARCHAR(100), -- Museum, Park, Monument, Church, etc.
    sub_category VARCHAR(100),
    
    -- Location
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Details
    description TEXT,
    history_significance INT, -- 1-5, how important historically
    popular_for JSONB, -- ["Photos", "History", "Architecture"]
    
    -- Visiting Info
    opening_hours JSONB, -- {"monday": "09:00-17:00"}
    entry_fee DECIMAL(10, 2),
    free_entry BOOLEAN,
    currency VARCHAR(3),
    avg_visit_duration_minutes INT,
    
    -- Rating
    average_rating DECIMAL(3, 2),
    total_reviews INT,
    
    -- Logistics
    closest_parking_distance INT, -- in meters
    has_restrooms BOOLEAN,
    has_cafeteria BOOLEAN,
    wheelchair_accessible BOOLEAN,
    guide_services BOOLEAN,
    
    -- More Info
    official_website VARCHAR(500),
    booking_required BOOLEAN,
    best_time_to_visit VARCHAR(100),
    peak_hours JSONB,
    
    verified BOOLEAN DEFAULT FALSE,
    source VARCHAR(50),
    trending BOOLEAN DEFAULT FALSE,
    popularity_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE attraction_reviews (
    id UUID PRIMARY KEY,
    attraction_id UUID NOT NULL,
    user_id UUID,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    visit_date DATE,
    crowdedness INT, -- 1-5, how crowded it was
    worth_visit BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (attraction_id) REFERENCES attractions(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE attraction_photos (
    id UUID PRIMARY KEY,
    attraction_id UUID NOT NULL,
    photo_url VARCHAR(500),
    photo_type VARCHAR(50), -- EXTERIOR, INTERIOR, DETAIL
    uploader_user_id UUID,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (attraction_id) REFERENCES attractions(id)
);
```

### API Endpoints

```
# Attractions Discovery
GET    /api/v1/attractions/search
       ?destination=Paris
       &category=Museum,Park
       &rating_min=4.0
       &free=true
       &wheelchair_accessible=true
       &sort_by=rating,popular,trending
       &limit=20

GET    /api/v1/attractions/{id}
       - Full details with photos
       - Reviews and ratings
       - Visitor tips
       - Operating hours
       - Nearby facilities

GET    /api/v1/destinations/{destination}/top-attractions
       - Top-rated attractions
       - Must-see places
       - Hidden gems
       - Best photo spots

GET    /api/v1/destinations/{destination}/attractions/by-category
       - Grouped by category
       - Ranked by rating
       - With visitor count
```

---

## 4. ⭐ SMART RECOMMENDATIONS ENGINE

### Recommendation Types

```python
class RecommendationEngine:
    
    # 1. Based on Itinerary Style
    def recommend_for_style(travel_style: str, destination: str):
        """
        Adventure → Outdoor activities, hiking, water sports
        Culture → Museums, historical sites, guided tours
        Luxury → 5-star hotels, fine dining, exclusive experiences
        Budget → Cheap eats, free attractions, hostels
        Romance → Scenic spots, candlelight dinners, spa
        Family → Kid-friendly attractions, parks, restaurants
        """
    
    # 2. Based on Price Budget
    def recommend_by_budget(budget: float, destination: str):
        """Filter all recommendations by budget"""
    
    # 3. Based on Interests
    def recommend_by_interests(interests: list, destination: str):
        """
        interests = ["Art", "Food", "History", "Nature"]
        Return matching hotels, restaurants, attractions
        """
    
    # 4. Trending/Popular Right Now
    def get_trending(destination: str):
        """Most visited, most reviewed, most photographed"""
    
    # 5. Hidden Gems
    def get_hidden_gems(destination: str):
        """High-rated but less crowded alternatives"""
    
    # 6. Best for Time of Day
    def get_recommendations_by_time(
        destination: str,
        time_of_day: str # morning, afternoon, evening, night
    ):
        """Best activities for different times"""
    
    # 7. Personalized (ML-Based)
    def get_personalized_recommendations(user_id: str):
        """Based on user's past travels and preferences"""
```

---

## 5. 📍 LOCATION-BASED FEATURES

### Nearby Discovery

```python
class LocationService:
    
    @staticmethod
    def find_nearby(
        latitude: float,
        longitude: float,
        radius_km: float = 1,
        category: str = None  # hotels, restaurants, attractions
    ) -> list:
        """Find places within radius using geospatial queries"""
        
        # Using PostGIS in PostgreSQL
        nearby = db.query(Place).filter(
            func.ST_Distance(
                func.ST_GeomFromText(f'POINT({longitude} {latitude})'),
                Place.location
            ) < radius_km * 1000
        )
        
        if category:
            nearby = nearby.filter(Place.category == category)
        
        return nearby.order_by(
            func.ST_Distance(
                func.ST_GeomFromText(f'POINT({longitude} {latitude})'),
                Place.location
            )
        ).all()
    
    @staticmethod
    def get_route_recommendations(
        start_point: tuple,  # (lat, lng)
        end_point: tuple,
        interests: list = None
    ):
        """Get interesting stops along a route"""
```

---

## 6. 🔍 ADVANCED FILTERING

### Filter Categories

```
Hotels:
- Price range (min-max)
- Star rating
- Amenities (multi-select)
- Guest rating (min)
- Property type (luxury, budget, boutique)
- Distance from landmarks
- Payment options

Restaurants:
- Cuisine type (multi)
- Price level
- Rating (min)
- Dietary preferences
- Seating (outdoor, private room)
- Reservation available
- Michelin guide
- Time (open now, opens today)

Attractions:
- Category (multi)
- Rating (min)
- Entry fee (free/paid)
- Accessibility
- Duration (quick visit, full day)
- Opening status (open now)
- Popularity (trending)
```

---

## 7. 📊 USER PREFERENCES & PROFILE

### Tracking User Preferences

```sql
CREATE TABLE user_travel_preferences (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE,
    
    -- Style
    preferred_travel_styles JSONB, -- [Adventure, Culture, Luxury]
    
    -- Budget
    budget_preference VARCHAR(50), -- Budget, Moderate, Luxury
    avg_spending_per_day DECIMAL(10, 2),
    
    -- Interests
    interests JSONB, -- [Art, Food, Nature, History]
    
    -- Dietary
    dietary_restrictions JSONB, -- [Vegan, Gluten-free]
    
    -- Hotel Preferences
    preferred_hotel_types JSONB, -- [Boutique, Resort]
    preferred_amenities JSONB,
    preferred_chain_hotels VARCHAR(100),
    
    -- Accessibility
    mobility_requirements VARCHAR(255),
    accessibility_needs JSONB,
    
    -- Social
    group_size INT,
    travel_companions VARCHAR(50), -- Solo, Partner, Family, Friends
    
    -- Pace
    trip_pace VARCHAR(50), -- Relaxed, Moderate, Fast-paced
    
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE user_save_history (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    saved_item_id UUID,
    saved_item_type VARCHAR(50), -- hotel, restaurant, attraction
    saved_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 8. 🎁 PERSONALIZATION & RECOMMENDATIONS

### AI-Powered Suggestions

```python
# backend/app/services/recommendation_service.py

class RecommendationService:
    
    @staticmethod
    def get_personalized_itinerary_items(
        user_id: str,
        destination: str,
        itinerary_duration: int,
        budget: float
    ):
        """Generate personalized recommendations"""
        
        user = get_user_preferences(user_id)
        
        recommendations = {
            "hotels": rank_by_user_preferences(
                get_hotels(destination, budget),
                user.preferred_hotel_types,
                user.preferred_amenities
            ),
            "restaurants": rank_by_cuisine(
                get_restaurants(destination, budget),
                user.interests,
                user.dietary_restrictions
            ),
            "attractions": rank_by_interests(
                get_attractions(destination),
                user.interests
            ),
            "experiences": get_experiences(
                destination,
                user.interests,
                user.trip_pace
            )
        }
        
        return recommendations
    
    @staticmethod
    def calculate_relevance_score(
        item: dict,
        user_preferences: dict
    ) -> float:
        """Calculate how relevant item is to user (0-100)"""
        
        score = 0
        
        # Rating match (30%)
        score += (item['rating'] / 5) * 30
        
        # Price match (25%)
        score += price_alignment(item['price'], user_preferences['budget']) * 25
        
        # Interest match (30%)
        score += interest_alignment(item['tags'], user_preferences['interests']) * 30
        
        # Popularity match (15%)
        score += (item['popularity'] / 100) * 15
        
        return score
```

---

## 9. 📱 UI/UX COMPONENTS

### Frontend Components Needed

```jsx
// Hotels
<HotelSearch
  filters={{ priceRange, amenities, rating }}
  sortBy="best_value"
  results={hotels}
/>

<HotelCard
  hotel={hotel}
  reviews={hotel.reviews}
  images={hotel.images}
  actions={{ save, book, share }}
/>

// Restaurants
<RestaurantSearch
  filters={{ cuisine, priceLevel, dietary }}
  location={userLocation}
/>

<RestaurantCard
  restaurant={restaurant}
  signatureDishes={dishes}
  reservation={bookingUrl}
/>

// Attractions
<AttractionMap
  attractions={attractions}
  userLocation={userLocation}
  interactive={true}
/>

<AttractionCard
  attraction={attraction}
  reviews={reviews}
  photos={photos}
  operatingHours={hours}
/>

// General Discovery
<DiscoveryFeed>
  <TrendingNow />
  <HiddenGems />
  <PersonalizedForYou />
  <ExperienceGuides />
</DiscoveryFeed>
```

---

## 📋 IMPLEMENTATION ROADMAP

### Phase 2A (Week 3-4)
- [ ] Hotel discovery system
- [ ] Restaurant search
- [ ] Attraction directory
- [ ] Review aggregation

### Phase 2B (Week 5)
- [ ] Location-based features
- [ ] Advanced filtering
- [ ] User preferences
- [ ] Save/Wishlist feature

### Phase 3 (Week 6+)
- [ ] Recommendation engine
- [ ] AI personalization
- [ ] Trending detection
- [ ] Hidden gems algorithm

---

## 🔌 THIRD-PARTY INTEGRATIONS

```python
# Data Sources

# Hotels
- Booking.com API
- Google Hotels
- Expedia API

# Restaurants
- Google Places API
- Michelin Guide API
- TripAdvisor API
- OpenTable API

# Attractions
- Google Places API
- WikiData API
- ToursByLocals API

# Reviews
- Google Reviews
- TripAdvisor Reviews
- Booking.com Reviews

# Maps & Location
- Google Maps API
- Mapbox
- OpenStreetMap
```

---

## ✅ NEXT STEPS

1. **Design Database Schema** - All models ready above
2. **Create API Endpoints** - Endpoints specified above
3. **Implement Search Logic** - Code examples provided
4. **Build Frontend Components** - Component structure outlined
5. **Add Third-party Integrations** - Integration points identified
6. **Implement Recommendations** - ML logic ready to implement

