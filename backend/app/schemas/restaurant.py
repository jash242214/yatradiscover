"""Pydantic schemas for restaurant discovery endpoints"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class SignatureDishResponse(BaseModel):
    """Response model for signature dish"""
    id: str = Field(..., description="Dish ID")
    name: str = Field(..., description="Dish name")
    description: Optional[str] = None
    cuisine: Optional[str] = None
    ingredients: Optional[List[str]] = None
    dietary_info: Optional[List[str]] = None
    price: Optional[Decimal] = None
    popularity_score: Optional[Decimal] = Field(None, ge=0, le=10)
    reviewer_mentions: int = 0
    photo_url: Optional[str] = None
    availability: Optional[str] = None
    is_seasonal: bool = False

    class Config:
        from_attributes = True


class RestaurantReviewResponse(BaseModel):
    """Response model for restaurant review"""
    id: str = Field(..., description="Review ID")
    title: Optional[str] = None
    content: str = Field(..., description="Review content")
    rating: Decimal = Field(..., description="Rating 0.00-10.00 or 0-5", ge=0, le=10)
    reviewer_name: str
    source: str = Field(..., description="google, tripadvisor, michelin, etc.")
    review_date: Optional[datetime] = None
    aspects: Optional[Dict[str, float]] = None
    helpful_count: int = 0
    verified_visit: bool = False

    class Config:
        from_attributes = True


class RestaurantPhotoResponse(BaseModel):
    """Response model for restaurant photo"""
    id: str = Field(..., description="Photo ID")
    url: str = Field(..., description="Photo URL")
    photo_type: str = Field(..., description="exterior, interior, food, ambiance")
    caption: Optional[str] = None
    source: str = Field(..., description="google, tripadvisor, etc.")
    helpful_count: int = 0

    class Config:
        from_attributes = True


class RestaurantDetailResponse(BaseModel):
    """Detailed restaurant response"""
    id: str = Field(..., description="Restaurant ID")
    name: str = Field(..., description="Restaurant name")
    description: Optional[str] = None
    address: str
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    primary_cuisine: str = Field(..., description="Italian, Chinese, etc.")
    cuisines: Optional[List[str]] = None
    price_level: str = Field(..., description="$, $$, $$$, $$$$")
    avg_cost_per_person: Optional[Decimal] = None
    currency: str = "USD"
    overall_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    review_count: int = 0
    michelin_stars: int = 0
    has_michelin_green: bool = False
    dining_style: Optional[str] = None
    menu_type: Optional[List[str]] = None
    atmosphere: Optional[List[str]] = None
    accepts_reservations: bool = True
    reservation_url: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    closed_on: Optional[List[str]] = None
    dietary_options: Optional[List[str]] = None
    parking_available: Optional[bool] = None
    wheelchair_accessible: Optional[bool] = None
    booking_url: Optional[str] = None
    reviews: List[RestaurantReviewResponse] = []
    signature_dishes: List[SignatureDishResponse] = []
    photos: List[RestaurantPhotoResponse] = []
    is_featured: bool = False
    is_trending: bool = False

    class Config:
        from_attributes = True


class RestaurantSearchResponse(BaseModel):
    """Brief restaurant response for search results"""
    id: str = Field(..., description="Restaurant ID")
    name: str = Field(..., description="Restaurant name")
    city: str
    country: str
    primary_cuisine: str
    cuisines: Optional[List[str]] = None
    price_level: str
    avg_cost_per_person: Optional[Decimal] = None
    currency: str = "USD"
    overall_rating: Optional[Decimal] = None
    review_count: int = 0
    michelin_stars: int = 0
    distance_km: Optional[float] = Field(None, description="Distance from search location")
    dining_style: Optional[str] = None
    is_featured: bool = False
    is_trending: bool = False

    class Config:
        from_attributes = True


class RestaurantSearchRequest(BaseModel):
    """Restaurant search request parameters"""
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = Field(None, description="Latitude for location search")
    longitude: Optional[float] = Field(None, description="Longitude for location search")
    distance_km: int = Field(default=5, ge=1, le=50)
    cuisines: Optional[List[str]] = None
    price_levels: Optional[List[str]] = Field(None, description="$, $$, $$$, $$$$")
    min_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    michelin_only: bool = False
    dietary_options: Optional[List[str]] = None
    dining_style: Optional[str] = None
    accepts_reservations: Optional[bool] = None
    sort_by: str = Field(default="rating", description="rating, distance, michelin_stars, trending")
    sort_order: str = Field(default="desc", description="asc or desc")
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    class Config:
        extra = "ignore"


class RestaurantFilterRequest(BaseModel):
    """Restaurant filtering parameters"""
    cuisines: Optional[List[str]] = None
    price_levels: Optional[List[str]] = None
    min_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    michelin_only: bool = False
    michelin_min_stars: Optional[int] = Field(None, ge=1, le=3)
    dietary_options: Optional[List[str]] = None
    dining_style: Optional[List[str]] = None

    class Config:
        extra = "ignore"


class UserRestaurantPreferenceResponse(BaseModel):
    """User restaurant preferences"""
    id: str
    user_id: str
    preferred_price_levels: Optional[List[str]] = None
    max_cost_per_person: Optional[Decimal] = None
    currency: str = "USD"
    preferred_cuisines: Optional[List[str]] = None
    disliked_cuisines: Optional[List[str]] = None
    dietary_options: Optional[List[str]] = None
    preferred_dining_style: Optional[List[str]] = None
    atmosphere_preferences: Optional[List[str]] = None
    prefer_michelin_restaurants: bool = False
    max_distance_km: int = 5

    class Config:
        from_attributes = True


class UserRestaurantPreferenceRequest(BaseModel):
    """Request to update user restaurant preferences"""
    preferred_price_levels: Optional[List[str]] = None
    max_cost_per_person: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = "USD"
    preferred_cuisines: Optional[List[str]] = None
    disliked_cuisines: Optional[List[str]] = None
    dietary_options: Optional[List[str]] = None
    preferred_dining_style: Optional[List[str]] = None
    atmosphere_preferences: Optional[List[str]] = None
    prefer_michelin_restaurants: Optional[bool] = None
    max_distance_km: Optional[int] = Field(None, ge=1, le=100)

    class Config:
        extra = "ignore"
