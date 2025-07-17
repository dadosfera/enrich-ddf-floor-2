#!/usr/bin/env python3
"""
Basic test to verify the application setup.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))


def test_basic_imports():
    """Test that basic imports work."""
    try:
        from app.main import app  # noqa: F401
        print("✅ Main application import successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_app_creation():
    """Test that the app can be created."""
    try:
        from app.main import create_application
        app = create_application()
        print("✅ Application creation successful")
        print(f"   App title: {app.title}")
        print(f"   App version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False


def main():
    """Run basic tests."""
    print("🧪 Running basic tests for Enrich DDF Floor 2")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_app_creation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! Application setup is working.")
        return 0
    else:
        print("❌ Some tests failed. Please check the setup.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 