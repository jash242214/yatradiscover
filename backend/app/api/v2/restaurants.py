"""
Restaurant Discovery API Endpoints
Provides restaurant search, recommendations, and preference management
"""

from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.restaurant import (
    RestaurantDetailResponse,
    RestaurantSearchRequest,
    RestaurantSearchResponse,
    UserRestaurantPreferenceRequest,
    UserRestaurantPreferenceResponse,
)
from app.services.restaurant_service import (
    RestaurantRecommendationService,
    RestaurantSearchService,
)

# Create router
router = APIRouter()


# Dependency to get restaurant search service
def get_restaurant_search_service(db: Session = Depends(get_db)) -> RestaurantSearchService:
    """Get restaurant search service instance"""
    return RestaurantSearchService(db)


# Dependency to get restaurant recommendation service
def get_restaurant_recommendation_service(db: Session = Depends(get_db)) -> RestaurantRecommendationService:
    """Get restaurant recommendation service instance"""
    return RestaurantRecommendationService(db)


@router.post(
    "/search",
    response_model=dict,
    summary="Search Restaurants",
    description="Search for restaurants with various filters",
    tags=["Restaurants"]
)
async def search_restaurants(
    request: RestaurantSearchRequest,
    service: RestaurantSearchService = Depends(get_restaurant_search_service),
):
    """
    Search restaurants with comprehensive filtering:
    - Location (city, geospatial)
    - Cuisine types
    - Price level
    - Rating and reviews
    - Dietary preferences
    - Availability

    Returns paginated results with restaurant details and booking links
    """
    try:
        results, total = service.search(
            city_id=request.city_id,
            cuisines=request.cuisines,
            price_level=request.price_level,
            min_rating=request.min_rating,
            dietary_preferences=request.dietary_preferences,
            limit=request.limit,
            offset=request.offset,
        )

        return {
            "success": True,
            "data": results,
            "pagination": {
                "total": total,
                "limit": request.limit,
                "offset": request.offset,
                "has_more": (request.offset + request.limit) < total,
            },
            "filters_applied": {
                "city_id": request.city_id,
                "cuisines": request.cuisines or [],
                "price_level": request.price_level,
                "min_rating": request.min_rating,
                "dietary_preferences": request.dietary_preferences or [],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Search failed: {str(e)}"
        )


@router.get(
    "/michelin",
    response_model=dict,
    summary="Get Michelin-Starred Restaurants",
    description="Get Michelin-starred fine dining restaurants",
    tags=["Restaurants"]
)
async def get_michelin_restaurants(
    city_id: int = Query(..., description="City ID"),
    min_stars: int = Query(1, ge=1, le=3, description="Minimum Michelin stars"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: RestaurantSearchService = Depends(get_restaurant_search_service),
):
    """
    Get Michelin-starred fine dining restaurants.
    
    Stars:
    - 1 star: Very good cuisine in its category
    - 2 stars: Excellent cuisine, worth a detour
    - 3 stars: Exceptional cuisine, worth a special journey
    """
    try:
        results, total = service.get_michelin_restaurants(
            city_id=city_id,
            min_stars=min_stars,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "michelin_starred",
            "filters": {
                "min_stars": min_stars,
                "star_meanings": {
                    "1": "Very good cuisine",
                    "2": "Excellent, worth a detour",
                    "3": "Exceptional, worth special journey"
                }
            },
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get Michelin restaurants: {str(e)}"
        )


@router.get(
    "/best-value",
    response_model=dict,
    summary="Get Best Value Restaurants",
    description="Get restaurants with best rating/price ratio",
    tags=["Restaurants"]
)
async def get_best_value_restaurants(
    city_id: int = Query(..., description="City ID"),
    min_rating: float = Query(3.5, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: RestaurantSearchService = Depends(get_restaurant_search_service),
):
    """
    Get restaurants with the best value ratings (rating/price ratio).
    
    Value Score = overall_rating / price_level_numeric ($ = 1 to $$$$ = 4)
    
    Higher score = better value (high rating at lower price level)
    """
    try:
        results, total = service.get_best_value_restaurants(
            city_id=city_id,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "best_value",
            "value_calculation": "rating / price_level",
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get best value restaurants: {str(e)}"
        )


@router.get(
    "/budget",
    response_model=dict,
    summary="Get Budget-Friendly Restaurants",
    description="Get affordable restaurants for budget travelers",
    tags=["Restaurants"]
)
async def get_budget_restaurants(
    city_id: int = Query(..., description="City ID"),
    max_price_level: int = Query(1, ge=1, le=4, description="Max price level (1=$ to 4=$$$$)"),
    min_rating: float = Query(3.5, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: RestaurantSearchService = Depends(get_restaurant_search_service),
):
    """
    Get budget-friendly restaurants for cost-conscious diners.
    
    Price Levels:
    - $ = Budget-friendly
    - $$ = Moderate
    - $$$ = Upscale
    - $$$$ = Fine dining
    """
    try:
        results, total = service.get_budget_friendly(
            city_id=city_id,
            price_level=max_price_level,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "budget_friendly",
            "filters": {
                "max_price_level": max_price_level,
                "price_label": "$" * max_price_level,
                "min_rating": min_rating,
            },
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get budget restaurants: {str(e)}"
        )


@router.get(
    "/fine-dining",
    response_model=dict,
    summary="Get Fine Dining Restaurants",
    description="Get upscale and fine dining restaurants",
    tags=["Restaurants"]
)
async def get_fine_dining_restaurants(
    city_id: int = Query(..., description="City ID"),
    min_rating: float = Query(4.0, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: RestaurantSearchService = Depends(get_restaurant_search_service),
):
    """
    Get fine dining and upscale restaurants for special occasions.
    
    Price Range: $$$ to $$$$
    """
    try:
        results, total = service.get_fine_dining(
            city_id=city_id,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "fine_dining",
            "filters": {
                "min_rating": min_rating,
                "price_range": "$$$ to $$$$",
                "occasion": "Special dining experiences"
            },
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get fine dining restaurants: {str(e)}"
        )


@router.get(
    "/{restaurant_id}",
    response_model=dict,
    summary="Get Restaurant Details",
    description="Get comprehensive restaurant information",
    tags=["Restaurants"]
)
async def get_restaurant_details(
    restaurant_id: str,
    service: RestaurantSearchService = Depends(get_restaurant_search_service),
):
    """
    Get detailed restaurant information including:
    - Restaurant info (name, location, rating, Michelin stars)
    - Cuisines and specialties
    - Price level and reviews
    - Signature dishes
    - Photos and menus
    - Hours of operation
    - Booking links and reservation options
    """
    try:
        restaurant = service.get_by_id(restaurant_id)
        
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restaurant {restaurant_id} not found"
            )

        return {
            "success": True,
            "data": restaurant,
            "booking_options": restaurant.get("sources", {}),
            "signature_dishes": restaurant.get("signature_dishes", []),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get restaurant details: {str(e)}"
        )


@router.get(
    "/{restaurant_id}/signature-dishes",
    response_model=dict,
    summary="Get Signature Dishes",
    description="Get signature dishes of a restaurant",
    tags=["Restaurants"]
)
async def get_signature_dishes(
    restaurant_id: str,
    service: RestaurantSearchService = Depends(get_restaurant_search_service),
):
    """
    Get the signature dishes and specialties of a restaurant.
    
    Includes:
    - Dish name and description
    - Guest ratings for the dish
    - Specialty/must-try indicator
    """
    try:
        dishes = service.get_signature_dishes(restaurant_id)

        return {
            "success": True,
            "data": dishes,
            "restaurant_id": restaurant_id,
            "count": len(dishes),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get signature dishes: {str(e)}"
        )


@router.get(
    "/occasion/{occasion}",
    response_model=dict,
    summary="Get Occasion-Based Recommendations",
    description="Get restaurants recommended for specific occasions",
    tags=["Restaurants"]
)
async def get_occasion_recommendations(
    occasion: Literal["casual", "date", "business", "family"],
    city_id: int = Query(..., description="City ID"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: RestaurantRecommendationService = Depends(get_restaurant_recommendation_service),
):
    """
    Get restaurant recommendations for specific occasions:
    
    - **casual**: Relaxed, family-friendly atmospheres
    - **date**: Romantic settings, intimate ambiance
    - **business**: Professional atmosphere, good for meetings
    - **family**: Kid-friendly, diverse menu options
    """
    try:
        results, total = service.get_personalized_recommendations(
            city_id=city_id,
            occasion=occasion,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": f"occasion_{occasion}",
            "occasion": occasion,
            "occasion_description": {
                "casual": "Relaxed and casual dining",
                "date": "Romantic and intimate",
                "business": "Professional atmosphere",
                "family": "Kid-friendly and diverse"
            }.get(occasion),
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get recommendations: {str(e)}"
        )


@router.post(
    "/{restaurant_id}/preferences",
    response_model=dict,
    summary="Save Restaurant Preferences",
    description="Save user preferences for restaurant searches",
    tags=["Restaurants", "User Preferences"]
)
async def save_restaurant_preferences(
    restaurant_id: str,
    preferences: UserRestaurantPreferenceRequest,
    db: Session = Depends(get_db),
):
    """
    Save user preferences for restaurant discoveries:
    - Cuisine preferences
    - Budget range
    - Dietary preferences (vegetarian, vegan, halal, etc.)
    - Special requirements

    These preferences are applied automatically to personalize recommendations
    """
    try:
        service = RestaurantSearchService(db)
        result = service.save_user_preferences(
            user_id=preferences.user_id,
            preferences=preferences.dict(),
        )

        return {
            "success": True,
            "message": "Preferences saved successfully",
            "data": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to save preferences: {str(e)}"
        )
