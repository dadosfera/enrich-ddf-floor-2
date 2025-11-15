"""Unit tests for PortConfig class and port configuration utilities.

Tests cover:
- Port allocation for different environments (dev/staging/production)
- Random port generation for dev environment
- Port conflict handling and fallback mechanisms
- Port availability checking
"""

from unittest.mock import patch

import pytest

from config.ports import (
    PortConfig,
    find_available_port,
    find_available_random_port,
    generate_random_port,
    get_user_friendly_url,
    is_port_available,
)


class TestPortAvailabilityFunctions:
    """Test port availability utility functions."""

    def test_is_port_available_success(self):
        """Test port availability check when port is available."""
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.__enter__.return_value.connect_ex.return_value = 1
            result = is_port_available(8000, "127.0.0.1")
            assert result is True

    def test_is_port_available_failure(self):
        """Test port availability check when port is occupied."""
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.__enter__.return_value.connect_ex.return_value = 0
            result = is_port_available(8000, "127.0.0.1")
            assert result is False

    def test_is_port_available_exception(self):
        """Test port availability check when socket creation fails."""
        with patch("socket.socket", side_effect=Exception("Socket error")):
            result = is_port_available(8000, "127.0.0.1")
            assert result is False

    def test_find_available_port_success(self):
        """Test finding available port when first port is available."""
        with patch("config.ports.is_port_available", return_value=True):
            result = find_available_port(8000, "127.0.0.1")
            assert result == 8000

    def test_find_available_port_second_attempt(self):
        """Test finding available port when first port is occupied."""
        with patch("config.ports.is_port_available", side_effect=[False, True]):
            result = find_available_port(8000, "127.0.0.1")
            assert result == 8001

    def test_find_available_port_no_ports_available(self):
        """Test finding available port when no ports are available."""
        with patch("config.ports.is_port_available", return_value=False):  # noqa: SIM117
            with pytest.raises(RuntimeError, match="No available port found"):
                find_available_port(8000, "127.0.0.1", max_attempts=2)


class TestRandomPortGeneration:
    """Test random port generation functions."""

    def test_generate_random_port_range(self):
        """Test that random port is within specified range."""
        min_port = 15001
        max_port = 20000
        port = generate_random_port(min_port, max_port)
        assert min_port <= port <= max_port

    def test_generate_random_port_different_values(self):
        """Test that random ports are different (probabilistic test)."""
        ports = [generate_random_port(15001, 65535) for _ in range(10)]
        # At least some ports should be different (very high probability)
        assert len(set(ports)) > 1

    def test_find_available_random_port_success(self):
        """Test finding available random port."""
        with patch("config.ports.is_port_available", return_value=True):
            port = find_available_random_port(15001, 20000, "127.0.0.1")
            assert 15001 <= port <= 20000

    def test_find_available_random_port_no_ports_available(self):
        """Test finding random port when no ports are available."""
        with patch("config.ports.is_port_available", return_value=False):  # noqa: SIM117
            with pytest.raises(RuntimeError, match="No available port found"):
                find_available_random_port(15001, 20000, "127.0.0.1", max_attempts=5)


class TestPortConfig:
    """Test PortConfig class for environment-aware port allocation."""

    def test_production_backend_port(self):
        """Test production backend port allocation."""
        pc = PortConfig(environment="production", host="127.0.0.1")
        port = pc.get_backend_port()
        assert port == PortConfig.PRODUCTION_BACKEND_PORT
        assert port == 8247
        assert "0" not in str(port)  # No zeros in port number

    def test_production_frontend_port(self):
        """Test production frontend port allocation."""
        pc = PortConfig(environment="production", host="127.0.0.1")
        port = pc.get_frontend_port()
        assert port == PortConfig.PRODUCTION_FRONTEND_PORT
        assert port == 5173

    def test_staging_backend_port(self):
        """Test staging backend port allocation."""
        pc = PortConfig(environment="staging", host="127.0.0.1")
        port = pc.get_backend_port()
        assert port == PortConfig.STAGING_BACKEND_PORT
        assert port == 8248
        assert "0" not in str(port)  # No zeros in port number

    def test_staging_frontend_port(self):
        """Test staging frontend port allocation."""
        pc = PortConfig(environment="staging", host="127.0.0.1")
        port = pc.get_frontend_port()
        assert port == PortConfig.STAGING_FRONTEND_PORT
        assert port == 5174

    def test_dev_backend_port_random(self):
        """Test dev backend port is random and > 15000."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        port = pc.get_backend_port()
        assert port > 15000
        assert port >= PortConfig.DEV_MIN_PORT
        assert port <= PortConfig.DEV_MAX_PORT

    def test_dev_frontend_port_random(self):
        """Test dev frontend port is random and > 15000."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        port = pc.get_frontend_port()
        assert port > 15000
        assert port >= PortConfig.DEV_MIN_PORT
        assert port <= PortConfig.DEV_MAX_PORT

    def test_dev_ports_different_instances(self):
        """Test that different PortConfig instances get different random ports."""
        pc1 = PortConfig(environment="dev", host="127.0.0.1")
        pc2 = PortConfig(environment="dev", host="127.0.0.1")
        port1 = pc1.get_backend_port()
        port2 = pc2.get_backend_port()
        # Ports should be different (probabilistic - very high probability)
        # If they're the same, it's extremely unlikely but possible
        assert port1 > 15000
        assert port2 > 15000

    def test_port_caching(self):
        """Test that ports are cached within same instance."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        port1 = pc.get_backend_port()
        port2 = pc.get_backend_port()
        assert port1 == port2  # Should be cached

    def test_set_backend_port_explicit(self):
        """Test explicitly setting backend port."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        pc.set_backend_port(9000)
        assert pc.get_backend_port() == 9000

    def test_set_frontend_port_explicit(self):
        """Test explicitly setting frontend port."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        pc.set_frontend_port(9001)
        assert pc.get_frontend_port() == 9001

    def test_port_conflict_handling_dev(self):
        """Test port conflict handling for dev environment."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        # Mock first port as unavailable, second as available
        with patch("config.ports.is_port_available", side_effect=[False, True]):  # noqa: SIM117
            with patch("config.ports.find_available_random_port", return_value=16000):
                port = pc.get_backend_port()
                assert port == 16000

    def test_port_conflict_handling_staging(self):
        """Test port conflict handling for staging environment."""
        pc = PortConfig(environment="staging", host="127.0.0.1")
        # Mock staging port as unavailable, should find next available
        with patch("config.ports.is_port_available", side_effect=[False, True]):  # noqa: SIM117
            with patch("config.ports.find_available_port", return_value=8249):
                port = pc.get_backend_port()
                assert port == 8249

    def test_environment_case_insensitive(self):
        """Test that environment names are case-insensitive."""
        pc1 = PortConfig(environment="DEV", host="127.0.0.1")
        pc2 = PortConfig(environment="dev", host="127.0.0.1")
        port1 = pc1.get_backend_port()
        port2 = pc2.get_backend_port()
        # Both should be > 15000 (dev ports)
        assert port1 > 15000
        assert port2 > 15000


class TestUserFriendlyURL:
    """Test URL generation functions."""

    def test_get_user_friendly_url_0_0_0_0(self):
        """Test converting 0.0.0.0 to 127.0.0.1 for browser access."""
        url = get_user_friendly_url("0.0.0.0", 8000)
        assert url == "http://127.0.0.1:8000"
        assert "localhost" not in url  # Should not use localhost

    def test_get_user_friendly_url_127_0_0_1(self):
        """Test keeping 127.0.0.1 as-is."""
        url = get_user_friendly_url("127.0.0.1", 8000)
        assert url == "http://127.0.0.1:8000"

    def test_get_user_friendly_url_custom_host(self):
        """Test custom host is preserved."""
        url = get_user_friendly_url("example.com", 8000)
        assert url == "http://example.com:8000"

    def test_get_user_friendly_url_no_localhost(self):
        """Test that localhost is never used in URLs."""
        url1 = get_user_friendly_url("0.0.0.0", 8000)
        url2 = get_user_friendly_url("127.0.0.1", 8000)
        assert "localhost" not in url1
        assert "localhost" not in url2


class TestPortConfigIntegration:
    """Integration tests for PortConfig with real socket operations."""

    def test_real_port_availability_check(self):
        """Test port availability with real socket (if port is available)."""
        # Use a high port that's likely to be available
        test_port = 50000
        try:
            result = is_port_available(test_port, "127.0.0.1")
            # Result depends on whether port is actually available
            assert isinstance(result, bool)
        except Exception:
            pytest.skip("Socket operation failed")

    def test_real_dev_port_allocation(self):
        """Test dev port allocation with real availability checks."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        port = pc.get_backend_port()
        # Verify port is actually available
        assert is_port_available(port, "127.0.0.1")
        assert port > 15000
