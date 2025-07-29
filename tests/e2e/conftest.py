import pytest


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context for tests."""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "tests/e2e/videos/",
        "record_video_size": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application."""
    return "http://127.0.0.1:8247"


@pytest.fixture(scope="session")
def test_data():
    """Test data for E2E tests."""
    return {
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
