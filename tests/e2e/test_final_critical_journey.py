#!/usr/bin/env python3
"""
Final Comprehensive E2E Test for Critical User Journey - Enrich DDF Floor 2

This script completes the critical user journey without errors by testing:
1. Application startup and health
2. API functionality
3. UI interactions
4. Data creation and verification
"""

import json
import sys
import time

import requests
from playwright.sync_api import sync_playwright


def wait_for_server(base_url, max_attempts=30):
    """Wait for the server to be ready."""
    print("🔍 Waiting for server to be ready...")

    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass

        print(f"⏳ Attempt {attempt + 1}/{max_attempts} - Server not ready yet...")
        time.sleep(2)

    print("❌ Server failed to start within expected time")
    return False


def test_api_health_check(base_url):
    """Test that the application is healthy via API."""
    print("🔍 Testing API health check...")

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
            f"✅ API Health check passed - Status: {health_data['status']}, "
            f"Version: {health_data['version']}"
        )
        return True
    except Exception as e:
        print(f"❌ API Health check failed: {e}")
        return False


def test_api_root_endpoint(base_url):
    """Test the root endpoint via API."""
    print("🔍 Testing API root endpoint...")

    try:
        response = requests.get(f"{base_url}/", timeout=10)
        response.raise_for_status()

        root_data = response.json()

        # Verify basic application info is present
        assert "message" in root_data or "title" in root_data or "version" in root_data

        print("✅ API Root endpoint verification passed")
        return True
    except Exception as e:
        print(f"❌ API Root endpoint test failed: {e}")
        return False


def test_api_create_company(base_url, test_data):
    """Test creating a company via API."""
    print("🔍 Testing API company creation...")

    try:
        response = requests.post(
            f"{base_url}/api/v1/companies", json=test_data["company"], timeout=10
        )
        response.raise_for_status()

        response_data = response.json()

        # Handle the actual response format
        data = response_data.get("data", response_data)

        assert "id" in data
        assert data["name"] == test_data["company"]["name"]

        print(f"✅ API Company created successfully - ID: {data['id']}")
        return True
    except Exception as e:
        print(f"❌ API Company creation test failed: {e}")
        return False


def test_api_create_contact(base_url, test_data):
    """Test creating a contact via API."""
    print("🔍 Testing API contact creation...")

    try:
        response = requests.post(
            f"{base_url}/api/v1/contacts", json=test_data["contact"], timeout=10
        )
        response.raise_for_status()

        response_data = response.json()

        # Handle the actual response format
        data = response_data.get("data", response_data)

        assert "id" in data
        assert data["first_name"] == test_data["contact"]["first_name"]
        assert data["last_name"] == test_data["contact"]["last_name"]
        assert data["email"] == test_data["contact"]["email"]

        print(f"✅ API Contact created successfully - ID: {data['id']}")
        return True
    except Exception as e:
        print(f"❌ API Contact creation test failed: {e}")
        return False


def test_api_create_product(base_url, test_data):
    """Test creating a product via API."""
    print("🔍 Testing API product creation...")

    try:
        response = requests.post(
            f"{base_url}/api/v1/products", json=test_data["product"], timeout=10
        )
        response.raise_for_status()

        response_data = response.json()

        # Handle the actual response format
        data = response_data.get("data", response_data)

        assert "id" in data
        assert data["name"] == test_data["product"]["name"]
        assert data["description"] == test_data["product"]["description"]
        assert float(data["price"]) == test_data["product"]["price"]

        print(f"✅ API Product created successfully - ID: {data['id']}")
        return True
    except Exception as e:
        print(f"❌ API Product creation test failed: {e}")
        return False


def test_ui_api_documentation(page, base_url):
    """Test access to API documentation via UI."""
    print("🔍 Testing UI API documentation access...")

    try:
        # Navigate to API docs
        page.goto(f"{base_url}/docs")

        # Wait for Swagger UI to load
        page.wait_for_selector("div.swagger-ui", timeout=15000)

        # Verify key elements are present
        title = page.locator("h1").text_content()
        assert "Enrich DDF Floor 2" in title

        # Check for API endpoints
        companies_endpoint = page.locator("text=/api/v1/companies").first
        assert companies_endpoint.is_visible()

        contacts_endpoint = page.locator("text=/api/v1/contacts").first
        assert contacts_endpoint.is_visible()

        products_endpoint = page.locator("text=/api/v1/products").first
        assert products_endpoint.is_visible()

        print("✅ UI API documentation loaded successfully")
        return True
    except Exception as e:
        print(f"❌ UI API documentation test failed: {e}")
        return False


def test_ui_create_company_via_docs(page, base_url, test_data):
    """Test creating a company via the UI documentation."""
    print("🔍 Testing UI company creation via docs...")

    try:
        # Navigate to companies endpoint
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=15000)

        # Find and click on POST /api/v1/companies
        companies_post = page.locator("text=POST /api/v1/companies").first
        companies_post.click()

        # Click "Try it out" button
        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        # Fill in the request body
        request_body = page.locator("textarea[data-param-name='body']").first
        company_data = test_data["company"]
        request_body.fill(json.dumps(company_data, indent=2))

        # Click "Execute" button
        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        # Wait for response
        page.wait_for_selector("div.responses-wrapper", timeout=15000)

        # Verify successful response
        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        # Verify response body contains company data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        # Handle the actual response format
        data = response_data.get("data", response_data)

        assert "id" in data
        assert data["name"] == company_data["name"]

        print(f"✅ UI Company created successfully - ID: {data['id']}")
        return True
    except Exception as e:
        print(f"❌ UI Company creation test failed: {e}")
        return False


def test_ui_verify_data_creation(page, base_url, test_data):
    """Verify that created data can be retrieved via UI."""
    print("🔍 Testing UI data verification...")

    try:
        # Test GET companies endpoint via UI
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=15000)

        # Test companies list
        companies_get = page.locator("text=GET /api/v1/companies").first
        companies_get.click()

        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        page.wait_for_selector("div.responses-wrapper", timeout=15000)

        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        companies_data = json.loads(response_text)

        # Verify our test company is in the list
        test_company_found = any(
            company["name"] == test_data["company"]["name"]
            for company in companies_data
        )
        assert test_company_found, "Test company not found in companies list"

        print("✅ UI Companies list verification passed")
        print("🎉 All critical user journey tests completed successfully!")
        return True
    except Exception as e:
        print(f"❌ UI Data verification test failed: {e}")
        return False


def main():
    """Run all comprehensive E2E tests."""
    base_url = "http://127.0.0.1:8000"

    test_data = {
        "company": {
            "name": "Final Test Company E2E",
            "domain": "finaltestcompany-e2e.com",
            "industry": "Technology",
            "website": "https://finaltestcompany-e2e.com",
            "description": "Final test company for E2E testing",
        },
        "contact": {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson.final@finaltestcompany-e2e.com",
            "phone": "+1-555-0125",
            "job_title": "Final Test Engineer",
        },
        "product": {
            "name": "Final Test Product E2E",
            "sku": "FINAL-TEST-PROD-E2E-001",
            "description": "A final test product for E2E testing",
            "price": 199.99,
            "category": "Final Software",
        },
    }

    print("🚀 Starting Final Comprehensive E2E Tests for Enrich DDF Floor 2")
    print("=" * 70)

    # Wait for server to be ready
    if not wait_for_server(base_url):
        print("❌ Server is not ready. Exiting.")
        return 1

    # Run API tests first
    api_tests = [
        ("API Health Check", lambda: test_api_health_check(base_url)),
        ("API Root Endpoint", lambda: test_api_root_endpoint(base_url)),
        ("API Create Company", lambda: test_api_create_company(base_url, test_data)),
        ("API Create Contact", lambda: test_api_create_contact(base_url, test_data)),
        ("API Create Product", lambda: test_api_create_product(base_url, test_data)),
    ]

    print("\n📋 Running API Tests...")
    api_passed = 0
    api_total = len(api_tests)

    for test_name, test_func in api_tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            api_passed += 1
        else:
            print(f"❌ {test_name} failed")
        time.sleep(1)

    print(f"\n📊 API Test Results: {api_passed}/{api_total} tests passed")

    # Run UI tests
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            ui_tests = [
                (
                    "UI API Documentation",
                    lambda: test_ui_api_documentation(page, base_url),
                ),
                (
                    "UI Create Company",
                    lambda: test_ui_create_company_via_docs(page, base_url, test_data),
                ),
                (
                    "UI Verify Data",
                    lambda: test_ui_verify_data_creation(page, base_url, test_data),
                ),
            ]

            print("\n📋 Running UI Tests...")
            ui_passed = 0
            ui_total = len(ui_tests)

            for test_name, test_func in ui_tests:
                print(f"\n📋 Running: {test_name}")
                if test_func():
                    ui_passed += 1
                else:
                    print(f"❌ {test_name} failed")
                time.sleep(2)

            print(f"\n📊 UI Test Results: {ui_passed}/{ui_total} tests passed")

            total_passed = api_passed + ui_passed
            total_tests = api_total + ui_total

            print("\n" + "=" * 70)
            print(f"📊 FINAL TEST RESULTS: {total_passed}/{total_tests} tests passed")

            if total_passed == total_tests:
                print("🎉 ALL CRITICAL USER JOURNEY TESTS COMPLETED SUCCESSFULLY!")
                print("✅ Application is fully functional and ready for production!")
                print("✅ API endpoints are working correctly!")
                print("✅ UI interactions are working properly!")
                print("✅ Data creation and retrieval is functional!")
                return 0
            else:
                print("❌ Some tests failed. Please check the application.")
                return 1

        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return 1
        finally:
            browser.close()


if __name__ == "__main__":
    sys.exit(main())
