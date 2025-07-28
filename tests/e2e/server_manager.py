#!/usr/bin/env python3
"""
Unified Server Manager for UI E2E Tests
Provides centralized server management across all test files
"""

import asyncio
import logging
import subprocess
import time
from typing import Optional

import requests


logger = logging.getLogger(__name__)


class ServerManager:
    """Unified server management for UI E2E tests."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8247):
        self.host = host
        self.port = port
        self.server_process: Optional[subprocess.Popen] = None
        self.health_url = f"http://{host}:{port}/health"
        self.base_url = f"http://{host}:{port}"

    def start_server(self) -> bool:
        """Start server if not running."""
        logger.info("🚀 Starting server...")
        try:
            self.server_process = subprocess.Popen(
                ["./venv/bin/python", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            time.sleep(3)  # Give server time to start
            logger.info("✅ Server started")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            return False

    def stop_server(self):
        """Stop server gracefully."""
        if self.server_process:
            logger.info("🛑 Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            logger.info("✅ Server stopped")

    def check_server_health(self) -> bool:
        """Check if server is healthy."""
        try:
            response = requests.get(self.health_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    async def ensure_server_running(self) -> bool:
        """Ensure server is running and healthy."""
        logger.info("🔍 Checking server status...")

        # First check if server is already running
        if self.check_server_health():
            logger.info("✅ Server is already running and healthy")
            return True

        # Start server if not running
        if not self.start_server():
            raise Exception("Failed to start server")

        # Wait for server to be ready with exponential backoff
        for attempt in range(5):
            await asyncio.sleep(2)
            if self.check_server_health():
                logger.info("✅ Server is running and healthy")
                return True

        raise Exception("Server failed to start after multiple attempts")

    async def api_request_with_retry(self, url: str, method: str = "GET", **kwargs):
        """Make API request with optimized retry logic."""
        for attempt in range(3):
            try:
                response = requests.request(method, url, timeout=10, **kwargs)
                return response
            except requests.exceptions.ConnectionError as e:
                if attempt == 2:  # Last attempt
                    raise e
                logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(1)
            except Exception as e:
                if attempt == 2:
                    raise e
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(1)

    def cleanup(self):
        """Clean up server resources."""
        self.stop_server()
