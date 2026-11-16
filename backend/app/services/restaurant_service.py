"""Restaurant discovery service with search, filtering, and recommendations"""
from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from geoalchemy2.functions import ST_DWithin, ST_Distance
from geoalchemy2.elements import WKTElement

from app.db.models import (
    Restaurant,
    RestaurantReview,
    SignatureDish,
    UserRestaurantPreference,
)
from app.schemas.restaurant import (
    RestaurantSearchRequest,
    RestaurantSearchResponse,
    RestaurantDetailResponse,
)


class RestaurantSearchService:
    """Service for restaurant discovery and search"""

    def __init__(self, db: Session):
        self.db = db

    def search_restaurants(
        self,
        request: RestaurantSearchRequest,
        user_id: Optional[str] = None,
    ) -> Tuple[List[RestaurantSearchResponse], int]:
        """
        Search restaurants with advanced filtering and sorting.
        
        Args:
            request: Restaurant search parameters
            user_id: Optional user ID to apply user preferences
            
        Returns:
            Tuple of (results, total_count)
        """
        query = self.db.query(Restaurant).filter(Restaurant.is_active == True)

        # Location-based search
        if request.latitude is not None and request.longitude is not None:
            point = WKTElement(f'POINT({request.longitude} {request.latitude})', srid=4326)
            distance_meters = request.distance_km * 1000
            
            query = query.filter(
                ST_DWithin(Restaurant.location, point, distance_meters)
            )
            query = query.add_columns(
                ST_Distance(Restaurant.location, point).label('distance')
            )
        elif request.city:
            query = query.filter(
                and_(
                    func.lower(Restaurant.city) == func.lower(request.city),
                    func.lower(Restaurant.country) == func.lower(request.country or "")
                )
            )

        # Cuisine filtering
        if request.cuisines:
            # Filter by any matching cuisine
            cuisine_filters = [
                Restaurant.primary_cuisine.in_(request.cuisines),
                Restaurant.cuisines.astext.contains(c) for c in request.cuisines
            ]
            query = query.filter(or_(*cuisine_filters))

        # Price level filtering
        if request.price_levels:
            query = query.filter(Restaurant.price_level.in_(request.price_levels))

        # Rating filtering
        if request.min_rating is not None:
            query = query.filter(Restaurant.overall_rating >= request.min_rating)

        # Michelin filtering
        if request.michelin_only:
            query = query.filter(Restaurant.michelin_stars > 0)

        # Dietary options filtering
        if request.dietary_options:
            for dietary in request.dietary_options:
                query = query.filter(
                    Restaurant.dietary_options.astext.contains(dietary)
                )

        # Dining style filtering
        if request.dining_style:
            query = query.filter(
                Restaurant.dining_style.ilike(f"%{request.dining_style}%")
            )

        # Reservation filter
        if request.accepts_reservations is not None:
            query = query.filter(
                Restaurant.accepts_reservations == request.accepts_reservations
            )

        # Apply user preferences if provided
        if user_id:
            query = self._apply_user_preferences(query, user_id)

        # Sorting
        if request.sort_by == "rating":
            sort_col = Restaurant.overall_rating.desc() if request.sort_order == "desc" else Restaurant.overall_rating.asc()
        elif request.sort_by == "michelin_stars":
            sort_col = Restaurant.michelin_stars.desc() if request.sort_order == "desc" else Restaurant.michelin_stars.asc()
        elif request.sort_by == "distance" and request.latitude is not None:
            sort_col = "distance asc"
        elif request.sort_by == "trending":
            sort_col = (
                Restaurant.is_trending.desc()
                if request.sort_order == "desc"
                else Restaurant.is_trending.asc()
            )
        else:
            sort_col = Restaurant.overall_rating.desc()

        query = query.order_by(sort_col)

        # Get total count
        total_count = query.count() if not request.latitude else len(query.all())

        # Pagination
        results = query.offset(request.offset).limit(request.limit).all()

        # Convert to response objects
        restaurant_responses = []
        for row in results:
            if isinstance(row, tuple):
                restaurant = row[0]
            else:
                restaurant = row
            
            response = RestaurantSearchResponse.from_orm(restaurant)
            restaurant_responses.append(response)

        return restaurant_responses, total_count

    def get_michelin_restaurants(
        self,
        city: str,
        country: str,
        min_stars: int = 1,
        limit: int = 10,
    ) -> List[RestaurantSearchResponse]:
        """
        Get Michelin-starred restaurants.
        
        Strategy:
        - Filter by Michelin stars >= min_stars
        - Sort by stars descending, then by rating
        """
        query = (
            self.db.query(Restaurant)
            .filter(
                and_(
                    func.lower(Restaurant.city) == func.lower(city),
                    func.lower(Restaurant.country) == func.lower(country),
                    Restaurant.is_active == True,
                    Restaurant.michelin_stars >= min_stars,
                )
            )
            .order_by(
                Restaurant.michelin_stars.desc(),
                Restaurant.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [RestaurantSearchResponse.from_orm(r) for r in query]

    def get_budget_friendly_restaurants(
        self,
        city: str,
        country: str,
        price_levels: Optional[List[str]] = None,
        min_rating: Decimal = Decimal("3.5"),
        limit: int = 10,
    ) -> List[RestaurantSearchResponse]:
        """
        Get budget-friendly restaurants with good ratings.
        
        Strategy:
        - Filter by price levels (default: $ and $$)
        - Filter by minimum rating for quality
        - Sort by rating descending
        """
        if not price_levels:
            price_levels = ["$", "$$"]

        query = (
            self.db.query(Restaurant)
            .filter(
                and_(
                    func.lower(Restaurant.city) == func.lower(city),
                    func.lower(Restaurant.country) == func.lower(country),
                    Restaurant.is_active == True,
                    Restaurant.price_level.in_(price_levels),
                    Restaurant.overall_rating >= min_rating,
                )
            )
            .order_by(Restaurant.overall_rating.desc())
            .limit(limit)
            .all()
        )

        return [RestaurantSearchResponse.from_orm(r) for r in query]

    def get_fine_dining_restaurants(
        self,
        city: str,
        country: str,
        price_levels: Optional[List[str]] = None,
        limit: int = 5,
    ) -> List[RestaurantSearchResponse]:
        """
        Get fine dining restaurants.
        
        Strategy:
        - Filter by price level ($$$, $$$$)
        - Filter by dining style
        - Sort by Michelin stars, then rating
        """
        if not price_levels:
            price_levels = ["$$$", "$$$$"]

        query = (
            self.db.query(Restaurant)
            .filter(
                and_(
                    func.lower(Restaurant.city) == func.lower(city),
                    func.lower(Restaurant.country) == func.lower(country),
                    Restaurant.is_active == True,
                    Restaurant.price_level.in_(price_levels),
                )
            )
            .order_by(
                Restaurant.michelin_stars.desc(),
                Restaurant.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [RestaurantSearchResponse.from_orm(r) for r in query]

    def get_trending_restaurants(
        self,
        city: str,
        country: str,
        limit: int = 10,
    ) -> List[RestaurantSearchResponse]:
        """
        Get trending/featured restaurants with recent reviews.
        """
        query = (
            self.db.query(Restaurant)
            .filter(
                and_(
                    func.lower(Restaurant.city) == func.lower(city),
                    func.lower(Restaurant.country) == func.lower(country),
                    Restaurant.is_active == True,
                    Restaurant.is_trending == True,
                )
            )
            .order_by(
                Restaurant.updated_at.desc(),
                Restaurant.review_count.desc(),
            )
            .limit(limit)
            .all()
        )

        return [RestaurantSearchResponse.from_orm(r) for r in query]

    def get_best_value_restaurants(
        self,
        city: str,
        country: str,
        limit: int = 10,
        min_rating: Decimal = Decimal("3.5"),
    ) -> List[RestaurantSearchResponse]:
        """
        Get best value restaurants ranked by rating/price ratio.
        
        Strategy:
        - Filter by minimum rating
        - Calculate value score: rating / price_level_numeric
        - Rank by value score
        """
        # Price level mapping to numeric for value calculation
        price_level_scores = {"$": 1, "$$": 2, "$$$": 3, "$$$$": 4}

        query = (
            self.db.query(Restaurant)
            .filter(
                and_(
                    func.lower(Restaurant.city) == func.lower(city),
                    func.lower(Restaurant.country) == func.lower(country),
                    Restaurant.is_active == True,
                    Restaurant.overall_rating >= min_rating,
                )
            )
            .all()
        )

        # Calculate value scores
        restaurants_with_score = []
        for restaurant in query:
            price_score = price_level_scores.get(restaurant.price_level, 2)
            rating = float(restaurant.overall_rating or 0)
            value_score = rating / price_score if price_score > 0 else 0
            
            restaurants_with_score.append((restaurant, value_score))

        # Sort by value score descending
        restaurants_with_score.sort(key=lambda x: x[1], reverse=True)

        return [
            RestaurantSearchResponse.from_orm(r)
            for r, _ in restaurants_with_score[:limit]
        ]

    def get_restaurant_details(self, restaurant_id: str) -> Optional[RestaurantDetailResponse]:
        """
        Get detailed restaurant information including reviews and signature dishes.
        """
        restaurant = (
            self.db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id)
            .first()
        )
        if not restaurant:
            return None

        response = RestaurantDetailResponse.from_orm(restaurant)
        return response

    def get_signature_dishes(self, restaurant_id: str) -> List[dict]:
        """
        Get signature dishes for a restaurant ordered by popularity.
        """
        dishes = (
            self.db.query(SignatureDish)
            .filter(SignatureDish.restaurant_id == restaurant_id)
            .order_by(
                SignatureDish.popularity_score.desc(),
                SignatureDish.reviewer_mentions.desc(),
            )
            .all()
        )

        return [
            {
                "id": str(dish.id),
                "name": dish.name,
                "description": dish.description,
                "cuisine": dish.cuisine,
                "price": dish.price,
                "popularity_score": dish.popularity_score,
                "reviewer_mentions": dish.reviewer_mentions,
                "photo_url": dish.photo_url,
                "availability": dish.availability,
                "is_seasonal": dish.is_seasonal,
            }
            for dish in dishes
        ]

    def _apply_user_preferences(self, query, user_id: str):
        """Apply user preferences to restaurant search"""
        preference = (
            self.db.query(UserRestaurantPreference)
            .filter(UserRestaurantPreference.user_id == user_id)
            .first()
        )

        if not preference:
            return query

        # Apply price level preferences
        if preference.preferred_price_levels:
            query = query.filter(
                Restaurant.price_level.in_(preference.preferred_price_levels)
            )

        # Apply cuisine preferences
        if preference.preferred_cuisines:
            cuisine_filters = [
                Restaurant.primary_cuisine.in_(preference.preferred_cuisines)
            ]
            query = query.filter(or_(*cuisine_filters))

        # Apply dietary preferences
        if preference.dietary_options:
            for dietary in preference.dietary_options:
                query = query.filter(
                    Restaurant.dietary_options.astext.contains(dietary)
                )

        # Apply dining style preferences
        if preference.preferred_dining_style:
            query = query.filter(
                Restaurant.dining_style.in_(preference.preferred_dining_style)
            )

        return query


class RestaurantRecommendationService:
    """Service for personalized restaurant recommendations"""

    def __init__(self, db: Session):
        self.db = db

    def get_personalized_recommendations(
        self,
        user_id: str,
        city: str,
        country: str,
        occasion: Optional[str] = None,
        limit: int = 10,
    ) -> List[RestaurantSearchResponse]:
        """
        Get recommendations based on user profile and occasion.
        
        Occasions:
        - "casual": Budget-friendly, relaxed atmosphere
        - "date": Fine dining, romantic atmosphere
        - "business": Upscale, professional atmosphere
        - "family": Family-friendly, variety options
        """
        preference = (
            self.db.query(UserRestaurantPreference)
            .filter(UserRestaurantPreference.user_id == user_id)
            .first()
        )

        query = self.db.query(Restaurant).filter(
            and_(
                func.lower(Restaurant.city) == func.lower(city),
                func.lower(Restaurant.country) == func.lower(country),
                Restaurant.is_active == True,
            )
        )

        # Apply occasion-based filters
        if occasion == "casual":
            price_levels = ["$", "$$"]
            query = query.filter(Restaurant.price_level.in_(price_levels))
        elif occasion == "date":
            query = query.filter(
                or_(
                    Restaurant.michelin_stars > 0,
                    Restaurant.price_level.in_(["$$$", "$$$$"]),
                )
            )
            if "romantic" in (query.first().atmosphere or []):
                query = query.filter(
                    Restaurant.atmosphere.astext.contains("romantic")
                )
        elif occasion == "business":
            query = query.filter(Restaurant.price_level.in_(["$$", "$$$", "$$$$"]))
        elif occasion == "family":
            query = query.filter(
                Restaurant.atmosphere.astext.contains("family-friendly")
            )

        # Apply user preferences
        if preference:
            if preference.preferred_cuisines:
                cuisine_filters = [
                    Restaurant.primary_cuisine.in_(preference.preferred_cuisines)
                ]
                query = query.filter(or_(*cuisine_filters))

        # Order by rating and featured status
        restaurants = (
            query.order_by(
                Restaurant.is_featured.desc(),
                Restaurant.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [RestaurantSearchResponse.from_orm(r) for r in restaurants]
