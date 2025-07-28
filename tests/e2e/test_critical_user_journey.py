"""
E2E Tests for Critical User Journey - Enrich DDF Floor 2

This test suite covers the complete critical user journey:
1. Access API documentation
2. Test health endpoint
3. Create company data
4. Create contact data
5. Create product data
6. Validate all created data
"""

import json

from playwright.sync_api import Page, expect


class TestCriticalUserJourney:
    """Test the complete critical user journey for the Enrich DDF Floor 2 application."""

    def test_01_application_health_check(self, page: Page, base_url: str):
        """Test that the application is healthy and accessible."""
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

    def test_02_api_documentation_access(self, page: Page, base_url: str):
        """Test access to API documentation and verify it loads correctly."""
        # Navigate to API docs
        page.goto(f"{base_url}/docs")

        # Wait for Swagger UI to load
        page.wait_for_selector("div.swagger-ui", timeout=10000)

        # Verify key elements are present
        expect(page.locator("h1")).to_contain_text("Enrich DDF Floor 2")
        expect(page.locator("div.swagger-ui")).to_be_visible()

        # Check for API endpoints
        expect(page.locator("text=/api/v1/companies")).to_be_visible()
        expect(page.locator("text=/api/v1/contacts")).to_be_visible()
        expect(page.locator("text=/api/v1/products")).to_be_visible()

        print("✅ API documentation loaded successfully")

    def test_03_create_company_via_api(
        self, page: Page, base_url: str, test_data: dict
    ):
        """Test creating a company via the API."""
        # Navigate to companies endpoint
        page.goto(f"{base_url}/docs")

        # Wait for Swagger UI
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
        expect(response_code).to_contain_text("200")

        # Verify response body contains company data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        assert "id" in response_data
        assert response_data["name"] == company_data["name"]
        assert response_data["industry"] == company_data["industry"]

        print(f"✅ Company created successfully - ID: {response_data['id']}")

        # Store company ID for later tests
        page.context.storage_state(path="tests/e2e/company_id.json")
        with open("tests/e2e/company_id.json", "w") as f:
            json.dump({"company_id": response_data["id"]}, f)

    def test_04_create_contact_via_api(
        self, page: Page, base_url: str, test_data: dict
    ):
        """Test creating a contact via the API."""
        # Navigate to contacts endpoint
        page.goto(f"{base_url}/docs")

        # Wait for Swagger UI
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
        expect(response_code).to_contain_text("200")

        # Verify response body contains contact data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        assert "id" in response_data
        assert response_data["first_name"] == contact_data["first_name"]
        assert response_data["last_name"] == contact_data["last_name"]
        assert response_data["email"] == contact_data["email"]

        print(f"✅ Contact created successfully - ID: {response_data['id']}")

        # Store contact ID for later tests
        with open("tests/e2e/contact_id.json", "w") as f:
            json.dump({"contact_id": response_data["id"]}, f)

    def test_05_create_product_via_api(
        self, page: Page, base_url: str, test_data: dict
    ):
        """Test creating a product via the API."""
        # Navigate to products endpoint
        page.goto(f"{base_url}/docs")

        # Wait for Swagger UI
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
        expect(response_code).to_contain_text("200")

        # Verify response body contains product data
        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        response_data = json.loads(response_text)

        assert "id" in response_data
        assert response_data["name"] == product_data["name"]
        assert response_data["description"] == product_data["description"]
        assert float(response_data["price"]) == product_data["price"]

        print(f"✅ Product created successfully - ID: {response_data['id']}")

        # Store product ID for later tests
        with open("tests/e2e/product_id.json", "w") as f:
            json.dump({"product_id": response_data["id"]}, f)

    def test_06_verify_all_data_created(
        self, page: Page, base_url: str, test_data: dict
    ):
        """Verify that all created data can be retrieved successfully."""
        # Test GET companies endpoint
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=10000)

        # Test companies list
        companies_get = page.locator("text=GET /api/v1/companies").first
        companies_get.click()

        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        page.wait_for_selector("div.responses-wrapper", timeout=10000)

        response_code = page.locator("td.response-col_status").first
        expect(response_code).to_contain_text("200")

        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        companies_data = json.loads(response_text)

        # Verify our test company is in the list
        test_company_found = any(
            company["name"] == test_data["company"]["name"]
            for company in companies_data
        )
        assert test_company_found, "Test company not found in companies list"

        print("✅ Companies list verification passed")

        # Test contacts list
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=10000)

        contacts_get = page.locator("text=GET /api/v1/contacts").first
        contacts_get.click()

        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        page.wait_for_selector("div.responses-wrapper", timeout=10000)

        response_code = page.locator("td.response-col_status").first
        expect(response_code).to_contain_text("200")

        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        contacts_data = json.loads(response_text)

        # Verify our test contact is in the list
        test_contact_found = any(
            contact["email"] == test_data["contact"]["email"]
            for contact in contacts_data
        )
        assert test_contact_found, "Test contact not found in contacts list"

        print("✅ Contacts list verification passed")

        # Test products list
        page.goto(f"{base_url}/docs")
        page.wait_for_selector("div.swagger-ui", timeout=10000)

        products_get = page.locator("text=GET /api/v1/products").first
        products_get.click()

        try_it_out_btn = page.locator("button:has-text('Try it out')").first
        try_it_out_btn.click()

        execute_btn = page.locator("button:has-text('Execute')").first
        execute_btn.click()

        page.wait_for_selector("div.responses-wrapper", timeout=10000)

        response_code = page.locator("td.response-col_status").first
        expect(response_code).to_contain_text("200")

        response_body = page.locator("div.highlight-code").first
        response_text = response_body.text_content()
        products_data = json.loads(response_text)

        # Verify our test product is in the list
        test_product_found = any(
            product["name"] == test_data["product"]["name"] for product in products_data
        )
        assert test_product_found, "Test product not found in products list"

        print("✅ Products list verification passed")
        print("🎉 All critical user journey tests completed successfully!")

    def test_07_application_root_endpoint(self, page: Page, base_url: str):
        """Test the root endpoint of the application."""
        # Navigate to root endpoint
        page.goto(f"{base_url}/")

        # Verify response is JSON
        response_text = page.content()
        root_data = json.loads(response_text)

        # Verify basic application info is present
        assert "message" in root_data or "title" in root_data or "version" in root_data

        print("✅ Root endpoint verification passed")
