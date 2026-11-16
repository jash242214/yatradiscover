"""Initial migration: Add hotel discovery tables

Revision ID: 001_initial_hotel_tables
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '001_initial_hotel_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    
    # Create hotels table
    op.create_table(
        'hotels',
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
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('star_rating', sa.Numeric(precision=2, scale=1), nullable=True),
        sa.Column('chain_name', sa.String(255), nullable=True),
        sa.Column('lowest_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('avg_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('overall_rating', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('review_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('rating_breakdown', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('amenities', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('total_rooms', sa.Integer(), nullable=True),
        sa.Column('room_types', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('check_in_time', sa.String(10), server_default='15:00', nullable=False),
        sa.Column('check_out_time', sa.String(10), server_default='11:00', nullable=False),
        sa.Column('sources', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('booking_url', sa.String(500), nullable=True),
        sa.Column('partner_id', sa.String(100), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_featured', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('last_updated', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
        sa.Index('idx_hotel_active_featured', 'is_active', 'is_featured'),
        sa.Index('idx_hotel_category', 'category'),
        sa.Index('idx_hotel_city_country', 'city', 'country'),
        sa.Index('idx_hotel_location', 'location', postgresql_using='gist'),
        sa.Index('idx_hotel_price', 'avg_price'),
        sa.Index('idx_hotel_rating', 'overall_rating'),
    )
    op.create_index('idx_hotel_chain', 'hotels', ['chain_name'])
    op.create_index('idx_hotel_partner', 'hotels', ['partner_id'])

    # Create hotel_reviews table
    op.create_table(
        'hotel_reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('hotel_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('rating', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('reviewer_name', sa.String(255), nullable=False),
        sa.Column('reviewer_id', sa.String(100), nullable=True),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('source_id', sa.String(500), nullable=True),
        sa.Column('review_date', sa.DateTime(), nullable=True),
        sa.Column('helpful_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('verified_purchase', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('aspects', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ondelete='CASCADE'),
        sa.Index('idx_review_hotel', 'hotel_id'),
        sa.Index('idx_review_rating', 'rating'),
        sa.Index('idx_review_source', 'source'),
    )

    # Create hotel_prices table
    op.create_table(
        'hotel_prices',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('hotel_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nightly_rate', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('check_in_date', sa.DateTime(), nullable=False),
        sa.Column('check_out_date', sa.DateTime(), nullable=False),
        sa.Column('quote_date', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('room_type', sa.String(100), nullable=True),
        sa.Column('occupancy', sa.String(100), nullable=True),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('booking_url', sa.String(500), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ondelete='CASCADE'),
        sa.Index('idx_price_dates', 'check_in_date', 'check_out_date'),
        sa.Index('idx_price_hotel', 'hotel_id'),
        sa.Index('idx_price_source', 'source'),
    )

    # Create hotel_amenities table
    op.create_table(
        'hotel_amenities',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('hotel_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(50), nullable=True),
        sa.Column('available', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('free', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ondelete='CASCADE'),
        sa.Index('idx_amenity_category', 'category'),
        sa.Index('idx_amenity_hotel', 'hotel_id'),
        sa.Index('idx_amenity_name', 'name'),
    )

    # Create user_hotel_preferences table
    op.create_table(
        'user_hotel_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('min_budget', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('max_budget', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('currency', sa.String(3), server_default='USD', nullable=False),
        sa.Column('preferred_categories', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('min_star_rating', sa.Numeric(precision=2, scale=1), nullable=True),
        sa.Column('preferred_amenities', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('preferred_chains', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('max_distance_km', sa.Integer(), server_default='5', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id'),
        sa.Index('idx_hotel_pref_user', 'user_id'),
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('user_hotel_preferences')
    op.drop_table('hotel_amenities')
    op.drop_table('hotel_prices')
    op.drop_table('hotel_reviews')
    op.drop_table('hotels')
