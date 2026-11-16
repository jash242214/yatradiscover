"""
Restaurant database models for food discovery features
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


class Restaurant(Base):
    """Restaurant model for dining discovery"""

    __tablename__ = "restaurants"

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

    # Cuisine and classification
    primary_cuisine = Column(String(100), nullable=False, index=True)  # "Italian", "Chinese", etc.
    cuisines = Column(JSONB, nullable=True)  # ["Italian", "Seafood"]
    
    # Price level
    price_level = Column(String(50), nullable=False, index=True)  # "$", "$$", "$$$", "$$$$"
    avg_cost_per_person = Column(Numeric(8, 2), nullable=True)  # Average cost
    currency = Column(String(3), default="USD", nullable=False)

    # Rating and reviews
    overall_rating = Column(Numeric(3, 2), nullable=True)  # 0.00 to 10.00 or 0-5
    review_count = Column(Integer, default=0, nullable=False)
    rating_breakdown = Column(JSONB, nullable=True)  # {"taste": 4.5, "service": 4.8, ...}

    # Michelin and awards
    michelin_stars = Column(Integer, default=0, nullable=False, index=True)  # 0, 1, 2, or 3
    has_michelin_green = Column(Boolean, default=False, nullable=False)  # Green star (sustainable)
    awards = Column(JSONB, nullable=True)  # [{"name": "Best Italian", "year": 2023}, ...]

    # Dining features
    dining_style = Column(String(50), nullable=True)  # "casual", "fine dining", "fast casual"
    menu_type = Column(JSONB, nullable=True)  # ["dinner", "lunch", "brunch", "takeout"]
    atmosphere = Column(JSONB, nullable=True)  # ["romantic", "family-friendly", "lively"]

    # Reservation information
    accepts_reservations = Column(Boolean, default=True, nullable=False)
    reservation_url = Column(String(500), nullable=True)

    # Operating hours
    opening_hours = Column(JSONB, nullable=True)  # {"monday": "11:00-22:00", ...}
    closed_on = Column(JSONB, nullable=True)  # ["sunday", "monday"]

    # Special dietary support
    dietary_options = Column(JSONB, nullable=True)  # ["vegetarian", "vegan", "gluten-free"]

    # Parking and accessibility
    parking_available = Column(Boolean, nullable=True)
    wheelchair_accessible = Column(Boolean, nullable=True)

    # Data sources
    sources = Column(JSONB, nullable=True)  # {"google": "id123", "tripadvisor": "id456", ...}
    booking_url = Column(String(500), nullable=True)

    # Business logic
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    is_trending = Column(Boolean, default=False, nullable=False, index=True)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    reviews = relationship("RestaurantReview", back_populates="restaurant", cascade="all, delete-orphan")
    signature_dishes = relationship("SignatureDish", back_populates="restaurant", cascade="all, delete-orphan")
    photos = relationship("RestaurantPhoto", back_populates="restaurant", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_restaurant_city_country", "city", "country"),
        Index("idx_restaurant_cuisine", "primary_cuisine"),
        Index("idx_restaurant_price_level", "price_level"),
        Index("idx_restaurant_rating", "overall_rating"),
        Index("idx_restaurant_michelin", "michelin_stars"),
        Index("idx_restaurant_location", "location", postgresql_using="gist"),
        Index("idx_restaurant_active_featured", "is_active", "is_featured"),
        Index("idx_restaurant_trending", "is_trending"),
    )

    def __repr__(self) -> str:
        return f"<Restaurant(id={self.id}, name={self.name}, city={self.city})>"


class RestaurantReview(Base):
    """Restaurant reviews from various sources"""

    __tablename__ = "restaurant_reviews"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id", ondelete="CASCADE"),
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
    source = Column(String(50), nullable=False, index=True)  # "google", "tripadvisor", "michelin", etc.
    source_id = Column(String(500), nullable=True)
    review_date = Column(DateTime, nullable=True)

    # Aspects
    aspects = Column(JSONB, nullable=True)  # {"taste": 5, "service": 4, "ambiance": 5, ...}

    # Review metadata
    helpful_count = Column(Integer, default=0, nullable=False)
    verified_visit = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    restaurant = relationship("Restaurant", back_populates="reviews")

    # Indexes
    __table_args__ = (
        Index("idx_rest_review_restaurant", "restaurant_id"),
        Index("idx_rest_review_source", "source"),
        Index("idx_rest_review_rating", "rating"),
    )

    def __repr__(self) -> str:
        return f"<RestaurantReview(id={self.id}, restaurant_id={self.restaurant_id})>"


class SignatureDish(Base):
    """Signature dishes at a restaurant"""

    __tablename__ = "signature_dishes"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Dish info
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Cuisine details
    cuisine = Column(String(100), nullable=True)
    ingredients = Column(JSONB, nullable=True)  # ["tomato", "basil", "mozzarella"]
    dietary_info = Column(JSONB, nullable=True)  # ["vegetarian", "gluten-free"]

    # Pricing and popularity
    price = Column(Numeric(8, 2), nullable=True)
    popularity_score = Column(Numeric(3, 2), nullable=True)  # 0 to 10
    reviewer_mentions = Column(Integer, default=0, nullable=False)

    # Media
    photo_url = Column(String(500), nullable=True)

    # Details
    availability = Column(String(50), nullable=True)  # "always", "seasonal", "limited"
    is_seasonal = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    restaurant = relationship("Restaurant", back_populates="signature_dishes")

    # Indexes
    __table_args__ = (
        Index("idx_dish_restaurant", "restaurant_id"),
        Index("idx_dish_name", "name"),
    )

    def __repr__(self) -> str:
        return f"<SignatureDish(id={self.id}, name={self.name})>"


class RestaurantPhoto(Base):
    """Photos of restaurants and their food"""

    __tablename__ = "restaurant_photos"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Foreign key
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Photo details
    url = Column(String(500), nullable=False)
    photo_type = Column(String(50), nullable=False)  # "exterior", "interior", "food", "ambiance"
    caption = Column(Text, nullable=True)
    source = Column(String(50), nullable=False)  # "google", "tripadvisor", etc.

    # Photo metadata
    uploaded_by = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    helpful_count = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    restaurant = relationship("Restaurant", back_populates="photos")

    # Indexes
    __table_args__ = (
        Index("idx_photo_restaurant", "restaurant_id"),
        Index("idx_photo_type", "photo_type"),
    )

    def __repr__(self) -> str:
        return f"<RestaurantPhoto(id={self.id}, restaurant_id={self.restaurant_id})>"


class UserRestaurantPreference(Base):
    """User preferences for restaurant discovery"""

    __tablename__ = "user_restaurant_preferences"

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
    preferred_price_levels = Column(JSONB, nullable=True)  # ["$", "$$", "$$$"]
    max_cost_per_person = Column(Numeric(8, 2), nullable=True)
    currency = Column(String(3), default="USD", nullable=False)

    # Cuisine preferences
    preferred_cuisines = Column(JSONB, nullable=True)  # ["Italian", "Japanese", "Thai"]
    disliked_cuisines = Column(JSONB, nullable=True)

    # Dietary preferences
    dietary_options = Column(JSONB, nullable=True)  # ["vegetarian", "gluten-free", "vegan"]

    # Dining preferences
    preferred_dining_style = Column(JSONB, nullable=True)  # ["casual", "fine dining"]
    atmosphere_preferences = Column(JSONB, nullable=True)  # ["romantic", "family-friendly"]

    # Michelin preference
    prefer_michelin_restaurants = Column(Boolean, default=False, nullable=False)

    # Location preferences
    max_distance_km = Column(Integer, default=5, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Indexes
    __table_args__ = (
        Index("idx_rest_pref_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<UserRestaurantPreference(user_id={self.user_id})>"
