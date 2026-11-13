"""
User database model
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class User(Base):
    """User model for authentication"""

    __tablename__ = "users"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    # Basic info
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)

    # Password (hashed)
    hashed_password = Column(String(255), nullable=False)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Indexes for performance
    __table_args__ = (
        Index("idx_email", "email"),
        Index("idx_username", "username"),
        Index("idx_is_active", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
