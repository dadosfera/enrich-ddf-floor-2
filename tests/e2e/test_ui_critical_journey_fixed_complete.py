#!/usr/bin/env python3
"""
Fixed Complete UI E2E Test for Enrich DDF Floor 2
Critical User Journey: Complete without errors
Implements all fixes from comprehensive plan
"""

import asyncio
import logging
import subprocess
import time
import uuid

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


class FixedCompleteUITest:
    """Fixed Complete UI E2E test with all optimizations."""

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.created_entities = {}
        self.test_results = {}
        self.server_process = None

        # Generate unique test data with timestamp
        unique_id = str(uuid.uuid4())[:8]

        self.test_data = {
            "company": {
                "name": f"Test Company {timestamp}_{unique_id}",
                "domain": f"test{timestamp}{unique_id}.com",
                "industry": "Technology",
                "size": "Medium",
                "location": "San Francisco, CA",
                "description": "A test company for UI E2E testing",
                "website": f"https://test{timestamp}{unique_id}.com",
                "phone": "+1-555-123-4567",
                "email": f"contact@test{timestamp}{unique_id}.com",
            },
            "contact": {
                "first_name": "John",
                "last_name": "Doe",
                "email": f"john.doe.{timestamp}{unique_id}@example.com",
                "phone": "+1-555-987-6543",
                "job_title": "Senior Developer",
                "department": "Engineering",
                "linkedin_url": f"https://linkedin.com/in/john-doe-{timestamp}{unique_id}",
                "twitter_url": f"https://twitter.com/johndoe{timestamp}{unique_id}",
            },
            "product": {
                "name": f"Test Product {timestamp}_{unique_id}",
                "sku": f"SKU-{timestamp}-{unique_id}",
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
                "product_url": f"https://test{timestamp}{unique_id}.com/product",
                "image_url": f"https://test{timestamp}{unique_id}.com/image.jpg",
            },
        }

    def start_server(self):
        """Start server if not running."""
        logger.info("🚀 Starting server...")
        try:
            self.server_process = subprocess.Popen(
                ["./venv/bin/python", "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            time.sleep(3)  # Give server time to start
            logger.info("✅ Server started")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            return False

    def stop_server(self):
        """Stop server gracefully."""
        if self.server_process:
            logger.info("🛑 Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            logger.info("✅ Server stopped")

    def check_server_health(self):
        """Check if server is healthy."""
        try:
            response = requests.get(HEALTH_URL, timeout=5)
            return response.status_code == 200
        except:
            return False

    async def ensure_server_running(self):
        """Ensure server is running and healthy."""
        logger.info("🔍 Checking server status...")

        # First check if server is already running
        if self.check_server_health():
            logger.info("✅ Server is already running and healthy")
            return True

        # Start server if not running
        if not self.start_server():
            raise Exception("Failed to start server")

        # Wait for server to be ready
        for attempt in range(5):
            await asyncio.sleep(2)
            if self.check_server_health():
                logger.info("✅ Server is running and healthy")
                return True

        raise Exception("Server failed to start after multiple attempts")

    async def api_request_with_retry(self, url, method="GET", **kwargs):
        """Make API request with optimized retry logic."""
        for attempt in range(3):  # Reduced from 10 to 3
            try:
                response = requests.request(
                    method, url, timeout=10, **kwargs
                )  # Reduced from 20s to 10s
                return response
            except requests.exceptions.ConnectionError as e:
                if attempt == 2:  # Last attempt
                    raise e
                logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(1)  # Reduced delay
            except Exception as e:
                if attempt == 2:
                    raise e
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(1)

    async def setup(self):
        """Set up test environment with server management."""
        logger.info("🔧 Setting up fixed complete UI test environment...")

        # Ensure server is running
        await self.ensure_server_running()

        # Initialize Playwright with optimized settings
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-web-security"],
        )
        self.page = await self.browser.new_page()

        # Set optimized timeouts
        self.page.set_default_timeout(15000)  # Reduced from 30s to 15s
        self.page.set_default_navigation_timeout(15000)

        logger.info("✅ Test environment setup complete")

    async def test_server_health(self) -> bool:
        """Test server health endpoint."""
        logger.info("❤️ Testing server health...")

        try:
            response = await self.api_request_with_retry(HEALTH_URL)
            if response.status_code == 200:
                health_data = response.json()
                logger.info(f"✅ Server health: {health_data.get('status')}")
                return True
            else:
                raise Exception(f"Health check failed: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Server health test failed: {e}")
            return False

    async def test_api_documentation_access(self) -> bool:
        """Test API documentation access."""
        logger.info("📚 Testing API documentation access...")

        try:
            await self.page.goto(DOCS_URL, wait_until="networkidle")

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
            await self.page.goto(HEALTH_URL, wait_until="networkidle")

            content = await self.page.content()
            if "healthy" not in content.lower():
                raise Exception("Health endpoint not displaying expected content")

            logger.info("✅ Health endpoint UI test successful")
            return True

        except Exception as e:
            logger.error(f"❌ Health endpoint UI test failed: {e}")
            return False

    async def test_api_data_creation(self) -> bool:
        """Test API data creation."""
        logger.info("🔧 Testing API data creation...")

        try:
            # Create company
            company_response = await self.api_request_with_retry(
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

            contact_response = await self.api_request_with_retry(
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
            product_response = await self.api_request_with_retry(
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

    async def test_api_data_verification(self) -> bool:
        """Test API data verification."""
        logger.info("🔍 Testing API data verification...")

        try:
            # Verify companies
            companies_response = await self.api_request_with_retry(
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
            contacts_response = await self.api_request_with_retry(
                f"{API_BASE_URL}/contacts"
            )
            if contacts_response.status_code != 200:
                raise Exception(
                    f"Contacts retrieval failed: {contacts_response.status_code}"
                )

            contacts = contacts_response.json()
            if not isinstance(contacts, list):
                raise Exception("Contacts response is not a list")

            # Verify products
            products_response = await self.api_request_with_retry(
                f"{API_BASE_URL}/products"
            )
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

    async def test_ui_navigation(self) -> bool:
        """Test basic UI navigation."""
        logger.info("🧭 Testing UI navigation...")

        try:
            await self.page.goto(DOCS_URL, wait_until="networkidle")

            # Wait for documentation to load with shorter timeout
            await self.page.wait_for_selector("div.opblock", timeout=5000)

            # Try multiple selector strategies
            selectors = [
                "text=GET",
                "text=POST",
                "text=companies",
                "text=contacts",
                "text=products",
            ]

            for selector in selectors:
                try:
                    await self.page.click(selector, timeout=3000)
                    logger.info(f"✅ Found UI element with selector: {selector}")
                    break
                except Exception:
                    continue
            else:
                logger.info("✅ API documentation loaded successfully")

            logger.info("✅ UI navigation test successful")
            return True

        except Exception as e:
            logger.error(f"❌ UI navigation test failed: {e}")
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

        # Don't stop server here as it might be used by other tests
        logger.info("✅ Test environment cleanup complete")

    async def run_fixed_complete_test(self):
        """Run fixed complete UI E2E test."""
        logger.info("🚀 Starting Fixed Complete UI E2E Test")
        logger.info("=" * 60)

        try:
            await self.setup()

            tests = [
                ("server_health", self.test_server_health),
                ("api_documentation_access", self.test_api_documentation_access),
                ("health_endpoint_ui", self.test_health_endpoint_ui),
                ("api_data_creation", self.test_api_data_creation),
                ("api_data_verification", self.test_api_data_verification),
                ("ui_navigation", self.test_ui_navigation),
            ]

            for test_name, test_func in tests:
                try:
                    result = await test_func()
                    self.test_results[test_name] = result
                except Exception as e:
                    logger.error(f"❌ {test_name} failed with exception: {e}")
                    self.test_results[test_name] = False

            passed_tests = sum(1 for result in self.test_results.values() if result)  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
            total_tests = len(self.test_results)
            success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

            logger.info("=" * 60)
            logger.info("📊 FIXED COMPLETE UI E2E TEST RESULTS")
            logger.info("=" * 60)

            for test_name, result in self.test_results.items():  # TODO: Review loop variable naming (PLW2901)  # TODO: Review loop variable naming (PLW2901)
                status = "✅ PASS" if result else "❌ FAIL"
                logger.info(f"{test_name}: {status}")

            logger.info("=" * 60)
            logger.info(
                f"📈 Overall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)"
            )

            if success_rate == 100:
                logger.info("🎉 All tests passed - Critical User Journey Complete!")
                logger.info("🎯 MISSION ACCOMPLISHED!")
            else:
                logger.info("⚠️ Some tests failed - Critical User Journey Incomplete")

            return success_rate == 100

        except Exception as e:
            logger.error(f"❌ Fixed complete test failed: {e}")
            return False

        finally:
            await self.cleanup()


async def main():
    """Main test runner."""
    test = FixedCompleteUITest()
    success = await test.run_fixed_complete_test()
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
