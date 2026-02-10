"""
Application settings and configuration management.

Loads configuration from environment variables using Pydantic Settings.
All sensitive data (tokens, secrets) must be stored in environment variables.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "TeleFinder"
    env: str = Field(default="development", description="Environment: development, staging, production")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # API Configuration
    api_base_url: str = Field(default="http://localhost:8000", description="Backend API base URL")
    frontend_url: str = Field(default="http://localhost:5173", description="Frontend URL for CORS")
    
    # Database (SQLite)
    sqlite_db_path: str = Field(default="backend/telefinder.db", description="Path to SQLite database file")
    
    # Telegram API
    telegram_api_id: int = Field(..., description="Telegram API ID from my.telegram.org")
    telegram_api_hash: str = Field(..., description="Telegram API Hash from my.telegram.org")
    telegram_bot_token: str = Field(..., description="Telegram Bot Token from @BotFather")
    
    # Security & Authentication
    secret_key: str = Field(..., description="JWT secret key (min 32 chars)")
    session_encryption_key: str = Field(..., description="Telegram session encryption key (min 32 chars)")
    access_token_expire_minutes: int = Field(default=10080, description="JWT token expiry in minutes (default: 7 days)")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    
    # Machine Learning
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence transformer model for semantic filtering"
    )
    default_semantic_threshold: float = Field(
        default=0.65,
        ge=0.5,
        le=0.9,
        description="Default semantic similarity threshold"
    )
    
    # Rate Limiting
    auth_rate_limit: int = Field(default=10, description="Auth endpoint rate limit (requests/minute)")
    api_rate_limit: int = Field(default=100, description="API rate limit (requests/minute per user)")
    
    # Notifications
    max_notification_retries: int = Field(default=3, description="Max notification delivery retries")
    notification_retry_delay: int = Field(default=60, description="Notification retry delay (seconds)")
    
    # Data Retention (days)
    message_retention_days: int = Field(default=30, description="Regular message retention period")
    hot_match_retention_days: int = Field(default=90, description="Hot match message retention period")
    notification_retention_days: int = Field(default=30, description="Notification history retention")
    
    # WebSocket
    max_websocket_connections: int = Field(default=5, description="Max WebSocket connections per user")
    websocket_keepalive_interval: int = Field(default=30, description="WebSocket keepalive interval (seconds)")
    
    # Performance
    message_batch_size: int = Field(default=100, description="Message processing batch size")
    
    # Testing
    test_db_path: Optional[str] = Field(default="backend/test_telefinder.db", description="Test database path")
    skip_telegram_auth_in_tests: bool = Field(default=True, description="Skip Telegram auth in tests")
    
    @validator("secret_key", "session_encryption_key")
    def validate_key_length(cls, v: str, field) -> str:
        """Ensure security keys are at least 32 characters."""
        if len(v) < 32:
            raise ValueError(f"{field.name} must be at least 32 characters long")
        return v
    
    @validator("env")
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"env must be one of {allowed}")
        return v
    
    @property
    def database_url(self) -> str:
        """Get SQLite database URL for SQLAlchemy."""
        return f"sqlite:///{self.sqlite_db_path}"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.env == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.env == "development"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings instance.
    
    Returns:
        Settings: Application settings
    """
    return settings

