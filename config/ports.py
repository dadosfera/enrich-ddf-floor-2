"""Centralized port configuration for Enrich DDF Floor 2.

This module provides centralized port management with environment-specific
configuration and random port generation for development environments.
"""

import random
import socket
from typing import Optional


def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a port is available for binding.

    Args:
        port: Port number to check
        host: Host address to check (default: 127.0.0.1)

    Returns:
        True if port is available, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0
    except Exception:
        return False


def generate_random_port(min_port: int = 15001, max_port: int = 65535) -> int:
    """Generate a random port number within specified range.

    Args:
        min_port: Minimum port number (default: 15001)
        max_port: Maximum port number (default: 65535)

    Returns:
        Random port number
    """
    return random.randint(min_port, max_port)


def find_available_random_port(
    min_port: int = 15001,
    max_port: int = 65535,
    host: str = "127.0.0.1",
    max_attempts: int = 100,
) -> int:
    """Find an available random port within specified range.

    Args:
        min_port: Minimum port number (default: 15001)
        max_port: Maximum port number (default: 65535)
        host: Host address to check (default: 127.0.0.1)
        max_attempts: Maximum attempts to find available port (default: 100)

    Returns:
        Available port number

    Raises:
        RuntimeError: If no available port found after max_attempts
    """
    for _ in range(max_attempts):
        port = generate_random_port(min_port, max_port)
        if is_port_available(port, host):
            return port
    raise RuntimeError(
        f"No available port found in range {min_port}-{max_port} after {max_attempts} attempts"
    )


def find_available_port(
    start_port: int, host: str = "127.0.0.1", max_attempts: int = 10
) -> int:
    """Find an available port starting from start_port.

    Args:
        start_port: Starting port number
        host: Host address to check (default: 127.0.0.1)
        max_attempts: Maximum attempts to find available port (default: 10)

    Returns:
        Available port number

    Raises:
        RuntimeError: If no available port found after max_attempts
    """
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port, host):
            return port
    raise RuntimeError(
        f"No available port found in range {start_port}-{start_port + max_attempts - 1}"
    )


class PortConfig:
    """Centralized port configuration manager."""

    # Production ports (no zeros in port numbers)
    PRODUCTION_BACKEND_PORT = 8247
    PRODUCTION_FRONTEND_PORT = 5173

    # Staging ports
    STAGING_BACKEND_PORT = 8248
    STAGING_FRONTEND_PORT = 5174

    # Development ports - will use random ports > 15000
    DEV_MIN_PORT = 15001
    DEV_MAX_PORT = 65535

    def __init__(self, environment: str = "dev", host: str = "127.0.0.1"):
        """Initialize port configuration.

        Args:
            environment: Environment name (dev, staging, production)
            host: Host address for port checking (default: 127.0.0.1)
        """
        self.environment = environment.lower()
        self.host = host
        self._backend_port: Optional[int] = None
        self._frontend_port: Optional[int] = None

    def get_backend_port(self) -> int:
        """Get backend port for current environment.

        Returns:
            Backend port number
        """
        if self._backend_port is not None:
            return self._backend_port

        if self.environment == "production":
            port = self.PRODUCTION_BACKEND_PORT
        elif self.environment == "staging":
            port = self.STAGING_BACKEND_PORT
        else:  # dev
            # Use random port > 15000 for dev
            port = find_available_random_port(
                min_port=self.DEV_MIN_PORT, max_port=self.DEV_MAX_PORT, host=self.host
            )

        # Verify port is available, find alternative if needed
        if not is_port_available(port, self.host):
            if self.environment == "dev":
                port = find_available_random_port(
                    min_port=self.DEV_MIN_PORT,
                    max_port=self.DEV_MAX_PORT,
                    host=self.host,
                )
            else:
                port = find_available_port(port, self.host)

        self._backend_port = port
        return port

    def get_frontend_port(self) -> int:
        """Get frontend port for current environment.

        Returns:
            Frontend port number
        """
        if self._frontend_port is not None:
            return self._frontend_port

        if self.environment == "production":
            port = self.PRODUCTION_FRONTEND_PORT
        elif self.environment == "staging":
            port = self.STAGING_FRONTEND_PORT
        else:  # dev
            # Use random port > 15000 for dev
            port = find_available_random_port(
                min_port=self.DEV_MIN_PORT, max_port=self.DEV_MAX_PORT, host=self.host
            )

        # Verify port is available, find alternative if needed
        if not is_port_available(port, self.host):
            if self.environment == "dev":
                port = find_available_random_port(
                    min_port=self.DEV_MIN_PORT,
                    max_port=self.DEV_MAX_PORT,
                    host=self.host,
                )
            else:
                port = find_available_port(port, self.host)

        self._frontend_port = port
        return port

    def set_backend_port(self, port: int) -> None:
        """Set backend port explicitly.

        Args:
            port: Port number to set
        """
        self._backend_port = port

    def set_frontend_port(self, port: int) -> None:
        """Set frontend port explicitly.

        Args:
            port: Port number to set
        """
        self._frontend_port = port


def get_user_friendly_url(host: str, port: int) -> str:
    """Convert bind address to user-friendly URL for browser access.

    Args:
        host: Host address (e.g., "0.0.0.0", "127.0.0.1")
        port: Port number

    Returns:
        User-friendly URL string
    """
    # Convert 0.0.0.0 to 127.0.0.1 for browser access
    # Keep other addresses as-is (e.g., 127.0.0.1, custom domains)
    display_host = "127.0.0.1" if host == "0.0.0.0" else host
    return f"http://{display_host}:{port}"
