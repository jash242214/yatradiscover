"""
Authentication endpoints
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.user import UserLogin, UserRegister, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account and return access/refresh tokens",
)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user

    - **email**: User email address (must be unique)
    - **username**: Username (must be unique, 3-50 characters)
    - **full_name**: User's full name
    - **password**: Password (minimum 8 characters)

    Returns: User info with access and refresh tokens
    """
    try:
        return AuthService.register_user(db, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration",
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user and return access/refresh tokens",
)
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Login a user

    - **email**: User email address
    - **password**: User password

    Returns: User info with access and refresh tokens
    """
    try:
        return AuthService.login_user(db, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login",
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Get a new access token using refresh token",
)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    """
    Refresh access token

    - **refresh_token**: Valid refresh token

    Returns: New access token with user info
    """
    try:
        return AuthService.refresh_access_token(db, refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during token refresh",
        )
