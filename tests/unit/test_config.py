"""Unit tests for configuration module."""

import pytest
from app.core.config import Settings


class TestSettings:
    """Test suite for application settings."""
    
    def test_settings_initialization(self):
        """Test that settings can be initialized with defaults."""
        settings = Settings()
        
        assert settings.PROJECT_NAME == "Enrich DDF Floor 2"
        assert settings.VERSION == "1.0.0"
        assert settings.DEBUG is False
        assert settings.ENVIRONMENT == "production"
    
    def test_settings_with_environment_override(self, monkeypatch):
        """Test that settings can be overridden by environment variables."""
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("ENVIRONMENT", "development")
        
        settings = Settings()
        
        assert settings.DEBUG is True
        assert settings.ENVIRONMENT == "development"
    
    def test_database_url_validation(self):
        """Test database URL validation."""
        settings = Settings()
        
        # Should contain valid database URL components
        assert "postgresql" in settings.DATABASE_URL
        assert "asyncpg" in settings.DATABASE_URL
    
    def test_redis_url_validation(self):
        """Test Redis URL validation."""
        settings = Settings()
        
        # Should contain valid Redis URL components
        assert "redis://" in settings.REDIS_URL
    
    @pytest.mark.slow
    def test_external_api_configuration(self):
        """Test external API configuration (marked as slow test)."""
        settings = Settings()
        
        # Should have placeholder values for external APIs
        assert hasattr(settings, 'APOLLO_API_KEY')
        assert hasattr(settings, 'PEOPLEDATALABS_API_KEY')
        assert hasattr(settings, 'ZEROBOUNCE_API_KEY') 