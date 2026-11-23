# Advanced Features - API Specification

**Version:** 1.0  
**Status:** Ready for Implementation  

---

## 🏨 HOTEL SEARCH & DISCOVERY API

### 1. Search Hotels

**Endpoint:** `GET /api/v2/hotels/search`

**Query Parameters:**
```json
{
  "destination": "Paris, France",
  "check_in": "2024-06-01",
  "check_out": "2024-06-07",
  "guests": 2,
  "rooms": 1,
  
  "min_price": 50,
  "max_price": 300,
  "currency": "USD",
  
  "min_rating": 4.0,
  "amenities": ["WiFi", "Pool", "Restaurant", "Gym"],
  "hotel_type": ["Boutique", "Resort"],
  
  "sort_by": "best_value",  // best_value, price_asc, price_desc, rating, newest
  "limit": 20,
  "offset": 0
}
```

**Response:**
```json
{
  "total": 245,
  "page": 1,
  "hotels": [
    {
      "id": "uuid-hotel-1",
      "name": "Le Marais Boutique Hotel",
      "destination": "Paris, France",
      "address": "123 Rue de Rivoli, Paris",
      "location": {
        "latitude": 48.8566,
        "longitude": 2.3522
      },
      "pricing": {
        "per_night": 150,
        "min_stay_nights": 2,
        "total_stay_price": 900,
        "currency": "USD",
        "taxes_and_fees": 100,
        "final_price": 1000
      },
      "rating": {
        "average": 4.7,
        "count": 524,
        "breakdown": {
          "5_stars": 380,
          "4_stars": 120,
          "3_stars": 20,
          "2_stars": 3,
          "1_star": 1
        }
      },
      "hotel_type": "Boutique",
      "star_rating": 4,
      "amenities": ["WiFi", "Pool", "Gym", "Restaurant", "Spa"],
      "image_url": "https://...jpg",
      "images_count": 45,
      "best_for": ["Couples", "Art Lovers", "Luxury"],
      "distance_from_center_km": 0.5,
      "verified": true,
      "booking_url": "https://booking.com/...",
      "quick_review": {
        "top_comment": "Amazing location and staff!",
        "recommended_by_percent": 98
      }
    }
  ]
}
```

### 2. Get Hotel Details

**Endpoint:** `GET /api/v2/hotels/{hotel_id}`

**Response:**
```json
{
  "id": "uuid-hotel-1",
  "name": "Le Marais Boutique Hotel",
  "description": "Charming 4-star boutique hotel...",
  "location": {
    "address": "123 Rue de Rivoli, Paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "nearby_landmarks": [
      {
        "name": "Louvre Museum",
        "distance_km": 1.2,
        "travel_time_minutes": 15
      }
    ]
  },
  "images": [
    {
      "type": "main",
      "url": "https://...",
      "caption": "Hotel Exterior"
    }
  ],
  "pricing": {
    "min_price": 120,
    "max_price": 250,
    "average_price": 150,
    "currency": "USD",
    "price_history": [...],
    "special_offers": [
      {
        "name": "Early Bird",
        "discount_percent": 15,
        "valid_until": "2024-05-15"
      }
    ]
  },
  "rooms": [
    {
      "id": "room-101",
      "type": "Deluxe Double",
      "price_per_night": 150,
      "capacity": 2,
      "amenities": ["AC", "Minibar", "Smart TV"],
      "size_sqft": 250
    }
  ],
  "amenities": {
    "facilities": ["Pool", "Gym", "Spa", "Restaurant"],
    "services": ["Room Service", "Concierge", "Laundry"],
    "wellness": ["Sauna", "Steam Room", "Yoga"]
  },
  "rating": {
    "overall": 4.7,
    "cleanliness": 4.9,
    "comfort": 4.6,
    "location": 4.8,
    "value_for_money": 4.5,
    "staff_service": 4.8
  },
  "reviews": [
    {
      "id": "review-1",
      "author": "John Doe",
      "rating": 5,
      "title": "Perfect Parisian Experience",
      "comment": "Amazing hotel, great location...",
      "visit_date": "2024-05-10",
      "verified_booking": true,
      "helpful_count": 245,
      "photos": [...]
    }
  ],
  "contact": {
    "phone": "+33 1 23 45 67 89",
    "email": "info@lemaraishotel.com",
    "website": "https://lemaraishotel.com"
  },
  "booking": {
    "url": "https://booking.com/...",
    "availability": "Available"
  }
}
```

### 3. Filter Hotel Amenities

**Endpoint:** `GET /api/v2/hotels/amenities`

**Response:**
```json
{
  "facilities": [
    "Pool",
    "Gym",
    "Spa",
    "Sauna",
    "Restaurant",
    "Bar",
    "Lounge"
  ],
  "services": [
    "Room Service",
    "Concierge",
    "Laundry",
    "Dry Cleaning",
    "Car Rental"
  ],
  "connectivity": [
    "WiFi",
    "Mobile Coverage"
  ],
  "accessibility": [
    "Wheelchair Access",
    "Disabled Parking",
    "Accessible Bathrooms"
  ]
}
```

---

## 🍽️ RESTAURANT & FOOD DISCOVERY API

### 1. Search Restaurants

**Endpoint:** `GET /api/v2/restaurants/search`

**Query Parameters:**
```json
{
  "destination": "Paris, France",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "radius_km": 2,
  
  "cuisines": ["Italian", "French"],
  "price_level": [1, 2, 3],  // 1=Budget, 2=Moderate, 3=Expensive, 4=Very Expensive
  "min_rating": 4.0,
  
  "dietary": ["Vegan", "Vegetarian"],
  "michelin_stars": 1,
  "has_reservation": true,
  
  "sort_by": "rating",  // rating, price_asc, price_desc, nearby, trending
  "limit": 20
}
```

**Response:**
```json
{
  "total": 1245,
  "restaurants": [
    {
      "id": "uuid-rest-1",
      "name": "L'Absinthe Restaurant",
      "cuisine": "French",
      "sub_cuisine": "Fine Dining",
      "location": {
        "address": "456 Boulevard Saint-Germain",
        "latitude": 48.8530,
        "longitude": 2.3410,
        "distance_km": 0.8,
        "neighborhood": "Latin Quarter"
      },
      "pricing": {
        "price_level": 3,
        "average_cost": 65,
        "currency": "USD",
        "price_range": "$$$$"
      },
      "rating": {
        "overall": 4.6,
        "food_quality": 4.8,
        "service": 4.5,
        "atmosphere": 4.7,
        "total_reviews": 382
      },
      "specialties": [
        "Duck Confit",
        "Foie Gras",
        "Coq au Vin"
      ],
      "michelin_stars": 1,
      "dietary_options": ["Vegetarian", "Gluten-free"],
      "image_url": "https://...",
      "operating_hours": {
        "tuesday": "12:00-14:00, 18:00-23:00",
        "wednesday": "12:00-14:00, 18:00-23:00",
        "sunday_closed": true
      },
      "reservation_required": true,
      "booking_url": "https://opentable.com/...",
      "amenities": ["WiFi", "Private Rooms", "Outdoor Seating"]
    }
  ]
}
```

### 2. Get Restaurant Details with Menu

**Endpoint:** `GET /api/v2/restaurants/{restaurant_id}`

**Response:**
```json
{
  "id": "uuid-rest-1",
  "name": "L'Absinthe Restaurant",
  "description": "Michelin-starred French bistro...",
  "images": [
    {
      "type": "exterior",
      "url": "https://..."
    }
  ],
  "menu": {
    "appetizers": [
      {
        "name": "Foie Gras Terrine",
        "description": "Classic French preparation",
        "price": 18,
        "is_signature": true
      }
    ],
    "mains": [
      {
        "name": "Duck Confit",
        "description": "Slow-cooked with garlic and herbs",
        "price": 32,
        "is_signature": true,
        "is_trending": true
      }
    ],
    "desserts": [...]
  },
  "signature_dishes": [
    {
      "name": "Duck Confit",
      "description": "...",
      "price": 32,
      "popularity_score": 98
    }
  ],
  "best_time_to_visit": {
    "least_crowded": "Monday afternoon",
    "most_crowded": "Saturday evening",
    "peak_hours": ["12:30-13:30", "19:30-20:30"]
  },
  "dietary_accommodations": {
    "vegan": true,
    "vegetarian": true,
    "gluten_free": true,
    "notes": "Chef will prepare custom dishes upon request"
  },
  "contact": {
    "phone": "+33 1 43 25 50 45",
    "email": "info@labsinthe.fr",
    "website": "https://labsinthe.fr"
  },
  "reviews": [
    {
      "id": "review-1",
      "author": "Sarah Martin",
      "rating": 5,
      "food_quality": 5,
      "service": 5,
      "atmosphere": 5,
      "comment": "Exceptional meal, attentive staff...",
      "dishes_tried": ["Duck Confit", "Foie Gras Terrine"],
      "would_recommend": true,
      "visit_date": "2024-05-20"
    }
  ]
}
```

### 3. Get Food Guide for Destination

**Endpoint:** `GET /api/v2/destinations/{destination_id}/food-guide`

**Response:**
```json
{
  "destination": "Paris, France",
  "local_specialties": [
    {
      "name": "Coq au Vin",
      "description": "Chicken braised in wine",
      "where_to_try": [
        {
          "restaurant": "L'Absinthe",
          "price": 32
        }
      ]
    }
  ],
  "best_restaurants_by_category": {
    "fine_dining": [...],
    "casual": [...],
    "street_food": [...]
  },
  "michelin_starred": [
    {
      "name": "Restaurant Name",
      "stars": 2,
      "rating": 4.9
    }
  ],
  "trending_now": [
    {
      "name": "Modern French Fusion",
      "rating": 4.7,
      "trending_score": 95
    }
  ],
  "budget_guide": {
    "cheap_eats": [...],
    "moderate": [...],
    "expensive": [...]
  }
}
```

---

## 🎯 ATTRACTIONS & PLACES API

### 1. Search Attractions

**Endpoint:** `GET /api/v2/attractions/search`

**Query Parameters:**
```json
{
  "destination": "Paris, France",
  "categories": ["Museum", "Monument", "Park"],
  "min_rating": 4.0,
  "free_entry": false,
  "wheelchair_accessible": true,
  "sort_by": "rating",  // rating, popular, trending, new
  "limit": 20
}
```

**Response:**
```json
{
  "total": 324,
  "attractions": [
    {
      "id": "uuid-attr-1",
      "name": "Louvre Museum",
      "category": "Museum",
      "sub_category": "Art Museum",
      "location": {
        "address": "Rue de Rivoli, Paris",
        "latitude": 48.8606,
        "longitude": 2.3352
      },
      "description": "World's largest art museum...",
      "rating": {
        "overall": 4.6,
        "total_reviews": 15432
      },
      "visiting_info": {
        "entry_fee": 17,
        "currency": "EUR",
        "free_entry": false,
        "opening_hours": {
          "monday": "Closed",
          "tuesday": "09:00-21:45",
          "wednesday": "09:00-21:45"
        },
        "avg_visit_duration_minutes": 180
      },
      "practical_info": {
        "wheelchair_accessible": true,
        "has_restrooms": true,
        "has_cafeteria": true,
        "closest_parking_distance_meters": 200
      },
      "highlights": [
        "Mona Lisa",
        "Winged Victory",
        "Venus de Milo"
      ],
      "best_time_to_visit": "Early morning or late evening",
      "official_website": "https://louvre.fr",
      "image_url": "https://..."
    }
  ]
}
```

### 2. Get Attraction Details

**Endpoint:** `GET /api/v2/attractions/{attraction_id}`

**Response:**
```json
{
  "id": "uuid-attr-1",
  "name": "Louvre Museum",
  "description": "The world's largest and most visited art museum...",
  "images": [
    {
      "type": "exterior",
      "url": "https://...",
      "caption": "Iconic glass pyramid"
    }
  ],
  "visiting_info": {
    "entry_fee": 17,
    "hours": {
      "monday": "Closed",
      "tuesday_to_sunday": "09:00-21:45"
    },
    "last_admission": "21:00",
    "avg_visit_duration": "3 hours"
  },
  "collections": [
    "Egyptian Antiquities",
    "Greek & Roman Sculptures",
    "Paintings",
    "Decorative Arts"
  ],
  "must_see": [
    {
      "name": "Mona Lisa",
      "location": "Room 6",
      "wait_time_minutes": 45
    }
  ],
  "tours_available": [
    {
      "name": "Guided Tour",
      "duration_hours": 1.5,
      "price": 25,
      "languages": ["English", "French", "Spanish"]
    }
  ],
  "facilities": {
    "restrooms": true,
    "cafeteria": true,
    "wifi": true,
    "cloakroom": true,
    "wheelchair_accessible": true,
    "parking_nearby": true
  },
  "crowd_analysis": {
    "least_crowded_day": "Tuesday",
    "least_crowded_hours": "09:00-11:00",
    "peak_hours": ["14:00-16:00"],
    "avg_wait_time_minutes": 30
  },
  "reviews": [
    {
      "author": "Alice Johnson",
      "rating": 5,
      "comment": "Iconic museum, must-visit...",
      "visit_date": "2024-05-15",
      "crowdedness": 4,  // 1=Empty, 5=Very Crowded
      "would_recommend": true
    }
  ],
  "tips_from_visitors": [
    "Get tickets online to avoid queues",
    "Come early morning for better experience",
    "At least 3 hours needed for main collections"
  ]
}
```

### 3. Get Destination Highlights

**Endpoint:** `GET /api/v2/destinations/{destination_id}/highlights`

**Response:**
```json
{
  "destination": "Paris, France",
  "must_see": [
    {
      "rank": 1,
      "name": "Eiffel Tower",
      "rating": 4.7,
      "why_visit": "Iconic landmark with best city views"
    }
  ],
  "hidden_gems": [
    {
      "name": "Sainte-Chapelle",
      "rating": 4.8,
      "why_visit": "Stunning Gothic architecture, less crowded"
    }
  ],
  "best_for_photos": [...],
  "quick_visits": [...],
  "full_day_experiences": [...]
}
```

---

## 🎁 RECOMMENDATIONS API

### 1. Get Personalized Recommendations

**Endpoint:** `GET /api/v2/recommendations/personalized`

**Query Parameters:**
```json
{
  "destination": "Paris, France",
  "trip_duration_days": 7,
  "budget": 3000,
  "interests": ["Art", "Food", "History"],
  "travel_style": "Cultural",
  "group_size": 2
}
```

**Response:**
```json
{
  "personalized_score": 85,
  "recommendations": {
    "hotels": [
      {
        "id": "uuid-hotel-1",
        "name": "Le Marais Boutique",
        "match_score": 92,
        "why_recommended": "Matches your love for art, near museums, within budget",
        "price": 150,
        "rating": 4.7
      }
    ],
    "restaurants": [
      {
        "id": "uuid-rest-1",
        "name": "L'Absinthe",
        "match_score": 88,
        "why_recommended": "Fine dining experience, local specialties",
        "price_level": 3,
        "rating": 4.6
      }
    ],
    "attractions": [
      {
        "id": "uuid-attr-1",
        "name": "Musée d'Orsay",
        "match_score": 95,
        "why_recommended": "Perfect for art lovers, Impressionist collection"
      }
    ],
    "experiences": [
      {
        "name": "Wine tasting tour",
        "match_score": 82,
        "why_recommended": "Local experience combining culture and food"
      }
    ]
  }
}
```

### 2. Get Trending Now

**Endpoint:** `GET /api/v2/destinations/{destination_id}/trending`

**Response:**
```json
{
  "destination": "Paris, France",
  "trending_hotels": [
    {
      "name": "Hotel Name",
      "trending_score": 95,
      "why_trending": "95% of visitors mention excellent service"
    }
  ],
  "trending_restaurants": [...],
  "trending_attractions": [...],
  "trending_experiences": [...]
}
```

### 3. Get Hidden Gems

**Endpoint:** `GET /api/v2/destinations/{destination_id}/hidden-gems`

**Response:**
```json
{
  "destination": "Paris, France",
  "hidden_gems": [
    {
      "name": "Local Bistro Name",
      "type": "restaurant",
      "rating": 4.8,
      "why_gem": "Excellent food, authentic experience, less touristy",
      "visitor_count": 245,
      "discovered_by_percent": 12
    }
  ]
}
```

---

## 📊 SAVED & WISHLIST API

### 1. Save/Bookmark Item

**Endpoint:** `POST /api/v2/users/me/saved-items`

**Request:**
```json
{
  "item_id": "uuid-hotel-1",
  "item_type": "hotel",  // hotel, restaurant, attraction
  "collection_id": "uuid-collection-1"  // optional, for grouping
}
```

**Response:**
```json
{
  "success": true,
  "saved_item": {
    "id": "uuid-saved-1",
    "item": {...},
    "saved_at": "2024-05-20T10:30:00Z"
  }
}
```

### 2. Get User's Saved Items

**Endpoint:** `GET /api/v2/users/me/saved-items`

**Query Parameters:**
```json
{
  "item_type": "hotel",  // optional filter
  "collection_id": "uuid-collection-1",  // optional filter
  "limit": 20,
  "offset": 0
}
```

---

## Summary of Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v2/hotels/search` | Search hotels with filters |
| GET | `/api/v2/hotels/{id}` | Get hotel details |
| GET | `/api/v2/restaurants/search` | Search restaurants |
| GET | `/api/v2/restaurants/{id}` | Get restaurant details with menu |
| GET | `/api/v2/attractions/search` | Search attractions |
| GET | `/api/v2/attractions/{id}` | Get attraction details |
| GET | `/api/v2/destinations/{id}/food-guide` | Get food guide |
| GET | `/api/v2/destinations/{id}/highlights` | Get top attractions |
| GET | `/api/v2/recommendations/personalized` | Personalized recommendations |
| GET | `/api/v2/destinations/{id}/trending` | Trending places |
| GET | `/api/v2/destinations/{id}/hidden-gems` | Hidden gems |
| POST | `/api/v2/users/me/saved-items` | Save item to wishlist |
| GET | `/api/v2/users/me/saved-items` | Get saved items |

