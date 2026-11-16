"""Hotel discovery service with search, filtering, and recommendations"""
from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from geoalchemy2.functions import ST_DWithin, ST_Distance
from geoalchemy2.elements import WKTElement

from app.db.models import (
    Hotel,
    HotelReview,
    HotelPrice,
    UserHotelPreference,
)
from app.schemas.hotel import (
    HotelSearchRequest,
    HotelSearchResponse,
    HotelDetailResponse,
)


class HotelSearchService:
    """Service for hotel discovery and search"""

    def __init__(self, db: Session):
        self.db = db

    def search_hotels(
        self,
        request: HotelSearchRequest,
        user_id: Optional[str] = None,
    ) -> Tuple[List[HotelSearchResponse], int]:
        """
        Search hotels with advanced filtering and sorting.
        
        Args:
            request: Hotel search parameters
            user_id: Optional user ID to apply user preferences
            
        Returns:
            Tuple of (results, total_count)
        """
        query = self.db.query(Hotel).filter(Hotel.is_active == True)

        # Location-based search with geospatial queries
        if request.latitude is not None and request.longitude is not None:
            # Create a point from lat/lon
            point = WKTElement(f'POINT({request.longitude} {request.latitude})', srid=4326)
            distance_meters = request.distance_km * 1000
            
            # Filter by distance using PostGIS
            query = query.filter(
                ST_DWithin(Hotel.location, point, distance_meters)
            )
            
            # Add distance calculation for sorting
            query = query.add_columns(
                ST_Distance(Hotel.location, point).label('distance')
            )
        elif request.city:
            # City-based search
            query = query.filter(
                and_(
                    func.lower(Hotel.city) == func.lower(request.city),
                    func.lower(Hotel.country) == func.lower(request.country or "")
                )
            )

        # Price filtering
        if request.min_price is not None:
            query = query.filter(Hotel.avg_price >= request.min_price)
        if request.max_price is not None:
            query = query.filter(Hotel.avg_price <= request.max_price)

        # Rating filtering
        if request.min_rating is not None:
            query = query.filter(Hotel.overall_rating >= request.min_rating)

        # Star rating filtering
        if request.min_stars is not None:
            query = query.filter(Hotel.star_rating >= request.min_stars)

        # Category filtering
        if request.category:
            query = query.filter(func.lower(Hotel.category) == func.lower(request.category))

        # Chain filtering
        if request.chain_name:
            query = query.filter(func.lower(Hotel.chain_name) == func.lower(request.chain_name))

        # Amenities filtering (JSONB array contains)
        if request.amenities:
            for amenity in request.amenities:
                query = query.filter(
                    Hotel.amenities.astext.contains(amenity)
                )

        # Apply user preferences if provided
        if user_id:
            query = self._apply_user_preferences(query, user_id)

        # Sorting
        if request.sort_by == "rating":
            sort_col = Hotel.overall_rating.desc() if request.sort_order == "desc" else Hotel.overall_rating.asc()
        elif request.sort_by == "price":
            sort_col = Hotel.avg_price.desc() if request.sort_order == "desc" else Hotel.avg_price.asc()
        elif request.sort_by == "distance" and request.latitude is not None:
            sort_col = text("distance asc")  # Distance always ascending (closest first)
        elif request.sort_by == "review_count":
            sort_col = Hotel.review_count.desc() if request.sort_order == "desc" else Hotel.review_count.asc()
        else:
            sort_col = Hotel.overall_rating.desc()

        query = query.order_by(sort_col)

        # Get total count before pagination
        total_count = query.count() if not request.latitude else len(query.all())

        # Pagination
        results = query.offset(request.offset).limit(request.limit).all()

        # Convert to response objects
        hotel_responses = []
        for row in results:
            if isinstance(row, tuple):
                hotel = row[0]
            else:
                hotel = row
            
            response = HotelSearchResponse.from_orm(hotel)
            hotel_responses.append(response)

        return hotel_responses, total_count

    def get_best_value_hotels(
        self,
        city: str,
        country: str,
        limit: int = 10,
        min_rating: Decimal = Decimal("3.5"),
    ) -> List[HotelSearchResponse]:
        """
        Get best value hotels ranked by rating/price ratio.
        
        Strategy:
        - Filter hotels with minimum rating
        - Calculate value score: (rating / avg_price) * 100
        - Rank by value score descending
        """
        query = (
            self.db.query(Hotel)
            .filter(
                and_(
                    func.lower(Hotel.city) == func.lower(city),
                    func.lower(Hotel.country) == func.lower(country),
                    Hotel.is_active == True,
                    Hotel.overall_rating >= min_rating,
                    Hotel.avg_price.isnot(None),
                    Hotel.avg_price > 0,
                )
            )
            .all()
        )

        # Calculate value scores in Python
        hotels_with_score = []
        for hotel in query:
            if hotel.avg_price and hotel.avg_price > 0:
                value_score = (float(hotel.overall_rating or 0) / float(hotel.avg_price)) * 100
            else:
                value_score = 0
            
            hotels_with_score.append((hotel, value_score))

        # Sort by value score descending
        hotels_with_score.sort(key=lambda x: x[1], reverse=True)

        # Convert to response objects
        return [
            HotelSearchResponse.from_orm(hotel)
            for hotel, _ in hotels_with_score[:limit]
        ]

    def get_budget_friendly_hotels(
        self,
        city: str,
        country: str,
        max_price: Decimal,
        min_rating: Decimal = Decimal("3.5"),
        limit: int = 10,
    ) -> List[HotelSearchResponse]:
        """
        Get budget-friendly hotels within price range with good ratings.
        
        Strategy:
        - Filter by max price
        - Filter by minimum rating (quality assurance)
        - Sort by rating descending (best-reviewed first)
        """
        query = (
            self.db.query(Hotel)
            .filter(
                and_(
                    func.lower(Hotel.city) == func.lower(city),
                    func.lower(Hotel.country) == func.lower(country),
                    Hotel.is_active == True,
                    Hotel.avg_price <= max_price,
                    Hotel.overall_rating >= min_rating,
                )
            )
            .order_by(Hotel.overall_rating.desc())
            .limit(limit)
            .all()
        )

        return [HotelSearchResponse.from_orm(hotel) for hotel in query]

    def get_luxury_recommendations(
        self,
        city: str,
        country: str,
        min_stars: int = 4,
        limit: int = 5,
    ) -> List[HotelSearchResponse]:
        """
        Get luxury hotel recommendations.
        
        Strategy:
        - Filter by star rating
        - Filter by category
        - Sort by overall rating and featured status
        """
        query = (
            self.db.query(Hotel)
            .filter(
                and_(
                    func.lower(Hotel.city) == func.lower(city),
                    func.lower(Hotel.country) == func.lower(country),
                    Hotel.is_active == True,
                    Hotel.star_rating >= min_stars,
                    Hotel.category.in_(["luxury", "upscale"]),
                )
            )
            .order_by(
                Hotel.is_featured.desc(),
                Hotel.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [HotelSearchResponse.from_orm(hotel) for hotel in query]

    def get_trending_hotels(
        self,
        city: str,
        country: str,
        limit: int = 10,
    ) -> List[HotelSearchResponse]:
        """
        Get trending/featured hotels with recent reviews.
        
        Strategy:
        - Filter by featured flag and active status
        - Sort by recent updates and review count
        """
        query = (
            self.db.query(Hotel)
            .filter(
                and_(
                    func.lower(Hotel.city) == func.lower(city),
                    func.lower(Hotel.country) == func.lower(country),
                    Hotel.is_active == True,
                    Hotel.is_featured == True,
                )
            )
            .order_by(
                Hotel.last_updated.desc(),
                Hotel.review_count.desc(),
            )
            .limit(limit)
            .all()
        )

        return [HotelSearchResponse.from_orm(hotel) for hotel in query]

    def get_hotel_details(self, hotel_id: str) -> Optional[HotelDetailResponse]:
        """
        Get detailed hotel information including reviews and prices.
        """
        hotel = self.db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            return None

        # Convert to response with related data
        response = HotelDetailResponse.from_orm(hotel)
        return response

    def _apply_user_preferences(self, query, user_id: str):
        """Apply user preferences to the hotel search query"""
        preference = (
            self.db.query(UserHotelPreference)
            .filter(UserHotelPreference.user_id == user_id)
            .first()
        )

        if not preference:
            return query

        # Apply budget filters
        if preference.min_budget:
            query = query.filter(Hotel.avg_price >= preference.min_budget)
        if preference.max_budget:
            query = query.filter(Hotel.avg_price <= preference.max_budget)

        # Apply category filters
        if preference.preferred_categories:
            query = query.filter(
                Hotel.category.in_(preference.preferred_categories)
            )

        # Apply star rating filter
        if preference.min_star_rating:
            query = query.filter(Hotel.star_rating >= preference.min_star_rating)

        # Apply chain preferences
        if preference.preferred_chains:
            query = query.filter(
                Hotel.chain_name.in_(preference.preferred_chains)
            )

        # Apply amenity preferences
        if preference.preferred_amenities:
            for amenity in preference.preferred_amenities:
                query = query.filter(
                    Hotel.amenities.astext.contains(amenity)
                )

        return query

    def get_price_trends(
        self,
        hotel_id: str,
        days_back: int = 30,
    ) -> dict:
        """
        Get price trends for a hotel.
        
        Returns:
        {
            "current_price": Decimal,
            "min_price_7days": Decimal,
            "max_price_7days": Decimal,
            "avg_price_7days": Decimal,
            "trend": "increasing" | "decreasing" | "stable",
        }
        """
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days_back)

        prices = (
            self.db.query(HotelPrice)
            .filter(
                and_(
                    HotelPrice.hotel_id == hotel_id,
                    HotelPrice.quote_date >= cutoff_date,
                )
            )
            .all()
        )

        if not prices:
            return {"current_price": None, "trend": "no_data"}

        rates = [p.nightly_rate for p in prices]
        current_price = rates[-1] if rates else None

        # Get 7-day window for comparison
        prices_7days = [
            p for p in prices
            if p.quote_date >= datetime.utcnow() - timedelta(days=7)
        ]

        if prices_7days:
            rates_7days = [p.nightly_rate for p in prices_7days]
            min_7days = min(rates_7days)
            max_7days = max(rates_7days)
            avg_7days = sum(rates_7days) / len(rates_7days)
        else:
            min_7days = max_7days = avg_7days = current_price

        # Calculate trend
        if len(rates) >= 2:
            old_avg = sum(rates[:-7]) / max(len(rates) - 7, 1)
            new_avg = sum(rates[-7:]) / min(7, len(rates))
            
            if new_avg > old_avg * 1.05:
                trend = "increasing"
            elif new_avg < old_avg * 0.95:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "no_data"

        return {
            "current_price": current_price,
            "min_price_7days": min_7days,
            "max_price_7days": max_7days,
            "avg_price_7days": avg_7days,
            "trend": trend,
        }

    def get_price_prediction(
        self,
        hotel_id: str,
        check_in_date: datetime,
        check_out_date: datetime,
    ) -> dict:
        """
        Get price prediction and booking recommendation.
        
        Based on:
        - Historical price data
        - Current trend
        - Seasonal patterns
        """
        trends = self.get_price_trends(hotel_id)

        recommendation = "book_now"
        if trends["trend"] == "decreasing":
            recommendation = "wait"
        elif trends["trend"] == "increasing":
            recommendation = "book_now"

        return {
            "estimated_price": trends.get("current_price"),
            "price_trend": trends["trend"],
            "recommendation": recommendation,
            "booking_links": self._get_booking_links(hotel_id),
        }

    def _get_booking_links(self, hotel_id: str) -> dict:
        """
        Get booking links for affiliate partners.
        
        Returns links to external booking sites (no direct booking).
        """
        hotel = self.db.query(Hotel).filter(Hotel.id == hotel_id).first()
        if not hotel:
            return {}

        links = {}

        # Use partner booking URLs if available
        if hotel.booking_url:
            links["booking_url"] = hotel.booking_url

        # Add affiliate partner links (MMT-style for Indian users, etc.)
        if hotel.sources:
            # Extract booking IDs from sources
            if "booking" in hotel.sources:
                links["booking.com"] = (
                    f"https://www.booking.com/hotel/{hotel.sources['booking']}.html"
                )
            if "google" in hotel.sources:
                links["google_hotels"] = (
                    f"https://www.google.com/travel/hotels/{hotel.sources['google']}"
                )

        # Generic fallback (search hotel name)
        if not links:
            links["search"] = f"https://www.booking.com/searchresults.html?ss={hotel.name}+{hotel.city}"

        return links


class HotelRecommendationService:
    """Service for personalized hotel recommendations"""

    def __init__(self, db: Session):
        self.db = db

    def get_personalized_recommendations(
        self,
        user_id: str,
        city: str,
        country: str,
        limit: int = 10,
    ) -> List[HotelSearchResponse]:
        """
        Get recommendations based on user preferences and profile.
        
        Algorithm:
        1. Get user preferences
        2. Search hotels matching preferences
        3. Rank by compatibility score
        """
        preference = (
            self.db.query(UserHotelPreference)
            .filter(UserHotelPreference.user_id == user_id)
            .first()
        )

        # Build search request based on preferences
        if preference:
            max_price = preference.max_budget or Decimal("99999")
            min_rating = Decimal("3.0")
            categories = preference.preferred_categories or []
        else:
            max_price = Decimal("99999")
            min_rating = Decimal("3.0")
            categories = []

        query = self.db.query(Hotel).filter(
            and_(
                func.lower(Hotel.city) == func.lower(city),
                func.lower(Hotel.country) == func.lower(country),
                Hotel.is_active == True,
                Hotel.overall_rating >= min_rating,
                Hotel.avg_price <= max_price,
            )
        )

        if categories:
            query = query.filter(Hotel.category.in_(categories))

        # Order by rating and featured status
        hotels = (
            query.order_by(
                Hotel.is_featured.desc(),
                Hotel.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [HotelSearchResponse.from_orm(hotel) for hotel in hotels]
