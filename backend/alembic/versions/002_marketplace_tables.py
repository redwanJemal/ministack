"""Marketplace tables: categories, listings, chats, favorites.

Revision ID: 002
Revises: 001
Create Date: 2024-02-06 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to users table
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    op.add_column('users', sa.Column('is_phone_verified', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('users', sa.Column('phone_verified_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(100), server_default='Addis Ababa', nullable=False))
    op.add_column('users', sa.Column('area', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('rating', sa.Float(), server_default='0', nullable=False))
    op.add_column('users', sa.Column('total_ratings', sa.Integer(), server_default='0', nullable=False))
    op.add_column('users', sa.Column('total_sales', sa.Integer(), server_default='0', nullable=False))
    op.add_column('users', sa.Column('total_listings', sa.Integer(), server_default='0', nullable=False))
    op.add_column('users', sa.Column('is_verified_seller', sa.Boolean(), server_default='false', nullable=False))
    op.create_index('ix_users_phone', 'users', ['phone'])

    # Categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name_am', sa.String(100), nullable=False),
        sa.Column('name_en', sa.String(100), nullable=False),
        sa.Column('icon', sa.String(50), server_default='📦', nullable=False),
        sa.Column('slug', sa.String(100), nullable=False),
        sa.Column('sort_order', sa.Integer(), server_default='0', nullable=False),
        sa.Column('parent_id', sa.UUID(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['parent_id'], ['categories.id']),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_categories_slug', 'categories', ['slug'])

    # Listings table
    listing_status = postgresql.ENUM('draft', 'active', 'sold', 'expired', 'deleted', name='listingstatus', create_type=False)
    listing_status.create(op.get_bind(), checkfirst=True)
    
    listing_condition = postgresql.ENUM('new', 'like_new', 'used', 'for_parts', name='listingcondition', create_type=False)
    listing_condition.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'listings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('category_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), server_default='ETB', nullable=False),
        sa.Column('is_negotiable', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('condition', listing_condition, server_default='used', nullable=False),
        sa.Column('images', postgresql.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('city', sa.String(100), server_default='Addis Ababa', nullable=False),
        sa.Column('area', sa.String(100), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('status', listing_status, server_default='active', nullable=False),
        sa.Column('views_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('favorites_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_featured', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('featured_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), server_default='{}', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sold_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
    )
    op.create_index('ix_listings_user_id', 'listings', ['user_id'])
    op.create_index('ix_listings_category_id', 'listings', ['category_id'])
    op.create_index('ix_listings_status', 'listings', ['status'])

    # Chats table
    op.create_table(
        'chats',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('listing_id', sa.UUID(), nullable=False),
        sa.Column('buyer_id', sa.UUID(), nullable=False),
        sa.Column('seller_id', sa.UUID(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_message_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['buyer_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['seller_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_chats_listing_id', 'chats', ['listing_id'])
    op.create_index('ix_chats_buyer_id', 'chats', ['buyer_id'])
    op.create_index('ix_chats_seller_id', 'chats', ['seller_id'])

    # Messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('chat_id', sa.UUID(), nullable=False),
        sa.Column('sender_id', sa.UUID(), nullable=False),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(500), nullable=True),
        sa.Column('is_read', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_messages_chat_id', 'messages', ['chat_id'])

    # Favorites table
    op.create_table(
        'favorites',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('listing_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'listing_id', name='unique_user_listing_favorite'),
    )
    op.create_index('ix_favorites_user_id', 'favorites', ['user_id'])
    op.create_index('ix_favorites_listing_id', 'favorites', ['listing_id'])

    # Seed categories
    op.execute("""
        INSERT INTO categories (id, name_am, name_en, icon, slug, sort_order) VALUES
        ('a1111111-1111-1111-1111-111111111111', 'ኤሌክትሮኒክስ', 'Electronics', '📱', 'electronics', 1),
        ('a2222222-2222-2222-2222-222222222222', 'ተሽከርካሪዎች', 'Vehicles', '🚗', 'vehicles', 2),
        ('a3333333-3333-3333-3333-333333333333', 'ፋሽን', 'Fashion', '👗', 'fashion', 3),
        ('a4444444-4444-4444-4444-444444444444', 'ቤትና የአትክልት ስፍራ', 'Home & Garden', '🏠', 'home-garden', 4),
        ('a5555555-5555-5555-5555-555555555555', 'ስራዎች', 'Jobs', '💼', 'jobs', 5),
        ('a6666666-6666-6666-6666-666666666666', 'ጌምስ', 'Gaming', '🎮', 'gaming', 6),
        ('a7777777-7777-7777-7777-777777777777', 'መጻሕፍት', 'Books', '📚', 'books', 7),
        ('a8888888-8888-8888-8888-888888888888', 'እንስሳት', 'Pets', '🐕', 'pets', 8),
        ('a9999999-9999-9999-9999-999999999999', 'ስፖርት', 'Sports', '🏋️', 'sports', 9),
        ('b1111111-1111-1111-1111-111111111111', 'ልጆች እና ሕፃናት', 'Kids & Baby', '👶', 'kids-baby', 10),
        ('b2222222-2222-2222-2222-222222222222', 'ውበት', 'Beauty', '💄', 'beauty', 11),
        ('b3333333-3333-3333-3333-333333333333', 'ሙዚቃ', 'Music', '🎵', 'music', 12),
        ('b4444444-4444-4444-4444-444444444444', 'አገልግሎቶች', 'Services', '🔧', 'services', 13),
        ('b5555555-5555-5555-5555-555555555555', 'ሪል እስቴት', 'Real Estate', '🏢', 'real-estate', 14),
        ('b6666666-6666-6666-6666-666666666666', 'ሌሎች', 'Other', '📦', 'other', 15);
    """)


def downgrade() -> None:
    op.drop_table('favorites')
    op.drop_table('messages')
    op.drop_table('chats')
    op.drop_table('listings')
    op.drop_table('categories')
    
    op.drop_index('ix_users_phone')
    op.drop_column('users', 'is_verified_seller')
    op.drop_column('users', 'total_listings')
    op.drop_column('users', 'total_sales')
    op.drop_column('users', 'total_ratings')
    op.drop_column('users', 'rating')
    op.drop_column('users', 'area')
    op.drop_column('users', 'city')
    op.drop_column('users', 'phone_verified_at')
    op.drop_column('users', 'is_phone_verified')
    op.drop_column('users', 'phone')
    
    op.execute("DROP TYPE listingstatus")
    op.execute("DROP TYPE listingcondition")
