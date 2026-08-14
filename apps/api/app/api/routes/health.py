from fastapi import APIRouter

from app.core.config import settings

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