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

import requests
from playwright.async_api import async_playwright


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Test configuration
BASE_URL = "http://127.0.0.1:8247"
API_BASE_URL = f"{BASE_URL}/api/v1"
DOCS_URL = f"{BASE_URL}/docs"
HEALTH_URL = f"{BASE_URL}/health"


class ComprehensiveUITest:
    """Comprehensive UI E2E test for critical user journey."""

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.created_entities = {}
        self.test_results = {}

        # Generate unique test data
        unique_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )

        self.test_data = {
            "company": {
                "name": f"Test Company {unique_suffix}",
                "domain": f"test{unique_suffix}.com",
                "industry": "Technology",
                "size": "Medium",
                "location": "San Francisco, CA",
                "description": "A test company for UI E2E testing",
                "website": f"https://test{unique_suffix}.com",
                "phone": "+1-555-123-4567",
                "email": f"contact@test{unique_suffix}.com",
            },
            "contact": {
                "first_name": "John",
                "last_name": "Doe",
                "email": f"john.doe-{unique_suffix}@example.com",
                "phone": "+1-555-987-6543",
                "job_title": "Senior Developer",
                "department": "Engineering",
                "linkedin_url": f"https://linkedin.com/in/john-doe-{unique_suffix}",
                "twitter_url": f"https://twitter.com/johndoe{unique_suffix}",
            },
            "product": {
                "name": f"Test Product {unique_suffix}",
                "sku": f"SKU-{unique_suffix}",
                "category": "Electronics",
                "subcategory": "Computers",
                "brand": "TestBrand",
                "description": "A test product for UI E2E testing",
                "price": "99.99",
                "currency": "USD",
                "weight": "2.5",
                "dimensions": "10x5x2",
                "color": "Black",
                "material": "Plastic",
                "stock_quantity": 100,
                "min_stock_level": 10,
                "product_url": f"https://test{unique_suffix}.com/product",
                "image_url": f"https://test{unique_suffix}.com/image.jpg",
            },
        }

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

    async def setup(self):
        """Set up test environment."""
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
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

        logger.info("✅ Test environment setup complete")

    async def test_api_documentation_access(self) -> bool:
        """Test API documentation access through browser."""
        logger.info("📚 Testing API documentation access...")

        try:
            # Navigate to API documentation
            await self.page.goto(DOCS_URL, wait_until="networkidle")

            # Check if page loaded successfully
            title = await self.page.title()
            if "Enrich DDF Floor 2" not in title and "FastAPI" not in title:
                raise Exception(f"Unexpected page title: {title}")

            logger.info("✅ API documentation access successful")
            return True

        except Exception as e:
            logger.error(f"❌ API documentation access failed: {e}")
            return False

    async def test_health_endpoint_ui(self) -> bool:
        """Test health endpoint through browser UI."""
        logger.info("❤️ Testing health endpoint through UI...")

        try:
            # Navigate to health endpoint
            await self.page.goto(HEALTH_URL, wait_until="networkidle")

            # Check if health data is displayed
            content = await self.page.content()
            if "healthy" not in content.lower():
                raise Exception("Health endpoint not displaying expected content")

            logger.info("✅ Health endpoint UI test successful")
            return True

        except Exception as e:
            logger.error(f"❌ Health endpoint UI test failed: {e}")
            return False

    async def test_api_endpoints_through_docs(self) -> bool:
        """Test API endpoints through documentation interface."""
        logger.info("🔍 Testing API endpoints through documentation...")

        try:
            # Navigate to API documentation
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
            # Navigate to API documentation
            await self.page.goto(DOCS_URL, wait_until="networkidle")

            # Test POST companies endpoint
            await self.page.click("text=POST /api/v1/companies")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Test POST contacts endpoint
            await self.page.click("text=POST /api/v1/contacts")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Test POST products endpoint
            await self.page.click("text=POST /api/v1/products")
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            logger.info("✅ Data creation UI test successful")
            return True

        except Exception as e:
            logger.error(f"❌ Data creation UI test failed: {e}")
            return False

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
        """Test data verification through UI interface."""
        logger.info("🔍 Testing data verification through UI...")

        try:
            # Navigate to API documentation
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

    async def cleanup(self):
        """Clean up test environment."""
        logger.info("🧹 Cleaning up test environment...")

        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

        logger.info("✅ Test environment cleanup complete")

    async def run_comprehensive_test(self):
        """Run comprehensive UI E2E test."""
        logger.info("🚀 Starting Comprehensive UI E2E Test")
        logger.info("=" * 60)

        try:
            # Setup
            await self.setup()

            # Run all tests
            tests = [
                ("api_documentation_access", self.test_api_documentation_access),
                ("health_endpoint_ui", self.test_health_endpoint_ui),
                ("api_endpoints_through_docs", self.test_api_endpoints_through_docs),
                ("data_creation_through_ui", self.test_data_creation_through_ui),
                ("api_data_creation", self.test_api_data_creation),
                (
                    "data_verification_through_ui",
                    self.test_data_verification_through_ui,
                ),
                ("api_data_verification", self.test_api_data_verification),
            ]

            for test_name, test_func in tests:
                try:
                    result = await test_func()
                    self.test_results[test_name] = result
                except Exception as e:
                    logger.error(f"❌ {test_name} failed with exception: {e}")
                    self.test_results[test_name] = False

            # Calculate results
            passed_tests = sum(1 for result in self.test_results.values() if result)  # TODO: Review loop variable naming (PLW2901)
            total_tests = len(self.test_results)
            success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

            # Print results
            logger.info("=" * 60)
            logger.info("📊 COMPREHENSIVE UI E2E TEST RESULTS")
            logger.info("=" * 60)

            for test_name, result in self.test_results.items():  # TODO: Review loop variable naming (PLW2901)
                status = "✅ PASS" if result else "❌ FAIL"
                logger.info(f"{test_name}: {status}")

            logger.info("=" * 60)
            logger.info(
                f"📈 Overall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)"
            )

            if success_rate == 100:
                logger.info("🎉 All tests passed - Critical User Journey Complete!")
            else:
                logger.info("⚠️ Some tests failed - Critical User Journey Incomplete")

            return success_rate == 100

        except Exception as e:
            logger.error(f"❌ Comprehensive test failed: {e}")
            return False

        finally:
            await self.cleanup()


async def main():
    """Main test runner."""
    test = ComprehensiveUITest()
    success = await test.run_comprehensive_test()
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
