"""
Attraction Discovery API Endpoints
Provides attraction search, recommendations, and preference management
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.attraction import (
    AttractionDetailResponse,
    AttractionSearchRequest,
    AttractionSearchResponse,
    UserAttractionPreferenceRequest,
    UserAttractionPreferenceResponse,
)
from app.services.attraction_service import (
    AttractionRecommendationService,
    AttractionSearchService,
)

# Create router
router = APIRouter()


# Dependency to get attraction search service
def get_attraction_search_service(db: Session = Depends(get_db)) -> AttractionSearchService:
    """Get attraction search service instance"""
    return AttractionSearchService(db)


# Dependency to get attraction recommendation service
def get_attraction_recommendation_service(db: Session = Depends(get_db)) -> AttractionRecommendationService:
    """Get attraction recommendation service instance"""
    return AttractionRecommendationService(db)


@router.post(
    "/search",
    response_model=dict,
    summary="Search Attractions",
    description="Search for attractions with various filters",
    tags=["Attractions"]
)
async def search_attractions(
    request: AttractionSearchRequest,
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Search attractions with comprehensive filtering:
    - Location (city, geospatial)
    - Category (museum, park, historical, etc.)
    - Entry fee range
    - Rating and reviews
    - Accessibility requirements
    - Visit duration

    Returns paginated results with attraction details and booking links
    """
    try:
        results, total = service.search(
            city_id=request.city_id,
            categories=request.categories,
            min_rating=request.min_rating,
            max_entry_fee=request.max_entry_fee,
            accessibility_features=request.accessibility_features,
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
                "categories": request.categories or [],
                "min_rating": request.min_rating,
                "max_entry_fee": request.max_entry_fee,
                "accessibility_features": request.accessibility_features or [],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Search failed: {str(e)}"
        )


@router.get(
    "/popular",
    response_model=dict,
    summary="Get Popular Attractions",
    description="Get most popular and highly-rated attractions",
    tags=["Attractions"]
)
async def get_popular_attractions(
    city_id: int = Query(..., description="City ID"),
    min_rating: float = Query(4.0, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Get the most popular and highly-rated attractions in a city.
    
    Sorted by: Rating (descending) → Popularity → Reviews count
    """
    try:
        results, total = service.get_popular_attractions(
            city_id=city_id,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "popular",
            "filters": {
                "min_rating": min_rating,
                "sorted_by": "popularity & rating"
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
            detail=f"Failed to get popular attractions: {str(e)}"
        )


@router.get(
    "/budget",
    response_model=dict,
    summary="Get Budget-Friendly Attractions",
    description="Get free and low-cost attractions",
    tags=["Attractions"]
)
async def get_budget_attractions(
    city_id: int = Query(..., description="City ID"),
    max_entry_fee: float = Query(10, ge=0, description="Max entry fee (USD)"),
    min_rating: float = Query(3.5, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Get budget-friendly and free attractions.
    
    Prioritizes:
    1. Free attractions (entry_fee = 0)
    2. Low-cost (< $10)
    3. High ratings
    """
    try:
        results, total = service.get_budget_friendly_attractions(
            city_id=city_id,
            max_entry_fee=max_entry_fee,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "budget_friendly",
            "filters": {
                "max_entry_fee": max_entry_fee,
                "priority": ["Free attractions first", "Then low-cost", "Then high-rated"],
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
            detail=f"Failed to get budget attractions: {str(e)}"
        )


@router.get(
    "/quick-visit",
    response_model=dict,
    summary="Get Quick-Visit Attractions",
    description="Get attractions perfect for short visits (30-60 minutes)",
    tags=["Attractions"]
)
async def get_quick_visit_attractions(
    city_id: int = Query(..., description="City ID"),
    max_duration_minutes: int = Query(60, ge=15, le=180, description="Max visit duration in minutes"),
    min_rating: float = Query(3.5, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Get attractions perfect for quick visits.
    
    Useful for travelers with limited time who want to:
    - Maximize experiences in short timeframes
    - Visit multiple attractions in one day
    - Quick sightseeing between other activities
    """
    try:
        results, total = service.get_quick_visit_attractions(
            city_id=city_id,
            duration_minutes=max_duration_minutes,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "quick_visit",
            "filters": {
                "max_duration_minutes": max_duration_minutes,
                "ideal_for": "Short visits, quick sightseeing",
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
            detail=f"Failed to get quick-visit attractions: {str(e)}"
        )


@router.get(
    "/hidden-gems",
    response_model=dict,
    summary="Get Hidden Gems",
    description="Get high-rated but lesser-known attractions",
    tags=["Attractions"]
)
async def get_hidden_gems(
    city_id: int = Query(..., description="City ID"),
    min_rating: float = Query(4.0, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Get hidden gems - high-rated attractions that aren't as well-known.
    
    Perfect for travelers looking to:
    - Discover lesser-known places
    - Avoid overly touristy spots
    - Have unique local experiences
    
    Criteria: High rating (4.0+) but lower popularity ranking
    """
    try:
        results, total = service.get_hidden_gems(
            city_id=city_id,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )

        return {
            "success": True,
            "data": results,
            "recommendation_type": "hidden_gems",
            "filters": {
                "min_rating": min_rating,
                "popularity": "Less touristy, more local experiences",
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
            detail=f"Failed to get hidden gems: {str(e)}"
        )


@router.get(
    "/{attraction_id}",
    response_model=dict,
    summary="Get Attraction Details",
    description="Get comprehensive attraction information",
    tags=["Attractions"]
)
async def get_attraction_details(
    attraction_id: str,
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Get detailed attraction information including:
    - Attraction info (name, location, category, rating)
    - Description and history
    - Entry fee and hours of operation
    - Typical visit duration
    - Accessibility information
    - Photos and media
    - Visitor tips and advice
    - Booking links and ticket options
    """
    try:
        attraction = service.get_by_id(attraction_id)
        
        if not attraction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attraction {attraction_id} not found"
            )

        return {
            "success": True,
            "data": attraction,
            "booking_options": attraction.get("sources", {}),
            "visitor_tips": attraction.get("visitor_tips", []),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get attraction details: {str(e)}"
        )


@router.get(
    "/{attraction_id}/visitor-tips",
    response_model=dict,
    summary="Get Visitor Tips",
    description="Get tips and advice from visitors",
    tags=["Attractions"]
)
async def get_visitor_tips(
    attraction_id: str,
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Get helpful tips from visitors about an attraction.
    
    Includes:
    - What to know before visiting
    - Best times to visit
    - Photos and descriptions
    - Hidden secrets and must-sees
    - Practical advice
    """
    try:
        tips = service.get_visitor_tips(attraction_id)

        return {
            "success": True,
            "data": tips,
            "attraction_id": attraction_id,
            "count": len(tips),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get visitor tips: {str(e)}"
        )


@router.get(
    "/nearby",
    response_model=dict,
    summary="Find Nearby Attractions",
    description="Find attractions near a location using geospatial search",
    tags=["Attractions", "Geospatial"]
)
async def get_nearby_attractions(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude"),
    radius_km: float = Query(5, ge=0.1, le=50, description="Search radius in kilometers"),
    min_rating: float = Query(3.0, ge=0, le=5, description="Minimum rating"),
    limit: int = Query(20, ge=1, le=100, description="Results limit"),
    service: AttractionSearchService = Depends(get_attraction_search_service),
):
    """
    Find attractions near a given location using geospatial search.
    
    Useful for:
    - Finding things to do in your current area
    - Exploring nearby attractions while traveling
    - Quick local discovery
    
    Results sorted by distance (nearest first)
    """
    try:
        results, total = service.get_nearby(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            min_rating=min_rating,
            limit=limit,
        )

        return {
            "success": True,
            "data": results,
            "search_location": {
                "latitude": latitude,
                "longitude": longitude,
                "radius_km": radius_km,
            },
            "sorted_by": "distance (nearest first)",
            "pagination": {
                "total": total,
                "limit": limit,
                "has_more": len(results) >= limit,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to find nearby attractions: {str(e)}"
        )


@router.post(
    "/{attraction_id}/preferences",
    response_model=dict,
    summary="Save Attraction Preferences",
    description="Save user preferences for attraction searches",
    tags=["Attractions", "User Preferences"]
)
async def save_attraction_preferences(
    attraction_id: str,
    preferences: UserAttractionPreferenceRequest,
    db: Session = Depends(get_db),
):
    """
    Save user preferences for attraction discoveries:
    - Preferred categories
    - Budget range
    - Accessibility needs
    - Maximum visit duration
    - Special interests

    These preferences are applied automatically to personalize recommendations
    """
    try:
        service = AttractionSearchService(db)
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
    "/itinerary/recommend",
    response_model=dict,
    summary="Get Itinerary Recommendations",
    description="Get attraction recommendations for multi-day itinerary",
    tags=["Attractions"]
)
async def get_itinerary_recommendations(
    city_id: int = Query(..., description="City ID"),
    trip_duration_days: int = Query(3, ge=1, le=30, description="Trip duration in days"),
    daily_hours_available: float = Query(8, ge=1, le=24, description="Daily hours available for attractions"),
    limit: int = Query(30, ge=5, le=100, description="Max recommendations"),
    service: AttractionRecommendationService = Depends(get_attraction_recommendation_service),
):
    """
    Get a curated list of attractions for a multi-day itinerary.
    
    Takes into account:
    - Total trip duration
    - Available time per day
    - Travel time between attractions
    - Variety of experiences
    - Optimal routing
    
    Returns a prioritized recommendation that can be used to plan a day-by-day itinerary
    """
    try:
        results = service.get_itinerary_recommendations(
            city_id=city_id,
            trip_duration_days=trip_duration_days,
            daily_hours_available=daily_hours_available,
            limit=limit,
        )

        return {
            "success": True,
            "data": results,
            "itinerary_config": {
                "city_id": city_id,
                "trip_duration_days": trip_duration_days,
                "daily_hours_available": daily_hours_available,
            },
            "recommendations_count": len(results),
            "note": "These are prioritized recommendations. Actual itinerary should account for travel time between attractions.",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get itinerary recommendations: {str(e)}"
        )
