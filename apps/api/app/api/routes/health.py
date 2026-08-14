from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.database import engine


router = APIRouter()


@router.get(
    "/health",
    summary="Check API health",
    description="Returns the current operational status of the EnerWise AI API.",
)
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get(
    "/health/database",
    summary="Check database health",
    description="Checks whether the API can connect to PostgreSQL.",
)
def database_health_check() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "postgresql",
        }

    except SQLAlchemyError:
        return {
            "status": "unavailable",
            "database": "postgresql",
        }