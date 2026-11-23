"""API schemas package"""
from app.schemas.user import UserResponse, UserRegister, UserLogin, TokenResponse

# Hotel schemas
from app.schemas.hotel import (
    HotelDetailResponse,
    HotelSearchResponse,
    HotelSearchRequest,
    HotelFilterRequest,
    UserHotelPreferenceResponse,
    UserHotelPreferenceRequest,
)

# Restaurant schemas
from app.schemas.restaurant import (
    RestaurantDetailResponse,
    RestaurantSearchResponse,
    RestaurantSearchRequest,
    RestaurantFilterRequest,
    UserRestaurantPreferenceResponse,
    UserRestaurantPreferenceRequest,
)

# Attraction schemas
from app.schemas.attraction import (
    AttractionDetailResponse,
    AttractionSearchResponse,
    AttractionSearchRequest,
    AttractionFilterRequest,
    UserAttractionPreferenceResponse,
    UserAttractionPreferenceRequest,
)

__all__ = [
    # User
    "UserResponse",
    "UserRegister",
    "UserLogin",
    "TokenResponse",
    # Hotel
    "HotelDetailResponse",
    "HotelSearchResponse",
    "HotelSearchRequest",
    "HotelFilterRequest",
    "UserHotelPreferenceResponse",
    "UserHotelPreferenceRequest",
    # Restaurant
    "RestaurantDetailResponse",
    "RestaurantSearchResponse",
    "RestaurantSearchRequest",
    "RestaurantFilterRequest",
    "UserRestaurantPreferenceResponse",
    "UserRestaurantPreferenceRequest",
    # Attraction
    "AttractionDetailResponse",
    "AttractionSearchResponse",
    "AttractionSearchRequest",
    "AttractionFilterRequest",
    "UserAttractionPreferenceResponse",
    "UserAttractionPreferenceRequest",
]
