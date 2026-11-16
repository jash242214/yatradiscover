"""
Database models package
"""
from app.db.models.user import User

# Hotel discovery models
from app.db.models.hotel import (
    Hotel,
    HotelReview,
    HotelPrice,
    HotelAmenity,
    UserHotelPreference,
)

# Restaurant discovery models
from app.db.models.restaurant import (
    Restaurant,
    RestaurantReview,
    SignatureDish,
    RestaurantPhoto,
    UserRestaurantPreference,
)

# Attraction discovery models
from app.db.models.attraction import (
    Attraction,
    AttractionReview,
    VisitorTip,
    AttractionPhoto,
    UserAttractionPreference,
)

__all__ = [
    # User
    "User",
    # Hotel
    "Hotel",
    "HotelReview",
    "HotelPrice",
    "HotelAmenity",
    "UserHotelPreference",
    # Restaurant
    "Restaurant",
    "RestaurantReview",
    "SignatureDish",
    "RestaurantPhoto",
    "UserRestaurantPreference",
    # Attraction
    "Attraction",
    "AttractionReview",
    "VisitorTip",
    "AttractionPhoto",
    "UserAttractionPreference",
]
