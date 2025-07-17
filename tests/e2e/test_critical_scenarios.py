"""Critical End-to-End tests for real user scenarios.

These tests simulate complete user journeys and critical business scenarios:
1. User onboarding and data entry workflows
2. System-wide data processing scenarios
3. Real-world usage patterns
"""

import uuid
from fastapi.testclient import TestClient


class TestCriticalUserJourneys:
    """Critical E2E tests for complete user journeys."""

    def test_new_user_onboarding_journey(self, client: TestClient):
        """CRITICAL: Test complete new user onboarding workflow."""
        # Step 1: User checks if system is available
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"

        # Step 2: User explores API documentation
        root_response = client.get("/")
        assert root_response.status_code == 200
        root_data = root_response.json()
        assert "docs_url" in root_data

        # Step 3: User starts with listing existing data
        companies_list = client.get("/api/v1/companies")
        contacts_list = client.get("/api/v1/contacts")
        products_list = client.get("/api/v1/products")

        assert companies_list.status_code == 200
        assert contacts_list.status_code == 200
        assert products_list.status_code == 200
        # All should be lists
        assert isinstance(companies_list.json(), list)
        assert isinstance(contacts_list.json(), list)
        assert isinstance(products_list.json(), list)

    def test_data_enrichment_business_scenario(self, client: TestClient):
        """CRITICAL: Test complete business data enrichment scenario."""
        unique_id = str(uuid.uuid4())[:8]

        # Step 1: Add a new company to database (use only accepted fields)
        company_data = {
            "name": "TechCorp Solutions",
            "domain": f"techcorp-{unique_id}.com",
            "industry": "Technology",
        }
        company_response = client.post(
            "/api/v1/companies",
            json=company_data,
        )
        assert company_response.status_code == 200

        # Step 2: Add contacts associated with the company (use only accepted fields)
        contact_data = {
            "first_name": "Maria",
            "last_name": "Silva",
            "email": (
                f"maria.silva-{unique_id}@techcorp.com"
            ),
            "phone": "+55 11 99999-1234",
        }
        contact_response = client.post(
            "/api/v1/contacts",
            json=contact_data,
        )
        assert contact_response.status_code == 200

        # Step 3: Add products that the company sells (use only accepted fields)
        product_data = {
            "name": "Enterprise Software Solution",
            "description": (
                "Cloud-based enterprise management system"
            ),
            "brand": "TechCorp",
            "category": "Software",
        }
        product_response = client.post(
            "/api/v1/products",
            json=product_data,
        )
        assert product_response.status_code == 200

        # Step 4: Verify all data was accepted
        assert company_response.json()["status"] == "created"
        assert contact_response.json()["status"] == "created"
        assert product_response.json()["status"] == "created"


class TestCriticalSystemBehavior:
    """Critical tests for system-wide behavior under real conditions."""

    def test_system_stability_under_normal_load(self, client: TestClient):
        """CRITICAL: Test system remains stable under normal operational load."""
        unique_id = str(uuid.uuid4())[:8]
        
        # Simulate normal user activity over time
        operations = [
            lambda: client.get("/health"),
            lambda: client.get("/api/v1/companies"),
            lambda: client.post(
                "/api/v1/companies",
                json={"name": f"Test Co {unique_id}"},
            ),
            lambda: client.get("/api/v1/contacts"),
            lambda: client.post(
                "/api/v1/contacts",
                json={
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": (
                        f"john.doe-{unique_id}@example.com"
                    ),
                },
            ),
        ]
        # Execute operations multiple times
        for _i in range(5):
            for operation in operations:
                response = operation()
                # Accept 400 for POST requests (duplicate/invalid data)
                if response.request.method == "POST":
                    assert response.status_code in [200, 201, 400]
                else:
                    assert response.status_code in [200, 201]

    def test_api_consistency_across_endpoints(self, client: TestClient):
        """CRITICAL: Test that all endpoints maintain consistent behavior."""
        unique_id = str(uuid.uuid4())[:8]
        
        endpoints = [
            "/api/v1/companies",
            "/api/v1/contacts",
            "/api/v1/products",
        ]

        # Test GET consistency
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            data = response.json()
            # All listing endpoints should be lists
            assert isinstance(data, list)

        # Test POST consistency
        post_payloads = {
            "/api/v1/companies": {"name": f"Test {unique_id}"},
            "/api/v1/contacts": {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": (
                    f"jane.smith-{unique_id}@example.com"
                ),
            },
            "/api/v1/products": {"name": f"Test Product {unique_id}"},
        }
        for endpoint in endpoints:
            response = client.post(
                endpoint,
                json=post_payloads[endpoint],
            )
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert data["status"] == "created"


class TestCriticalDataIntegrity:
    """Critical tests for data integrity and validation."""

    def test_data_integrity_across_operations(self, client: TestClient):
        """CRITICAL: Test data integrity is maintained across operations."""
        unique_id = str(uuid.uuid4())[:8]
        
        # Create entities with structured data (use only accepted fields)
        company_data = {
            "name": "DataCorp Analytics",
            "domain": f"datacorp-{unique_id}.com",
            "industry": "Analytics",
        }
        # Create and verify data structure is preserved
        response = client.post(
            "/api/v1/companies",
            json=company_data,
        )
        assert response.status_code == 200
        response_data = response.json()
        assert "data" in response_data
        assert response_data["data"]["name"] == company_data["name"]
        assert response_data["data"]["domain"] == company_data["domain"]

    def test_system_handles_edge_cases(self, client: TestClient):
        """CRITICAL: Test system handles edge cases gracefully."""
        edge_cases = [
            {},
            {"special_chars": "!@#$%^&*()"},
            {"unicode": "\u30c6\u30b9\u30c8\u4f1a\u793e"},
            {"large_text": "x" * 1000},
        ]

        for edge_case in edge_cases:
            response = client.post(
                "/api/v1/companies",
                json=edge_case,
            )
            # System should handle gracefully (not crash)
            assert response.status_code in [200, 400, 422]
