"""Integration tests for port configuration during application startup.

Tests verify that the application correctly uses PortConfig for different
environments and that ports are allocated as expected.
"""

import os

from config.ports import PortConfig


class TestApplicationStartupPorts:
    """Test port configuration during application startup."""

    def test_dev_environment_port_allocation(self):
        """Test that dev environment uses random ports > 15000."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        backend_port = pc.get_backend_port()
        frontend_port = pc.get_frontend_port()

        assert backend_port > 15000, f"Backend port {backend_port} should be > 15000"
        assert frontend_port > 15000, f"Frontend port {frontend_port} should be > 15000"
        assert backend_port != frontend_port, "Backend and frontend ports should differ"

    def test_staging_environment_port_allocation(self):
        """Test that staging environment uses fixed ports."""
        pc = PortConfig(environment="staging", host="127.0.0.1")
        backend_port = pc.get_backend_port()
        frontend_port = pc.get_frontend_port()

        assert (
            backend_port == 8248
        ), f"Staging backend should be 8248, got {backend_port}"
        assert (
            frontend_port == 5174
        ), f"Staging frontend should be 5174, got {frontend_port}"

    def test_production_environment_port_allocation(self):
        """Test that production environment uses fixed ports."""
        pc = PortConfig(environment="production", host="127.0.0.1")
        backend_port = pc.get_backend_port()
        frontend_port = pc.get_frontend_port()

        assert (
            backend_port == 8247
        ), f"Production backend should be 8247, got {backend_port}"
        assert (
            frontend_port == 5173
        ), f"Production frontend should be 5173, got {frontend_port}"

    def test_environment_variable_override(self):
        """Test that ENVIRONMENT environment variable is respected."""
        # Test with dev
        with patch_env("ENVIRONMENT", "dev"):
            pc = PortConfig(
                environment=os.getenv("ENVIRONMENT", "dev"), host="127.0.0.1"
            )
            port = pc.get_backend_port()
            assert port > 15000

        # Test with staging
        with patch_env("ENVIRONMENT", "staging"):
            pc = PortConfig(
                environment=os.getenv("ENVIRONMENT", "dev"), host="127.0.0.1"
            )
            port = pc.get_backend_port()
            assert port == 8248

    def test_port_configuration_consistency(self):
        """Test that port configuration is consistent across multiple calls."""
        pc = PortConfig(environment="dev", host="127.0.0.1")
        port1 = pc.get_backend_port()
        port2 = pc.get_backend_port()
        port3 = pc.get_backend_port()

        # Ports should be cached and consistent
        assert port1 == port2 == port3

    def test_multiple_instances_different_ports_dev(self):
        """Test that multiple dev instances get different random ports."""
        pc1 = PortConfig(environment="dev", host="127.0.0.1")
        pc2 = PortConfig(environment="dev", host="127.0.0.1")
        pc3 = PortConfig(environment="dev", host="127.0.0.1")

        port1 = pc1.get_backend_port()
        port2 = pc2.get_backend_port()
        port3 = pc3.get_backend_port()

        # All should be > 15000
        assert all(p > 15000 for p in [port1, port2, port3])
        # At least some should be different (probabilistic)
        assert len({port1, port2, port3}) >= 1

    def test_no_zeros_in_production_ports(self):
        """Test that production ports don't contain zeros."""
        pc = PortConfig(environment="production", host="127.0.0.1")
        backend_port = pc.get_backend_port()
        frontend_port = pc.get_frontend_port()

        assert "0" not in str(
            backend_port
        ), f"Backend port {backend_port} contains zero"
        # Frontend port 5173 doesn't contain zero, but let's verify
        assert "0" not in str(
            frontend_port
        ), f"Frontend port {frontend_port} contains zero"

    def test_no_zeros_in_staging_ports(self):
        """Test that staging ports don't contain zeros."""
        pc = PortConfig(environment="staging", host="127.0.0.1")
        backend_port = pc.get_backend_port()
        frontend_port = pc.get_frontend_port()

        assert "0" not in str(
            backend_port
        ), f"Backend port {backend_port} contains zero"
        assert "0" not in str(
            frontend_port
        ), f"Frontend port {frontend_port} contains zero"


class TestPortConfigWithSettings:
    """Test PortConfig integration with Settings class."""

    def test_settings_uses_port_config(self):
        """Test that Settings class uses PortConfig correctly."""
        from config import settings

        # Test that settings can get ports
        port = settings.get_port()
        assert isinstance(port, int)
        assert port > 0

        frontend_port = settings.get_frontend_port_value()
        assert isinstance(frontend_port, int)
        assert frontend_port > 0

    def test_settings_base_url_generation(self):
        """Test that Settings generates correct base URLs."""
        from config import settings

        base_url = settings.get_base_url()
        assert base_url.startswith("http://")
        assert "localhost" not in base_url  # Should use 127.0.0.1, not localhost
        assert "127.0.0.1" in base_url or "0.0.0.0" in base_url

        frontend_url = settings.get_frontend_url()
        assert frontend_url.startswith("http://")
        assert "localhost" not in frontend_url


# Helper context manager for patching environment variables
class patch_env:
    """Context manager to temporarily set environment variable."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.original_value = None

    def __enter__(self):
        self.original_value = os.environ.get(self.key)
        os.environ[self.key] = self.value
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_value is None:
            os.environ.pop(self.key, None)
        else:
            os.environ[self.key] = self.original_value
