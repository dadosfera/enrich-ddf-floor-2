#!/usr/bin/env python3
"""
Comprehensive Test Runner for All Fixed UI E2E Tests
Runs all fixed tests to verify critical user journey completion
"""

import asyncio
import logging
import subprocess
import sys
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Test files to run
TEST_FILES = [
    "tests/e2e/test_ui_critical_journey_fixed_server.py",
    "tests/e2e/test_ui_critical_journey_final_complete_fixed.py",
    "tests/e2e/test_ui_critical_journey_comprehensive_ui_fixed.py",
    "tests/e2e/test_ui_critical_journey_fixed_complete.py",
    "tests/e2e/test_ui_critical_journey_comprehensive_fixed.py",
    "tests/e2e/test_ui_critical_journey_legacy_fixed.py",
    "tests/e2e/test_ui_critical_journey_final_complete_legacy_fixed.py",
]


async def run_test_file(test_file):
    """Run a single test file and return results."""
    logger.info(f"🚀 Running test: {test_file}")

    try:
        # Run the test file
        result = subprocess.run(
            ["./venv/bin/python", test_file],
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )

        if result.returncode == 0:
            logger.info(f"✅ {test_file}: PASSED")
            return {"file": test_file, "status": "PASS", "output": result.stdout}
        else:
            logger.error(f"❌ {test_file}: FAILED")
            logger.error(f"Error output: {result.stderr}")
            return {"file": test_file, "status": "FAIL", "output": result.stderr}

    except subprocess.TimeoutExpired:
        logger.exception(f"⏰ {test_file}: TIMEOUT")
        return {
            "file": test_file,
            "status": "TIMEOUT",
            "output": "Test execution timed out",
        }
    except Exception as e:
        logger.exception(f"💥 {test_file}: ERROR")
        return {"file": test_file, "status": "ERROR", "output": str(e)}


async def run_all_tests():
    """Run all fixed test files and report results."""
    logger.info("🚀 Starting Comprehensive UI E2E Test Suite")
    logger.info("=" * 80)
    logger.info(f"📅 Test run started at: {datetime.now()}")
    logger.info(f"📋 Total test files: {len(TEST_FILES)}")
    logger.info("=" * 80)

    results = []

    for test_file in TEST_FILES:
        result = await run_test_file(test_file)
        results.append(result)
        logger.info("-" * 60)

    # Calculate statistics
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    timeout = sum(1 for r in results if r["status"] == "TIMEOUT")
    error = sum(1 for r in results if r["status"] == "ERROR")
    total = len(results)

    success_rate = (passed / total) * 100 if total > 0 else 0

    # Print summary
    logger.info("=" * 80)
    logger.info("📊 COMPREHENSIVE TEST SUITE RESULTS")
    logger.info("=" * 80)

    for result in results:
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        logger.info(f"{status_icon} {result['file']}: {result['status']}")

    logger.info("=" * 80)
    logger.info("📈 Overall Statistics:")
    logger.info(f"   Total Tests: {total}")
    logger.info(f"   Passed: {passed}")
    logger.info(f"   Failed: {failed}")
    logger.info(f"   Timeout: {timeout}")
    logger.info(f"   Error: {error}")
    logger.info(f"   Success Rate: {success_rate:.1f}%")

    if success_rate == 100:
        logger.info("🎉 ALL TESTS PASSED - CRITICAL USER JOURNEY COMPLETE!")
        logger.info("🏆 MISSION ACCOMPLISHED!")
        return True
    else:
        logger.info("⚠️ Some tests failed - Critical User Journey Incomplete")
        return False


async def main():
    """Main test runner."""
    success = await run_all_tests()
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
