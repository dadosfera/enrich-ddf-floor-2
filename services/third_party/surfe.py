"""
Surfe API Integration for People and Company Search/Enrichment
Professional B2B data platform
"""

import logging
from typing import Any, Dict, List, Optional

import requests


logger = logging.getLogger(__name__)


class SurfeService:
    """Surfe API service for people and company search and enrichment."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.surfe.com/v2"

        if not self.api_key:
            logger.warning(
                "Surfe API key not provided. Set SURFE_API_KEY environment variable or pass api_key parameter."
            )

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Surfe API requests."""
        if not self.api_key:
            raise ValueError("Surfe API key not configured")

        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Enrich-DDF-Floor-2/1.0",
        }

    async def search_people(
        self, filters: Dict[str, Any], limit: int = 10, offset: int = 0
    ) -> Dict[str, Any]:
        """Search for people using Surfe API."""
        try:
            payload = {"filters": filters, "limit": limit, "offset": offset}

            response = requests.post(
                f"{self.base_url}/people/search",
                headers=self._get_headers(),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "people": data.get("people", []),
                "total_count": data.get("total_count", 0),
                "message": f"Found {len(data.get('people', []))} people",
            }

        except Exception as e:
            logger.exception(f"Surfe people search error: {e}")
            return {"success": False, "error": str(e), "people": []}

    async def enrich_people(
        self,
        people_data: List[Dict[str, Any]],
        include_email: bool = True,
        include_mobile: bool = False,
    ) -> Dict[str, Any]:
        """Enrich people data using Surfe API."""
        try:
            payload = {
                "include": {
                    "email": include_email,
                    "mobile": include_mobile,
                    "linkedin": True,
                },
                "people": people_data,
            }

            response = requests.post(
                f"{self.base_url}/people/enrich",
                headers=self._get_headers(),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "people": data.get("people", []),
                "credits_used": data.get("credits_used", {}),
                "credits_remaining": data.get("credits_remaining", {}),
                "message": f"Enriched {len(data.get('people', []))} people",
            }

        except Exception as e:
            logger.exception(f"Surfe people enrichment error: {e}")
            return {"success": False, "error": str(e), "people": []}

    async def search_companies(
        self, filters: Dict[str, Any], limit: int = 10, offset: int = 0
    ) -> Dict[str, Any]:
        """Search for companies using Surfe API."""
        try:
            payload = {"filters": filters, "limit": limit, "offset": offset}

            response = requests.post(
                f"{self.base_url}/companies/search",
                headers=self._get_headers(),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "companies": data.get("companies", []),
                "total_count": data.get("total_count", 0),
                "message": f"Found {len(data.get('companies', []))} companies",
            }

        except Exception as e:
            logger.exception(f"Surfe company search error: {e}")
            return {"success": False, "error": str(e), "companies": []}

    async def enrich_companies(
        self, companies_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Enrich company data using Surfe API."""
        try:
            payload = {"companies": companies_data}

            response = requests.post(
                f"{self.base_url}/companies/enrich",
                headers=self._get_headers(),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "companies": data.get("companies", []),
                "message": f"Enriched {len(data.get('companies', []))} companies",
            }

        except Exception as e:
            logger.exception(f"Surfe company enrichment error: {e}")
            return {"success": False, "error": str(e), "companies": []}

    async def get_credits(self) -> Dict[str, Any]:
        """Get account credits information."""
        try:
            response = requests.get(
                f"{self.base_url}/credits", headers=self._get_headers(), timeout=10
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "credits": data,
                "message": "Credits retrieved successfully",
            }

        except Exception as e:
            logger.exception(f"Surfe credits check error: {e}")
            return {"success": False, "error": str(e)}

    async def get_filters(self) -> Dict[str, Any]:
        """Get available search filters."""
        try:
            response = requests.get(
                f"{self.base_url}/filters", headers=self._get_headers(), timeout=10
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "filters": data,
                "message": "Filters retrieved successfully",
            }

        except Exception as e:
            logger.exception(f"Surfe filters error: {e}")
            return {"success": False, "error": str(e)}

    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            response = requests.get(
                f"{self.base_url}/credits", headers=self._get_headers(), timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.exception(f"Surfe connection test failed: {e}")
            return False
