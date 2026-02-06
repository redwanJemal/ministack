"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Admin
    ADMIN_TELEGRAM_IDS: str = ""  # Comma-separated Telegram IDs
    
    # S3/MinIO
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = "gebeya-uploads"
    S3_REGION: str = "us-east-1"
    
    @property
    def admin_ids(self) -> set[int]:
        """Parse admin Telegram IDs."""
        if not self.ADMIN_TELEGRAM_IDS:
            return set()
        return {int(x.strip()) for x in self.ADMIN_TELEGRAM_IDS.split(",") if x.strip()}

    """Application settings loaded from environment."""

    # App
    APP_NAME: str = "MiniStack"
    APP_URL: str = "http://localhost:5173"
    DEBUG: bool = False

    # Telegram
    BOT_TOKEN: str = ""
    BOT_USERNAME: str = ""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://ministack:secret@localhost:5432/ministack"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "change-me-in-production"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    CORS_ORIGINS: str = "*"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
