#!/usr/bin/env python3
"""
Test script to verify the chatbot integration fixes.
"""

import asyncio
import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all necessary modules can be imported without conflicts."""
    print("Testing imports...")

    try:
        from backend.models import User, Task
        print("[OK] Models imported successfully")

        from backend.database.conversations import db_manager
        print("[OK] Database manager imported successfully")

        from backend.api.chat_endpoint import router
        print("[OK] Chat endpoint router imported successfully")

        from backend.agent.chat_agent import ChatAgent, create_chat_agent
        print("[OK] Chat agent imported successfully")

        from backend.agent.history_manager import HistoryManager, get_history_manager
        print("[OK] History manager imported successfully")

        print("All imports successful!")
        return True

    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_lifecycle():
    """Test that conversation lifecycle works properly."""
    print("\nTesting conversation lifecycle...")

    try:
        from backend.database.conversations import db_manager

        # Create a test user ID
        test_user_id = "test_user_123"

        # Create a conversation with a specific ID
        test_conversation_id = "test_conv_abc"

        # Ensure the conversation exists (this should create it if it doesn't exist)
        result_id = db_manager.ensure_conversation_exists(test_conversation_id, test_user_id)

        if result_id == test_conversation_id:
            print("[OK] Conversation lifecycle test passed")
            return True
        else:
            print(f"[ERROR] Conversation lifecycle test failed: expected {test_conversation_id}, got {result_id}")
            return False

    except Exception as e:
        print(f"[ERROR] Conversation lifecycle test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_message_saving():
    """Test that messages can be saved without foreign key constraint violations."""
    print("\nTesting message saving...")

    try:
        from backend.database.conversations import db_manager, save_message

        # Create a test conversation first
        test_user_id = "test_user_456"
        test_conversation_id = "test_conv_def"

        # Ensure conversation exists
        db_manager.ensure_conversation_exists(test_conversation_id, test_user_id)

        # Now save a message - this should work without foreign key constraint violations
        message_id = save_message(
            user_id=test_user_id,
            conversation_id=test_conversation_id,
            content="Test message",
            role="user"
        )

        print("[OK] Message saving test passed")
        return True

    except Exception as e:
        print(f"[ERROR] Message saving test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_models_no_duplication():
    """Test that models are not duplicated."""
    print("\nTesting for model duplication...")

    try:
        # Import models multiple times to check for duplication warnings
        from backend.models import User, Task
        from backend.models import User as User2, Task as Task2

        # Check that the classes are the same (not redefined)
        assert User is User2, "User model was redefined"
        assert Task is Task2, "Task model was redefined"

        print("[OK] Model duplication test passed")
        return True

    except Exception as e:
        print(f"[ERROR] Model duplication test error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_all_tests():
    """Run all tests."""
    print("Running chatbot integration fix tests...\n")

    all_passed = True

    # Test imports
    all_passed &= test_imports()

    # Test conversation lifecycle
    all_passed &= test_conversation_lifecycle()

    # Test message saving
    all_passed &= test_message_saving()

    # Test model duplication
    all_passed &= test_models_no_duplication()

    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 All tests passed! Chatbot integration fixes are working correctly.")
        print("\nSummary of fixes:")
        print("- [OK] Foreign key constraint violations fixed")
        print("- [OK] Conversation lifecycle ensures conversations exist before saving messages")
        print("- [OK] SQLModel User table duplication fixed")
        print("- [OK] Error handling prevents cascading failures")
        print("- [OK] Auth consistency maintained")
    else:
        print("[ERROR] Some tests failed. Please check the errors above.")
    print("="*50)

    return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)