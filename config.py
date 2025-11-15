"""Application configuration using pydantic-settings."""

import os
from typing import Optional

from pydantic_settings import BaseSettings

from config.ports import PortConfig, get_user_friendly_url


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application settings
    app_name: str = "Enrich DDF Floor 2"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: Optional[int] = None  # Will be set from PortConfig if not provided

    # Frontend settings
    frontend_host: str = "0.0.0.0"
    frontend_port: Optional[int] = None  # Will be set from PortConfig if not provided

    # Environment setting
    environment: str = "dev"  # dev, staging, production

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

    def _get_port_config(self) -> PortConfig:
        """Get port configuration instance for current environment."""
        env = os.getenv("ENVIRONMENT", self.environment)
        return PortConfig(environment=env, host=self.host)

    def get_port(self) -> int:
        """Get backend port, using PortConfig if not explicitly set."""
        if self.port is not None:
            return self.port
        port_config = self._get_port_config()
        return port_config.get_backend_port()

    def get_frontend_port_value(self) -> int:
        """Get frontend port, using PortConfig if not explicitly set."""
        if self.frontend_port is not None:
            return self.frontend_port
        port_config = self._get_port_config()
        return port_config.get_frontend_port()

    def get_base_url(self) -> str:
        """Generate base URL from host and port configuration."""
        port = self.get_port()
        return get_user_friendly_url(self.host, port)

    def get_frontend_url(self) -> str:
        """Generate frontend URL from host and port configuration."""
        port = self.get_frontend_port_value()
        return get_user_friendly_url(self.frontend_host, port)


# Global settings instance
settings = Settings()
