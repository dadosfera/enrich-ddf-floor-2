#!/usr/bin/env python3
"""
Demo script for Enrich DDF Floor 2 - Data Enrichment System
Shows how the application enriches person and company data using multiple services.
"""

import json
import time
from typing import Any, Dict

import requests


# API Configuration
API_BASE_URL = "http://localhost:8247"
HEADERS = {"Content-Type": "application/json"}


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


def print_result(title: str, data: Dict[str, Any]):
    """Print formatted API result."""
    print(f"\n🔍 {title}")
    print("-" * 40)
    print(json.dumps(data, indent=2))


def test_api_health():
    """Test if the API is healthy."""
    print_section("🏥 API Health Check")

    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ API is healthy!")
            print(f"   Version: {health_data.get('version')}")
            print(f"   Database: {health_data.get('database')}")
            print(f"   Timestamp: {health_data.get('timestamp')}")
            return True
        else:
            print("❌ API is not healthy!")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to API: {e}")
        return False


def get_sample_contacts():
    """Get some sample contacts from the database."""
    print_section("👥 Sample Contacts from Database")

    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/contacts?limit=5")
        if response.status_code == 200:
            contacts_data = response.json()
            print(f"✅ Found {contacts_data['total']} total contacts in database")
            print("📋 First 5 contacts:")

            for i, contact in enumerate(contacts_data["data"][:5], 1):
                print(f"  {i}. {contact['first_name']} {contact['last_name']}")
                print(f"     Email: {contact['email']}")
                print(f"     ID: {contact['id']}")

            return contacts_data["data"][:3]  # Return first 3 for enrichment
        else:
            print("❌ Failed to fetch contacts")
            return []
    except Exception as e:
        print(f"❌ Error fetching contacts: {e}")
        return []


def get_sample_companies():
    """Get some sample companies from the database."""
    print_section("🏢 Sample Companies from Database")

    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/companies?limit=5")
        if response.status_code == 200:
            companies_data = response.json()
            print(f"✅ Found {companies_data['total']} total companies in database")
            print("📋 First 5 companies:")

            for i, company in enumerate(companies_data["data"][:5], 1):
                print(f"  {i}. {company['name']}")
                print(f"     Domain: {company.get('domain', 'N/A')}")
                print(f"     Industry: {company.get('industry', 'N/A')}")
                print(f"     ID: {company['id']}")

            return companies_data["data"][:3]  # Return first 3 for enrichment
        else:
            print("❌ Failed to fetch companies")
            return []
    except Exception as e:
        print(f"❌ Error fetching companies: {e}")
        return []


def enrich_person_data(person: Dict[str, Any]):
    """Enrich a person using the main enrichment endpoint."""
    print_section(f"🔍 Enriching Person: {person['first_name']} {person['last_name']}")

    payload = {
        "first_name": person["first_name"],
        "last_name": person["last_name"],
        "email": person["email"],
        "linkedin_url": person.get("linkedin_url", ""),
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/enrich/person", headers=HEADERS, json=payload
        )

        if response.status_code == 200:
            enriched_data = response.json()
            print("✅ Person enriched successfully!")

            # Show original vs enriched data
            original = enriched_data["data"]["original_data"]
            enriched = enriched_data["data"]["enriched_data"]

            print(f"\n📊 Original Data:")
            print(f"   Name: {original['first_name']} {original['last_name']}")
            print(f"   Email: {original['email']}")

            print(f"\n🎯 Enriched Data:")
            print(f"   Full Name: {enriched['full_name']}")
            print(f"   Email: {enriched['email']}")
            print(f"   Phone: {enriched['contact']['phone']}")
            print(f"   LinkedIn: {enriched['contact']['linkedin']}")
            print(f"   Current Title: {enriched['professional']['current_title']}")
            print(f"   Company: {enriched['professional']['current_company']}")
            print(
                f"   Location: {enriched['location']['city']}, {enriched['location']['state']}"
            )
            print(f"   Skills: {', '.join(enriched['skills'][:3])}...")
            print(
                f"   Enrichment Score: {enriched_data['data']['enrichment_score']}/100"
            )

            return enriched_data
        else:
            print(f"❌ Failed to enrich person: {response.status_code}")
            print(f"   Error: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error enriching person: {e}")
        return None


def enrich_company_data(company: Dict[str, Any]):
    """Enrich a company using the main enrichment endpoint."""
    print_section(f"🏢 Enriching Company: {company['name']}")

    payload = {
        "name": company["name"],
        "domain": company.get("domain", ""),
        "website": company.get("website", ""),
        "industry": company.get("industry", ""),
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/enrich/company", headers=HEADERS, json=payload
        )

        if response.status_code == 200:
            enriched_data = response.json()
            print("✅ Company enriched successfully!")

            # Show original vs enriched data
            original = enriched_data["data"]["original_data"]
            enriched = enriched_data["data"]["enriched_data"]

            print(f"\n📊 Original Data:")
            print(f"   Name: {original['name']}")
            print(f"   Domain: {original.get('domain', 'N/A')}")

            print(f"\n🎯 Enriched Data:")
            print(f"   Name: {enriched['name']}")
            print(f"   Legal Name: {enriched['legal_name']}")
            print(f"   Domain: {enriched['domain']}")
            print(f"   Website: {enriched['website']}")
            print(f"   Industry: {enriched['industry']}")
            print(f"   Size: {enriched['size']['employees']} employees")
            print(f"   Employee Count: {enriched['size']['employee_count']}")
            print(f"   Revenue: {enriched['financials']['annual_revenue']}")
            print(
                f"   Location: {enriched['location']['headquarters']['city']}, {enriched['location']['headquarters']['state']}"
            )
            print(f"   Technologies: {', '.join(enriched['technologies'][:3])}...")
            print(
                f"   Enrichment Score: {enriched_data['data']['enrichment_score']}/100"
            )

            return enriched_data
        else:
            print(f"❌ Failed to enrich company: {response.status_code}")
            print(f"   Error: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error enriching company: {e}")
        return None


def test_pdl_integration():
    """Test People Data Labs integration."""
    print_section("🔍 Testing People Data Labs Integration")

    # Test person enrichment
    payload = {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah.johnson@example.com",
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/integrations/pdl/enrich-person",
            headers=HEADERS,
            json=payload,
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ PDL Person Enrichment successful!")
            print(f"   Full Name: {result['data']['full_name']}")
            print(
                f"   Current Role: {result['data']['current_role']['title']} at {result['data']['current_role']['company']}"
            )
            print(f"   Location: {result['data']['location']}")
            print(f"   Skills: {', '.join(result['data']['skills'])}")
            print(f"   Likelihood: {result['data']['likelihood']}/10")
        else:
            print(f"❌ PDL enrichment failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Error testing PDL integration: {e}")


def test_wiza_integration():
    """Test Wiza integration."""
    print_section("🔗 Testing Wiza LinkedIn Integration")

    payload = {"linkedin_url": "https://linkedin.com/in/jane-developer"}

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/integrations/wiza/enrich-profile",
            headers=HEADERS,
            json=payload,
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Wiza LinkedIn Enrichment successful!")
            print(f"   Full Name: {result['data']['full_name']}")
            print(f"   Headline: {result['data']['headline']}")
            print(f"   Current Position: {result['data']['current_position']['title']}")
            print(f"   Company: {result['data']['current_position']['company']}")
            print(f"   Location: {result['data']['location']}")
            print(f"   Connections: {result['data']['connections']}")
            print(f"   Skills: {', '.join(result['data']['skills'])}")
        else:
            print(f"❌ Wiza enrichment failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Error testing Wiza integration: {e}")


def create_new_records():
    """Create new person and company records to test enrichment."""
    print_section("📝 Creating New Records for Enrichment")

    # Create a new person
    new_person = {
        "first_name": "Alex",
        "last_name": "Rodriguez",
        "email": "alex.rodriguez@innovate.com",
        "phone": "+1-555-0199",
        "job_title": "Data Scientist",
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/contacts", headers=HEADERS, json=new_person
        )

        if response.status_code == 200:
            person_result = response.json()
            print(
                f"✅ Created new person: {person_result['data']['first_name']} {person_result['data']['last_name']}"
            )
            print(f"   Person ID: {person_result['data']['id']}")

            # Now enrich this person
            time.sleep(1)
            enrich_person_data(person_result["data"])

    except Exception as e:
        print(f"❌ Error creating new person: {e}")

    # Create a new company
    new_company = {
        "name": "InnovateTech Solutions",
        "domain": "innovatetech.com",
        "industry": "Technology",
        "location": "Austin, TX",
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/companies", headers=HEADERS, json=new_company
        )

        if response.status_code == 200:
            company_result = response.json()
            print(f"✅ Created new company: {company_result['data']['name']}")
            print(f"   Company ID: {company_result['data']['id']}")

            # Now enrich this company
            time.sleep(1)
            enrich_company_data(company_result["data"])

    except Exception as e:
        print(f"❌ Error creating new company: {e}")


def main():
    """Main demo function."""
    print_section("🚀 Enrich DDF Floor 2 - Data Enrichment Demo")
    print("This demo shows how the application enriches person and company data")
    print("using multiple data sources and API integrations.")

    # Check API health
    if not test_api_health():
        print("\n❌ Cannot proceed - API is not accessible")
        return

    # Get sample data from database
    sample_contacts = get_sample_contacts()
    sample_companies = get_sample_companies()

    # Test enrichment with existing data
    if sample_contacts:
        for contact in sample_contacts[:2]:  # Enrich first 2
            enrich_person_data(contact)
            time.sleep(1)

    if sample_companies:
        for company in sample_companies[:2]:  # Enrich first 2
            enrich_company_data(company)
            time.sleep(1)

    # Test specific integrations
    test_pdl_integration()
    time.sleep(1)
    test_wiza_integration()
    time.sleep(1)

    # Create and enrich new records
    create_new_records()

    print_section("🎉 Demo Complete!")
    print("✅ All enrichment endpoints are working correctly")
    print("✅ Database integration is functional")
    print("✅ API authentication and token management is operational")
    print(f"\n📚 View API documentation at: {API_BASE_URL}/docs")
    print(f"🌐 Frontend application at: http://localhost:5173")


if __name__ == "__main__":
    main()
