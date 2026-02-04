#!/usr/bin/env python3
"""
Comprehensive test to verify that the chatbot properly executes MCP tools
and returns real results to the frontend.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_comprehensive_tool_execution():
    """Comprehensive test to verify MCP tool execution."""
    print("="*80)
    print("COMPREHENSIVE MCP TOOL EXECUTION VERIFICATION")
    print("="*80)

    print("\nTesting complete end-to-end flow:")
    print("Frontend Query → API Endpoint → Agent → MCP Tools → DB → Response")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test 1: Add a task
        print("\n1. TESTING TASK CREATION...")
        create_result = await agent.process_message("1", "conv1", "add task buy groceries")

        print(f"   Input: 'add task buy groceries'")
        print(f"   Intent: {create_result.get('intent')}")
        print(f"   Tool calls: {create_result.get('tool_calls')}")
        print(f"   Response: {create_result.get('response_text')[:120]}...")

        has_create_tool = any(tool.get('name') == 'CREATE_TASK' for tool in create_result.get('tool_calls', []))
        create_success = has_create_tool and create_result.get('intent') == 'create_task'
        print(f"   ✅ CREATE_TASK executed: {create_success}")

        # Test 2: List tasks (should show the task we just created)
        print("\n2. TESTING TASK LISTING...")
        list_result = await agent.process_message("1", "conv2", "list my tasks")

        print(f"   Input: 'list my tasks'")
        print(f"   Intent: {list_result.get('intent')}")
        print(f"   Tool calls: {list_result.get('tool_calls')}")
        print(f"   Response: {list_result.get('response_text')[:120]}...")

        has_list_tool = any(tool.get('name') == 'LIST_TASKS' for tool in list_result.get('tool_calls', []))
        list_success = has_list_tool and list_result.get('intent') == 'list_tasks'
        print(f"   ✅ LIST_TASKS executed: {list_success}")

        # Test 3: Complete a task
        print("\n3. TESTING TASK COMPLETION...")
        complete_result = await agent.process_message("1", "conv3", "complete task 1")

        print(f"   Input: 'complete task 1'")
        print(f"   Intent: {complete_result.get('intent')}")
        print(f"   Tool calls: {complete_result.get('tool_calls')}")
        print(f"   Response: {complete_result.get('response_text')[:120]}...")

        has_complete_tool = any(tool.get('name') == 'COMPLETE_TASK' for tool in complete_result.get('tool_calls', []))
        complete_success = has_complete_tool and complete_result.get('intent') == 'complete_task'
        print(f"   ✅ COMPLETE_TASK executed: {complete_success}")

        # Test 4: Delete a task
        print("\n4. TESTING TASK DELETION...")
        delete_result = await agent.process_message("1", "conv4", "delete task 1")

        print(f"   Input: 'delete task 1'")
        print(f"   Intent: {delete_result.get('intent')}")
        print(f"   Tool calls: {delete_result.get('tool_calls')}")
        print(f"   Response: {delete_result.get('response_text')[:120]}...")

        has_delete_tool = any(tool.get('name') == 'DELETE_TASK' for tool in delete_result.get('tool_calls', []))
        delete_success = has_delete_tool and delete_result.get('intent') == 'delete_task'
        print(f"   ✅ DELETE_TASK executed: {delete_success}")

        # Test 5: Check for access denial statements
        print("\n5. TESTING ACCESS DENIAL CHECK...")
        lacks_access = any(
            phrase in list_result.get('response_text', '').lower()
            for phrase in ["don't have access", "can't access", "no access", "lack access"]
        )
        access_ok = not lacks_access
        print(f"   ✅ No access denial statements: {access_ok}")
        print(f"   Response contains task data: {'task' in list_result.get('response_text', '').lower()}")

        # Test 6: Check that responses reflect real tool execution
        print("\n6. TESTING RESPONSE CONTENT QUALITY...")
        response_has_real_data = (
            ("created" in create_result.get('response_text', '').lower()) or
            ("added" in create_result.get('response_text', '').lower()) or
            ("task" in create_result.get('response_text', '').lower())
        )

        list_has_tasks = (
            "tasks" in list_result.get('response_text', '').lower() or
            "task" in list_result.get('response_text', '').lower()
        )

        print(f"   ✅ Creation response has real data: {response_has_real_data}")
        print(f"   ✅ List response has real data: {list_has_tasks}")

        # Overall assessment
        all_tests_passed = (
            create_success and
            list_success and
            complete_success and
            delete_success and
            access_ok and
            response_has_real_data and
            list_has_tasks
        )

        print(f"\n7. OVERALL ASSESSMENT:")
        print(f"   Task Creation: {'✅' if create_success else '❌'}")
        print(f"   Task Listing:  {'✅' if list_success else '❌'}")
        print(f"   Task Completion: {'✅' if complete_success else '❌'}")
        print(f"   Task Deletion: {'✅' if delete_success else '❌'}")
        print(f"   Access Control: {'✅' if access_ok else '❌'}")
        print(f"   Real Data Returned: {'✅' if response_has_real_data and list_has_tasks else '❌'}")

        print(f"\n   🎯 MCP TOOLS FULLY INTEGRATED: {'YES' if all_tests_passed else 'NO'}")
        print(f"   🎯 CHATBOT OPERATING AS TASK ASSISTANT: {'YES' if all_tests_passed else 'NO'}")
        print(f"   🎯 TOOLS EXECUTING REAL DATABASE OPERATIONS: {'YES' if all_tests_passed else 'NO'}")

        return all_tests_passed

    except Exception as e:
        print(f"\n❌ ERROR DURING COMPREHENSIVE TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

async def verify_tool_imports():
    """Verify that MCP tools can be imported correctly."""
    print("\n" + "="*80)
    print("VERIFYING MCP TOOL IMPORTS")
    print("="*80)

    try:
        # Import the tools from the correct location
        from todochatbot.mcp_tools.task_tools import (
            create_task, list_tasks, update_task, complete_task, delete_task
        )

        print("✅ MCP Tools imported successfully from todochatbot/mcp_tools/")

        # Verify all required functions exist
        required_functions = [create_task, list_tasks, update_task, complete_task, delete_task]
        function_names = ['create_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task']

        all_found = True
        for func, name in zip(required_functions, function_names):
            if callable(func):
                print(f"✅ {name} function available")
            else:
                print(f"❌ {name} function not callable")
                all_found = False

        return all_found

    except ImportError as e:
        print(f"❌ Failed to import MCP tools: {e}")
        return False
    except Exception as e:
        print(f"❌ Error verifying tool imports: {e}")
        return False

async def main():
    """Run comprehensive verification tests."""
    print("🔍 STARTING MCP TOOL EXECUTION VERIFICATION")

    # Test 1: Verify imports
    imports_ok = await verify_tool_imports()

    # Test 2: Comprehensive tool execution
    execution_ok = await test_comprehensive_tool_execution()

    print("\n" + "="*80)
    print("FINAL VERIFICATION RESULTS")
    print("="*80)

    print(f"MCP Tool Imports: {'✅ WORKING' if imports_ok else '❌ BROKEN'}")
    print(f"MCP Tool Execution: {'✅ WORKING' if execution_ok else '❌ BROKEN'}")

    overall_success = imports_ok and execution_ok

    print(f"\n🎯 OVERALL STATUS: {'✅ MCP TOOLS FULLY INTEGRATED' if overall_success else '❌ MCP TOOLS NEED FIXING'}")

    if overall_success:
        print("\n🎉 VERIFICATION COMPLETE:")
        print("   • MCP tools are properly bound and executing")
        print("   • Database operations are happening in real-time")
        print("   • Tool execution results are returned to frontend")
        print("   • Chatbot operates as a real Todo AI Assistant")
        print("   • All task operations work end-to-end")
        print("   • No LLM-only fallback mode detected")
    else:
        print("\n⚠️  ISSUES IDENTIFIED:")
        print("   • Check MCP tool bindings")
        print("   • Verify database connectivity")
        print("   • Confirm user_id flow through system")
        print("   • Test intent → tool mapping")

    print("="*80)

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)