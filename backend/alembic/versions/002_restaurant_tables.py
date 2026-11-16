"""Add restaurant discovery tables

Revision ID: 002_restaurant_tables
Revises: 001_initial_hotel_tables
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '002_restaurant_tables'
down_revision = '001_initial_hotel_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create restaurants table
    op.create_table(
        'restaurants',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('address', sa.String(500), nullable=False),
        sa.Column('city', sa.String(100), nullable=False),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('country', sa.String(100), nullable=False),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('primary_cuisine', sa.String(100), nullable=False),
        sa.Column('cuisines', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('price_level', sa.String(50), nullable=False),
        sa.Column('avg_cost_per_person', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('overall_rating', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('review_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('rating_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('michelin_stars', sa.Integer(), server_default='0', nullable=False),
        sa.Column('has_michelin_green', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('awards', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('dining_style', sa.String(50), nullable=True),
        sa.Column('menu_type', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('atmosphere', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('accepts_reservations', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('reservation_url', sa.String(500), nullable=True),
        sa.Column('opening_hours', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('closed_on', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('dietary_options', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('parking_available', sa.Boolean(), nullable=True),
        sa.Column('wheelchair_accessible', sa.Boolean(), nullable=True),
        sa.Column('sources', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('booking_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_featured', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_trending', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('last_updated', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
        sa.Index('idx_restaurant_active_featured', 'is_active', 'is_featured'),
        sa.Index('idx_restaurant_city_country', 'city', 'country'),
        sa.Index('idx_restaurant_cuisine', 'primary_cuisine'),
        sa.Index('idx_restaurant_location', 'location', postgresql_using='gist'),
        sa.Index('idx_restaurant_michelin', 'michelin_stars'),
        sa.Index('idx_restaurant_price_level', 'price_level'),
        sa.Index('idx_restaurant_rating', 'overall_rating'),
        sa.Index('idx_restaurant_trending', 'is_trending'),
    )

    # Create restaurant_reviews table
    op.create_table(
        'restaurant_reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('restaurant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('rating', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('reviewer_name', sa.String(255), nullable=False),
        sa.Column('reviewer_id', sa.String(100), nullable=True),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('source_id', sa.String(500), nullable=True),
        sa.Column('review_date', sa.DateTime(), nullable=True),
        sa.Column('aspects', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('helpful_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('verified_visit', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
        sa.Index('idx_rest_review_rating', 'rating'),
        sa.Index('idx_rest_review_restaurant', 'restaurant_id'),
        sa.Index('idx_rest_review_source', 'source'),
    )

    # Create signature_dishes table
    op.create_table(
        'signature_dishes',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('restaurant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cuisine', sa.String(100), nullable=True),
        sa.Column('ingredients', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('dietary_info', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('price', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('popularity_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('reviewer_mentions', sa.Integer(), server_default='0', nullable=False),
        sa.Column('photo_url', sa.String(500), nullable=True),
        sa.Column('availability', sa.String(50), nullable=True),
        sa.Column('is_seasonal', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
        sa.Index('idx_dish_name', 'name'),
        sa.Index('idx_dish_restaurant', 'restaurant_id'),
    )

    # Create restaurant_photos table
    op.create_table(
        'restaurant_photos',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('restaurant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('photo_type', sa.String(50), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('uploaded_by', sa.String(255), nullable=True),
        sa.Column('is_verified', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('helpful_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
        sa.Index('idx_photo_restaurant', 'restaurant_id'),
        sa.Index('idx_photo_type', 'photo_type'),
    )

    # Create user_restaurant_preferences table
    op.create_table(
        'user_restaurant_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('preferred_price_levels', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('max_cost_per_person', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('preferred_cuisines', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('disliked_cuisines', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('dietary_options', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('preferred_dining_style', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('atmosphere_preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('prefer_michelin_restaurants', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('max_distance_km', sa.Integer(), server_default='5', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id'),
        sa.Index('idx_rest_pref_user', 'user_id'),
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('user_restaurant_preferences')
    op.drop_table('restaurant_photos')
    op.drop_table('signature_dishes')
    op.drop_table('restaurant_reviews')
    op.drop_table('restaurants')
