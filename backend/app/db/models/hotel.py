"""
Hotel database models for discovery features
"""
from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    Column, DateTime, String, Boolean, Index, ForeignKey,
    Numeric, Integer, Text, JSON, ARRAY, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base import Base


class Hotel(Base):
    """Hotel model for accommodation discovery"""

    __tablename__ = "hotels"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Basic info
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)

    # Address and location
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False, index=True)
    postal_code = Column(String(20), nullable=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    # Contact
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)

    # Classification
    category = Column(String(50), nullable=False, index=True)  # luxury, midrange, budget, economy
    star_rating = Column(Numeric(2, 1), nullable=True)  # 1.0 to 5.0
    chain_name = Column(String(255), nullable=True, index=True)

    # Pricing
    lowest_price = Column(Numeric(10, 2), nullable=True)  # Lowest available nightly rate
    avg_price = Column(Numeric(10, 2), nullable=True)  # Average nightly rate
    currency = Column(String(3), default="USD", nullable=False)

    # Reviews and ratings
    overall_rating = Column(Numeric(3, 2), nullable=True)  # 0.00 to 10.00 or 0-5
    review_count = Column(Integer, default=0, nullable=False)
    rating_breakdown = Column(JSONB, nullable=True)  # {"cleanliness": 4.5, "service": 4.8, ...}

    # Amenities (stored as JSONB for flexibility)
    amenities = Column(JSONB, nullable=True)  # {"wifi": true, "pool": true, ...}

    # Room information
    total_rooms = Column(Integer, nullable=True)
    room_types = Column(JSONB, nullable=True)  # [{"type": "single", "count": 10}, ...]

    # Check-in/out
    check_in_time = Column(String(10), default="15:00", nullable=False)  # HH:MM
    check_out_time = Column(String(10), default="11:00", nullable=False)  # HH:MM

    # Data sources
    sources = Column(JSONB, nullable=True)  # {"booking": "id123", "google": "id456", ...}

    # Booking information
    booking_url = Column(String(500), nullable=True)
    partner_id = Column(String(100), nullable=True, index=True)

    # Business logic
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    reviews = relationship("HotelReview", back_populates="hotel", cascade="all, delete-orphan")
    prices = relationship("HotelPrice", back_populates="hotel", cascade="all, delete-orphan")
    amenity_tags = relationship("HotelAmenity", back_populates="hotel", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_hotel_city_country", "city", "country"),
        Index("idx_hotel_category", "category"),
        Index("idx_hotel_rating", "overall_rating"),
        Index("idx_hotel_price", "avg_price"),
        Index("idx_hotel_location", "location", postgresql_using="gist"),
        Index("idx_hotel_active_featured", "is_active", "is_featured"),
    )

    def __repr__(self) -> str:
        return f"<Hotel(id={self.id}, name={self.name}, city={self.city})>"


class HotelReview(Base):
    """Hotel reviews from various sources"""

    __tablename__ = "hotel_reviews"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    hotel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Review content
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    rating = Column(Numeric(3, 2), nullable=False)  # 0.00 to 10.00 or 0-5

    # Reviewer info
    reviewer_name = Column(String(255), nullable=False)
    reviewer_id = Column(String(100), nullable=True)

    # Review details
    source = Column(String(50), nullable=False, index=True)  # "booking", "google", "tripadvisor", etc.
    source_id = Column(String(500), nullable=True)  # External review ID
    review_date = Column(DateTime, nullable=True)

    # Review metadata
    helpful_count = Column(Integer, default=0, nullable=False)
    verified_purchase = Column(Boolean, default=False, nullable=False)

    # Aspects (flexibility for different sources)
    aspects = Column(JSONB, nullable=True)  # {"cleanliness": 5, "service": 4, ...}

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    hotel = relationship("Hotel", back_populates="reviews")

    # Indexes
    __table_args__ = (
        Index("idx_review_hotel", "hotel_id"),
        Index("idx_review_source", "source"),
        Index("idx_review_rating", "rating"),
    )

    def __repr__(self) -> str:
        return f"<HotelReview(id={self.id}, hotel_id={self.hotel_id}, rating={self.rating})>"


class HotelPrice(Base):
    """Hotel price history for trend analysis"""

    __tablename__ = "hotel_prices"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    hotel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Price data
    nightly_rate = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)

    # Dates
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    quote_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Room type
    room_type = Column(String(100), nullable=True)
    occupancy = Column(String(100), nullable=True)  # "2 guests", "1 adult 2 children", etc.

    # Source
    source = Column(String(50), nullable=False, index=True)  # "booking", "google", etc.
    booking_url = Column(String(500), nullable=True)

    # Relationship
    hotel = relationship("Hotel", back_populates="prices")

    # Indexes
    __table_args__ = (
        Index("idx_price_hotel", "hotel_id"),
        Index("idx_price_dates", "check_in_date", "check_out_date"),
        Index("idx_price_source", "source"),
    )

    def __repr__(self) -> str:
        return f"<HotelPrice(id={self.id}, hotel_id={self.hotel_id}, rate={self.nightly_rate})>"


class HotelAmenity(Base):
    """Hotel amenities and facilities"""

    __tablename__ = "hotel_amenities"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    hotel_id = Column(
        UUID(as_uuid=True),
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Amenity info
    category = Column(String(50), nullable=False, index=True)  # "room", "facility", "service"
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # For frontend icon mapping

    # Availability
    available = Column(Boolean, default=True, nullable=False)
    free = Column(Boolean, default=False, nullable=False)  # Is it free or paid?

    # Additional info
    details = Column(JSONB, nullable=True)

    # Relationship
    hotel = relationship("Hotel", back_populates="amenity_tags")

    # Indexes
    __table_args__ = (
        Index("idx_amenity_hotel", "hotel_id"),
        Index("idx_amenity_category", "category"),
        Index("idx_amenity_name", "name"),
    )

    def __repr__(self) -> str:
        return f"<HotelAmenity(id={self.id}, name={self.name}, category={self.category})>"


class UserHotelPreference(Base):
    """User preferences for hotel discovery"""

    __tablename__ = "user_hotel_preferences"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
    )

    # Budget preferences
    min_budget = Column(Numeric(10, 2), nullable=True)
    max_budget = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="USD", nullable=False)

    # Hotel preferences
    preferred_categories = Column(JSONB, nullable=True)  # ["luxury", "midrange"]
    min_star_rating = Column(Numeric(2, 1), nullable=True)
    preferred_amenities = Column(JSONB, nullable=True)  # ["wifi", "pool", "gym"]
    preferred_chains = Column(JSONB, nullable=True)

    # Location preferences
    max_distance_km = Column(Integer, default=5, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Indexes
    __table_args__ = (
        Index("idx_hotel_pref_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<UserHotelPreference(user_id={self.user_id})>"
