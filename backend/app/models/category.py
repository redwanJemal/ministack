"""Category model for marketplace."""

import uuid

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Category(Base):
    """Product category."""

    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name_am: Mapped[str] = mapped_column(String(100), nullable=False)  # Amharic
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)  # English
    icon: Mapped[str] = mapped_column(String(50), default="📦")
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    
    # Self-referential for subcategories
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    
    # Relationships
    listings = relationship("Listing", back_populates="category")
    subcategories = relationship("Category", backref="parent", remote_side=[id])

    def __repr__(self) -> str:
        return f"<Category {self.name_en}>"
