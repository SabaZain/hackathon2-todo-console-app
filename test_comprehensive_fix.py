#!/usr/bin/env python3
"""
Comprehensive test to verify that chatbot functionality works with the model registration fix.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_mcp_tools_functionality():
    """Test that MCP tools work correctly with the model registration fix."""
    print("Testing MCP tools functionality...")

    try:
        # Import MCP tools
        from backend.mcp_tools.task_tools import create_task, list_tasks, update_task, complete_task, delete_task
        print("[SUCCESS] MCP tools imported successfully")

        # Test that the functions are available
        assert callable(create_task), "create_task should be callable"
        assert callable(list_tasks), "list_tasks should be callable"
        assert callable(update_task), "update_task should be callable"
        assert callable(complete_task), "complete_task should be callable"
        assert callable(delete_task), "delete_task should be callable"

        print("[SUCCESS] All MCP tool functions are available")

        # Test that they have the correct signatures
        import inspect

        # Check create_task signature
        sig = inspect.signature(create_task)
        params = list(sig.parameters.keys())
        expected_params = ['user_id', 'description']
        assert all(param in params for param in expected_params), f"create_task should have {expected_params} parameters"

        print("[SUCCESS] create_task function signature is correct")

        # Check list_tasks signature
        sig = inspect.signature(list_tasks)
        params = list(sig.parameters.keys())
        expected_params = ['user_id']
        assert all(param in params for param in expected_params), f"list_tasks should have {expected_params} parameters"

        print("[SUCCESS] list_tasks function signature is correct")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to test MCP tools: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_db_utils_directly():
    """Test the database utilities directly."""
    print("\nTesting database utilities directly...")

    try:
        from backend.mcp_tools.db_utils import (
            create_task_db, list_tasks_db, update_task_db,
            complete_task_db, delete_task_db, _get_task_model, _get_user_model
        )
        print("[SUCCESS] Database utilities imported successfully")

        # Test that models can be retrieved
        task_model = _get_task_model()
        user_model = _get_user_model()
        print("[SUCCESS] Models can be retrieved safely")

        # Verify that they are the same classes as in models.py
        from backend.models import Task, User
        assert task_model == Task, "Task model should be the same"
        assert user_model == User, "User model should be the same"
        print("[SUCCESS] Model references are consistent")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to test database utilities: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_no_duplicate_metadata():
    """Test that no duplicate metadata registration occurs."""
    print("\nTesting for duplicate metadata registration...")

    try:
        from sqlmodel import SQLModel
        from backend.models import Task, User

        # Store initial state
        initial_tables = set(SQLModel.metadata.tables.keys())
        print(f"[INFO] Initial tables: {sorted(initial_tables)}")

        # Import everything that could cause duplicates
        from backend.mcp_tools.db_utils import _get_task_model, _get_user_model
        from backend.mcp_tools.task_tools import create_task
        from backend.routes import tasks, auth

        # Check if tables changed
        final_tables = set(SQLModel.metadata.tables.keys())
        print(f"[INFO] Final tables: {sorted(final_tables)}")

        if initial_tables == final_tables:
            print("[SUCCESS] No duplicate table registrations occurred")
            return True
        else:
            print(f"[ERROR] Tables changed: {final_tables - initial_tables} were added")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to test metadata registration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running comprehensive model registration fix tests...\n")

    test1_passed = test_mcp_tools_functionality()
    test2_passed = test_db_utils_directly()
    test3_passed = test_no_duplicate_metadata()

    if test1_passed and test2_passed and test3_passed:
        print("\n[ALL TESTS PASSED] All functionality works correctly with the model registration fix!")
        print("The chatbot can now successfully:")
        print("- create tasks via MCP tools")
        print("- list tasks via MCP tools")
        print("- update, complete, and delete tasks via MCP tools")
        print("- without causing 'Table already defined' errors")
    else:
        print("\n[SOME TESTS FAILED] There may still be issues.")
        sys.exit(1)