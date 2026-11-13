"""
FastAPI application factory
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base, engine

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

    yield

    # Shutdown
    logger.info("Shutting down application")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-powered travel planning platform",
        version=settings.PROJECT_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    # Add CORS middleware
    if settings.ALLOWED_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info(f"CORS enabled for origins: {settings.ALLOWED_ORIGINS}")

    # Include API routers
    app.include_router(api_router)

    # Health check endpoint
    @app.get(
        "/health",
        tags=["health"],
        summary="Health check",
        description="Check if the API is running",
    )
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "ok",
            "service": settings.PROJECT_NAME,
            "version": settings.PROJECT_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    # Root endpoint
    @app.get(
        "/",
        tags=["root"],
        summary="API Info",
        description="Get API information",
    )
    async def root():
        """Root endpoint"""
        return {
            "message": f"Welcome to {settings.PROJECT_NAME}",
            "version": settings.PROJECT_VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    logger.info(f"Application initialized: {settings.PROJECT_NAME}")

    return app


# Create app instance
app = create_app()
