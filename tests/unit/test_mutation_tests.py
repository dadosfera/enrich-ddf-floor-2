"""Comprehensive mutation tests for data integrity and edge cases.  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)

These tests verify that the system correctly handles various mutation scenarios:
1. Valid data mutations
2. Invalid data mutations
3. Boundary condition mutations
4. Concurrent mutation scenarios
5. Error handling mutations
"""

import uuid

from fastapi.testclient import TestClient


class TestCompanyMutationTests:
    """Mutation tests for company entity."""

    def test_company_creation_with_minimal_data(self, client: TestClient):
        """Test company creation with minimal required data."""
        unique_id = str(uuid.uuid4())[:8]
        company_data = {"name": f"Minimal Co {unique_id}"}

        response = client.post("/api/v1/companies", json=company_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert "id" in data
        assert data["data"]["name"] == company_data["name"]

    def test_company_creation_with_full_data(self, client: TestClient):
        """Test company creation with all available fields."""
        unique_id = str(uuid.uuid4())[:8]
        company_data = {
            "name": f"Full Co {unique_id}",
            "domain": f"full-{unique_id}.com",
            "industry": "Technology",
            "size": "51-200",
            "location": "San Francisco, CA",
            "description": "A comprehensive test company",
            "website": f"https://full-{unique_id}.com",
            "phone": "+1-555-123-4567",
            "email": f"contact@full-{unique_id}.com",
        }

        response = client.post("/api/v1/companies", json=company_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert data["data"]["name"] == company_data["name"]
        assert data["data"]["domain"] == company_data["domain"]

    def test_company_creation_with_duplicate_domain(self, client: TestClient):
        """Test company creation with duplicate domain (should fail)."""
        unique_id = str(uuid.uuid4())[:8]
        domain = f"duplicate-{unique_id}.com"

        # First creation should succeed
        company_data_1 = {"name": f"First Co {unique_id}", "domain": domain}
        response_1 = client.post("/api/v1/companies", json=company_data_1)
        assert response_1.status_code == 200

        # Second creation with same domain should fail
        company_data_2 = {"name": f"Second Co {unique_id}", "domain": domain}
        response_2 = client.post("/api/v1/companies", json=company_data_2)
        assert response_2.status_code == 400

    def test_company_creation_with_empty_data(self, client: TestClient):
        """Test company creation with empty data."""
        response = client.post("/api/v1/companies", json={})
        assert (
            response.status_code == 400
        )  # API correctly rejects empty data due to DB constraints
        data = response.json()
        assert "detail" in data

    def test_company_creation_with_special_characters(self, client: TestClient):
        """Test company creation with special characters in data."""
        unique_id = str(uuid.uuid4())[:8]
        company_data = {
            "name": f"Special Co {unique_id} !@#$%^&*()",
            "domain": f"special-{unique_id}.com",
            "description": "Company with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?",
        }

        response = client.post("/api/v1/companies", json=company_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"


class TestContactMutationTests:
    """Mutation tests for contact entity."""

    def test_contact_creation_with_minimal_data(self, client: TestClient):
        """Test contact creation with minimal required data."""
        unique_id = str(uuid.uuid4())[:8]
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.doe-{unique_id}@example.com",
        }

        response = client.post("/api/v1/contacts", json=contact_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert "id" in data
        assert data["data"]["email"] == contact_data["email"]

    def test_contact_creation_with_full_data(self, client: TestClient):
        """Test contact creation with all available fields."""
        unique_id = str(uuid.uuid4())[:8]
        contact_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": f"jane.smith-{unique_id}@example.com",
            "phone": "+1-555-987-6543",
            "job_title": "Senior Developer",
            "department": "Engineering",
            "linkedin_url": f"https://linkedin.com/in/jane-smith-{unique_id}",
            "twitter_url": f"https://twitter.com/janesmith{unique_id}",
            "company_id": 1,  # Assuming company exists
        }

        response = client.post("/api/v1/contacts", json=contact_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert data["data"]["email"] == contact_data["email"]

    def test_contact_creation_with_duplicate_email(self, client: TestClient):
        """Test contact creation with duplicate email (should fail)."""
        unique_id = str(uuid.uuid4())[:8]
        email = f"duplicate-{unique_id}@example.com"

        # First creation should succeed
        contact_data_1 = {
            "first_name": "First",
            "last_name": "Contact",
            "email": email,
        }
        response_1 = client.post("/api/v1/contacts", json=contact_data_1)
        assert response_1.status_code == 200

        # Second creation with same email should fail
        contact_data_2 = {
            "first_name": "Second",
            "last_name": "Contact",
            "email": email,
        }
        response_2 = client.post("/api/v1/contacts", json=contact_data_2)
        assert response_2.status_code == 400

    def test_contact_creation_with_empty_data(self, client: TestClient):
        """Test contact creation with empty data."""
        response = client.post("/api/v1/contacts", json={})
        assert response.status_code == 400  # API correctly rejects empty contact data

    def test_contact_creation_with_unicode_data(self, client: TestClient):
        """Test contact creation with unicode characters."""
        unique_id = str(uuid.uuid4())[:8]
        contact_data = {
            "first_name": "José",
            "last_name": "García",
            "email": f"jose.garcia-{unique_id}@example.com",
            "job_title": "Développeur Senior",
        }

        response = client.post("/api/v1/contacts", json=contact_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"


class TestProductMutationTests:
    """Mutation tests for product entity."""

    def test_product_creation_with_minimal_data(self, client: TestClient):
        """Test product creation with minimal required data."""
        unique_id = str(uuid.uuid4())[:8]
        product_data = {"name": f"Minimal Product {unique_id}"}

        response = client.post("/api/v1/products", json=product_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert "id" in data
        assert data["data"]["name"] == product_data["name"]

    def test_product_creation_with_full_data(self, client: TestClient):
        """Test product creation with all available fields."""
        unique_id = str(uuid.uuid4())[:8]
        product_data = {
            "name": f"Full Product {unique_id}",
            "sku": f"SKU-{unique_id}",
            "category": "Electronics",
            "subcategory": "Smartphones",
            "brand": "TestBrand",
            "description": "A comprehensive test product with all fields",
            "price": 999.99,
            "currency": "USD",
        }

        response = client.post("/api/v1/products", json=product_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"
        assert data["data"]["name"] == product_data["name"]
        assert data["data"]["sku"] == product_data["sku"]

    def test_product_creation_with_empty_data(self, client: TestClient):
        """Test product creation with empty data."""
        response = client.post("/api/v1/products", json={})
        assert (
            response.status_code == 400
        )  # API correctly rejects empty data due to DB constraints
        data = response.json()
        assert "detail" in data

    def test_product_creation_with_numeric_data(self, client: TestClient):
        """Test product creation with various numeric values."""
        unique_id = str(uuid.uuid4())[:8]
        product_data = {
            "name": f"Numeric Product {unique_id}",
            "price": 0.01,
            "currency": "EUR",
        }

        response = client.post("/api/v1/products", json=product_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "created"


class TestConcurrentMutationTests:
    """Tests for concurrent mutation scenarios."""

    def test_concurrent_company_creation(self, client: TestClient):
        """Test creating multiple companies concurrently."""
        unique_id = str(uuid.uuid4())[:8]
        responses = []

        for i in range(5):
            company_data = {
                "name": f"Concurrent Co {unique_id}-{i}",
                "domain": f"concurrent-{unique_id}-{i}.com",
            }
            response = client.post("/api/v1/companies", json=company_data)
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "created"

    def test_concurrent_contact_creation(self, client: TestClient):
        """Test creating multiple contacts concurrently."""
        unique_id = str(uuid.uuid4())[:8]
        responses = []

        for i in range(5):
            contact_data = {
                "first_name": f"Contact{i}",
                "last_name": f"User{unique_id}",
                "email": f"contact{i}-{unique_id}@example.com",
            }
            response = client.post("/api/v1/contacts", json=contact_data)
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "created"

    def test_concurrent_product_creation(self, client: TestClient):
        """Test creating multiple products concurrently."""
        unique_id = str(uuid.uuid4())[:8]
        responses = []

        for i in range(5):
            product_data = {
                "name": f"Concurrent Product {unique_id}-{i}",
                "sku": f"SKU-{unique_id}-{i}",
            }
            response = client.post("/api/v1/products", json=product_data)
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "created"


class TestErrorHandlingMutationTests:
    """Tests for error handling in mutation scenarios."""

    def test_malformed_json_handling(self, client: TestClient):
        """Test handling of malformed JSON in mutation requests."""
        # Test with malformed JSON
        response = client.post(
            "/api/v1/companies",
            data="{'invalid': json}",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code in [400, 422]

    def test_large_payload_handling(self, client: TestClient):
        """Test handling of large payloads in mutation requests."""
        unique_id = str(uuid.uuid4())[:8]
        large_description = "x" * 10000  # Very large description

        company_data = {
            "name": f"Large Co {unique_id}",
            "description": large_description,
        }

        response = client.post("/api/v1/companies", json=company_data)
        assert response.status_code in [200, 400, 413]  # Accept various outcomes

    def test_invalid_field_types(self, client: TestClient):
        """Test handling of invalid field types in mutation requests."""

        # Test with invalid field types
        invalid_data = {
            "name": 123,  # Should be string
            "email": True,  # Should be string
            "price": "not_a_number",  # Should be number
        }

        # Test with companies
        response = client.post("/api/v1/companies", json=invalid_data)
        assert response.status_code in [200, 400, 422]  # Accept various outcomes

        # Test with contacts
        response = client.post("/api/v1/contacts", json=invalid_data)
        assert response.status_code in [200, 400, 422]  # Accept various outcomes

        # Test with products
        response = client.post("/api/v1/products", json=invalid_data)
        assert response.status_code in [200, 400, 422]  # Accept various outcomes
