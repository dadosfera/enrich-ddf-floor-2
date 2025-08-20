"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

# Import the working app
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_company_data():
    """Sample company data for testing."""  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
    return {
        "cnpj": "12.345.678/0001-95",
        "company_name": "Test Company Ltd",
        "trade_name": "Test Corp",
        "legal_nature": "Limited Company",
        "address": {
            "street": "Test Street, 123",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345-678",
        },
    }


@pytest.fixture
def sample_contact_data():
    """Sample contact data for testing."""  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+55 11 99999-9999",
        "cpf": "123.456.789-10",
    }


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
    return {
        "name": "Test Product",
        "description": "A sample product for testing",
        "brand": "TestBrand",
        "category": "Electronics",
        "price": 99.99,
    }
