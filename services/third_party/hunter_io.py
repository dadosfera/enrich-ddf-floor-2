"""
Hunter.io API Integration for Email Enrichment
Free tier: 50 searches/month
"""

import logging
from typing import Any, Dict

import requests


logger = logging.getLogger(__name__)


class HunterIOService:
    """Hunter.io API service for email finding and verification."""

    def __init__(self):
        from config import settings

        self.api_key = settings.hunter_api_key
        self.base_url = "https://api.hunter.io/v2"

        if not self.api_key:
            logger.warning(
                "Hunter.io API key not found. Set HUNTER_API_KEY environment variable."
            )

    async def find_email(
        self, first_name: str, last_name: str, domain: str
    ) -> Dict[str, Any]:
        """Find email address using Hunter.io API."""
        if not self.api_key:
            return {"success": False, "error": "API key not configured"}

        try:
            url = f"{self.base_url}/email-finder"
            params = {
                "domain": domain,
                "first_name": first_name,
                "last_name": last_name,
                "api_key": self.api_key,
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("data", {}).get("email"):
                return {
                    "success": True,
                    "email": data["data"]["email"],
                    "confidence": data["data"]["confidence"],
                    "sources": data["data"]["sources"],
                    "verification_status": data["data"]["verification"]["result"],
                }
            else:
                return {"success": False, "error": "Email not found"}

        except Exception as e:
            logger.error(f"Hunter.io API error: {e}")
            return {"success": False, "error": str(e)}

    async def verify_email(self, email: str) -> Dict[str, Any]:
        """Verify email address using Hunter.io."""
        if not self.api_key:
            return {"success": False, "error": "API key not configured"}

        try:
            url = f"{self.base_url}/email-verifier"
            params = {"email": email, "api_key": self.api_key}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                "success": True,
                "result": data["data"]["result"],
                "score": data["data"]["score"],
                "email": data["data"]["email"],
                "regexp": data["data"]["regexp"],
                "gibberish": data["data"]["gibberish"],
                "disposable": data["data"]["disposable"],
                "webmail": data["data"]["webmail"],
                "mx_records": data["data"]["mx_records"],
                "smtp_server": data["data"]["smtp_server"],
                "smtp_check": data["data"]["smtp_check"],
                "accept_all": data["data"]["accept_all"],
            }

        except Exception as e:
            logger.error(f"Hunter.io verification error: {e}")
            return {"success": False, "error": str(e)}
