"""
Application configuration using Pydantic Settings.
"""

from typing import List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Application
    DEBUG: bool = Field(default=False, description="Debug mode")
    SECRET_KEY: str = Field(..., description="JWT secret key")
    API_V1_STR: str = Field(default="/api/v1", description="API v1 prefix")
    
    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=1, description="Number of workers")
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="JWT expiration"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["*"], description="Allowed hosts"
    )
    CORS_ORIGINS: List[str] = Field(default=["*"], description="CORS origins")
    
    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    DATABASE_POOL_SIZE: int = Field(
        default=20, description="DB connection pool size"
    )
    DATABASE_MAX_OVERFLOW: int = Field(
        default=0, description="DB max overflow"
    )
    
    # Redis
    REDIS_URL: str = Field(..., description="Redis connection URL")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    
    # Celery
    CELERY_BROKER_URL: str = Field(..., description="Celery broker URL")
    CELERY_RESULT_BACKEND: str = Field(
        ..., description="Celery result backend"
    )
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(
        default=True, description="Enable rate limiting"
    )
    DEFAULT_RATE_LIMIT: str = Field(
        default="100/minute", description="Default rate limit"
    )
    
    # External APIs
    APOLLO_API_KEY: Optional[str] = Field(
        default=None, description="Apollo API key"
    )
    ZEROBOUNCE_API_KEY: Optional[str] = Field(
        default=None, description="ZeroBounce API key"
    )
    PDL_API_KEY: Optional[str] = Field(
        default=None, description="People Data Labs API key"
    )
    SURFE_API_KEY: Optional[str] = Field(
        default=None, description="Surfe API key"
    )
    
    # Brazil specific
    SERPRO_API_KEY: Optional[str] = Field(
        default=None, description="Serpro API key"
    )
    SERPRO_API_URL: str = Field(
        default="https://apigateway.serpro.gov.br",
        description="Serpro API URL"
    )
    
    # Argentina
    AFIP_API_URL: str = Field(
        default="https://soa.afip.gob.ar",
        description="AFIP API URL"
    )
    
    # Mexico
    SAT_API_URL: str = Field(
        default="https://portalsat.plataforma.sat.gob.mx",
        description="SAT Mexico API URL"
    )
    
    # Colombia
    RUES_API_URL: str = Field(
        default="https://www.rues.org.co",
        description="RUES Colombia API URL"
    )
    
    # Chile
    SII_API_URL: str = Field(
        default="https://maullin.sii.cl",
        description="SII Chile API URL"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="json", description="Log format (json/text)"
    )
    
    # Metrics
    METRICS_ENABLED: bool = Field(
        default=True, description="Enable Prometheus metrics"
    )
    METRICS_PORT: int = Field(default=9090, description="Metrics server port")
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        """Parse allowed hosts from string."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore",
        "validate_assignment": True
    }


# Global settings instance
settings = Settings()