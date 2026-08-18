from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import UserRole
from app.models.profile import Profile
from app.schemas.auth import AuthenticatedUser, CurrentUser
from app.services.auth import verify_access_token


bearer_scheme = HTTPBearer(auto_error=False)


async def get_authenticated_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> AuthenticatedUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await verify_access_token(credentials.credentials)


def get_current_user(
    authenticated_user: Annotated[
        AuthenticatedUser,
        Depends(get_authenticated_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> CurrentUser:
    profile = db.get(Profile, authenticated_user.id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User profile is unavailable",
        )

    return CurrentUser(
        id=authenticated_user.id,
        email=authenticated_user.email,
        full_name=profile.full_name,
        role=profile.role,
    )


def require_admin(
    current_user: Annotated[
        CurrentUser,
        Depends(get_current_user),
    ],
) -> CurrentUser:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )

    return current_user