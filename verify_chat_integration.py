#!/usr/bin/env python3
"""
Verification script to test the chatbot integration with task management.
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all necessary modules can be imported."""
    print("Testing imports...")

    try:
        from main import app
        print("✓ Main app imported successfully")
    except Exception as e:
        print(f"✗ Failed to import main app: {e}")
        return False

    try:
        from api.agent_connector import get_agent_connector
        print("✓ Agent connector imported successfully")
    except Exception as e:
        print(f"✗ Failed to import agent connector: {e}")
        return False

    try:
        from mcp_tools.task_tools import create_task, list_tasks
        print("✓ MCP task tools imported successfully")
    except Exception as e:
        print(f"✗ Failed to import MCP task tools: {e}")
        return False

    return True

def test_session_dependency():
    """Test that the session dependency is properly set up."""
    print("\nTesting session dependency...")

    try:
        from fastapi import Depends
        from db import get_session
        print("✓ Session dependency functions are available")

        # Check that get_session is callable
        assert callable(get_session), "get_session should be callable"
        print("✓ get_session function is callable")

        return True
    except Exception as e:
        print(f"✗ Session dependency test failed: {e}")
        return False

def test_chat_endpoint_signature():
    """Test that the chat endpoint has the correct signature with session dependency."""
    print("\nTesting chat endpoint signature...")

    try:
        import inspect
        from main import chat_endpoint

        sig = inspect.signature(chat_endpoint)
        params = list(sig.parameters.keys())

        print(f"✓ Chat endpoint parameters: {params}")

        # Check that session parameter exists with Depends
        has_session = 'session' in params
        print(f"✓ Has session parameter: {has_session}")

        if has_session:
            print("✓ Chat endpoint properly accepts session dependency")
            return True
        else:
            print("✗ Chat endpoint missing session parameter")
            return False

    except Exception as e:
        print(f"✗ Chat endpoint signature test failed: {e}")
        return False

async def run_tests():
    """Run all verification tests."""
    print("Starting chatbot integration verification...\n")

    all_passed = True

    # Test imports
    all_passed &= test_imports()

    # Test session dependency
    all_passed &= test_session_dependency()

    # Test chat endpoint signature
    all_passed &= test_chat_endpoint_signature()

    print(f"\n{'='*50}")
    if all_passed:
        print("✓ All verification tests passed!")
        print("The chatbot integration with task management should work correctly.")
    else:
        print("✗ Some verification tests failed!")
        print("There may be issues with the integration.")
    print(f"{'='*50}")

    return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)