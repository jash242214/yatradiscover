"""Add attraction/places discovery tables

Revision ID: 003_attraction_tables
Revises: 002_restaurant_tables
Create Date: 2024-01-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '003_attraction_tables'
down_revision = '002_restaurant_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create attractions table
    op.create_table(
        'attractions',
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
        sa.Column('website', sa.String(500), nullable=True),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('subcategories', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('attraction_type', sa.String(50), nullable=False),
        sa.Column('has_entry_fee', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('entry_fee', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('ticket_url', sa.String(500), nullable=True),
        sa.Column('overall_rating', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('review_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('rating_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('popularity_rank', sa.Integer(), nullable=True),
        sa.Column('typical_visit_duration_minutes', sa.Integer(), nullable=True),
        sa.Column('annual_visitor_count', sa.Integer(), nullable=True),
        sa.Column('crowd_level_current', sa.String(50), nullable=True),
        sa.Column('opening_hours', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('closed_on', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_seasonal', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('seasonal_info', sa.Text(), nullable=True),
        sa.Column('wheelchair_accessible', sa.Boolean(), nullable=True),
        sa.Column('parking_available', sa.Boolean(), nullable=True),
        sa.Column('public_transport_accessible', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('has_guide_service', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('has_gift_shop', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('has_restaurant', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('photography_allowed', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('photography_restrictions', sa.Text(), nullable=True),
        sa.Column('sources', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_featured', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_trending', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('last_updated', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
        sa.Index('idx_attraction_active_featured', 'is_active', 'is_featured'),
        sa.Index('idx_attraction_category', 'category'),
        sa.Index('idx_attraction_city_country', 'city', 'country'),
        sa.Index('idx_attraction_location', 'location', postgresql_using='gist'),
        sa.Index('idx_attraction_rating', 'overall_rating'),
        sa.Index('idx_attraction_trending', 'is_trending'),
        sa.Index('idx_attraction_type', 'attraction_type'),
    )

    # Create attraction_reviews table
    op.create_table(
        'attraction_reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('attraction_id', postgresql.UUID(as_uuid=True), nullable=False),
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
        sa.Column('visit_date', sa.DateTime(), nullable=True),
        sa.Column('visit_type', sa.String(50), nullable=True),
        sa.Column('visit_season', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['attraction_id'], ['attractions.id'], ondelete='CASCADE'),
        sa.Index('idx_attr_review_attraction', 'attraction_id'),
        sa.Index('idx_attr_review_rating', 'rating'),
        sa.Index('idx_attr_review_source', 'source'),
    )

    # Create visitor_tips table
    op.create_table(
        'visitor_tips',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('attraction_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tip_type', sa.String(50), nullable=False),
        sa.Column('is_official', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('author_name', sa.String(255), nullable=True),
        sa.Column('author_id', sa.String(100), nullable=True),
        sa.Column('helpful_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('rating', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['attraction_id'], ['attractions.id'], ondelete='CASCADE'),
        sa.Index('idx_tip_attraction', 'attraction_id'),
        sa.Index('idx_tip_type', 'tip_type'),
    )

    # Create attraction_photos table
    op.create_table(
        'attraction_photos',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('attraction_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('photo_type', sa.String(50), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('uploaded_by', sa.String(255), nullable=True),
        sa.Column('is_verified', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('helpful_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['attraction_id'], ['attractions.id'], ondelete='CASCADE'),
        sa.Index('idx_attr_photo_attraction', 'attraction_id'),
        sa.Index('idx_attr_photo_type', 'photo_type'),
    )

    # Create user_attraction_preferences table
    op.create_table(
        'user_attraction_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('preferred_categories', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('disliked_categories', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('preferred_activity_type', sa.String(50), nullable=True),
        sa.Column('max_visit_duration_hours', sa.Integer(), nullable=True),
        sa.Column('prefer_crowded', sa.Boolean(), nullable=True),
        sa.Column('wheelchair_required', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('parking_required', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('max_ticket_price', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('max_distance_km', sa.Integer(), server_default='10', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id'),
        sa.Index('idx_attr_pref_user', 'user_id'),
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('user_attraction_preferences')
    op.drop_table('attraction_photos')
    op.drop_table('visitor_tips')
    op.drop_table('attraction_reviews')
    op.drop_table('attractions')
