"""
API v1 endpoints router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)

__all__ = ["api_router"]
