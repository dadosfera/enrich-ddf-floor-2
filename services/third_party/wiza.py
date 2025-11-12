"""
Wiza API Integration for LinkedIn Profile Enrichment and Email Finding
Professional LinkedIn data extraction platform
"""

import logging
from typing import Any, Dict, Optional

import requests


logger = logging.getLogger(__name__)


class WizaService:
    """Wiza API service for LinkedIn profile enrichment and email finding."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.wiza.co/api/v1"

        if not self.api_key:
            logger.warning(
                "Wiza API key not provided. Set WIZA_API_KEY environment variable or pass api_key parameter."
            )

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Wiza API requests."""
        if not self.api_key:
            raise ValueError("Wiza API key not configured")

        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Enrich-DDF-Floor-2/1.0",
        }

    async def enrich_linkedin_profile(
        self, linkedin_url: str, include_emails: bool = True, include_phone: bool = True
    ) -> Dict[str, Any]:
        """Enrich LinkedIn profile using Wiza API."""
        try:
            payload = {
                "linkedin_url": linkedin_url,
                "include_emails": include_emails,
                "include_phone": include_phone,
            }

            response = requests.post(
                f"{self.base_url}/enrich/profile",
                headers=self._get_headers(),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "profile": self._transform_profile_response(data),
                "credits_used": data.get("credits_used", 0),
                "credits_remaining": data.get("credits_remaining", 0),
                "message": "LinkedIn profile enriched successfully",
            }

        except Exception as e:
            logger.exception(f"Wiza LinkedIn profile enrichment error: {e}")
            return {"success": False, "error": str(e)}

    async def find_email(
        self,
        first_name: str,
        last_name: str,
        company_domain: str,
        linkedin_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Find email for a person using Wiza API."""
        try:
            payload = {
                "first_name": first_name,
                "last_name": last_name,
                "company_domain": company_domain,
            }

            if linkedin_url:
                payload["linkedin_url"] = linkedin_url

            response = requests.post(
                f"{self.base_url}/enrich/email",
                headers=self._get_headers(),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "emails": data.get("emails", []),
                "credits_used": data.get("credits_used", 0),
                "credits_remaining": data.get("credits_remaining", 0),
                "message": f"Found {len(data.get('emails', []))} email(s)",
            }

        except Exception as e:
            logger.exception(f"Wiza email finding error: {e}")
            return {"success": False, "error": str(e), "emails": []}

    async def enrich_company(
        self,
        company_domain: Optional[str] = None,
        company_name: Optional[str] = None,
        linkedin_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Enrich company data using Wiza API."""
        try:
            payload = {}

            if company_domain:
                payload["company_domain"] = company_domain
            if company_name:
                payload["company_name"] = company_name
            if linkedin_url:
                payload["linkedin_url"] = linkedin_url

            if not payload:
                raise ValueError("At least one company identifier is required")

            response = requests.post(
                f"{self.base_url}/enrich/company",
                headers=self._get_headers(),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "company": self._transform_company_response(data),
                "credits_used": data.get("credits_used", 0),
                "credits_remaining": data.get("credits_remaining", 0),
                "message": "Company enriched successfully",
            }

        except Exception as e:
            logger.exception(f"Wiza company enrichment error: {e}")
            return {"success": False, "error": str(e)}

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
                "credits": data.get("credits", 0),
                "message": "Credits retrieved successfully",
            }

        except Exception as e:
            logger.exception(f"Wiza credits check error: {e}")
            return {"success": False, "error": str(e)}

    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            response = requests.get(
                f"{self.base_url}/credits", headers=self._get_headers(), timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.exception(f"Wiza connection test failed: {e}")
            return False

    def _transform_profile_response(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Wiza profile response to standardized format."""
        return {
            "linkedin_url": raw_data.get("linkedin_url", ""),
            "first_name": raw_data.get("first_name", ""),
            "last_name": raw_data.get("last_name", ""),
            "full_name": raw_data.get("full_name", ""),
            "headline": raw_data.get("headline"),
            "summary": raw_data.get("summary"),
            "location": raw_data.get("location"),
            "industry": raw_data.get("industry"),
            "current_company": raw_data.get("current_company"),
            "previous_companies": raw_data.get("previous_companies", []),
            "education": raw_data.get("education", []),
            "skills": raw_data.get("skills", []),
            "emails": raw_data.get("emails", []),
            "phones": raw_data.get("phones", []),
            "social_profiles": raw_data.get("social_profiles", {}),
            "profile_image_url": raw_data.get("profile_image_url"),
            "connections_count": raw_data.get("connections_count"),
            "followers_count": raw_data.get("followers_count"),
        }

    def _transform_company_response(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Wiza company response to standardized format."""
        return {
            "company_name": raw_data.get("company_name", ""),
            "domain": raw_data.get("domain", ""),
            "linkedin_url": raw_data.get("linkedin_url"),
            "website": raw_data.get("website"),
            "industry": raw_data.get("industry"),
            "company_size": raw_data.get("company_size"),
            "founded_year": raw_data.get("founded_year"),
            "headquarters": raw_data.get("headquarters"),
            "description": raw_data.get("description"),
            "specialties": raw_data.get("specialties", []),
            "employee_count": raw_data.get("employee_count"),
            "revenue_range": raw_data.get("revenue_range"),
            "social_profiles": raw_data.get("social_profiles", {}),
            "employees": raw_data.get("employees", []),
            "technologies": raw_data.get("technologies", []),
            "company_type": raw_data.get("company_type"),
            "stock_symbol": raw_data.get("stock_symbol"),
        }
