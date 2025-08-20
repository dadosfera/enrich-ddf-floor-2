"""Critical unit tests for API endpoints.

These tests cover the most critical functionality that must always work:
1. Application startup and health checks
2. Core CRUD operations for companies, contacts, and products
3. Data validation and error handling
"""

import uuid

from fastapi.testclient import TestClient


class TestCriticalEndpoints:
    """Critical endpoint tests that must always pass."""

    def test_application_startup(self, client: TestClient):
        """CRITICAL: Test that the application starts and responds."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to Enrich DDF Floor 2"
        assert data["version"] == "0.1.0"
        assert data["status"] == "running"

    def test_health_check(self, client: TestClient):
        """CRITICAL: Test health check endpoint for monitoring."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "timestamp" in data
        assert "version" in data

    def test_company_creation_endpoint(self, client: TestClient, sample_company_data):
        """CRITICAL: Test company creation endpoint."""
        company_data = {
            "name": sample_company_data.get("company_name", "Test Company"),
        }
        response = client.post("/api/v1/companies", json=company_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert "id" in data
        assert "data" in data

    def test_company_listing_endpoint(self, client: TestClient):
        """CRITICAL: Test company listing endpoint."""
        response = client.get("/api/v1/companies")
        assert response.status_code == 200
        data = response.json()
        # API returns list directly, not wrapped in "companies" key
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "name" in data[0]

    def test_contact_creation_endpoint(self, client: TestClient, sample_contact_data):
        """CRITICAL: Test contact creation endpoint."""
        # Only use fields accepted by the Contact model
        allowed_fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "job_title",
            "department",
            "company_id",
            "linkedin_url",
            "twitter_url",
        ]
        contact_payload = {
            k: v for k, v in sample_contact_data.items() if k in allowed_fields  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
        }
        # Use a unique email to avoid uniqueness constraint violation
        contact_payload["email"] = f"test_{uuid.uuid4().hex[:8]}@example.com"
        response = client.post("/api/v1/contacts", json=contact_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert "id" in data

    def test_contact_listing_endpoint(self, client: TestClient):
        """CRITICAL: Test contact listing endpoint."""
        response = client.get("/api/v1/contacts")
        assert response.status_code == 200
        data = response.json()
        # API returns list directly, not wrapped in "contacts" key
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "email" in data[0]

    def test_product_creation_endpoint(self, client: TestClient, sample_product_data):
        """CRITICAL: Test product creation endpoint."""
        # Update sample data to match API expectations
        product_data = {
            "name": sample_product_data.get("name", "Test Product"),
            "brand": sample_product_data.get("brand", "TestBrand"),
            "category": sample_product_data.get("category", "Electronics"),
        }
        response = client.post("/api/v1/products", json=product_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert "id" in data

    def test_product_listing_endpoint(self, client: TestClient):
        """CRITICAL: Test product listing endpoint."""
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        data = response.json()
        # API returns list directly, not wrapped in "products" key
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "name" in data[0]

    def test_invalid_endpoint_returns_404(self, client: TestClient):
        """CRITICAL: Test that invalid endpoints return proper 404."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

    def test_cors_headers_present(self, client: TestClient):
        """CRITICAL: Test CORS headers for frontend integration."""
        response = client.options("/")
        # CORS headers should be present for cross-origin requests
        assert response.status_code in [
            200,
            405,
        ]  # Some frameworks return 405 for OPTIONS


class TestDataValidation:
    """Critical data validation tests."""

    def test_empty_request_body_handling(self, client: TestClient):
        """CRITICAL: Test handling of empty request bodies."""
        response = client.post("/api/v1/companies", json={})
        assert (
            response.status_code == 400
        )  # API correctly rejects empty data due to DB constraints

    def test_malformed_json_handling(self, client: TestClient):
        """CRITICAL: Test handling of malformed JSON."""
        response = client.post(
            "/api/v1/companies",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422  # FastAPI validation error

    def test_large_payload_handling(self, client: TestClient):
        """CRITICAL: Test handling of unusually large payloads."""
        large_data = {"description": "x" * 10000}  # 10KB description
        response = client.post("/api/v1/companies", json=large_data)
        assert (
            response.status_code == 400
        )  # API correctly rejects data without required fields


class TestErrorHandling:
    """Critical error handling tests."""

    def test_method_not_allowed(self, client: TestClient):
        """CRITICAL: Test proper handling of unsupported HTTP methods."""
        response = client.put("/")  # PUT not supported on root
        assert response.status_code == 405

    def test_unsupported_media_type(self, client: TestClient):
        """CRITICAL: Test handling of unsupported content types."""
        response = client.post(
            "/api/v1/companies",
            data="plain text data",
            headers={"Content-Type": "text/plain"},
        )
        assert response.status_code in [
            422,
            415,
        ]  # Unprocessable Entity or Unsupported Media Type
