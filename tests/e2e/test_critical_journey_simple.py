#!/usr/bin/env python3
"""
Simple E2E Test for Critical User Journey - Enrich DDF Floor 2

This script tests the complete critical user journey using direct API calls
to ensure all functionality works correctly.
"""

import sys
import time

import requests


def test_health_check(base_url):
    """Test that the application is healthy and accessible."""
    print("🔍 Testing application health check...")

    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        response.raise_for_status()

        health_data = response.json()

        # Validate health response structure
        assert "status" in health_data
        assert "version" in health_data
        assert "database" in health_data
        assert health_data["status"] == "healthy"
        assert health_data["database"] == "connected"

        print(
            f"✅ Health check passed - Status: {health_data['status']}, "
            f"Version: {health_data['version']}"
        )
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_root_endpoint(base_url):
    """Test the root endpoint of the application."""
    print("🔍 Testing root endpoint...")

    try:
        response = requests.get(f"{base_url}/", timeout=10)
        response.raise_for_status()

        root_data = response.json()

        # Verify basic application info is present
        assert "message" in root_data or "title" in root_data or "version" in root_data

        print("✅ Root endpoint verification passed")
        return True
    except Exception as e:
        print(f"❌ Root endpoint test failed: {e}")
        return False


def test_create_company(base_url, test_data):
    """Test creating a company via the API."""
    print("🔍 Testing company creation...")

    try:
        response = requests.post(
            f"{base_url}/api/v1/companies", json=test_data["company"], timeout=10
        )
        response.raise_for_status()

        response_data = response.json()

        # Handle the actual response format
        if "data" in response_data:
            data = response_data["data"]
        else:
            data = response_data

        assert "id" in data
        assert data["name"] == test_data["company"]["name"]

        print(f"✅ Company created successfully - ID: {response_data['id']}")
        return True, response_data["id"]
    except Exception as e:
        print(f"❌ Company creation test failed: {e}")
        return False, None


def test_create_contact(base_url, test_data):
    """Test creating a contact via the API."""
    print("🔍 Testing contact creation...")

    try:
        response = requests.post(
            f"{base_url}/api/v1/contacts", json=test_data["contact"], timeout=10
        )
        response.raise_for_status()

        response_data = response.json()

        # Handle the actual response format
        if "data" in response_data:
            data = response_data["data"]
        else:
            data = response_data

        assert "id" in data
        assert data["first_name"] == test_data["contact"]["first_name"]
        assert data["last_name"] == test_data["contact"]["last_name"]
        assert data["email"] == test_data["contact"]["email"]

        print(f"✅ Contact created successfully - ID: {response_data['id']}")
        return True, response_data["id"]
    except Exception as e:
        print(f"❌ Contact creation test failed: {e}")
        return False, None


def test_create_product(base_url, test_data):
    """Test creating a product via the API."""
    print("🔍 Testing product creation...")

    try:
        response = requests.post(
            f"{base_url}/api/v1/products", json=test_data["product"], timeout=10
        )
        response.raise_for_status()

        response_data = response.json()

        # Handle the actual response format
        if "data" in response_data:
            data = response_data["data"]
        else:
            data = response_data

        assert "id" in data
        assert data["name"] == test_data["product"]["name"]
        assert data["description"] == test_data["product"]["description"]
        assert float(data["price"]) == test_data["product"]["price"]

        print(f"✅ Product created successfully - ID: {response_data['id']}")
        return True, response_data["id"]
    except Exception as e:
        print(f"❌ Product creation test failed: {e}")
        return False, None


def test_list_companies(base_url, test_data):
    """Test listing companies and verify our test company is present."""
    print("🔍 Testing companies list...")

    try:
        response = requests.get(f"{base_url}/api/v1/companies", timeout=10)
        response.raise_for_status()

        companies_data = response.json()

        # Verify our test company is in the list
        test_company_found = any(
            company["name"] == test_data["company"]["name"]
            for company in companies_data  # TODO: Review loop variable naming (PLW2901)
        )
        assert test_company_found, "Test company not found in companies list"

        print("✅ Companies list verification passed")
        return True
    except Exception as e:
        print(f"❌ Companies list test failed: {e}")
        return False


def test_list_contacts(base_url, test_data):
    """Test listing contacts and verify our test contact is present."""
    print("🔍 Testing contacts list...")

    try:
        response = requests.get(f"{base_url}/api/v1/contacts", timeout=10)
        response.raise_for_status()

        contacts_data = response.json()

        # Verify our test contact is in the list
        test_contact_found = any(
            contact["email"] == test_data["contact"]["email"]
            for contact in contacts_data  # TODO: Review loop variable naming (PLW2901)
        )
        assert test_contact_found, "Test contact not found in contacts list"

        print("✅ Contacts list verification passed")
        return True
    except Exception as e:
        print(f"❌ Contacts list test failed: {e}")
        return False


def test_list_products(base_url, test_data):
    """Test listing products and verify our test product is present."""
    print("🔍 Testing products list...")

    try:
        response = requests.get(f"{base_url}/api/v1/products", timeout=10)
        response.raise_for_status()

        products_data = response.json()

        # Verify our test product is in the list
        test_product_found = any(
            product["name"] == test_data["product"]["name"] for product in products_data  # TODO: Review loop variable naming (PLW2901)
        )
        assert test_product_found, "Test product not found in products list"

        print("✅ Products list verification passed")
        return True
    except Exception as e:
        print(f"❌ Products list test failed: {e}")
        return False


def main():
    """Run all E2E tests."""
    base_url = "http://127.0.0.1:8000"

    test_data = {
        "company": {
            "name": "Test Company E2E",
            "domain": "testcompany-e2e-unique.com",
            "industry": "Technology",
            "website": "https://testcompany-e2e.com",
            "description": "Test company for E2E testing",
        },
        "contact": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe.e2e@testcompany-e2e.com",
            "phone": "+1-555-0123",
            "job_title": "Software Engineer",
        },
        "product": {
            "name": "Test Product E2E",
            "sku": "TEST-PROD-E2E-001",
            "description": "A test product for E2E testing",
            "price": 99.99,
            "category": "Software",
        },
    }

    print("🚀 Starting E2E Tests for Enrich DDF Floor 2")
    print("=" * 50)

    # Run all tests
    tests = [
        ("Health Check", lambda: test_health_check(base_url)),
        ("Root Endpoint", lambda: test_root_endpoint(base_url)),
        ("Create Company", lambda: test_create_company(base_url, test_data)),
        ("Create Contact", lambda: test_create_contact(base_url, test_data)),
        ("Create Product", lambda: test_create_product(base_url, test_data)),
        ("List Companies", lambda: test_list_companies(base_url, test_data)),
        ("List Contacts", lambda: test_list_contacts(base_url, test_data)),
        ("List Products", lambda: test_list_products(base_url, test_data)),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
        time.sleep(1)  # Brief pause between tests

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All critical user journey tests completed successfully!")
        print("✅ Application is fully functional and ready for use!")
        return 0
    else:
        print("❌ Some tests failed. Please check the application.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
