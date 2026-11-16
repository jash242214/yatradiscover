"""Pydantic schemas for attraction discovery endpoints"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class VisitorTipResponse(BaseModel):
    """Response model for visitor tip"""
    id: str = Field(..., description="Tip ID")
    title: str = Field(..., description="Tip title")
    content: str = Field(..., description="Tip content")
    tip_type: str = Field(..., description="timing, money, planning, experience")
    is_official: bool = False
    author_name: Optional[str] = None
    helpful_count: int = 0
    rating: Optional[Decimal] = None

    class Config:
        from_attributes = True


class AttractionReviewResponse(BaseModel):
    """Response model for attraction review"""
    id: str = Field(..., description="Review ID")
    title: Optional[str] = None
    content: str = Field(..., description="Review content")
    rating: Decimal = Field(..., description="Rating 0.00-10.00 or 0-5", ge=0, le=10)
    reviewer_name: str
    source: str = Field(..., description="google, tripadvisor, etc.")
    review_date: Optional[datetime] = None
    aspects: Optional[Dict[str, float]] = None
    helpful_count: int = 0
    verified_visit: bool = False
    visit_type: Optional[str] = Field(None, description="solo, couple, family, group")
    visit_season: Optional[str] = None

    class Config:
        from_attributes = True


class AttractionPhotoResponse(BaseModel):
    """Response model for attraction photo"""
    id: str = Field(..., description="Photo ID")
    url: str = Field(..., description="Photo URL")
    photo_type: str = Field(..., description="overview, interior, detail, crowd")
    caption: Optional[str] = None
    source: str = Field(..., description="google, tripadvisor, etc.")
    helpful_count: int = 0

    class Config:
        from_attributes = True


class AttractionDetailResponse(BaseModel):
    """Detailed attraction response"""
    id: str = Field(..., description="Attraction ID")
    name: str = Field(..., description="Attraction name")
    description: Optional[str] = None
    address: str
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    category: str = Field(..., description="museum, park, monument, etc.")
    subcategories: Optional[List[str]] = None
    attraction_type: str = Field(..., description="indoor, outdoor, virtual")
    has_entry_fee: bool = True
    entry_fee: Optional[Decimal] = None
    currency: str = "USD"
    ticket_url: Optional[str] = None
    overall_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    review_count: int = 0
    popularity_rank: Optional[int] = None
    typical_visit_duration_minutes: Optional[int] = None
    annual_visitor_count: Optional[int] = None
    crowd_level_current: Optional[str] = Field(None, description="empty, busy, very busy")
    opening_hours: Optional[Dict[str, str]] = None
    closed_on: Optional[List[str]] = None
    is_seasonal: bool = False
    seasonal_info: Optional[str] = None
    wheelchair_accessible: Optional[bool] = None
    parking_available: Optional[bool] = None
    public_transport_accessible: bool = True
    has_guide_service: bool = False
    has_gift_shop: bool = False
    has_restaurant: bool = False
    photography_allowed: bool = True
    photography_restrictions: Optional[str] = None
    reviews: List[AttractionReviewResponse] = []
    tips: List[VisitorTipResponse] = []
    photos: List[AttractionPhotoResponse] = []
    is_featured: bool = False
    is_trending: bool = False

    class Config:
        from_attributes = True


class AttractionSearchResponse(BaseModel):
    """Brief attraction response for search results"""
    id: str = Field(..., description="Attraction ID")
    name: str = Field(..., description="Attraction name")
    city: str
    country: str
    category: str
    subcategories: Optional[List[str]] = None
    attraction_type: str
    has_entry_fee: bool = True
    entry_fee: Optional[Decimal] = None
    currency: str = "USD"
    overall_rating: Optional[Decimal] = None
    review_count: int = 0
    distance_km: Optional[float] = Field(None, description="Distance from search location")
    typical_visit_duration_minutes: Optional[int] = None
    is_featured: bool = False
    is_trending: bool = False

    class Config:
        from_attributes = True


class AttractionSearchRequest(BaseModel):
    """Attraction search request parameters"""
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = Field(None, description="Latitude for location search")
    longitude: Optional[float] = Field(None, description="Longitude for location search")
    distance_km: int = Field(default=10, ge=1, le=100)
    categories: Optional[List[str]] = None
    subcategories: Optional[List[str]] = None
    attraction_type: Optional[str] = Field(None, description="indoor, outdoor, virtual")
    min_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    max_entry_fee: Optional[Decimal] = Field(None, ge=0)
    max_visit_duration_hours: Optional[int] = None
    has_parking: Optional[bool] = None
    wheelchair_accessible: Optional[bool] = None
    open_now: Optional[bool] = None
    sort_by: str = Field(default="rating", description="rating, distance, popularity, trending")
    sort_order: str = Field(default="desc", description="asc or desc")
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    class Config:
        extra = "ignore"


class AttractionFilterRequest(BaseModel):
    """Attraction filtering parameters"""
    categories: Optional[List[str]] = None
    subcategories: Optional[List[str]] = None
    attraction_type: Optional[str] = None
    min_rating: Optional[Decimal] = Field(None, ge=0, le=10)
    max_entry_fee: Optional[Decimal] = Field(None, ge=0)
    has_parking: Optional[bool] = None
    wheelchair_accessible: Optional[bool] = None
    has_guide_service: Optional[bool] = None
    is_seasonal: Optional[bool] = None

    class Config:
        extra = "ignore"


class UserAttractionPreferenceResponse(BaseModel):
    """User attraction preferences"""
    id: str
    user_id: str
    preferred_categories: Optional[List[str]] = None
    disliked_categories: Optional[List[str]] = None
    preferred_activity_type: Optional[str] = None
    max_visit_duration_hours: Optional[int] = None
    prefer_crowded: Optional[bool] = None
    wheelchair_required: bool = False
    parking_required: bool = False
    max_ticket_price: Optional[Decimal] = None
    currency: str = "USD"
    max_distance_km: int = 10

    class Config:
        from_attributes = True


class UserAttractionPreferenceRequest(BaseModel):
    """Request to update user attraction preferences"""
    preferred_categories: Optional[List[str]] = None
    disliked_categories: Optional[List[str]] = None
    preferred_activity_type: Optional[str] = None
    max_visit_duration_hours: Optional[int] = Field(None, ge=1, le=24)
    prefer_crowded: Optional[bool] = None
    wheelchair_required: Optional[bool] = None
    parking_required: Optional[bool] = None
    max_ticket_price: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = "USD"
    max_distance_km: Optional[int] = Field(None, ge=1, le=100)

    class Config:
        extra = "ignore"
