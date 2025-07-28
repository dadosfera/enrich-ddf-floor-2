#!/usr/bin/env python3
"""
UI E2E Test for Critical User Journey - Enrich DDF Floor 2

This script tests the complete critical user journey using Playwright
to ensure all UI interactions work correctly without errors.
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


def test_ui_health_check(page, base_url):
    """Test that the application health endpoint works via UI."""
    print("🔍 Testing UI health check...")

    try:
        # Navigate to health endpoint
        page.goto(f"{base_url}/health")

        # Verify response is JSON and contains expected fields
        response_text = page.content()
        health_data = json.loads(response_text)

        # Validate health response structure
        assert "status" in health_data
        assert "version" in health_data
        assert "database" in health_data
        assert health_data["status"] == "healthy"
        assert health_data["database"] == "connected"

        print(
            f"✅ UI Health check passed - Status: {health_data['status']}, "
            f"Version: {health_data['version']}"
        )
        return True
    except Exception as e:
        print(f"❌ UI Health check failed: {e}")
        return False


def test_ui_root_endpoint(page, base_url):
    """Test the root endpoint via UI."""
    print("🔍 Testing UI root endpoint...")

    try:
        # Navigate to root endpoint
        page.goto(f"{base_url}/")

        # Verify response is JSON
        response_text = page.content()
        root_data = json.loads(response_text)

        # Verify basic application info is present
        assert "message" in root_data or "title" in root_data or "version" in root_data

        print("✅ UI Root endpoint verification passed")
        return True
    except Exception as e:
        print(f"❌ UI Root endpoint test failed: {e}")
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
        if "data" in response_data:
            data = response_data["data"]
        else:
            data = response_data

        assert "id" in data
        assert data["name"] == company_data["name"]

        print(f"✅ UI Company created successfully - ID: {data['id']}")
        return True
    except Exception as e:
        print(f"❌ UI Company creation test failed: {e}")
        return False


def test_ui_create_contact_via_docs(page, base_url, test_data):
    """Test creating a contact via the UI documentation."""
    print("🔍 Testing UI contact creation via docs...")

    try:
        # Navigate to contacts endpoint
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=15000)

        # Find and click on POST /api/v1/contacts
        contacts_post = page.locator("text=POST /api/v1/contacts").first
        contacts_post.click()

        # Click "Try it out" button
        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        # Fill in the request body
        request_body = page.locator("textarea[data-param-name='body']").first
        contact_data = test_data["contact"]
        request_body.fill(json.dumps(contact_data, indent=2))

        # Click "Execute" button
        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        # Wait for response
        page.wait_for_selector("div.responses-wrapper", timeout=15000)

        # Verify successful response
        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        # Verify response body contains contact data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        # Handle the actual response format
        if "data" in response_data:
            data = response_data["data"]
        else:
            data = response_data

        assert "id" in data
        assert data["first_name"] == contact_data["first_name"]
        assert data["last_name"] == contact_data["last_name"]
        assert data["email"] == contact_data["email"]

        print(f"✅ UI Contact created successfully - ID: {data['id']}")
        return True
    except Exception as e:
        print(f"❌ UI Contact creation test failed: {e}")
        return False


def test_ui_create_product_via_docs(page, base_url, test_data):
    """Test creating a product via the UI documentation."""
    print("🔍 Testing UI product creation via docs...")

    try:
        # Navigate to products endpoint
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=15000)

        # Find and click on POST /api/v1/products
        products_post = page.locator("text=POST /api/v1/products").first
        products_post.click()

        # Click "Try it out" button
        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        # Fill in the request body
        request_body = page.locator("textarea[data-param-name='body']").first
        product_data = test_data["product"]
        request_body.fill(json.dumps(product_data, indent=2))

        # Click "Execute" button
        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        # Wait for response
        page.wait_for_selector("div.responses-wrapper", timeout=15000)

        # Verify successful response
        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        # Verify response body contains product data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        # Handle the actual response format
        if "data" in response_data:
            data = response_data["data"]
        else:
            data = response_data

        assert "id" in data
        assert data["name"] == product_data["name"]
        assert data["description"] == product_data["description"]
        assert float(data["price"]) == product_data["price"]

        print(f"✅ UI Product created successfully - ID: {data['id']}")
        return True
    except Exception as e:
        print(f"❌ UI Product creation test failed: {e}")
        return False


def test_ui_verify_data_creation(page, base_url, test_data):
    """Verify that all created data can be retrieved via UI."""
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

        # Test contacts list
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=15000)

        contacts_get = page.locator("text=GET /api/v1/contacts").first
        contacts_get.click()

        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        page.wait_for_selector("div.responses-wrapper", timeout=15000)

        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        contacts_data = json.loads(response_text)

        # Verify our test contact is in the list
        test_contact_found = any(
            contact["email"] == test_data["contact"]["email"]
            for contact in contacts_data
        )
        assert test_contact_found, "Test contact not found in contacts list"

        print("✅ UI Contacts list verification passed")

        # Test products list
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=15000)

        products_get = page.locator("text=GET /api/v1/products").first
        products_get.click()

        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        page.wait_for_selector("div.responses-wrapper", timeout=15000)

        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        products_data = json.loads(response_text)

        # Verify our test product is in the list
        test_product_found = any(
            product["name"] == test_data["product"]["name"] for product in products_data
        )
        assert test_product_found, "Test product not found in products list"

        print("✅ UI Products list verification passed")
        print("🎉 All UI critical user journey tests completed successfully!")
        return True
    except Exception as e:
        print(f"❌ UI Data verification test failed: {e}")
        return False


def main():
    """Run all UI E2E tests."""
    base_url = "http://127.0.0.1:8000"

    test_data = {
        "company": {
            "name": "UI Test Company E2E",
            "domain": "uitestcompany-e2e.com",
            "industry": "Technology",
            "website": "https://uitestcompany-e2e.com",
            "description": "UI test company for E2E testing",
        },
        "contact": {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith.ui@uitestcompany-e2e.com",
            "phone": "+1-555-0124",
            "job_title": "UI Test Engineer",
        },
        "product": {
            "name": "UI Test Product E2E",
            "sku": "UI-TEST-PROD-E2E-001",
            "description": "A UI test product for E2E testing",
            "price": 149.99,
            "category": "UI Software",
        },
    }

    print("🚀 Starting UI E2E Tests for Enrich DDF Floor 2")
    print("=" * 60)

    # Wait for server to be ready
    if not wait_for_server(base_url):
        print("❌ Server is not ready. Exiting.")
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Run all UI tests
            tests = [
                ("UI Health Check", lambda: test_ui_health_check(page, base_url)),
                ("UI Root Endpoint", lambda: test_ui_root_endpoint(page, base_url)),
                (
                    "UI API Documentation",
                    lambda: test_ui_api_documentation(page, base_url),
                ),
                (
                    "UI Create Company",
                    lambda: test_ui_create_company_via_docs(page, base_url, test_data),
                ),
                (
                    "UI Create Contact",
                    lambda: test_ui_create_contact_via_docs(page, base_url, test_data),
                ),
                (
                    "UI Create Product",
                    lambda: test_ui_create_product_via_docs(page, base_url, test_data),
                ),
                (
                    "UI Verify Data",
                    lambda: test_ui_verify_data_creation(page, base_url, test_data),
                ),
            ]

            passed = 0
            total = len(tests)

            for test_name, test_func in tests:
                print(f"\n📋 Running: {test_name}")
                if test_func():
                    passed += 1
                else:
                    print(f"❌ {test_name} failed")
                time.sleep(2)  # Brief pause between tests

            print("\n" + "=" * 60)
            print(f"📊 UI Test Results: {passed}/{total} tests passed")

            if passed == total:
                print("🎉 All UI critical user journey tests completed successfully!")
                print("✅ Application UI is fully functional and ready for use!")
                return 0
            else:
                print("❌ Some UI tests failed. Please check the application.")
                return 1

        except Exception as e:
            print(f"❌ UI Test execution failed: {e}")
            return 1
        finally:
            browser.close()


if __name__ == "__main__":
    sys.exit(main())
