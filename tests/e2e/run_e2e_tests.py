#!/usr/bin/env python3
"""
E2E Test Runner for Enrich DDF Floor 2

This script runs comprehensive E2E tests for the critical user journey
using Playwright directly without pytest.
"""

import json
import sys
import time

from playwright.sync_api import sync_playwright


def test_health_check(page, base_url):
    """Test that the application is healthy and accessible."""
    print("🔍 Testing application health check...")

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
            f"✅ Health check passed - Status: {health_data['status']}, "
            f"Version: {health_data['version']}"
        )
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_api_documentation(page, base_url):
    """Test access to API documentation and verify it loads correctly."""
    print("🔍 Testing API documentation access...")

    try:
        # Navigate to API docs
        page.goto(f"{base_url}/docs")

        # Wait for Swagger UI to load
        page.wait_for_selector("div.swagger-ui", timeout=10000)

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

        print("✅ API documentation loaded successfully")
        return True
    except Exception as e:
        print(f"❌ API documentation test failed: {e}")
        return False


def test_create_company(page, base_url, test_data):
    """Test creating a company via the API."""
    print("🔍 Testing company creation...")

    try:
        # Navigate to companies endpoint
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=10000)

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
        page.wait_for_selector("div.responses-wrapper", timeout=10000)

        # Verify successful response
        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        # Verify response body contains company data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        assert "id" in response_data
        assert response_data["name"] == company_data["name"]
        assert response_data["industry"] == company_data["industry"]

        print(f"✅ Company created successfully - ID: {response_data['id']}")
        return True
    except Exception as e:
        print(f"❌ Company creation test failed: {e}")
        return False


def test_create_contact(page, base_url, test_data):
    """Test creating a contact via the API."""
    print("🔍 Testing contact creation...")

    try:
        # Navigate to contacts endpoint
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=10000)

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
        page.wait_for_selector("div.responses-wrapper", timeout=10000)

        # Verify successful response
        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        # Verify response body contains contact data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        assert "id" in response_data
        assert response_data["first_name"] == contact_data["first_name"]
        assert response_data["last_name"] == contact_data["last_name"]
        assert response_data["email"] == contact_data["email"]

        print(f"✅ Contact created successfully - ID: {response_data['id']}")
        return True
    except Exception as e:
        print(f"❌ Contact creation test failed: {e}")
        return False


def test_create_product(page, base_url, test_data):
    """Test creating a product via the API."""
    print("🔍 Testing product creation...")

    try:
        # Navigate to products endpoint
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=10000)

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
        page.wait_for_selector("div.responses-wrapper", timeout=10000)

        # Verify successful response
        response_code = page.locator("td.response-col_status").first
        assert "200" in response_code.text_content()

        # Verify response body contains product data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        assert "id" in response_data
        assert response_data["name"] == product_data["name"]
        assert response_data["description"] == product_data["description"]
        assert float(response_data["price"]) == product_data["price"]

        print(f"✅ Product created successfully - ID: {response_data['id']}")
        return True
    except Exception as e:
        print(f"❌ Product creation test failed: {e}")
        return False


def main():
    """Run all E2E tests."""
    base_url = "http://127.0.0.1:8000"

    test_data = {
        "company": {
            "name": "Test Company E2E",
            "industry": "Technology",
            "website": "https://testcompany-e2e.com",
            "description": "Test company for E2E testing",
        },
        "contact": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@testcompany-e2e.com",
            "phone": "+1-555-0123",
            "position": "Software Engineer",
        },
        "product": {
            "name": "Test Product E2E",
            "description": "A test product for E2E testing",
            "price": 99.99,
            "category": "Software",
        },
    }

    print("🚀 Starting E2E Tests for Enrich DDF Floor 2")
    print("=" * 50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Run all tests
            tests = [
                ("Health Check", lambda: test_health_check(page, base_url)),
                ("API Documentation", lambda: test_api_documentation(page, base_url)),
                (
                    "Create Company",
                    lambda: test_create_company(page, base_url, test_data),
                ),
                (
                    "Create Contact",
                    lambda: test_create_contact(page, base_url, test_data),
                ),
                (
                    "Create Product",
                    lambda: test_create_product(page, base_url, test_data),
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
                time.sleep(1)  # Brief pause between tests

            print("\n" + "=" * 50)
            print(f"📊 Test Results: {passed}/{total} tests passed")

            if passed == total:
                print("🎉 All critical user journey tests completed successfully!")
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
