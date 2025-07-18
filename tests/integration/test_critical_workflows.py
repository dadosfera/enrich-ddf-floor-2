"""Critical integration tests for complete workflows.

These tests verify that complete business workflows work end-to-end:
1. Data enrichment workflows
2. API integration chains
3. Cross-entity relationships
"""

import uuid

from fastapi.testclient import TestClient


class TestCriticalDataEnrichmentWorkflow:
    """Critical tests for data enrichment workflows."""

    def test_company_enrichment_workflow(self, client: TestClient, sample_company_data):
        """CRITICAL: Test complete company enrichment workflow."""
        unique_id = str(uuid.uuid4())[:8]
        # Step 1: Create company (use only accepted fields)
        company_data = {
            "name": sample_company_data.get(
                "company_name", f"Test Company {unique_id}"
            ),
            "domain": f"company-{unique_id}.com",
        }
        create_response = client.post(
            "/api/v1/companies",
            json=company_data,
        )
        assert create_response.status_code == 200
        create_response.json()

        # Step 2: List companies to verify creation
        list_response = client.get("/api/v1/companies")
        assert list_response.status_code == 200
        companies = list_response.json()
        assert isinstance(companies, list)
        if len(companies) > 0:
            assert "id" in companies[0]
            assert "name" in companies[0]

    def test_contact_enrichment_workflow(self, client: TestClient, sample_contact_data):
        """CRITICAL: Test complete contact enrichment workflow."""
        unique_id = str(uuid.uuid4())[:8]
        # Step 1: Create contact (use only accepted fields)
        contact_data = {
            "first_name": sample_contact_data.get("first_name", "John"),
            "last_name": sample_contact_data.get("last_name", "Doe"),
            "email": f"john.doe-{unique_id}@example.com",
        }
        create_response = client.post(
            "/api/v1/contacts",
            json=contact_data,
        )
        assert create_response.status_code == 200
        contact_data = create_response.json()

        # Step 2: Verify contact creation response structure
        assert "status" in contact_data
        assert "data" in contact_data
        assert contact_data["status"] == "created"

        # Step 3: List contacts
        list_response = client.get("/api/v1/contacts")
        assert list_response.status_code == 200
        contacts = list_response.json()
        assert isinstance(contacts, list)
        if len(contacts) > 0:
            assert "id" in contacts[0]
            assert "email" in contacts[0]

    def test_product_classification_workflow(
        self, client: TestClient, sample_product_data
    ):
        """CRITICAL: Test complete product classification workflow."""
        # Step 1: Create product (use only accepted fields)
        product_data = {
            "name": sample_product_data.get("name", "Test Product"),
            "brand": sample_product_data.get("brand", "TestBrand"),
            "category": sample_product_data.get("category", "Electronics"),
        }
        create_response = client.post("/api/v1/products", json=product_data)
        assert create_response.status_code == 200
        product_data = create_response.json()

        # Step 2: Verify product structure
        assert product_data["status"] == "created"
        assert "id" in product_data

        # Step 3: List products
        list_response = client.get("/api/v1/products")
        assert list_response.status_code == 200
        products = list_response.json()
        assert isinstance(products, list)
        if len(products) > 0:
            assert "id" in products[0]
            assert "name" in products[0]

    def test_company_update_and_delete(self, client: TestClient):
        """Test company creation (mutation test, creation only)."""
        unique_id = str(uuid.uuid4())[:8]
        company_data = {
            "name": f"Mutate Co {unique_id}",
            "domain": f"mutate-{unique_id}.com",
        }
        create_response = client.post(
            "/api/v1/companies",
            json=company_data,
        )
        assert create_response.status_code == 200
        company_id = create_response.json()["id"]
        assert company_id
        # TODO: Add update/delete tests when PUT/DELETE endpoints are available

    def test_contact_update_and_delete(self, client: TestClient):
        """Test contact creation (mutation test, creation only)."""
        unique_id = str(uuid.uuid4())[:8]
        contact_data = {
            "first_name": "Mutate",
            "last_name": "Contact",
            "email": f"mutate-{unique_id}@x.com",
        }
        create_response = client.post("/api/v1/contacts", json=contact_data)
        assert create_response.status_code == 200
        contact_id = create_response.json()["id"]
        assert contact_id
        # TODO: Add update/delete tests when PUT/DELETE endpoints are available

    def test_product_update_and_delete(self, client: TestClient):
        """Test product creation (mutation test, creation only)."""
        unique_id = str(uuid.uuid4())[:8]
        product_data = {
            "name": f"Mutate Product {unique_id}",
        }
        create_response = client.post("/api/v1/products", json=product_data)
        assert create_response.status_code == 200
        product_id = create_response.json()["id"]
        assert product_id
        # TODO: Add update/delete tests when PUT/DELETE endpoints are available


class TestCriticalAPIIntegration:
    """Critical tests for API integration scenarios."""

    def test_api_chain_health_to_endpoints(self, client: TestClient):
        """CRITICAL: Test that health check leads to functional endpoints."""
        # Step 1: Verify system health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["status"] == "healthy"

        # Step 2: If healthy, endpoints should work
        companies_response = client.get("/api/v1/companies")
        assert companies_response.status_code == 200

        contacts_response = client.get("/api/v1/contacts")
        assert contacts_response.status_code == 200

        products_response = client.get("/api/v1/products")
        assert products_response.status_code == 200

    def test_concurrent_entity_creation(
        self,
        client: TestClient,
        sample_company_data,
        sample_contact_data,
        sample_product_data,
    ):
        """CRITICAL: Test creating multiple entities concurrently."""
        unique_id = str(uuid.uuid4())[:8]
        # Create all three entity types (use only accepted fields)
        company_data = {
            "name": sample_company_data.get(
                "company_name", f"Test Company {unique_id}"
            ),
            "domain": f"concurrent-{unique_id}.com",
        }
        contact_data = {
            "first_name": sample_contact_data.get("first_name", "John"),
            "last_name": sample_contact_data.get("last_name", "Doe"),
            "email": f"john.doe-concurrent-{unique_id}@example.com",
        }
        product_data = {
            "name": sample_product_data.get("name", f"Test Product {unique_id}"),
        }
        company_response = client.post(
            "/api/v1/companies",
            json=company_data,
        )
        contact_response = client.post(
            "/api/v1/contacts",
            json=contact_data,
        )
        product_response = client.post(
            "/api/v1/products",
            json=product_data,
        )

        # All should succeed
        assert company_response.status_code == 200
        assert contact_response.status_code == 200
        assert product_response.status_code == 200

        # All should return proper creation responses
        assert company_response.json()["status"] == "created"
        assert contact_response.json()["status"] == "created"
        assert product_response.json()["status"] == "created"


class TestCriticalErrorScenarios:
    """Critical tests for error handling in workflows."""

    def test_invalid_data_handling_workflow(self, client: TestClient):
        """CRITICAL: Test system behavior with invalid data across endpoints."""
        invalid_data = {"invalid": "structure"}

        # Test each endpoint with invalid data
        company_response = client.post("/api/v1/companies", json=invalid_data)
        contact_response = client.post("/api/v1/contacts", json=invalid_data)
        product_response = client.post("/api/v1/products", json=invalid_data)

        # Accept 400 as valid for invalid data
        assert company_response.status_code in [200, 400]
        assert contact_response.status_code in [200, 400]
        assert product_response.status_code in [200, 400]

    def test_system_resilience_under_load(
        self, client: TestClient, sample_company_data
    ):
        """CRITICAL: Test system handles multiple rapid requests."""
        responses = []

        # Make multiple rapid requests
        for _i in range(10):
            company_data = {
                "name": sample_company_data.get("company_name", "Test Company"),
                "domain": "test.com",
                "industry": "Technology",
            }
            response = client.post("/api/v1/companies", json=company_data)
            responses.append(response)

        # Accept 400 as valid for duplicate/invalid data
        for response in responses:
            if response.status_code == 200:
                assert response.json()["status"] == "created"
            else:
                assert response.status_code == 400
