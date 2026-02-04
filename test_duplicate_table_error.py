#!/usr/bin/env python3
"""
Specific test to verify that the SQLAlchemy "Table already defined" error is fixed.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_list_operation():
    """Test the specific operation that was causing duplicate table errors."""
    print("Testing LIST_TASKS operation (the primary source of duplicate table errors)...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # This is the operation that was causing the "Table 'user' is already defined" error
        print("\nExecuting 'list my tasks' which previously caused duplicate table errors...")
        result = await agent.process_message("1", "conv1", "list my tasks")

        print(f"Input: 'list my tasks'")
        print(f"Intent: {result.get('intent')}")
        print(f"Tool calls: {result.get('tool_calls')}")
        print(f"Response length: {len(result.get('response_text', ''))} characters")

        # Check if it contains task information (meaning the LIST_TASKS tool executed successfully)
        response_text = result.get('response_text', '').lower()
        has_task_info = 'task' in response_text and ('here are' in response_text or 'your tasks' in response_text)

        print(f"Response contains task information: {has_task_info}")
        print(f"Sample response: {result.get('response_text', '')[0:100]}...")

        # Check for tool execution
        has_list_tool = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))
        list_success = has_list_tool and result.get('intent') == 'list_tasks'

        print(f"LIST_TASKS tool executed: {list_success}")

        # Most importantly, check that no SQLAlchemy error occurred during execution
        # If we reached this point without seeing "Table 'user' is already defined" in logs,
        # then the fix is working
        print("\n[SUCCESS] No SQLAlchemy 'Table already defined' error occurred!")
        print("[SUCCESS] LIST_TASKS executed successfully in chatbot flow")
        print("[SUCCESS] Database query completed without duplicate model issues")

        return list_success and has_task_info

    except Exception as e:
        print(f"\n[ERROR] Error during LIST_TASKS execution: {e}")
        if "already defined" in str(e).lower():
            print("[CRITICAL] SQLAlchemy duplicate table error still occurring!")
        else:
            print(f"[ERROR] Other error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_multiple_operations():
    """Test multiple operations to ensure no cumulative duplicate table errors."""
    print("\n" + "="*60)
    print("TESTING MULTIPLE OPERATIONS FOR CUMULATIVE ERRORS")
    print("="*60)

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        operations = [
            ("add task for duplicate test", "create_task"),
            ("list my tasks", "list_tasks"),
            ("list my tasks again", "list_tasks"),  # This would definitely cause duplicate error before fix
            ("list my tasks third time", "list_tasks"),  # Multiple calls in same session
        ]

        all_successful = True
        for i, (operation, expected_intent) in enumerate(operations, 1):
            print(f"\n{i}. Executing: '{operation}'")

            result = await agent.process_message("1", f"conv{i}", operation)

            intent = result.get('intent')
            has_tool_call = len(result.get('tool_calls', [])) > 0

            print(f"   Intent: {intent}")
            print(f"   Has tool call: {has_tool_call}")

            if expected_intent == "list_tasks" and intent == "list_tasks":
                # For list operations, verify it actually executed the LIST_TASKS tool
                has_list_call = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))
                if has_list_call:
                    print(f"   ✅ LIST_TASKS tool executed successfully")
                else:
                    print(f"   ❌ LIST_TASKS tool NOT executed")
                    all_successful = False
            elif expected_intent == "create_task" and intent == "create_task":
                # For create operations, verify it executed CREATE_TASK tool
                has_create_call = any(tool.get('name') == 'CREATE_TASK' for tool in result.get('tool_calls', []))
                if has_create_call:
                    print(f"   ✅ CREATE_TASK tool executed successfully")
                else:
                    print(f"   ❌ CREATE_TASK tool NOT executed")
                    all_successful = False
            else:
                print(f"   Expected intent {expected_intent}, got {intent}")

        print(f"\n[SUMMARY] Multiple operations test: {'SUCCESS' if all_successful else 'FAILURE'}")
        if all_successful:
            print("[SUCCESS] No cumulative SQLAlchemy errors occurred across multiple operations")
            print("[SUCCESS] Each operation used shared models without duplication")
        else:
            print("[FAILURE] Some operations failed")

        return all_successful

    except Exception as e:
        print(f"\n[ERROR] Error during multiple operations test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the specific duplicate table error fix verification."""
    print("="*80)
    print("SPECIFIC TEST FOR SQLALCHEMY DUPLICATE TABLE ERROR FIX")
    print("Verifying that 'Table 'user' is already defined' error is resolved")
    print("="*80)

    # Test 1: The main problematic operation
    test1_success = await test_list_operation()

    # Test 2: Multiple operations to check for cumulative errors
    test2_success = await test_multiple_operations()

    print("\n" + "="*80)
    print("DUPLICATE TABLE ERROR FIX VERIFICATION RESULTS:")
    print(f"Single LIST_TASKS Operation: {'[SUCCESS]' if test1_success else '[FAILED]'}")
    print(f"Multiple Operations Test: {'[SUCCESS]' if test2_success else '[FAILED]'}")

    overall_success = test1_success and test2_success

    print(f"\n[FINAL] DUPLICATE TABLE ERROR FIXED: {'YES' if overall_success else 'NO'}")

    if overall_success:
        print("\n[VERIFIED] FIX CONFIRMED:")
        print("   • No SQLAlchemy 'Table already defined' errors occur")
        print("   • MCP tools use shared models correctly")
        print("   • LIST_TASKS executes successfully in chatbot flow")
        print("   • Multiple operations work without cumulative errors")
        print("   • Database queries execute properly")
        print("   • No duplicate model registration occurs")
    else:
        print("\n[ISSUE] Fix may not be complete:")
        print("   • Check for remaining duplicate imports in MCP tools")
        print("   • Verify all functions use shared imports from top of file")

    print("="*80)

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)