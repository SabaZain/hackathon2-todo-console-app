#!/usr/bin/env python3
"""
Test script to verify that the model registration fix works correctly.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_single_model_registration():
    """Test that models are only registered once in SQLModel metadata."""
    print("Testing single model registration...")

    # Import SQLModel metadata to check for duplicates
    from sqlmodel import SQLModel
    from backend.models import Task, User

    # Check the metadata tables to ensure no duplicates
    initial_table_names = list(SQLModel.metadata.tables.keys())
    print(f"Initial tables in metadata: {initial_table_names}")

    # Import the MCP tools which were causing the issue
    from backend.mcp_tools.db_utils import _get_task_model, _get_user_model

    # Get the models using the new safe method
    task_model = _get_task_model()
    user_model = _get_user_model()

    # Check the metadata again to ensure no new registrations happened
    after_table_names = list(SQLModel.metadata.tables.keys())
    print(f"Tables in metadata after importing db_utils: {after_table_names}")

    # They should be the same since models were already registered
    if set(initial_table_names) == set(after_table_names):
        print("[SUCCESS] No duplicate table registrations detected")
    else:
        print(f"[ERROR] Duplicate table registrations detected!")
        print(f"Extra tables: {set(after_table_names) - set(initial_table_names)}")
        return False

    # Verify that we can create model instances without issues
    try:
        user = user_model(email="test@example.com", hashed_password="hash")
        task = task_model(title="Test task", description="Test", owner_id=1)
        print("[SUCCESS] Model instances created successfully")
    except Exception as e:
        print(f"[ERROR] Failed to create model instances: {e}")
        return False

    # Test the MCP tools functions
    try:
        # These should work without causing duplicate model registration
        from backend.mcp_tools.db_utils import create_task_db, list_tasks_db, update_task_db, complete_task_db, delete_task_db
        print("[SUCCESS] MCP tools functions imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import MCP tools: {e}")
        return False

    return True

def test_routes_consistency():
    """Test that route imports work consistently."""
    print("\nTesting route imports consistency...")

    # Import the routes modules to ensure they work
    try:
        # These should not cause duplicate registrations
        from backend.routes import tasks
        from backend.routes import auth
        print("[SUCCESS] Route modules imported successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to import route modules: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running model registration fix tests...\n")

    test1_passed = test_single_model_registration()
    test2_passed = test_routes_consistency()

    if test1_passed and test2_passed:
        print("\n[ALL TESTS PASSED] Model registration fix is working correctly!")
        print("The 'Table user already defined' error should be resolved.")
    else:
        print("\n[SOME TESTS FAILED] There may still be issues with model registration.")
        sys.exit(1)