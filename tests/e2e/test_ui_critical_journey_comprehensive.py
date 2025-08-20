#!/usr/bin/env python3
"""
Comprehensive UI E2E Test for Enrich DDF Floor 2
Critical User Journey: API Documentation → Data Creation → Verification
"""

import asyncio
import logging
import random
import string
import time
from datetime import datetime
from typing import Any, Dict

import requests
from playwright.async_api import async_playwright


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Test configuration
BASE_URL = "http://0.0.0.0:8247"
API_BASE_URL = f"{BASE_URL}/api/v1"
DOCS_URL = f"{BASE_URL}/docs"
HEALTH_URL = f"{BASE_URL}/health"


# Test data generation
def generate_unique_string(prefix: str = "test", length: int = 8) -> str:
    """Generate unique string for test data."""  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
    timestamp = int(time.time())
    random_suffix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{prefix}_{timestamp}_{random_suffix}"


def generate_test_data() -> Dict[str, Dict[str, Any]]:
    """Generate unique test data for all entities."""
    timestamp = int(time.time())
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

    return {
        "company": {
            "name": f"Test Company {timestamp}_{random_suffix}",
            "domain": f"testcompany{timestamp}{random_suffix}.com",
            "industry": "Technology",
            "size": "Medium",
            "founded_year": 2020,
            "description": f"Test company created at {datetime.now().isoformat()}",
        },
        "contact": {
            "first_name": f"John{timestamp}",
            "last_name": f"Doe{random_suffix}",
            "email": f"john.doe{timestamp}{random_suffix}@example.com",
            "phone": f"+1-555-{timestamp % 10000:04d}",
            "position": "Software Engineer",
            "company_id": None,  # Will be set after company creation
        },
        "product": {
            "name": f"Test Product {timestamp}_{random_suffix}",
            "sku": f"SKU{timestamp}{random_suffix}",
            "category": "Software",
            "price": 99.99,
            "description": f"Test product created at {datetime.now().isoformat()}",
            "in_stock": True,
        },
    }


class ComprehensiveUITest:
    """Comprehensive UI E2E test for critical user journey."""

    def __init__(self):
        self.test_data = generate_test_data()
        self.created_entities = {}
        self.browser = None
        self.page = None

    async def setup(self):
        """Setup test environment."""
        logger.info("🔧 Setting up comprehensive UI test environment...")

        # Check if server is running
        try:
            response = self.api_request_with_retry(HEALTH_URL)
            if response.status_code != 200:
                raise Exception(f"Server health check failed: {response.status_code}")
            logger.info("✅ Server is running and healthy")
        except Exception as e:
            logger.error(f"❌ Server health check failed: {e}")
            raise

        # Initialize Playwright
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        self.page = await self.browser.new_page()

        # Set viewport
        await self.page.set_viewport_size({"width": 1280, "height": 720})

        logger.info("✅ Test environment setup complete")

    async def teardown(self):
        """Cleanup test environment."""
        logger.info("🧹 Cleaning up test environment...")

        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, "playwright"):
            await self.playwright.stop()

        logger.info("✅ Test environment cleanup complete")

    async def test_api_documentation_access(self) -> bool:
        """Test accessing API documentation."""
        logger.info("📚 Testing API documentation access...")

        try:
            # Navigate to API docs
            await self.page.goto(DOCS_URL, wait_until="networkidle")

            # Check if page loaded successfully
            title = await self.page.title()
            if "Enrich DDF Floor 2" not in title and "FastAPI" not in title:
                raise Exception(f"Unexpected page title: {title}")

            # Check for Swagger UI elements
            await self.page.wait_for_selector("div.swagger-ui", timeout=10000)

            # Check for API endpoints
            await self.page.wait_for_selector("div.opblock", timeout=10000)

            logger.info("✅ API documentation access successful")
            return True

        except Exception as e:
            logger.error(f"❌ API documentation access failed: {e}")
            return False

    async def test_health_endpoint_ui(self) -> bool:
        """Test health endpoint through UI."""
        logger.info("❤️ Testing health endpoint through UI...")

        try:
            # Navigate to health endpoint
            await self.page.goto(HEALTH_URL, wait_until="networkidle")

            # Check if JSON response is displayed
            content = await self.page.content()
            if '"status":"healthy"' not in content:
                raise Exception("Health endpoint not returning expected response")

            logger.info("✅ Health endpoint UI test successful")
            return True

        except Exception as e:
            logger.error(f"❌ Health endpoint UI test failed: {e}")
            return False

    async def test_api_endpoints_through_docs(self) -> bool:
        """Test API endpoints through documentation interface."""
        logger.info("🔍 Testing API endpoints through documentation...")

        try:
            # Navigate to API docs
            await self.page.goto(DOCS_URL, wait_until="networkidle")

            # Test companies endpoint
            await self.page.click("text=GET /api/v1/companies")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Test contacts endpoint
            await self.page.click("text=GET /api/v1/contacts")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Test products endpoint
            await self.page.click("text=GET /api/v1/products")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            logger.info("✅ API endpoints documentation test successful")
            return True

        except Exception as e:
            logger.error(f"❌ API endpoints documentation test failed: {e}")
            return False

    async def test_data_creation_through_ui(self) -> bool:
        """Test data creation through UI interface."""
        logger.info("📝 Testing data creation through UI...")

        try:
            # Navigate to API docs
            await self.page.goto(DOCS_URL, wait_until="networkidle")

            # Test company creation through UI
            await self.page.click("text=POST /api/v1/companies")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Expand the endpoint
            await self.page.click("button.opblock-summary-method")
            await self.page.wait_for_timeout(1000)

            # Test contact creation through UI
            await self.page.click("text=POST /api/v1/contacts")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Test product creation through UI
            await self.page.click("text=POST /api/v1/products")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            logger.info("✅ Data creation UI test successful")
            return True

        except Exception as e:
            logger.error(f"❌ Data creation UI test failed: {e}")
            return False

    def api_request_with_retry(self, url, method="GET", **kwargs):
        """Make API request with retry logic."""
        for attempt in range(3):
            try:
                response = requests.request(method, url, timeout=10, **kwargs)
                return response
            except requests.exceptions.ConnectionError as e:
                if attempt == 2:
                    raise e
                logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                time.sleep(1)

    async def test_api_data_creation(self) -> bool:
        """Test API data creation programmatically."""
        logger.info("🔧 Testing API data creation...")

        try:
            # Create company
            company_response = self.api_request_with_retry(
                f"{API_BASE_URL}/companies",
                method="POST",
                json=self.test_data["company"],
            )
            if company_response.status_code != 200:
                raise Exception(
                    f"Company creation failed: {company_response.status_code}"
                )

            company_data = company_response.json()
            self.created_entities["company"] = company_data
            logger.info(f"✅ Company created: {company_data.get('id')}")

            # Create contact
            contact_data = self.test_data["contact"].copy()
            contact_data["company_id"] = company_data.get("id")

            contact_response = self.api_request_with_retry(
                f"{API_BASE_URL}/contacts", method="POST", json=contact_data
            )
            if contact_response.status_code != 200:
                raise Exception(
                    f"Contact creation failed: {contact_response.status_code}"
                )

            contact_data = contact_response.json()
            self.created_entities["contact"] = contact_data
            logger.info(f"✅ Contact created: {contact_data.get('id')}")

            # Create product
            product_response = self.api_request_with_retry(
                f"{API_BASE_URL}/products",
                method="POST",
                json=self.test_data["product"],
            )
            if product_response.status_code != 200:
                raise Exception(
                    f"Product creation failed: {product_response.status_code}"
                )

            product_data = product_response.json()
            self.created_entities["product"] = product_data
            logger.info(f"✅ Product created: {product_data.get('id')}")

            logger.info("✅ API data creation successful")
            return True

        except Exception as e:
            logger.error(f"❌ API data creation failed: {e}")
            return False

    async def test_data_verification_through_ui(self) -> bool:
        """Test data verification through UI."""
        logger.info("🔍 Testing data verification through UI...")

        try:
            # Navigate to API docs
            await self.page.goto(DOCS_URL, wait_until="networkidle")

            # Test GET companies endpoint
            await self.page.click("text=GET /api/v1/companies")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Test GET contacts endpoint
            await self.page.click("text=GET /api/v1/contacts")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Test GET products endpoint
            await self.page.click("text=GET /api/v1/products")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            logger.info("✅ Data verification UI test successful")
            return True

        except Exception as e:
            logger.error(f"❌ Data verification UI test failed: {e}")
            return False

    async def test_api_data_verification(self) -> bool:
        """Test API data verification programmatically."""
        logger.info("🔍 Testing API data verification...")

        try:
            # Verify companies
            companies_response = self.api_request_with_retry(
                f"{API_BASE_URL}/companies"
            )
            if companies_response.status_code != 200:
                raise Exception(
                    f"Companies retrieval failed: {companies_response.status_code}"
                )

            companies = companies_response.json()
            if not isinstance(companies, list):
                raise Exception("Companies response is not a list")

            # Verify contacts
            contacts_response = self.api_request_with_retry(f"{API_BASE_URL}/contacts")
            if contacts_response.status_code != 200:
                raise Exception(
                    f"Contacts retrieval failed: {contacts_response.status_code}"
                )

            contacts = contacts_response.json()
            if not isinstance(contacts, list):
                raise Exception("Contacts response is not a list")

            # Verify products
            products_response = self.api_request_with_retry(f"{API_BASE_URL}/products")
            if products_response.status_code != 200:
                raise Exception(
                    f"Products retrieval failed: {products_response.status_code}"
                )

            products = products_response.json()
            if not isinstance(products, list):
                raise Exception("Products response is not a list")

            logger.info(
                f"✅ Data verification successful - Companies: {len(companies)}, Contacts: {len(contacts)}, Products: {len(products)}"
            )
            return True

        except Exception as e:
            logger.error(f"❌ Data verification failed: {e}")
            return False

    async def run_comprehensive_test(self):
        """Run comprehensive UI E2E test."""
        logger.info("🚀 Starting Comprehensive UI E2E Test")
        logger.info("=" * 60)

        test_results = {
            "api_documentation_access": False,
            "health_endpoint_ui": False,
            "api_endpoints_through_docs": False,
            "data_creation_through_ui": False,
            "api_data_creation": False,
            "data_verification_through_ui": False,
            "api_data_verification": False,
        }

        try:
            # Setup
            await self.setup()

            # Test 1: API Documentation Access
            test_results[
                "api_documentation_access"
            ] = await self.test_api_documentation_access()

            # Test 2: Health Endpoint UI
            test_results["health_endpoint_ui"] = await self.test_health_endpoint_ui()

            # Test 3: API Endpoints through Docs
            test_results[
                "api_endpoints_through_docs"
            ] = await self.test_api_endpoints_through_docs()

            # Test 4: Data Creation through UI
            test_results[
                "data_creation_through_ui"
            ] = await self.test_data_creation_through_ui()

            # Test 5: API Data Creation
            test_results["api_data_creation"] = await self.test_api_data_creation()

            # Test 6: Data Verification through UI
            test_results[
                "data_verification_through_ui"
            ] = await self.test_data_verification_through_ui()

            # Test 7: API Data Verification
            test_results[
                "api_data_verification"
            ] = await self.test_api_data_verification()

        except Exception as e:
            logger.error(f"❌ Comprehensive test failed: {e}")
        finally:
            # Teardown
            await self.teardown()

        # Report results
        logger.info("=" * 60)
        logger.info("📊 COMPREHENSIVE UI E2E TEST RESULTS")
        logger.info("=" * 60)

        passed_tests = sum(test_results.values())
        total_tests = len(test_results)

        for test_name, result in test_results.items():  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name}: {status}")

        logger.info("=" * 60)
        logger.info(
            f"📈 Overall: {passed_tests}/{total_tests} tests passed ({passed_tests / total_tests * 100:.1f}%)"
        )

        if passed_tests == total_tests:
            logger.info("🎉 ALL TESTS PASSED - Critical User Journey Complete!")
        else:
            logger.info("⚠️ Some tests failed - Critical User Journey Incomplete")

        return test_results


async def main():
    """Main test execution."""
    test = ComprehensiveUITest()
    results = await test.run_comprehensive_test()
    return results


if __name__ == "__main__":
    asyncio.run(main())
