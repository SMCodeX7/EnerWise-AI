import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import AssessmentStatus


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "public.profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    input_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    energy_profile: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    status: Mapped[AssessmentStatus] = mapped_column(
        Enum(
            AssessmentStatus,
            name="assessment_status",
            schema="public",
        ),
        nullable=False,
        default=AssessmentStatus.DRAFT,
        server_default=AssessmentStatus.DRAFT.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="assessments",
    )