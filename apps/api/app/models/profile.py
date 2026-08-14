import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import UserRole


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "auth.users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            schema="public",
        ),
        nullable=False,
        default=UserRole.USER,
        server_default=UserRole.USER.value,
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

    assessments: Mapped[list["Assessment"]] = relationship(
        "Assessment",
        back_populates="user",
        cascade="all, delete-orphan",
    )