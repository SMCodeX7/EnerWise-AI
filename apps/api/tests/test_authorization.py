from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.dependencies import require_admin
from app.models.enums import UserRole
from app.schemas.auth import CurrentUser


def test_admin_user_is_allowed() -> None:
    user = CurrentUser(
        id=uuid4(),
        email="admin@example.com",
        full_name="Admin User",
        role=UserRole.ADMIN,
    )

    result = require_admin(user)

    assert result == user


def test_normal_user_is_blocked_from_admin_access() -> None:
    user = CurrentUser(
        id=uuid4(),
        email="user@example.com",
        full_name="Normal User",
        role=UserRole.USER,
    )

    with pytest.raises(HTTPException) as exc_info:
        require_admin(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Administrator access required"