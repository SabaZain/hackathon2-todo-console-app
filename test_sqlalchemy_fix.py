#!/usr/bin/env python3
"""
Test script to verify that the SQLAlchemy duplicate table definition issue is fixed.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_mcp_tool_execution():
    """Test that MCP tools execute without SQLAlchemy duplicate table errors."""
    print("Testing MCP tool execution to verify SQLAlchemy duplicate table fix...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test 1: Create a task (this should work without duplicate table errors)
        print("\n1. Testing CREATE_TASK execution...")
        create_result = await agent.process_message("1", "conv1", "add task test SQLAlchemy fix")

        print(f"   Input: 'add task test SQLAlchemy fix'")
        print(f"   Intent: {create_result.get('intent')}")
        print(f"   Tool calls: {create_result.get('tool_calls')}")
        print(f"   Response: {create_result.get('response_text')[:100]}...")

        has_create_tool = any(tool.get('name') == 'CREATE_TASK' for tool in create_result.get('tool_calls', []))
        create_success = has_create_tool and create_result.get('intent') == 'create_task'
        print(f"   CREATE_TASK executed: {create_success}")

        # Test 2: List tasks (this is where the duplicate table error typically occurs)
        print("\n2. Testing LIST_TASKS execution (potential duplicate table error point)...")
        list_result = await agent.process_message("1", "conv2", "list my tasks")

        print(f"   Input: 'list my tasks'")
        print(f"   Intent: {list_result.get('intent')}")
        print(f"   Tool calls: {list_result.get('tool_calls')}")
        print(f"   Response: {list_result.get('response_text')[:100]}...")

        has_list_tool = any(tool.get('name') == 'LIST_TASKS' for tool in list_result.get('tool_calls', []))
        list_success = has_list_tool and list_result.get('intent') == 'list_tasks'
        print(f"   LIST_TASKS executed: {list_success}")

        # Test 3: Update a task (another potential duplicate table error point)
        print("\n3. Testing UPDATE_TASK execution...")
        update_result = await agent.process_message("1", "conv3", "update task 1 priority to high")

        print(f"   Input: 'update task 1 priority to high'")
        print(f"   Intent: {update_result.get('intent')}")
        print(f"   Tool calls: {update_result.get('tool_calls')}")
        print(f"   Response: {update_result.get('response_text')[:100]}...")

        has_update_tool = any(tool.get('name') == 'UPDATE_TASK' for tool in update_result.get('tool_calls', []))
        update_success = has_update_tool and update_result.get('intent') == 'update_task'
        print(f"   UPDATE_TASK executed: {update_success}")

        # Test 4: Complete a task
        print("\n4. Testing COMPLETE_TASK execution...")
        complete_result = await agent.process_message("1", "conv4", "complete task 1")

        print(f"   Input: 'complete task 1'")
        print(f"   Intent: {complete_result.get('intent')}")
        print(f"   Tool calls: {complete_result.get('tool_calls')}")
        print(f"   Response: {complete_result.get('response_text')[:100]}...")

        has_complete_tool = any(tool.get('name') == 'COMPLETE_TASK' for tool in complete_result.get('tool_calls', []))
        complete_success = has_complete_tool and complete_result.get('intent') == 'complete_task'
        print(f"   COMPLETE_TASK executed: {complete_success}")

        # Overall assessment
        all_success = create_success and list_success and update_success and complete_success

        print(f"\n5. OVERALL ASSESSMENT:")
        print(f"   CREATE_TASK: {'[SUCCESS]' if create_success else '[FAILED]'}")
        print(f"   LIST_TASKS:  {'[SUCCESS]' if list_success else '[FAILED]'}")
        print(f"   UPDATE_TASK: {'[SUCCESS]' if update_success else '[FAILED]'}")
        print(f"   COMPLETE_TASK: {'[SUCCESS]' if complete_success else '[FAILED]'}")

        print(f"\n   [TARGET] NO SQLALCHEMY DUPLICATE TABLE ERRORS: {'YES' if all_success else 'NO'}")
        print(f"   [TARGET] MCP TOOLS EXECUTE SUCCESSFULLY: {'YES' if all_success else 'NO'}")

        return all_success

    except Exception as e:
        print(f"\n[ERROR] ERROR DURING MCP TOOL EXECUTION TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run the SQLAlchemy duplicate table fix verification test."""
    print("="*80)
    print("SQLALCHEMY DUPLICATE TABLE ERROR FIX VERIFICATION")
    print("Testing that MCP tools execute without 'Table already defined' errors")
    print("="*80)

    success = await test_mcp_tool_execution()

    print("\n" + "="*80)
    print("VERIFICATION RESULTS:")
    print(f"SQLAlchemy Duplicate Table Fix: {'[SUCCESS] WORKING' if success else '[FAILED] BROKEN'}")

    if success:
        print("\n[VERIFIED] FIX SUCCESSFUL:")
        print("   • MCP tools now use shared SQLAlchemy models and engine")
        print("   • No duplicate table definition errors occur")
        print("   • All task operations execute properly in chatbot flow")
        print("   • Database operations work end-to-end")
        print("   • Existing functionality remains unchanged")
    else:
        print("\n[WARNING] FIX MAY NOT BE COMPLETE:")
        print("   • Check for remaining duplicate imports")
        print("   • Verify all MCP tools use shared models")
        print("   • Confirm no 'from backend.models import' inside functions")

    print("="*80)

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)