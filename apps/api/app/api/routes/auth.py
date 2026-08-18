from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.auth import AuthenticatedUser


router = APIRouter(prefix="/auth")


@router.get("/me", response_model=AuthenticatedUser)
async def read_current_user(
    current_user: Annotated[
        AuthenticatedUser,
        Depends(get_current_user),
    ],
) -> AuthenticatedUser:
    return current_user