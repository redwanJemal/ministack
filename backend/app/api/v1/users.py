"""User endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.deps import CurrentUser

router = APIRouter()


class UserResponse(BaseModel):
    """User data response."""
    id: str
    telegram_id: int
    username: str | None
    first_name: str
    last_name: str | None
    photo_url: str | None
    is_premium: bool
    language_code: str | None
    settings: dict

    class Config:
        from_attributes = True


class UpdateSettingsRequest(BaseModel):
    """Request to update user settings."""
    settings: dict


@router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUser):
    """Get current user profile."""
    return UserResponse(
        id=str(user.id),
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        photo_url=user.photo_url,
        is_premium=user.is_premium,
        language_code=user.language_code,
        settings=user.settings or {},
    )


@router.patch("/me/settings", response_model=UserResponse)
async def update_settings(
    body: UpdateSettingsRequest,
    user: CurrentUser,
):
    """Update current user settings."""
    # Merge settings
    current_settings = user.settings or {}
    current_settings.update(body.settings)
    user.settings = current_settings

    return UserResponse(
        id=str(user.id),
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        photo_url=user.photo_url,
        is_premium=user.is_premium,
        language_code=user.language_code,
        settings=user.settings,
    )
