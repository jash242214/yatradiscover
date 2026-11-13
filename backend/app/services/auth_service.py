"""
Authentication service for user registration and login
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    decode_token,
)
from app.db.models import User
from app.schemas.user import UserLogin, UserRegister, UserResponse, TokenResponse


class AuthService:
    """Service for authentication operations"""

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserRegister,
    ) -> TokenResponse:
        """Register a new user"""

        # Check if user already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise ValueError(f"User with email {user_data.email} already exists")

        existing_username = (
            db.query(User).filter(User.username == user_data.username).first()
        )
        if existing_username:
            raise ValueError(f"Username {user_data.username} is already taken")

        # Create new user
        hashed_password = get_password_hash(user_data.password)

        new_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Generate tokens
        access_token = create_access_token(subject=str(new_user.id))
        refresh_token = create_refresh_token(subject=str(new_user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.from_orm(new_user),
        )

    @staticmethod
    def login_user(
        db: Session,
        user_data: UserLogin,
    ) -> TokenResponse:
        """Authenticate and login a user"""

        # Find user by email
        user = db.query(User).filter(User.email == user_data.email).first()

        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        if not verify_password(user_data.password, user.hashed_password):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is inactive")

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

        # Generate tokens
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.from_orm(user),
        )

    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token: str,
    ) -> TokenResponse:
        """Generate a new access token using refresh token"""

        # Decode refresh token
        token_data = decode_token(refresh_token)

        if not token_data or token_data.type != "refresh":
            raise ValueError("Invalid refresh token")

        # Get user from database
        user = db.query(User).filter(User.id == token_data.sub).first()

        if not user or not user.is_active:
            raise ValueError("User not found or inactive")

        # Generate new access token
        access_token = create_access_token(subject=str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.from_orm(user),
        )

    @staticmethod
    def get_current_user(
        db: Session,
        access_token: str,
    ) -> Optional[User]:
        """Get current user from access token"""

        # Decode access token
        token_data = decode_token(access_token)

        if not token_data or token_data.type != "access":
            return None

        # Get user from database
        user = db.query(User).filter(User.id == token_data.sub).first()

        return user if user and user.is_active else None
