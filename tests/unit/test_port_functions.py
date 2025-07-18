"""Tests for port availability functions."""

from unittest.mock import patch

import pytest

from main import find_available_port, is_port_available


class TestPortAvailabilityFunctions:
    """Test port availability utility functions."""

    def test_is_port_available_success(self):
        """Test port availability check when port is available."""
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.__enter__.return_value.connect_ex.return_value = 1
            result = is_port_available(8000)
            assert result is True

    def test_is_port_available_failure(self):
        """Test port availability check when port is occupied."""
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.__enter__.return_value.connect_ex.return_value = 0
            result = is_port_available(8000)
            assert result is False

    def test_is_port_available_exception(self):
        """Test port availability check when socket creation fails."""
        with patch("socket.socket", side_effect=Exception("Socket error")):
            result = is_port_available(8000)
            assert result is False

    def test_find_available_port_success(self):
        """Test finding available port when first port is available."""
        with patch("main.is_port_available", return_value=True):
            result = find_available_port(8000)
            assert result == 8000

    def test_find_available_port_second_attempt(self):
        """Test finding available port when first port is occupied."""
        with patch("main.is_port_available", side_effect=[False, True]):
            result = find_available_port(8000)
            assert result == 8001

    def test_find_available_port_no_ports_available(self):
        """Test finding available port when no ports are available."""
        with patch("main.is_port_available", return_value=False), pytest.raises(
            RuntimeError, match="No available port found"
        ):
            find_available_port(8000, max_attempts=2)
