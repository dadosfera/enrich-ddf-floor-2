"""
Clearbit API Integration for Company & Person Enrichment
Free tier: 50 requests/month
"""

import os
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ClearbitService:
    """Clearbit API service for person and company enrichment."""
    
    def __init__(self):
        from config import settings
        self.api_key = settings.clearbit_api_key
        self.base_url = 'https://person.clearbit.com/v2'
        self.company_url = 'https://company.clearbit.com/v2'
        
        if not self.api_key:
            logger.warning("Clearbit API key not found. Set CLEARBIT_API_KEY environment variable.")
    
    async def enrich_person(self, email: str) -> Dict[str, Any]:
        """Enrich person data using Clearbit Person API."""
        if not self.api_key:
            return {"success": False, "error": "API key not configured"}
        
        try:
            url = f"{self.base_url}/find"
            headers = {'Authorization': f'Bearer {self.api_key}'}
            params = {'email': email}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    "success": True,
                    "person": {
                        "email": data.get('email'),
                        "full_name": data.get('name', {}).get('fullName'),
                        "first_name": data.get('name', {}).get('givenName'),
                        "last_name": data.get('name', {}).get('familyName'),
                        "avatar": data.get('avatar'),
                        "location": data.get('location'),
                        "bio": data.get('bio'),
                        "site": data.get('site'),
                        "linkedin": data.get('linkedin', {}).get('handle'),
                        "twitter": data.get('twitter', {}).get('handle'),
                        "github": data.get('github', {}).get('handle')
                    },
                    "employment": data.get('employment', {}),
                    "company": data.get('company', {})
                }
            elif response.status_code == 202:
                # Clearbit is processing the request
                return {"success": False, "error": "Processing, try again later", "status": "processing"}
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Clearbit person enrichment error: {e}")
            return {"success": False, "error": str(e)}
    
    async def enrich_company(self, domain: str) -> Dict[str, Any]:
        """Enrich company data using Clearbit Company API."""
        if not self.api_key:
            return {"success": False, "error": "API key not configured"}
        
        try:
            url = f"{self.company_url}/find"
            headers = {'Authorization': f'Bearer {self.api_key}'}
            params = {'domain': domain}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    "success": True,
                    "company": {
                        "name": data.get('name'),
                        "domain": data.get('domain'),
                        "description": data.get('description'),
                        "logo": data.get('logo'),
                        "website": data.get('site', {}).get('url'),
                        "phone": data.get('phone'),
                        "email": data.get('site', {}).get('emailAddress'),
                        "employees": data.get('metrics', {}).get('employees'),
                        "estimated_annual_revenue": data.get('metrics', {}).get('estimatedAnnualRevenue'),
                        "raised": data.get('metrics', {}).get('raised'),
                        "alexa_us_rank": data.get('metrics', {}).get('alexaUsRank'),
                        "alexa_global_rank": data.get('metrics', {}).get('alexaGlobalRank'),
                        "founded_year": data.get('foundedYear'),
                        "location": data.get('geo', {}),
                        "industry": data.get('category', {}).get('industry'),
                        "tags": data.get('tags', []),
                        "tech_stack": data.get('tech', []),
                        "linkedin": data.get('linkedin', {}).get('handle'),
                        "twitter": data.get('twitter', {}).get('handle'),
                        "facebook": data.get('facebook', {}).get('handle')
                    }
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Clearbit company enrichment error: {e}")
            return {"success": False, "error": str(e)}
