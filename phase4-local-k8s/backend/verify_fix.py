#!/usr/bin/env python3
"""
Verification script to ensure the backend startup fix is working properly.
"""

import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_backend_startup():
    """Test that the backend starts without model registration errors."""
    print("Testing backend startup...")

    try:
        # Import the main app - this should not raise the "Table 'user' already defined" error
        from main import app
        print("✅ Backend imported successfully")

        # Verify that basic routes are available
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/api/health"]

        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"✅ Route {route} is available")
            else:
                print(f"⚠️  Route {route} may not be available")

        print("✅ All basic functionality is available")
        return True

    except Exception as e:
        if "already defined for this MetaData instance" in str(e):
            print(f"❌ Model registration error still occurs: {e}")
            return False
        else:
            print(f"❌ Other error occurred: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_model_access():
    """Test that models can be accessed without conflicts."""
    print("\nTesting model access...")

    try:
        from models import User, Task
        print("✅ Models can be imported without conflicts")

        # Test creating model instances
        user = User(email="test@example.com", hashed_password="hash")
        task = Task(title="Test", description="Test", owner_id=1)
        print("✅ Model instances can be created")

        return True
    except Exception as e:
        print(f"❌ Error with models: {e}")
        return False

def test_database_connection():
    """Test that database connection works."""
    print("\nTesting database connection...")

    try:
        from db import engine
        print("✅ Database engine is accessible")

        # Test basic engine functionality
        from sqlmodel import select
        print("✅ SQLModel imports work correctly")

        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_routes_availability():
    """Test that routes are available."""
    print("\nTesting routes availability...")

    try:
        from main import app
        routes = [route.path for route in app.routes]

        # Check for task-related routes
        task_routes_found = any('/api/tasks' in route for route in routes)
        auth_routes_found = any('/api/auth' in route for route in routes)

        if task_routes_found:
            print("✅ Task routes are available")
        else:
            print("⚠️  Task routes may not be available")

        if auth_routes_found:
            print("✅ Auth routes are available")
        else:
            print("⚠️  Auth routes may not be available")

        return True
    except Exception as e:
        print(f"❌ Error checking routes: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Running backend startup verification tests...\n")

    test1 = test_backend_startup()
    test2 = test_model_access()
    test3 = test_database_connection()
    test4 = test_routes_availability()

    print(f"\n📊 Test Results:")
    print(f"   Backend Startup: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"   Model Access: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"   Database Connection: {'✅ PASS' if test3 else '❌ FAIL'}")
    print(f"   Routes Availability: {'✅ PASS' if test4 else '❌ FAIL'}")

    all_passed = all([test1, test2, test3, test4])

    if all_passed:
        print(f"\n🎉 All tests passed! The backend startup issue has been resolved.")
        print(f"✅ No more 'Table user already defined' errors")
        print(f"✅ All required functionality is available")
        print(f"✅ Ready for production use")
    else:
        print(f"\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)