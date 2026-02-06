"""Category endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.category import Category

router = APIRouter()


class CategoryResponse(BaseModel):
    """Category response."""
    id: str
    name_am: str
    name_en: str
    icon: str
    slug: str
    parent_id: str | None

    class Config:
        from_attributes = True


@router.get("", response_model=list[CategoryResponse])
async def list_categories(
    db: AsyncSession = Depends(get_db),
):
    """List all categories."""
    result = await db.execute(
        select(Category).order_by(Category.sort_order, Category.name_en)
    )
    categories = result.scalars().all()
    
    return [
        CategoryResponse(
            id=str(c.id),
            name_am=c.name_am,
            name_en=c.name_en,
            icon=c.icon,
            slug=c.slug,
            parent_id=str(c.parent_id) if c.parent_id else None,
        )
        for c in categories
    ]


@router.get("/{slug}", response_model=CategoryResponse)
async def get_category(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get category by slug."""
    result = await db.execute(
        select(Category).where(Category.slug == slug)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")
    
    return CategoryResponse(
        id=str(category.id),
        name_am=category.name_am,
        name_en=category.name_en,
        icon=category.icon,
        slug=category.slug,
        parent_id=str(category.parent_id) if category.parent_id else None,
    )
