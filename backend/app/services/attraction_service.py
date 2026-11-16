"""Attraction discovery service with search, filtering, and recommendations"""
from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, time
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from geoalchemy2.functions import ST_DWithin, ST_Distance
from geoalchemy2.elements import WKTElement

from app.db.models import (
    Attraction,
    AttractionReview,
    VisitorTip,
    UserAttractionPreference,
)
from app.schemas.attraction import (
    AttractionSearchRequest,
    AttractionSearchResponse,
    AttractionDetailResponse,
)


class AttractionSearchService:
    """Service for attraction discovery and search"""

    def __init__(self, db: Session):
        self.db = db

    def search_attractions(
        self,
        request: AttractionSearchRequest,
        user_id: Optional[str] = None,
    ) -> Tuple[List[AttractionSearchResponse], int]:
        """
        Search attractions with advanced filtering and sorting.
        
        Args:
            request: Attraction search parameters
            user_id: Optional user ID to apply user preferences
            
        Returns:
            Tuple of (results, total_count)
        """
        query = self.db.query(Attraction).filter(Attraction.is_active == True)

        # Location-based search
        if request.latitude is not None and request.longitude is not None:
            point = WKTElement(f'POINT({request.longitude} {request.latitude})', srid=4326)
            distance_meters = request.distance_km * 1000
            
            query = query.filter(
                ST_DWithin(Attraction.location, point, distance_meters)
            )
            query = query.add_columns(
                ST_Distance(Attraction.location, point).label('distance')
            )
        elif request.city:
            query = query.filter(
                and_(
                    func.lower(Attraction.city) == func.lower(request.city),
                    func.lower(Attraction.country) == func.lower(request.country or "")
                )
            )

        # Category filtering
        if request.categories:
            query = query.filter(Attraction.category.in_(request.categories))

        # Subcategory filtering
        if request.subcategories:
            for subcategory in request.subcategories:
                query = query.filter(
                    Attraction.subcategories.astext.contains(subcategory)
                )

        # Attraction type filtering
        if request.attraction_type:
            query = query.filter(
                Attraction.attraction_type == request.attraction_type
            )

        # Rating filtering
        if request.min_rating is not None:
            query = query.filter(Attraction.overall_rating >= request.min_rating)

        # Entry fee filtering
        if request.max_entry_fee is not None:
            query = query.filter(
                or_(
                    Attraction.entry_fee <= request.max_entry_fee,
                    Attraction.has_entry_fee == False,
                )
            )

        # Visit duration filtering
        if request.max_visit_duration_hours is not None:
            max_minutes = request.max_visit_duration_hours * 60
            query = query.filter(
                or_(
                    Attraction.typical_visit_duration_minutes <= max_minutes,
                    Attraction.typical_visit_duration_minutes.is_(None),
                )
            )

        # Parking filtering
        if request.has_parking is not None:
            query = query.filter(Attraction.parking_available == request.has_parking)

        # Accessibility filtering
        if request.wheelchair_accessible is not None:
            query = query.filter(
                Attraction.wheelchair_accessible == request.wheelchair_accessible
            )

        # Open now filter
        if request.open_now:
            query = query.filter(
                self._get_open_now_condition()
            )

        # Apply user preferences
        if user_id:
            query = self._apply_user_preferences(query, user_id)

        # Sorting
        if request.sort_by == "rating":
            sort_col = (
                Attraction.overall_rating.desc() if request.sort_order == "desc"
                else Attraction.overall_rating.asc()
            )
        elif request.sort_by == "popularity":
            sort_col = (
                Attraction.popularity_rank.asc() if request.sort_order == "asc"
                else Attraction.popularity_rank.desc()
            )
        elif request.sort_by == "distance" and request.latitude is not None:
            sort_col = "distance asc"
        elif request.sort_by == "trending":
            sort_col = (
                Attraction.is_trending.desc() if request.sort_order == "desc"
                else Attraction.is_trending.asc()
            )
        else:
            sort_col = Attraction.overall_rating.desc()

        query = query.order_by(sort_col)

        # Get total count
        total_count = query.count() if not request.latitude else len(query.all())

        # Pagination
        results = query.offset(request.offset).limit(request.limit).all()

        # Convert to response objects
        attraction_responses = []
        for row in results:
            if isinstance(row, tuple):
                attraction = row[0]
            else:
                attraction = row
            
            response = AttractionSearchResponse.from_orm(attraction)
            attraction_responses.append(response)

        return attraction_responses, total_count

    def get_popular_attractions(
        self,
        city: str,
        country: str,
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get most popular attractions by visitor count and ranking.
        """
        query = (
            self.db.query(Attraction)
            .filter(
                and_(
                    func.lower(Attraction.city) == func.lower(city),
                    func.lower(Attraction.country) == func.lower(country),
                    Attraction.is_active == True,
                    Attraction.popularity_rank.isnot(None),
                )
            )
            .order_by(Attraction.popularity_rank.asc())
            .limit(limit)
            .all()
        )

        return [AttractionSearchResponse.from_orm(a) for a in query]

    def get_budget_friendly_attractions(
        self,
        city: str,
        country: str,
        max_entry_fee: Optional[Decimal] = None,
        min_rating: Decimal = Decimal("3.5"),
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get budget-friendly attractions with no or low entry fees.
        
        Strategy:
        - Prioritize free attractions
        - Then filter by max entry fee
        - Sort by rating
        """
        query = self.db.query(Attraction).filter(
            and_(
                func.lower(Attraction.city) == func.lower(city),
                func.lower(Attraction.country) == func.lower(country),
                Attraction.is_active == True,
                Attraction.overall_rating >= min_rating,
            )
        )

        # First get free attractions
        free_attractions = query.filter(
            Attraction.has_entry_fee == False
        ).order_by(Attraction.overall_rating.desc()).limit(limit).all()

        if len(free_attractions) >= limit:
            return [AttractionSearchResponse.from_orm(a) for a in free_attractions]

        # Then add low-cost attractions
        if max_entry_fee:
            paid_attractions = query.filter(
                and_(
                    Attraction.has_entry_fee == True,
                    Attraction.entry_fee <= max_entry_fee,
                )
            ).order_by(Attraction.overall_rating.desc()).all()
        else:
            paid_attractions = query.filter(
                Attraction.has_entry_fee == True
            ).order_by(Attraction.overall_rating.desc()).all()

        combined = free_attractions + paid_attractions[:limit - len(free_attractions)]
        return [AttractionSearchResponse.from_orm(a) for a in combined]

    def get_indoor_attractions(
        self,
        city: str,
        country: str,
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get indoor attractions (museums, galleries, etc.).
        """
        query = (
            self.db.query(Attraction)
            .filter(
                and_(
                    func.lower(Attraction.city) == func.lower(city),
                    func.lower(Attraction.country) == func.lower(country),
                    Attraction.is_active == True,
                    Attraction.attraction_type == "indoor",
                )
            )
            .order_by(
                Attraction.is_featured.desc(),
                Attraction.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [AttractionSearchResponse.from_orm(a) for a in query]

    def get_outdoor_attractions(
        self,
        city: str,
        country: str,
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get outdoor attractions (parks, monuments, etc.).
        """
        query = (
            self.db.query(Attraction)
            .filter(
                and_(
                    func.lower(Attraction.city) == func.lower(city),
                    func.lower(Attraction.country) == func.lower(country),
                    Attraction.is_active == True,
                    Attraction.attraction_type == "outdoor",
                )
            )
            .order_by(
                Attraction.is_featured.desc(),
                Attraction.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [AttractionSearchResponse.from_orm(a) for a in query]

    def get_quick_visit_attractions(
        self,
        city: str,
        country: str,
        max_duration_hours: int = 2,
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get attractions that can be visited quickly.
        
        Perfect for travelers with limited time.
        """
        max_minutes = max_duration_hours * 60

        query = (
            self.db.query(Attraction)
            .filter(
                and_(
                    func.lower(Attraction.city) == func.lower(city),
                    func.lower(Attraction.country) == func.lower(country),
                    Attraction.is_active == True,
                    or_(
                        Attraction.typical_visit_duration_minutes <= max_minutes,
                        Attraction.typical_visit_duration_minutes.is_(None),
                    ),
                )
            )
            .order_by(Attraction.overall_rating.desc())
            .limit(limit)
            .all()
        )

        return [AttractionSearchResponse.from_orm(a) for a in query]

    def get_trending_attractions(
        self,
        city: str,
        country: str,
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get trending attractions with recent reviews.
        """
        query = (
            self.db.query(Attraction)
            .filter(
                and_(
                    func.lower(Attraction.city) == func.lower(city),
                    func.lower(Attraction.country) == func.lower(country),
                    Attraction.is_active == True,
                    Attraction.is_trending == True,
                )
            )
            .order_by(
                Attraction.updated_at.desc(),
                Attraction.review_count.desc(),
            )
            .limit(limit)
            .all()
        )

        return [AttractionSearchResponse.from_orm(a) for a in query]

    def get_hidden_gems(
        self,
        city: str,
        country: str,
        min_rating: Decimal = Decimal("4.0"),
        max_visitors_rank: int = 20,
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get hidden gems - highly rated but less visited attractions.
        
        Strategy:
        - Filter by high rating (>= 4.0)
        - Filter by lower popularity rank (higher rank = less visited)
        - Sort by rating descending
        """
        query = (
            self.db.query(Attraction)
            .filter(
                and_(
                    func.lower(Attraction.city) == func.lower(city),
                    func.lower(Attraction.country) == func.lower(country),
                    Attraction.is_active == True,
                    Attraction.overall_rating >= min_rating,
                    or_(
                        Attraction.popularity_rank.is_(None),
                        Attraction.popularity_rank > max_visitors_rank,
                    ),
                )
            )
            .order_by(Attraction.overall_rating.desc())
            .limit(limit)
            .all()
        )

        return [AttractionSearchResponse.from_orm(a) for a in query]

    def get_attraction_details(self, attraction_id: str) -> Optional[AttractionDetailResponse]:
        """
        Get detailed attraction information including reviews and tips.
        """
        attraction = (
            self.db.query(Attraction)
            .filter(Attraction.id == attraction_id)
            .first()
        )
        if not attraction:
            return None

        response = AttractionDetailResponse.from_orm(attraction)
        return response

    def get_visitor_tips(self, attraction_id: str, tip_type: Optional[str] = None) -> List[dict]:
        """
        Get visitor tips for an attraction.
        """
        query = self.db.query(VisitorTip).filter(
            VisitorTip.attraction_id == attraction_id
        )

        if tip_type:
            query = query.filter(VisitorTip.tip_type == tip_type)

        tips = query.order_by(
            VisitorTip.helpful_count.desc(),
            VisitorTip.rating.desc(),
        ).all()

        return [
            {
                "id": str(tip.id),
                "title": tip.title,
                "content": tip.content,
                "tip_type": tip.tip_type,
                "is_official": tip.is_official,
                "author_name": tip.author_name,
                "helpful_count": tip.helpful_count,
                "rating": tip.rating,
            }
            for tip in tips
        ]

    def _get_open_now_condition(self):
        """
        Get SQLAlchemy condition for attractions open now.
        """
        current_time = datetime.utcnow().time()
        current_day = datetime.utcnow().strftime("%A").lower()

        # This is a simplified check - real implementation would need
        # more robust handling of opening hours JSON
        return and_(
            Attraction.opening_hours.isnot(None),
            ~Attraction.closed_on.astext.contains(current_day),
        )

    def _apply_user_preferences(self, query, user_id: str):
        """Apply user preferences to attraction search"""
        preference = (
            self.db.query(UserAttractionPreference)
            .filter(UserAttractionPreference.user_id == user_id)
            .first()
        )

        if not preference:
            return query

        # Apply category preferences
        if preference.preferred_categories:
            query = query.filter(
                Attraction.category.in_(preference.preferred_categories)
            )

        # Exclude disliked categories
        if preference.disliked_categories:
            query = query.filter(
                ~Attraction.category.in_(preference.disliked_categories)
            )

        # Apply activity type preference
        if preference.preferred_activity_type:
            query = query.filter(
                Attraction.attraction_type == preference.preferred_activity_type
            )

        # Apply accessibility requirements
        if preference.wheelchair_required:
            query = query.filter(Attraction.wheelchair_accessible == True)

        if preference.parking_required:
            query = query.filter(Attraction.parking_available == True)

        # Apply ticket price limit
        if preference.max_ticket_price is not None:
            query = query.filter(
                or_(
                    Attraction.has_entry_fee == False,
                    Attraction.entry_fee <= preference.max_ticket_price,
                )
            )

        return query


class AttractionRecommendationService:
    """Service for personalized attraction recommendations"""

    def __init__(self, db: Session):
        self.db = db

    def get_personalized_recommendations(
        self,
        user_id: str,
        city: str,
        country: str,
        trip_duration_hours: int = 24,
        limit: int = 10,
    ) -> List[AttractionSearchResponse]:
        """
        Get recommendations based on user profile and trip duration.
        
        Algorithm:
        - Get user preferences
        - Match attractions to preferences
        - Filter by visit duration available
        - Rank by rating and compatibility
        """
        preference = (
            self.db.query(UserAttractionPreference)
            .filter(UserAttractionPreference.user_id == user_id)
            .first()
        )

        query = self.db.query(Attraction).filter(
            and_(
                func.lower(Attraction.city) == func.lower(city),
                func.lower(Attraction.country) == func.lower(country),
                Attraction.is_active == True,
            )
        )

        # Apply preferences
        if preference:
            if preference.preferred_categories:
                query = query.filter(
                    Attraction.category.in_(preference.preferred_categories)
                )

            if preference.wheelchair_required:
                query = query.filter(Attraction.wheelchair_accessible == True)

            if preference.parking_required:
                query = query.filter(Attraction.parking_available == True)

            if preference.max_ticket_price is not None:
                query = query.filter(
                    or_(
                        Attraction.has_entry_fee == False,
                        Attraction.entry_fee <= preference.max_ticket_price,
                    )
                )

        # Filter by trip duration if specified
        if trip_duration_hours > 0:
            max_minutes = trip_duration_hours * 60
            query = query.filter(
                or_(
                    Attraction.typical_visit_duration_minutes <= max_minutes,
                    Attraction.typical_visit_duration_minutes.is_(None),
                )
            )

        # Order by rating and featured status
        attractions = (
            query.order_by(
                Attraction.is_featured.desc(),
                Attraction.overall_rating.desc(),
            )
            .limit(limit)
            .all()
        )

        return [AttractionSearchResponse.from_orm(a) for a in attractions]
