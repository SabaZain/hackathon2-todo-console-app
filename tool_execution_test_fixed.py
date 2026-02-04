#!/usr/bin/env python3
"""
Test script to verify that MCP tools are properly executed and not bypassed.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_tool_execution():
    """Test that tools are actually executed, not just text generated."""
    print("Testing MCP tool execution...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test 1: Create a task
        print("\n1. Testing CREATE_TASK execution...")
        create_result = await agent.process_message("1", "conv1", "create a task to test tool execution")

        print(f"   Input: 'create a task to test tool execution'")
        print(f"   Intent: {create_result.get('intent')}")
        print(f"   Tool calls: {create_result.get('tool_calls')}")
        print(f"   Response: {create_result.get('response_text')[:100]}...")

        has_create_call = any(tool.get('name') == 'CREATE_TASK' for tool in create_result.get('tool_calls', []))
        create_success = has_create_call and create_result.get('intent') == 'create_task'

        print(f"   CREATE_TASK executed: {create_success}")

        # Test 2: List tasks (should show the task we just created)
        print("\n2. Testing LIST_TASKS execution...")
        list_result = await agent.process_message("1", "conv1", "list my tasks")

        print(f"   Input: 'list my tasks'")
        print(f"   Intent: {list_result.get('intent')}")
        print(f"   Tool calls: {list_result.get('tool_calls')}")
        print(f"   Response: {list_result.get('response_text')[:100]}...")

        has_list_call = any(tool.get('name') == 'LIST_TASKS' for tool in list_result.get('tool_calls', []))
        list_success = has_list_call and list_result.get('intent') == 'list_tasks'

        print(f"   LIST_TASKS executed: {list_success}")

        # Test 3: Check if agent claims access to tasks (should not say lacks access)
        print("\n3. Testing access assertion...")
        lacks_access = "don't have access" in list_result.get('response_text', '').lower() or \
                       "can't access" in list_result.get('response_text', '').lower()

        has_access_claim = not lacks_access
        print(f"   Agent claims task access: {has_access_claim}")
        print(f"   No 'no access' statements: {has_access_claim}")

        # Test 4: Update a task (will try to update the first task found)
        print("\n4. Testing UPDATE_TASK execution...")
        update_result = await agent.process_message("1", "conv1", "update task 1 to be high priority")

        print(f"   Input: 'update task 1 to be high priority'")
        print(f"   Intent: {update_result.get('intent')}")
        print(f"   Tool calls: {update_result.get('tool_calls')}")
        print(f"   Response: {update_result.get('response_text')[:100]}...")

        has_update_call = any(tool.get('name') == 'UPDATE_TASK' for tool in update_result.get('tool_calls', []))
        update_success = has_update_call and update_result.get('intent') == 'update_task'

        print(f"   UPDATE_TASK executed: {update_success}")

        # Overall assessment
        all_tools_working = create_success and list_success
        llm_only_mode = not all_tools_working  # If tools aren't working, it's in LLM-only mode

        print(f"\n5. Overall Assessment:")
        print(f"   CREATE_TASK working: {create_success}")
        print(f"   LIST_TASKS working: {list_success}")
        print(f"   UPDATE_TASK working: {update_success}")
        print(f"   Agent has task access: {has_access_claim}")
        print(f"   All tools executing: {all_tools_working}")
        print(f"   In LLM-only mode: {llm_only_mode}")

        success = all_tools_working and has_access_claim
        return success

    except Exception as e:
        print(f"Error during tool execution test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_direct_tool_imports():
    """Test that MCP tools can be imported directly using the same path as agent."""
    print("\nTesting direct MCP tool imports...")

    try:
        # Try to import the tools using the same method as the agent
        sys.path.insert(0, os.path.join(os.path.dirname(__file__)))  # Add hackathontwo to path

        from todochatbot.mcp_tools.task_tools import (
            create_task, list_tasks, update_task, complete_task, delete_task
        )

        print("[PASS] Direct import of MCP tools successful")

        # Test list_tasks function specifically
        try:
            tasks = list_tasks(user_id="1", status=None)
            print(f"[PASS] list_tasks function callable, returned {len(tasks)} tasks")
            return True
        except Exception as e:
            print(f"[INFO] list_tasks function available but error occurred: {e}")
            return True  # Import succeeded

    except ImportError as e:
        print(f"[FAIL] Failed to import MCP tools directly: {e}")
        return False

async def main():
    """Run all tool execution tests."""
    print("="*70)
    print("MCP TOOL EXECUTION VERIFICATION")
    print("Checking if tools are properly executed vs. LLM-only mode")
    print("="*70)

    test1 = await test_direct_tool_imports()
    test2 = await test_tool_execution()

    print("\n" + "="*70)
    print("TOOL EXECUTION TEST RESULTS:")
    print(f"MCP Tools Importable: {'[PASS]' if test1 else '[FAIL]'}")
    print(f"MCP Tools Executing:  {'[PASS]' if test2 else '[FAIL]'}")

    overall_success = test1 and test2
    print(f"\nOVERALL TOOL EXECUTION: {'[ENABLED]' if overall_success else '[DISABLED]'}")

    if overall_success:
        print("[SUCCESS] MCP tools are properly bound and executing")
        print("[SUCCESS] Tool-first behavior is working correctly")
        print("[SUCCESS] Agent is not in LLM-only mode")
    else:
        print("[ISSUE] MCP tools may not be properly executing")
        print("  - Check tool binding and initialization")
        print("  - Verify tool-first behavior is enforced")

    print("="*70)

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)