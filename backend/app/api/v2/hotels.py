"""
Hotel Discovery API Endpoints
Provides hotel search, recommendations, and preference management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.hotel import (
    HotelDetailResponse,
    HotelSearchRequest,
    HotelSearchResponse,
    UserHotelPreferenceRequest,
    UserHotelPreferenceResponse,
)
from app.services.hotel_service import (
    HotelRecommendationService,
    HotelSearchService,
)

# Create router
router = APIRouter()


# Dependency to get hotel search service
def get_hotel_search_service(db: Session = Depends(get_db)) -> HotelSearchService:
    """Get hotel search service instance"""
    return HotelSearchService(db)


# Dependency to get hotel recommendation service
def get_hotel_recommendation_service(db: Session = Depends(get_db)) -> HotelRecommendationService:
    """Get hotel recommendation service instance"""
    return HotelRecommendationService(db)


@router.post(
    "/search",
    response_model=dict,
    summary="Search Hotels",
    description="Search for hotels with various filters",
    tags=["Hotels"]
)
async def search_hotels(
    request: HotelSearchRequest,
    service: HotelSearchService = Depends(get_hotel_search_service),
):
    """
    Search hotels with comprehensive filtering:
    - Location (city, geospatial)
    - Price range (budget filtering)
    - Rating and reviews
    - Amenities
    - Availability

    Returns paginated results with hotel details and booking links
    """
    try:
        results, total = service.search(
            city_id=request.city_id,
            min_price=request.min_price,
            max_price=request.max_price,
            min_rating=request.min_rating,
            amenities=request.amenities,
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
                "price_range": f"${request.min_price}-${request.max_price}",
                "min_rating": request.min_rating,
                "amenities": request.amenities or [],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Search failed: {str(e)}"
        )


@router.get(
    "/best-value",
    response_model=dict,
    summary="Get Best Value Hotels",
    description="Get hotels with best rating/price ratio",
    tags=["Hotels"]
)
async def get_best_value_hotels(
    city_id: int = Query(..., description="City ID"),
    min_rating: float = Query(3.5, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: HotelSearchService = Depends(get_hotel_search_service),
):
    """
    Get hotels with the best value ratings (rating/price ratio).
    
    Value Score = (overall_rating / avg_price_usd) * 100
    
    Higher score = better value (high rating at lower price)
    """
    try:
        results, total = service.get_best_value_hotels(
            city_id=city_id,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "best_value",
            "value_calculation": "rating / price * 100",
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
            detail=f"Failed to get best value hotels: {str(e)}"
        )


@router.get(
    "/budget",
    response_model=dict,
    summary="Get Budget Hotels",
    description="Get affordable hotels for budget travelers",
    tags=["Hotels"]
)
async def get_budget_hotels(
    city_id: int = Query(..., description="City ID"),
    max_price: float = Query(50, ge=0, description="Maximum price per night (USD)"),
    min_rating: float = Query(3.5, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: HotelSearchService = Depends(get_hotel_search_service),
):
    """
    Get budget-friendly hotels for cost-conscious travelers.
    
    Budget Category: Economy (< $50/night)
    """
    try:
        results, total = service.get_budget_hotels(
            city_id=city_id,
            max_price=max_price,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "budget_friendly",
            "filters": {
                "max_price": max_price,
                "min_rating": min_rating,
                "category": "Economy"
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
            detail=f"Failed to get budget hotels: {str(e)}"
        )


@router.get(
    "/luxury",
    response_model=dict,
    summary="Get Luxury Hotels",
    description="Get premium and luxury hotels",
    tags=["Hotels"]
)
async def get_luxury_hotels(
    city_id: int = Query(..., description="City ID"),
    min_rating: float = Query(4.0, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: HotelSearchService = Depends(get_hotel_search_service),
):
    """
    Get premium and luxury hotels for discerning travelers.
    
    Premium Category: Luxury (> $300/night)
    """
    try:
        results, total = service.get_luxury_hotels(
            city_id=city_id,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "luxury",
            "filters": {
                "min_rating": min_rating,
                "category": "Luxury (Premium)",
                "price_range": "$300+"
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
            detail=f"Failed to get luxury hotels: {str(e)}"
        )


@router.get(
    "/trending",
    response_model=dict,
    summary="Get Trending Hotels",
    description="Get currently trending and popular hotels",
    tags=["Hotels"]
)
async def get_trending_hotels(
    city_id: int = Query(..., description="City ID"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: HotelSearchService = Depends(get_hotel_search_service),
):
    """
    Get trending hotels based on:
    - Recent bookings
    - High ratings
    - Positive reviews
    - Popularity
    """
    try:
        results, total = service.get_trending_hotels(
            city_id=city_id,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "trending",
            "timestamp": "latest",
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
            detail=f"Failed to get trending hotels: {str(e)}"
        )


@router.get(
    "/{hotel_id}",
    response_model=dict,
    summary="Get Hotel Details",
    description="Get comprehensive hotel information",
    tags=["Hotels"]
)
async def get_hotel_details(
    hotel_id: str,
    service: HotelSearchService = Depends(get_hotel_search_service),
):
    """
    Get detailed hotel information including:
    - Hotel info (name, location, rating)
    - Amenities
    - Reviews and guest feedback
    - Price history
    - Photos and descriptions
    - Booking links and options
    """
    try:
        hotel = service.get_by_id(hotel_id)
        
        if not hotel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hotel {hotel_id} not found"
            )

        return {
            "success": True,
            "data": hotel,
            "booking_options": hotel.get("sources", {}),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get hotel details: {str(e)}"
        )


@router.post(
    "/{hotel_id}/preferences",
    response_model=dict,
    summary="Save Hotel Preferences",
    description="Save user preferences for hotel searches",
    tags=["Hotels", "User Preferences"]
)
async def save_hotel_preferences(
    hotel_id: str,
    preferences: UserHotelPreferenceRequest,
    db: Session = Depends(get_db),
):
    """
    Save user preferences for hotel discoveries:
    - Budget range
    - Preferred amenities
    - Hotel types (business, resort, etc.)
    - Special requirements

    These preferences are applied automatically to personalize recommendations
    """
    try:
        service = HotelSearchService(db)
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


@router.get(
    "/{hotel_id}/price-trends",
    response_model=dict,
    summary="Get Price Trends",
    description="Get historical price data for a hotel",
    tags=["Hotels", "Analysis"]
)
async def get_price_trends(
    hotel_id: str,
    days: int = Query(30, ge=1, le=365, description="Days of history to retrieve"),
    service: HotelSearchService = Depends(get_hotel_search_service),
):
    """
    Get historical price trends to help users:
    - Identify best booking times
    - Compare prices over time
    - Make informed booking decisions
    - Predict future prices

    Returns daily average prices for the specified period
    """
    try:
        trends = service.get_price_trends(hotel_id, days)

        return {
            "success": True,
            "data": trends,
            "analysis": {
                "period_days": days,
                "lowest_price": min(t.get("price", 0) for t in trends) if trends else 0,
                "highest_price": max(t.get("price", 0) for t in trends) if trends else 0,
                "average_price": sum(t.get("price", 0) for t in trends) / len(trends) if trends else 0,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get price trends: {str(e)}"
        )
