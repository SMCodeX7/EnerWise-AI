from fastapi import APIRouter

from app.api.routes import assessments, auth, health


api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["Health"],
)

api_router.include_router(
    auth.router,
    tags=["Authentication"],
)

api_router.include_router(
    assessments.router,
    tags=["Assessments"],
)