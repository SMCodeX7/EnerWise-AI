from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AssessmentStatus


class AssessmentCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str | None = Field(
        default=None,
        max_length=200,
    )
    input_text: str = Field(
        min_length=1,
        max_length=10000,
    )


class AssessmentUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str | None = Field(
        default=None,
        max_length=200,
    )
    input_text: str | None = Field(
        default=None,
        min_length=1,
        max_length=10000,
    )


class AssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str | None
    input_text: str
    energy_profile: dict[str, Any]
    status: AssessmentStatus
    created_at: datetime
    updated_at: datetime