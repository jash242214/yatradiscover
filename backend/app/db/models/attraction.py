"""
Attraction database models for places/landmarks discovery
"""
from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    Column, DateTime, String, Boolean, Index, ForeignKey,
    Numeric, Integer, Text, JSON, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base import Base


class Attraction(Base):
    """Attraction/landmark model for places discovery"""

    __tablename__ = "attractions"

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
    website = Column(String(500), nullable=True)

    # Categorization
    category = Column(String(100), nullable=False, index=True)  # "museum", "park", "monument", etc.
    subcategories = Column(JSONB, nullable=True)  # ["art", "history", "contemporary"]

    # Type classification
    attraction_type = Column(String(50), nullable=False, index=True)  # "indoor", "outdoor", "virtual"

    # Entry information
    has_entry_fee = Column(Boolean, default=True, nullable=False)
    entry_fee = Column(Numeric(8, 2), nullable=True)
    currency = Column(String(3), default="USD", nullable=False)
    ticket_url = Column(String(500), nullable=True)

    # Rating and reviews
    overall_rating = Column(Numeric(3, 2), nullable=True)  # 0.00 to 10.00 or 0-5
    review_count = Column(Integer, default=0, nullable=False)
    rating_breakdown = Column(JSONB, nullable=True)  # {"uniqueness": 4.5, "worth_visiting": 4.8, ...}

    # Visitor information
    popularity_rank = Column(Integer, nullable=True)  # Rank among attractions in area
    typical_visit_duration_minutes = Column(Integer, nullable=True)  # Average time spent
    annual_visitor_count = Column(Integer, nullable=True)
    crowd_level_current = Column(String(50), nullable=True)  # "empty", "busy", "very busy"

    # Operating information
    opening_hours = Column(JSONB, nullable=True)  # {"monday": "09:00-18:00", ...}
    closed_on = Column(JSONB, nullable=True)  # ["sunday", "monday"]
    is_seasonal = Column(Boolean, default=False, nullable=False)
    seasonal_info = Column(Text, nullable=True)

    # Accessibility
    wheelchair_accessible = Column(Boolean, nullable=True)
    parking_available = Column(Boolean, nullable=True)
    public_transport_accessible = Column(Boolean, default=True, nullable=False)

    # Visitor services
    has_guide_service = Column(Boolean, default=False, nullable=False)
    has_gift_shop = Column(Boolean, default=False, nullable=False)
    has_restaurant = Column(Boolean, default=False, nullable=False)

    # Photography and media
    photography_allowed = Column(Boolean, default=True, nullable=False)
    photography_restrictions = Column(Text, nullable=True)

    # Data sources
    sources = Column(JSONB, nullable=True)  # {"google": "id123", "tripadvisor": "id456", ...}

    # Business logic
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    is_trending = Column(Boolean, default=False, nullable=False, index=True)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    reviews = relationship("AttractionReview", back_populates="attraction", cascade="all, delete-orphan")
    tips = relationship("VisitorTip", back_populates="attraction", cascade="all, delete-orphan")
    photos = relationship("AttractionPhoto", back_populates="attraction", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_attraction_city_country", "city", "country"),
        Index("idx_attraction_category", "category"),
        Index("idx_attraction_type", "attraction_type"),
        Index("idx_attraction_rating", "overall_rating"),
        Index("idx_attraction_location", "location", postgresql_using="gist"),
        Index("idx_attraction_active_featured", "is_active", "is_featured"),
        Index("idx_attraction_trending", "is_trending"),
    )

    def __repr__(self) -> str:
        return f"<Attraction(id={self.id}, name={self.name}, city={self.city})>"


class AttractionReview(Base):
    """Reviews for attractions"""

    __tablename__ = "attraction_reviews"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    attraction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attractions.id", ondelete="CASCADE"),
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
    source = Column(String(50), nullable=False, index=True)  # "google", "tripadvisor", etc.
    source_id = Column(String(500), nullable=True)
    review_date = Column(DateTime, nullable=True)

    # Aspects of the review
    aspects = Column(JSONB, nullable=True)  # {"unique_experience": 5, "worth_time": 4, ...}

    # Review metadata
    helpful_count = Column(Integer, default=0, nullable=False)
    verified_visit = Column(Boolean, default=False, nullable=False)
    visit_date = Column(DateTime, nullable=True)

    # Visitor profile
    visit_type = Column(String(50), nullable=True)  # "solo", "couple", "family", "group"
    visit_season = Column(String(50), nullable=True)  # "winter", "summer", "spring", "fall"

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    attraction = relationship("Attraction", back_populates="reviews")

    # Indexes
    __table_args__ = (
        Index("idx_attr_review_attraction", "attraction_id"),
        Index("idx_attr_review_source", "source"),
        Index("idx_attr_review_rating", "rating"),
    )

    def __repr__(self) -> str:
        return f"<AttractionReview(id={self.id}, attraction_id={self.attraction_id})>"


class VisitorTip(Base):
    """Visitor tips and advice for attractions"""

    __tablename__ = "visitor_tips"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    attraction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attractions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Tip content
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    tip_type = Column(String(50), nullable=False, index=True)  # "timing", "money", "planning", "experience"

    # Tip details
    is_official = Column(Boolean, default=False, nullable=False)  # From attraction or crowdsourced
    author_name = Column(String(255), nullable=True)
    author_id = Column(String(100), nullable=True)

    # Usefulness
    helpful_count = Column(Integer, default=0, nullable=False)
    rating = Column(Numeric(3, 2), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    attraction = relationship("Attraction", back_populates="tips")

    # Indexes
    __table_args__ = (
        Index("idx_tip_attraction", "attraction_id"),
        Index("idx_tip_type", "tip_type"),
    )

    def __repr__(self) -> str:
        return f"<VisitorTip(id={self.id}, title={self.title})>"


class AttractionPhoto(Base):
    """Photos of attractions"""

    __tablename__ = "attraction_photos"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    attraction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("attractions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Photo details
    url = Column(String(500), nullable=False)
    photo_type = Column(String(50), nullable=False)  # "overview", "interior", "detail", "crowd"
    caption = Column(Text, nullable=True)
    source = Column(String(50), nullable=False)  # "google", "tripadvisor", etc.

    # Photo metadata
    uploaded_by = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    helpful_count = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    attraction = relationship("Attraction", back_populates="photos")

    # Indexes
    __table_args__ = (
        Index("idx_attr_photo_attraction", "attraction_id"),
        Index("idx_attr_photo_type", "photo_type"),
    )

    def __repr__(self) -> str:
        return f"<AttractionPhoto(id={self.id}, attraction_id={self.attraction_id})>"


class UserAttractionPreference(Base):
    """User preferences for attraction discovery"""

    __tablename__ = "user_attraction_preferences"

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

    # Attraction type preferences
    preferred_categories = Column(JSONB, nullable=True)  # ["museum", "park", "monument"]
    disliked_categories = Column(JSONB, nullable=True)

    # Visit preferences
    preferred_activity_type = Column(String(50), nullable=True)  # "indoor", "outdoor", "mixed"
    max_visit_duration_hours = Column(Integer, nullable=True)
    prefer_crowded = Column(Boolean, nullable=True)  # Some prefer quiet, some prefer lively

    # Accessibility preferences
    wheelchair_required = Column(Boolean, default=False, nullable=False)
    parking_required = Column(Boolean, default=False, nullable=False)

    # Budget preferences (ticket prices)
    max_ticket_price = Column(Numeric(8, 2), nullable=True)
    currency = Column(String(3), default="USD", nullable=False)

    # Location preferences
    max_distance_km = Column(Integer, default=10, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Indexes
    __table_args__ = (
        Index("idx_attr_pref_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<UserAttractionPreference(user_id={self.user_id})>"
