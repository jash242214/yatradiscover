"""Pydantic schemas for hotel discovery endpoints"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class HotelAmenityResponse(BaseModel):
    """Response model for hotel amenity"""
    id: str = Field(..., description="Amenity ID")
    category: str = Field(..., description="Category: room, facility, service")
    name: str = Field(..., description="Amenity name")
    description: Optional[str] = None
    icon: Optional[str] = None
    available: bool = True
    free: bool = False
    details: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class HotelReviewResponse(BaseModel):
    """Response model for hotel review"""
    id: str = Field(..., description="Review ID")
    title: Optional[str] = None
    content: str = Field(..., description="Review content")
    rating: Decimal = Field(..., description="Rating 0.00-10.00 or 0-5", ge=0, le=10)
    reviewer_name: str = Field(..., description="Reviewer name")
    source: str = Field(..., description="Source: booking, google, tripadvisor")
    review_date: Optional[datetime] = None
    aspects: Optional[Dict[str, float]] = None
    helpful_count: int = 0
    verified_purchase: bool = False

    class Config:
        from_attributes = True


class HotelPriceResponse(BaseModel):
    """Response model for hotel price"""
    id: str = Field(..., description="Price record ID")
    nightly_rate: Decimal = Field(..., description="Nightly rate", ge=0)
    currency: str = Field(default="USD", max_length=3)
    check_in_date: datetime
    check_out_date: datetime
    room_type: Optional[str] = None
    occupancy: Optional[str] = None
    source: str = Field(..., description="booking, google, etc.")

    class Config:
        from_attributes = True


class HotelDetailResponse(BaseModel):
    """Detailed hotel response with reviews and prices"""
    id: str = Field(..., description="Hotel ID")
    name: str = Field(..., description="Hotel name")
    description: Optional[str] = None
    address: str
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    category: str = Field(..., description="luxury, midrange, budget, economy")
    star_rating: Optional[Decimal] = Field(None, ge=1, le=5)
    chain_name: Optional[str] = None
    lowest_price: Optional[Decimal] = None
    avg_price: Optional[Decimal] = None
    currency: str = "USD"
    overall_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    review_count: int = 0
    check_in_time: str = "15:00"
    check_out_time: str = "11:00"
    amenities: Optional[List[str]] = None
    room_types: Optional[List[Dict[str, Any]]] = None
    booking_url: Optional[str] = None
    reviews: List[HotelReviewResponse] = []
    amenity_list: List[HotelAmenityResponse] = Field(default_factory=list)
    recent_prices: List[HotelPriceResponse] = Field(default_factory=list)
    is_featured: bool = False

    class Config:
        from_attributes = True


class HotelSearchResponse(BaseModel):
    """Brief hotel response for search results"""
    id: str = Field(..., description="Hotel ID")
    name: str = Field(..., description="Hotel name")
    city: str
    country: str
    category: str
    star_rating: Optional[Decimal] = None
    overall_rating: Optional[Decimal] = None
    review_count: int = 0
    lowest_price: Optional[Decimal] = None
    avg_price: Optional[Decimal] = None
    currency: str = "USD"
    distance_km: Optional[float] = Field(None, description="Distance from search location")
    amenities: Optional[List[str]] = None
    is_featured: bool = False

    class Config:
        from_attributes = True


class HotelSearchRequest(BaseModel):
    """Hotel search request parameters"""
    city: Optional[str] = Field(None, description="City to search in")
    country: Optional[str] = None
    latitude: Optional[float] = Field(None, description="Latitude for location search")
    longitude: Optional[float] = Field(None, description="Longitude for location search")
    distance_km: int = Field(default=5, ge=1, le=50, description="Search radius in km")
    check_in_date: Optional[datetime] = None
    check_out_date: Optional[datetime] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    min_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    min_stars: Optional[int] = Field(None, ge=1, le=5)
    category: Optional[str] = Field(None, description="luxury, midrange, budget, economy")
    amenities: Optional[List[str]] = Field(None, description="Filter by amenities")
    chain_name: Optional[str] = None
    sort_by: str = Field(default="rating", description="rating, price, distance, review_count")
    sort_order: str = Field(default="desc", description="asc or desc")
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    class Config:
        extra = "ignore"


class HotelFilterRequest(BaseModel):
    """Hotel filtering parameters"""
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)
    min_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    min_stars: Optional[int] = Field(None, ge=1, le=5)
    max_stars: Optional[int] = Field(None, ge=1, le=5)
    categories: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    preferred_chains: Optional[List[str]] = None

    class Config:
        extra = "ignore"


class UserHotelPreferenceResponse(BaseModel):
    """User hotel preferences"""
    id: str
    user_id: str
    min_budget: Optional[Decimal] = None
    max_budget: Optional[Decimal] = None
    currency: str = "USD"
    preferred_categories: Optional[List[str]] = None
    min_star_rating: Optional[Decimal] = None
    preferred_amenities: Optional[List[str]] = None
    preferred_chains: Optional[List[str]] = None
    max_distance_km: int = 5

    class Config:
        from_attributes = True


class UserHotelPreferenceRequest(BaseModel):
    """Request to update user hotel preferences"""
    min_budget: Optional[Decimal] = Field(None, ge=0)
    max_budget: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = "USD"
    preferred_categories: Optional[List[str]] = None
    min_star_rating: Optional[Decimal] = Field(None, ge=1, le=5)
    preferred_amenities: Optional[List[str]] = None
    preferred_chains: Optional[List[str]] = None
    max_distance_km: Optional[int] = Field(None, ge=1, le=100)

    class Config:
        extra = "ignore"
