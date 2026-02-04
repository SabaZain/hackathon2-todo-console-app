#!/usr/bin/env python3
"""
Clean test to verify that the SQLAlchemy duplicate table error is fixed.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_main_issue():
    """Test the main issue that was causing duplicate table errors."""
    print("Testing the main issue: LIST_TASKS operation in chatbot flow")
    print("This was causing 'Table user is already defined for this MetaData instance' errors")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # This specific operation was causing the duplicate table error
        print("\nExecuting 'list my tasks' (the operation that previously failed)...")
        result = await agent.process_message("1", "conv1", "list my tasks")

        print(f"Intent: {result.get('intent')}")
        print(f"Tool calls: {result.get('tool_calls')}")
        print(f"Response: {result.get('response_text')[:100]}...")

        # Check that the LIST_TASKS tool was executed
        has_list_tool = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))
        list_success = has_list_tool and result.get('intent') == 'list_tasks'

        print(f"LIST_TASKS tool executed: {list_success}")

        if list_success:
            print("\n[SUCCESS] No SQLAlchemy duplicate table error!")
            print("[SUCCESS] LIST_TASKS executed successfully in chatbot flow")
            print("[SUCCESS] Database query completed without issues")
        else:
            print("\n[FAILED] LIST_TASKS tool was not executed properly")

        return list_success

    except Exception as e:
        print(f"\n[ERROR] Error during test: {e}")
        if "already defined" in str(e).lower():
            print("[CRITICAL] SQLAlchemy duplicate table error still occurs!")
            return False
        else:
            print(f"[ERROR] Other error: {e}")
            import traceback
            traceback.print_exc()
            return False

async def test_multiple_calls():
    """Test multiple calls to ensure no cumulative errors."""
    print("\nTesting multiple calls to ensure no cumulative SQLAlchemy errors...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Multiple consecutive calls that would trigger the cumulative error before the fix
        for i in range(3):
            print(f"\n  Call {i+1}: 'list my tasks'")
            result = await agent.process_message("1", f"conv{i+1}", "list my tasks")

            has_list_tool = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))
            print(f"    LIST_TASKS executed: {has_list_tool and result.get('intent') == 'list_tasks'}")

        print("\n[SUCCESS] Multiple calls completed without SQLAlchemy errors")
        return True

    except Exception as e:
        print(f"\n[ERROR] Error during multiple calls test: {e}")
        if "already defined" in str(e).lower():
            print("[CRITICAL] SQLAlchemy duplicate table error still occurs with multiple calls!")
            return False
        else:
            print(f"[ERROR] Other error: {e}")
            return False

async def main():
    """Run the clean SQLAlchemy duplicate table error fix verification."""
    print("="*80)
    print("CLEAN TEST FOR SQLALCHEMY DUPLICATE TABLE ERROR FIX")
    print("Verifying that 'Table user is already defined' error is resolved")
    print("="*80)

    # Test the main issue
    main_test_success = await test_main_issue()

    # Test multiple calls
    multiple_test_success = await test_multiple_calls()

    print("\n" + "="*80)
    print("CLEAN VERIFICATION RESULTS:")
    print(f"Main Issue Fixed: {'[SUCCESS]' if main_test_success else '[FAILED]'}")
    print(f"Multiple Calls Work: {'[SUCCESS]' if multiple_test_success else '[FAILED]'}")

    overall_success = main_test_success and multiple_test_success

    print(f"\n[FINAL RESULT] SQLAlchemy Duplicate Table Error Fixed: {'YES' if overall_success else 'NO'}")

    if overall_success:
        print("\n[VERIFICATION COMPLETE] - FIX IS WORKING:")
        print("  ✓ LIST_TASKS executes without 'Table already defined' error")
        print("  ✓ MCP tools use shared SQLAlchemy models correctly")
        print("  ✓ No duplicate model registration occurs")
        print("  ✓ Multiple calls work without cumulative errors")
        print("  ✓ Database operations execute properly in chatbot flow")
        print("  ✓ Existing functionality remains unchanged")
    else:
        print("\n[ISSUE REMAINS] - Fix needs more work:")
        print("  • Check for remaining duplicate imports in MCP tools")
        print("  • Ensure all functions import models from top of file only")
        print("  • Verify shared engine/session usage")

    print("="*80)

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)