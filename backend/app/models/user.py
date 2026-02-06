"""User model for Telegram users."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """Telegram user model."""

    __tablename__ = "users"

    # Primary key (our internal ID)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Telegram user ID (unique identifier from Telegram)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )

    # User info from Telegram
    username: Mapped[str | None] = mapped_column(String(255), index=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255))
    language_code: Mapped[str | None] = mapped_column(String(10))
    photo_url: Mapped[str | None] = mapped_column(String(500))
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)

    # App-specific data
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return f"<User {self.telegram_id} (@{self.username})>"

    def update_from_telegram(self, tg_user: dict) -> None:
        """Update user info from Telegram data."""
        self.username = tg_user.get("username")
        self.first_name = tg_user.get("first_name", self.first_name)
        self.last_name = tg_user.get("last_name")
        self.language_code = tg_user.get("language_code")
        self.photo_url = tg_user.get("photo_url")
        self.is_premium = tg_user.get("is_premium", False)
        self.last_seen_at = datetime.now(UTC)
