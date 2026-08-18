from uuid import UUID

from pydantic import BaseModel

from app.models.enums import UserRole


class AuthenticatedUser(BaseModel):
    id: UUID
    email: str | None = None


class CurrentUser(AuthenticatedUser):
    full_name: str | None = None
    role: UserRole