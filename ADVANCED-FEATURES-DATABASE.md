# Advanced Features - Database Schema

**Version:** 1.0  
**Database:** PostgreSQL with PostGIS extension  

---

## Extension Setup

```sql
-- Enable PostGIS for location-based queries
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
```

---

## 🏨 HOTEL TABLES

```sql
-- Main Hotels Table
CREATE TABLE IF NOT EXISTS hotels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    address TEXT,
    
    -- Geolocation
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    location GEOMETRY(POINT, 4326),
    
    -- Pricing
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    average_price DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    price_updated_at TIMESTAMP,
    
    -- Classification
    hotel_type VARCHAR(50), -- LUXURY, MIDRANGE, BUDGET, BOUTIQUE
    star_rating INT CHECK (star_rating >= 1 AND star_rating <= 5),
    description TEXT,
    
    -- Ratings
    average_rating DECIMAL(3, 2) CHECK (average_rating >= 0 AND average_rating <= 5),
    total_reviews INT DEFAULT 0,
    rating_breakdown JSONB, -- {"5": 100, "4": 50, "3": 20, "2": 5, "1": 2}
    
    -- Contact & Booking
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(500),
    booking_url VARCHAR(500),
    
    -- Content
    main_image_url VARCHAR(500),
    images_count INT DEFAULT 0,
    
    -- Metadata
    source VARCHAR(50), -- BOOKING, TRIPADVISOR, GOOGLE, MANUAL
    source_id VARCHAR(100),
    verified BOOLEAN DEFAULT FALSE,
    featured BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT fk_destination FOREIGN KEY (destination) REFERENCES destinations(name)
);

CREATE INDEX idx_hotels_destination ON hotels(destination);
CREATE INDEX idx_hotels_city ON hotels(city);
CREATE INDEX idx_hotels_rating ON hotels(average_rating DESC);
CREATE INDEX idx_hotels_price ON hotels(average_price);
CREATE INDEX idx_hotels_location ON hotels USING GIST(location);

-- Hotel Amenities
CREATE TABLE IF NOT EXISTS hotel_amenities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL,
    amenity_name VARCHAR(100),
    category VARCHAR(50), -- FACILITIES, SERVICES, WELLNESS, CONNECTIVITY
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
    UNIQUE(hotel_id, amenity_name)
);

CREATE INDEX idx_hotel_amenities_hotel ON hotel_amenities(hotel_id);

-- Hotel Rooms
CREATE TABLE IF NOT EXISTS hotel_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL,
    room_type VARCHAR(100), -- DELUXE, SUITE, STANDARD, etc.
    price_per_night DECIMAL(10, 2),
    capacity INT,
    amenities JSONB, -- ["AC", "Minibar", "TV", "WiFi"]
    size_sqft INT,
    max_occupancy INT,
    description TEXT,
    available_rooms INT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
);

-- Hotel Reviews
CREATE TABLE IF NOT EXISTS hotel_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL,
    user_id UUID,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    comment TEXT,
    verified_booking BOOLEAN DEFAULT FALSE,
    helpful_count INT DEFAULT 0,
    unhelpful_count INT DEFAULT 0,
    cleanliness_rating INT,
    comfort_rating INT,
    location_rating INT,
    service_rating INT,
    value_rating INT,
    source VARCHAR(50), -- BOOKING, TRIPADVISOR, GOOGLE, APP
    visit_month_year VARCHAR(7), -- "2024-05"
    review_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_hotel_reviews_hotel ON hotel_reviews(hotel_id);
CREATE INDEX idx_hotel_reviews_rating ON hotel_reviews(rating);
CREATE INDEX idx_hotel_reviews_created ON hotel_reviews(created_at DESC);

-- Hotel Images
CREATE TABLE IF NOT EXISTS hotel_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL,
    image_url VARCHAR(500),
    image_type VARCHAR(50), -- EXTERIOR, ROOM, LOBBY, POOL, DINING, etc.
    caption VARCHAR(255),
    display_order INT,
    uploader_user_id UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE,
    FOREIGN KEY (uploader_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_hotel_images_hotel ON hotel_images(hotel_id);

-- Hotel Pricing History
CREATE TABLE IF NOT EXISTS hotel_price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hotel_id UUID NOT NULL,
    price DECIMAL(10, 2),
    currency VARCHAR(3),
    check_in DATE,
    check_out DATE,
    record_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
);

CREATE INDEX idx_hotel_price_history_hotel ON hotel_price_history(hotel_id);
```

---

## 🍽️ RESTAURANT TABLES

```sql
-- Main Restaurants Table
CREATE TABLE IF NOT EXISTS restaurants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    
    -- Location
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    location GEOMETRY(POINT, 4326),
    
    -- Classification
    cuisine_type VARCHAR(100), -- Italian, Indian, Japanese, etc.
    sub_cuisine VARCHAR(100), -- Fine dining, Street food, Casual
    price_level INT CHECK (price_level >= 1 AND price_level <= 4),
    average_cost DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Ratings
    average_rating DECIMAL(3, 2),
    total_reviews INT DEFAULT 0,
    rating_breakdown JSONB,
    food_quality_avg DECIMAL(3, 2),
    service_avg DECIMAL(3, 2),
    atmosphere_avg DECIMAL(3, 2),
    
    -- Details
    description TEXT,
    specialties JSONB, -- ["Pasta", "Risotto"]
    dietary_options JSONB, -- ["Vegan", "Vegetarian", "Gluten-free"]
    seating_capacity INT,
    has_outdoor_seating BOOLEAN,
    has_private_rooms BOOLEAN,
    
    -- Service Info
    reservation_required BOOLEAN DEFAULT FALSE,
    reservation_url VARCHAR(500),
    phone VARCHAR(20),
    website VARCHAR(500),
    email VARCHAR(255),
    
    -- Amenities
    has_wifi BOOLEAN DEFAULT FALSE,
    has_parking BOOLEAN DEFAULT FALSE,
    has_bar BOOLEAN DEFAULT FALSE,
    accepts_credit_cards BOOLEAN DEFAULT TRUE,
    
    -- Recognition
    michelin_stars INT CHECK (michelin_stars >= 0 AND michelin_stars <= 3),
    is_trending BOOLEAN DEFAULT FALSE,
    popularity_score INT DEFAULT 0,
    
    -- Metadata
    source VARCHAR(50), -- GOOGLE, TRIPADVISOR, MICHELIN, MANUAL
    source_id VARCHAR(100),
    verified BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_restaurants_destination ON restaurants(destination);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine_type);
CREATE INDEX idx_restaurants_rating ON restaurants(average_rating DESC);
CREATE INDEX idx_restaurants_price ON restaurants(price_level);
CREATE INDEX idx_restaurants_location ON restaurants USING GIST(location);

-- Restaurant Dishes
CREATE TABLE IF NOT EXISTS restaurant_dishes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID NOT NULL,
    dish_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    currency VARCHAR(3),
    category VARCHAR(50), -- APPETIZER, MAIN, DESSERT, BEVERAGE
    is_signature BOOLEAN DEFAULT FALSE,
    is_trending BOOLEAN DEFAULT FALSE,
    popularity_score INT DEFAULT 0,
    ingredients JSONB,
    dietary_tags JSONB, -- ["Vegan", "Spicy", "Gluten-free"]
    allergens JSONB, -- ["Nuts", "Shellfish", "Dairy"]
    photo_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
);

CREATE INDEX idx_restaurant_dishes_restaurant ON restaurant_dishes(restaurant_id);
CREATE INDEX idx_restaurant_dishes_signature ON restaurant_dishes(is_signature) WHERE is_signature;

-- Restaurant Opening Hours
CREATE TABLE IF NOT EXISTS restaurant_opening_hours (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID NOT NULL,
    day_of_week INT CHECK (day_of_week >= 0 AND day_of_week <= 6), -- 0=Sunday
    opens_at TIME,
    closes_at TIME,
    closed BOOLEAN DEFAULT FALSE,
    special_hours_date DATE,
    special_hours_note VARCHAR(255),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    UNIQUE(restaurant_id, day_of_week)
);

-- Restaurant Reviews
CREATE TABLE IF NOT EXISTS restaurant_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID NOT NULL,
    user_id UUID,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    food_quality INT CHECK (food_quality >= 1 AND food_quality <= 5),
    service_quality INT CHECK (service_quality >= 1 AND service_quality <= 5),
    atmosphere INT CHECK (atmosphere >= 1 AND atmosphere <= 5),
    title VARCHAR(255),
    comment TEXT,
    would_recommend BOOLEAN,
    dishes_tried JSONB,
    visit_date DATE,
    helpful_count INT DEFAULT 0,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_restaurant_reviews_restaurant ON restaurant_reviews(restaurant_id);
CREATE INDEX idx_restaurant_reviews_rating ON restaurant_reviews(rating);

-- Restaurant Photos
CREATE TABLE IF NOT EXISTS restaurant_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID NOT NULL,
    photo_url VARCHAR(500),
    photo_type VARCHAR(50), -- EXTERIOR, INTERIOR, DISH, AMBIANCE
    uploader_user_id UUID,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    FOREIGN KEY (uploader_user_id) REFERENCES users(id) ON DELETE SET NULL
);
```

---

## 🎯 ATTRACTION TABLES

```sql
-- Main Attractions Table
CREATE TABLE IF NOT EXISTS attractions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    
    -- Location
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    location GEOMETRY(POINT, 4326),
    
    -- Classification
    category VARCHAR(100), -- Museum, Park, Monument, Church
    sub_category VARCHAR(100),
    historical_significance INT CHECK (historical_significance >= 1 AND historical_significance <= 5),
    popular_for JSONB, -- ["Photos", "History", "Architecture"]
    
    -- Details
    description TEXT,
    interesting_facts JSONB,
    
    -- Visiting Info
    entry_fee DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    free_entry BOOLEAN,
    avg_visit_duration_minutes INT,
    
    -- Ratings
    average_rating DECIMAL(3, 2),
    total_reviews INT DEFAULT 0,
    
    -- Facilities
    has_restrooms BOOLEAN DEFAULT FALSE,
    has_cafeteria BOOLEAN DEFAULT FALSE,
    has_wifi BOOLEAN DEFAULT FALSE,
    wheelchair_accessible BOOLEAN DEFAULT FALSE,
    has_parking BOOLEAN DEFAULT FALSE,
    guide_services BOOLEAN DEFAULT FALSE,
    
    -- Website & Booking
    official_website VARCHAR(500),
    booking_url VARCHAR(500),
    booking_required BOOLEAN DEFAULT FALSE,
    phone VARCHAR(20),
    
    -- Special Info
    best_time_to_visit VARCHAR(255),
    avg_crowd_level INT CHECK (avg_crowd_level >= 1 AND avg_crowd_level <= 5),
    is_trending BOOLEAN DEFAULT FALSE,
    popularity_score INT DEFAULT 0,
    
    -- Metadata
    source VARCHAR(50),
    verified BOOLEAN DEFAULT FALSE,
    featured BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_attractions_destination ON attractions(destination);
CREATE INDEX idx_attractions_category ON attractions(category);
CREATE INDEX idx_attractions_rating ON attractions(average_rating DESC);
CREATE INDEX idx_attractions_location ON attractions USING GIST(location);

-- Attraction Opening Hours
CREATE TABLE IF NOT EXISTS attraction_opening_hours (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attraction_id UUID NOT NULL,
    day_of_week INT,
    opens_at TIME,
    closes_at TIME,
    closed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE,
    UNIQUE(attraction_id, day_of_week)
);

-- Attraction Reviews
CREATE TABLE IF NOT EXISTS attraction_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attraction_id UUID NOT NULL,
    user_id UUID,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    visit_date DATE,
    crowdedness INT CHECK (crowdedness >= 1 AND crowdedness <= 5),
    worth_visit BOOLEAN,
    visited_all_sections BOOLEAN,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Attraction Photos
CREATE TABLE IF NOT EXISTS attraction_photos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attraction_id UUID NOT NULL,
    photo_url VARCHAR(500),
    photo_type VARCHAR(50), -- EXTERIOR, INTERIOR, DETAIL, VIEW
    uploader_user_id UUID,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE,
    FOREIGN KEY (uploader_user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Highlights/Must-See
CREATE TABLE IF NOT EXISTS attraction_highlights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attraction_id UUID NOT NULL,
    highlight_name VARCHAR(255),
    description TEXT,
    location_in_attraction VARCHAR(100),
    typical_wait_minutes INT,
    is_must_see BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
);
```

---

## 📍 DESTINATION & LOCATION TABLES

```sql
-- Destinations
CREATE TABLE IF NOT EXISTS destinations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100),
    region VARCHAR(100),
    description TEXT,
    climate VARCHAR(50),
    best_time_to_visit VARCHAR(100),
    currency VARCHAR(3),
    
    -- Location
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Info
    population INT,
    language VARCHAR(100),
    time_zone VARCHAR(50),
    official_website VARCHAR(500),
    
    -- Ratings
    average_rating DECIMAL(3, 2),
    total_reviews INT,
    
    -- Content
    main_image_url VARCHAR(500),
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_destinations_name ON destinations(name);
CREATE INDEX idx_destinations_country ON destinations(country);
CREATE INDEX idx_destinations_rating ON destinations(average_rating DESC);

-- Destination Guide (curated content)
CREATE TABLE IF NOT EXISTS destination_guides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    destination_id UUID NOT NULL,
    title VARCHAR(255),
    content TEXT,
    guide_type VARCHAR(50), -- OVERVIEW, ITINERARY, TIPS, LOCAL_INFO
    author_user_id UUID,
    helpful_count INT DEFAULT 0,
    views_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE,
    FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE SET NULL
);
```

---

## 💾 USER PREFERENCES & RECOMMENDATIONS

```sql
-- User Travel Preferences
CREATE TABLE IF NOT EXISTS user_travel_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    
    -- Travel Style
    preferred_travel_styles JSONB, -- ["Adventure", "Culture", "Luxury"]
    
    -- Budget
    budget_preference VARCHAR(50), -- Budget, Moderate, Luxury
    avg_daily_budget DECIMAL(10, 2),
    
    -- Interests
    interests JSONB, -- ["Art", "Food", "Nature"]
    
    -- Dietary
    dietary_restrictions JSONB,
    food_allergies JSONB,
    
    -- Hotel Preferences
    preferred_hotel_types JSONB,
    preferred_amenities JSONB,
    hotel_chain_affiliations VARCHAR(255),
    
    -- Accessibility
    mobility_requirements VARCHAR(255),
    accessibility_needs JSONB,
    
    -- Travel Companions
    typical_group_size INT,
    travel_companion_type VARCHAR(50), -- Solo, Couple, Family, Friends
    
    -- Pace
    trip_pace VARCHAR(50), -- Relaxed, Moderate, Fast-paced
    
    -- Notifications
    receive_recommendations BOOLEAN DEFAULT TRUE,
    
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id)
);

-- User Saved Items (Wishlist)
CREATE TABLE IF NOT EXISTS user_saved_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    saved_item_id UUID,
    saved_item_type VARCHAR(50), -- hotel, restaurant, attraction
    collection_id UUID,
    saved_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_saved_items_user ON user_saved_items(user_id);
CREATE INDEX idx_user_saved_items_type ON user_saved_items(saved_item_type);

-- User Saved Collections
CREATE TABLE IF NOT EXISTS user_saved_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name VARCHAR(255),
    description TEXT,
    destination VARCHAR(255),
    is_public BOOLEAN DEFAULT FALSE,
    items_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- User Recommendations Log
CREATE TABLE IF NOT EXISTS user_recommendation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    recommended_item_id UUID,
    recommended_item_type VARCHAR(50),
    recommendation_type VARCHAR(50), -- personalized, trending, hidden_gem
    score DECIMAL(5, 2),
    clicked BOOLEAN DEFAULT FALSE,
    saved BOOLEAN DEFAULT FALSE,
    booked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 🔍 SEARCH & DISCOVERY INDEXES

```sql
-- Full-text search indexes for hotels
CREATE INDEX idx_hotels_name_search ON hotels USING GIN(
    to_tsvector('english', name || ' ' || COALESCE(description, ''))
);

-- Full-text search for restaurants
CREATE INDEX idx_restaurants_name_search ON restaurants USING GIN(
    to_tsvector('english', name || ' ' || COALESCE(description, ''))
);

-- Full-text search for attractions
CREATE INDEX idx_attractions_name_search ON attractions USING GIN(
    to_tsvector('english', name || ' ' || COALESCE(description, ''))
);

-- Geospatial indexes for nearby searches
CREATE INDEX idx_hotels_nearby ON hotels USING GIST(location);
CREATE INDEX idx_restaurants_nearby ON restaurants USING GIST(location);
CREATE INDEX idx_attractions_nearby ON attractions USING GIST(location);

-- Performance indexes
CREATE INDEX idx_hotels_rating_count ON hotels(average_rating DESC, total_reviews DESC);
CREATE INDEX idx_restaurants_rating_count ON restaurants(average_rating DESC, total_reviews DESC);
CREATE INDEX idx_attractions_rating_count ON attractions(average_rating DESC, total_reviews DESC);
```

---

## 📊 Views for Common Queries

```sql
-- Best Value Hotels (Rating/Price Ratio)
CREATE VIEW best_value_hotels AS
SELECT 
    h.id,
    h.name,
    h.average_rating,
    h.average_price,
    (h.average_rating / NULLIF(h.average_price / 100, 0)) as value_score,
    h.destination
FROM hotels h
WHERE h.average_rating >= 4.0
ORDER BY value_score DESC;

-- Trending Restaurants
CREATE VIEW trending_restaurants AS
SELECT 
    r.id,
    r.name,
    r.cuisine_type,
    r.average_rating,
    r.popularity_score,
    COUNT(rr.id) as recent_reviews
FROM restaurants r
LEFT JOIN restaurant_reviews rr ON r.id = rr.restaurant_id 
    AND rr.created_at >= NOW() - INTERVAL '7 days'
GROUP BY r.id
ORDER BY r.popularity_score DESC, recent_reviews DESC;

-- Top-Rated Attractions
CREATE VIEW top_rated_attractions AS
SELECT 
    a.id,
    a.name,
    a.category,
    a.average_rating,
    a.total_reviews,
    a.destination
FROM attractions a
WHERE a.total_reviews >= 10
ORDER BY a.average_rating DESC, a.total_reviews DESC;
```

---

## 🔄 Migration Script

```sql
-- Run this to create all tables and indexes at once
BEGIN;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create all tables
-- [Insert all CREATE TABLE statements above]

-- Create all indexes
-- [Insert all CREATE INDEX statements above]

-- Create all views
-- [Insert all CREATE VIEW statements above]

COMMIT;
```

