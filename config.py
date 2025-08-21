"""Application configuration using pydantic-settings."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application settings
    app_name: str = "Enrich DDF Floor 2"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8247  # Non-round port to avoid conflicts

    # Database settings
    database_url: str = "sqlite:///./app.db"
    test_database_url: str = "sqlite:///./test.db"

    # Security settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Rate limiting
    rate_limit_per_minute: int = 60

    # Monitoring settings
    sentry_dsn: Optional[str] = None
    log_level: str = "INFO"
    metrics_enabled: bool = True

    # Real Data Enrichment API Keys
    hunter_api_key: Optional[str] = None
    zerobounce_api_key: Optional[str] = None
    github_token: Optional[str] = None
    pdl_api_key: Optional[str] = None
    apollo_api_key: Optional[str] = None
    
    # LinkedIn & Professional Data APIs
    wiza_api_key: Optional[str] = None
    surfe_api_key: Optional[str] = None
    
    # Brazil-Specific Data Sources
    bigdata_corp_api_key: Optional[str] = None
    bigdata_corp_secret: Optional[str] = None
    
    # Enterprise Data Providers
    coresignal_api_key: Optional[str] = None

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def get_base_url(self) -> str:
        """Generate base URL from host and port configuration."""
        return f"http://{self.host}:{self.port}"


# Global settings instance
settings = Settings()
