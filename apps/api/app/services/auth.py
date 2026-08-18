import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.auth import AuthenticatedUser


def unauthorized_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def verify_access_token(token: str) -> AuthenticatedUser:
    url = f"{settings.supabase_url.rstrip('/')}/auth/v1/user"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                url,
                headers={
                    "apikey": settings.supabase_publishable_key,
                    "Authorization": f"Bearer {token}",
                },
            )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        ) from exc

    if response.status_code != status.HTTP_200_OK:
        raise unauthorized_exception()

    try:
        data = response.json()
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid authentication service response",
        ) from exc

    if not data.get("id"):
        raise unauthorized_exception()

    return AuthenticatedUser(
        id=data["id"],
        email=data.get("email"),
    )