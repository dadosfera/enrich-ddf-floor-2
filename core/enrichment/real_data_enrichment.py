"""
Real Data Enrichment Engine
Integrates with actual APIs to provide real enrichment data
"""

import logging

# Import real API services
from datetime import datetime
from typing import Any, Dict


logger = logging.getLogger(__name__)


class QuotaManager:
    """Manages API quota limits for free tier services."""

    def __init__(self):
        self.limits = {
            "hunter": {"monthly": 50, "used": 0, "reset_date": None},
            "clearbit": {"monthly": 50, "used": 0, "reset_date": None},
            "zerobounce": {"monthly": 100, "used": 0, "reset_date": None},
            "fullcontact": {"monthly": 1000, "used": 0, "reset_date": None},
        }

    def can_make_request(self, service: str) -> bool:
        """Check if we can make a request within quota limits."""
        if service not in self.limits:
            return False
        return self.limits[service]["used"] < self.limits[service]["monthly"]

    def record_request(self, service: str):
        """Record that a request was made."""
        if service in self.limits:
            self.limits[service]["used"] += 1


class RealDataEnrichmentEngine:
    """Real data enrichment using actual API services."""

    def __init__(self):
        self.quota_manager = QuotaManager()
        self.services = {}
        self._initialize_services()

    def _initialize_services(self):
        """Initialize available API services."""
        # Import settings to access API keys
        from config import settings

        try:
            # Try to import Hunter.io service
            if settings.hunter_api_key:
                from services.third_party.hunter_io import HunterIOService

                self.services["hunter"] = HunterIOService()
                logger.info("✅ Hunter.io service initialized")
            else:
                logger.warning("❌ Hunter.io API key not found")
        except ImportError:
            logger.warning("❌ Hunter.io service not available")

        try:
            # Try to import Clearbit service
            if settings.clearbit_api_key:
                from services.third_party.clearbit import ClearbitService

                self.services["clearbit"] = ClearbitService()
                logger.info("✅ Clearbit service initialized")
            else:
                logger.warning("❌ Clearbit API key not found")
        except ImportError:
            logger.warning("❌ Clearbit service not available")

    async def enrich_person_real(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich person data using real APIs with fallback to mock."""
        email = person_data.get("email")
        first_name = person_data.get("first_name", "")
        last_name = person_data.get("last_name", "")

        enriched_data = {
            "full_name": f"{first_name} {last_name}".strip(),
            "email": email,
            "data_sources": [],
            "enrichment_score": 0,
            "professional": {},
            "contact": {},
            "location": {},
            "social": {},
            "skills": [],
            "education": {},
        }

        # Try Clearbit first (best quality)
        if (
            "clearbit" in self.services
            and self.quota_manager.can_make_request("clearbit")
            and email
        ):
            try:
                result = await self.services["clearbit"].enrich_person(email)
                if result.get("success"):
                    self._merge_clearbit_data(enriched_data, result)
                    self.quota_manager.record_request("clearbit")
                    enriched_data["data_sources"].append("clearbit")
                    logger.info(f"✅ Clearbit enrichment successful for {email}")
            except Exception as e:
                logger.error(f"Clearbit error: {e}")

        # Try Hunter.io for email verification
        if (
            "hunter" in self.services
            and self.quota_manager.can_make_request("hunter")
            and email
        ):
            try:
                result = await self.services["hunter"].verify_email(email)
                if result.get("success"):
                    self._merge_hunter_data(enriched_data, result)
                    self.quota_manager.record_request("hunter")
                    enriched_data["data_sources"].append("hunter")
                    logger.info(f"✅ Hunter.io verification successful for {email}")
            except Exception as e:
                logger.error(f"Hunter.io error: {e}")

        # Calculate enrichment score based on filled fields
        enriched_data["enrichment_score"] = self._calculate_enrichment_score(
            enriched_data
        )

        # If no real data was obtained, use enhanced mock data
        if not enriched_data["data_sources"]:
            logger.info("🔄 Falling back to mock data - no real APIs available")
            return self._generate_enhanced_mock_data(person_data)

        enriched_data["enriched_at"] = datetime.utcnow().isoformat()
        return enriched_data

    def _merge_clearbit_data(self, enriched_data: Dict, clearbit_result: Dict):
        """Merge Clearbit API response into enriched data."""
        person = clearbit_result.get("person", {})
        employment = clearbit_result.get("employment", {})
        company = clearbit_result.get("company", {})

        if person:
            enriched_data["full_name"] = (
                person.get("full_name") or enriched_data["full_name"]
            )
            enriched_data["contact"]["linkedin"] = person.get("linkedin")
            enriched_data["contact"]["twitter"] = person.get("twitter")
            enriched_data["contact"]["github"] = person.get("github")
            enriched_data["location"] = person.get("location") or {}

        if employment:
            enriched_data["professional"] = {
                "current_title": employment.get("title"),
                "current_company": employment.get("name"),
                "seniority": employment.get("seniority"),
                "role": employment.get("role"),
            }

        if company:
            enriched_data["professional"]["company_domain"] = company.get("domain")
            enriched_data["professional"]["company_industry"] = company.get(
                "category", {}
            ).get("industry")

    def _merge_hunter_data(self, enriched_data: Dict, hunter_result: Dict):
        """Merge Hunter.io API response into enriched data."""
        enriched_data["contact"]["email_verified"] = (
            hunter_result.get("result") == "deliverable"
        )
        enriched_data["contact"]["email_confidence"] = hunter_result.get("score", 0)
        enriched_data["contact"]["email_disposable"] = hunter_result.get(
            "disposable", False
        )
        enriched_data["contact"]["email_webmail"] = hunter_result.get("webmail", False)

    def _calculate_enrichment_score(self, data: Dict) -> int:
        """Calculate enrichment score based on data completeness."""
        key_fields = [
            "full_name",
            "email",
            "professional.current_title",
            "professional.current_company",
            "contact.linkedin",
            "location",
        ]

        filled_fields = 0
        for field in key_fields:
            if "." in field:
                parts = field.split(".")
                value = data
                for part in parts:
                    value = value.get(part, {}) if isinstance(value, dict) else None
                    if not value:
                        break
                if value:
                    filled_fields += 1
            else:
                if data.get(field):
                    filled_fields += 1

        return int((filled_fields / len(key_fields)) * 100)

    def _generate_enhanced_mock_data(self, person_data: Dict) -> Dict:
        """Generate enhanced mock data when real APIs are not available."""
        first_name = person_data.get("first_name", "Unknown")
        last_name = person_data.get("last_name", "Person")
        email = person_data.get(
            "email", f"{first_name.lower()}.{last_name.lower()}@example.com"
        )

        return {
            "full_name": f"{first_name} {last_name}",
            "email": email,
            "professional": {
                "current_title": "Software Engineer",
                "current_company": "Tech Innovations Inc",
                "seniority": "Senior",
                "years_experience": 5,
            },
            "contact": {
                "phone": "+1-555-0123",
                "linkedin": f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}",
            },
            "location": {
                "city": "San Francisco",
                "state": "California",
                "country": "United States",
            },
            "skills": ["Python", "JavaScript", "React", "API Development"],
            "education": {
                "degree": "Bachelor of Science",
                "field": "Computer Science",
                "university": "Tech University",
            },
            "enrichment_score": 75,
            "data_sources": ["mock_enhanced"],
            "enriched_at": datetime.utcnow().isoformat(),
            "note": "🚨 This is enhanced mock data - configure real API keys for actual enrichment",
        }

    async def enrich_company_real(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich company data using real APIs."""
        domain = company_data.get("domain")
        name = company_data.get("name")

        enriched_data = {
            "name": name,
            "domain": domain,
            "data_sources": [],
            "enrichment_score": 0,
            "industry": None,
            "employees": None,
            "revenue": None,
            "founded": None,
            "location": {},
            "tech_stack": [],
            "social": {},
        }

        # Try Clearbit for company enrichment
        if (
            "clearbit" in self.services
            and self.quota_manager.can_make_request("clearbit")
            and domain
        ):
            try:
                result = await self.services["clearbit"].enrich_company(domain)
                if result.get("success"):
                    self._merge_clearbit_company_data(enriched_data, result)
                    self.quota_manager.record_request("clearbit")
                    enriched_data["data_sources"].append("clearbit")
                    logger.info(
                        f"✅ Clearbit company enrichment successful for {domain}"
                    )
            except Exception as e:
                logger.error(f"Clearbit company error: {e}")

        enriched_data["enrichment_score"] = self._calculate_company_enrichment_score(
            enriched_data
        )

        if not enriched_data["data_sources"]:
            return self._generate_mock_company_data(company_data)

        enriched_data["enriched_at"] = datetime.utcnow().isoformat()
        return enriched_data

    def _merge_clearbit_company_data(self, enriched_data: Dict, clearbit_result: Dict):
        """Merge Clearbit company data into enriched data."""
        company = clearbit_result.get("company", {})

        if company:
            enriched_data["name"] = company.get("name") or enriched_data["name"]
            enriched_data["description"] = company.get("description")
            enriched_data["industry"] = company.get("industry")
            enriched_data["employees"] = company.get("employees")
            enriched_data["revenue"] = company.get("estimated_annual_revenue")
            enriched_data["founded"] = company.get("founded_year")
            enriched_data["location"] = company.get("location", {})
            enriched_data["tech_stack"] = company.get("tech_stack", [])
            enriched_data["social"] = {
                "linkedin": company.get("linkedin"),
                "twitter": company.get("twitter"),
                "facebook": company.get("facebook"),
            }

    def _calculate_company_enrichment_score(self, data: Dict) -> int:
        """Calculate company enrichment score."""
        key_fields = ["name", "domain", "industry", "employees", "founded", "location"]
        filled_fields = sum(1 for field in key_fields if data.get(field))
        return int((filled_fields / len(key_fields)) * 100)

    def _generate_mock_company_data(self, company_data: Dict) -> Dict:
        """Generate mock company data when real APIs are not available."""
        name = company_data.get("name", "Unknown Company")
        domain = company_data.get("domain", "example.com")

        return {
            "name": name,
            "domain": domain,
            "description": f"{name} is a leading technology company.",
            "industry": "Technology",
            "employees": 150,
            "revenue": 5000000,
            "founded": 2010,
            "location": {"city": "San Francisco", "state": "CA", "country": "USA"},
            "tech_stack": ["Python", "React", "PostgreSQL"],
            "social": {
                "linkedin": f"https://linkedin.com/company/{name.lower().replace(' ', '-')}",
                "twitter": f"https://twitter.com/{name.lower().replace(' ', '')}",
            },
            "enrichment_score": 70,
            "data_sources": ["mock_enhanced"],
            "enriched_at": datetime.utcnow().isoformat(),
            "note": "🚨 This is mock data - configure real API keys for actual enrichment",
        }


# Global instance
real_enrichment_engine = RealDataEnrichmentEngine()
