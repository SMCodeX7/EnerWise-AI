from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Backend API for EnerWise AI, an evidence-grounded multi-agent "
            "renewable energy feasibility and decision-support platform."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
    )

    return application


app = create_application()


@app.get(
    "/",
    tags=["System"],
    summary="EnerWise AI API root",
)
async def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "online",
        "docs": "/docs",
    }