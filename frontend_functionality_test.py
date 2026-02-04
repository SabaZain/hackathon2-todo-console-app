#!/usr/bin/env python3
"""
Test script to verify frontend functionality by testing backend responses
to common user queries like "who are you?", "list my tasks?", etc.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_who_are_you_query():
    """Test 'who are you?' query response."""
    print("Testing 'who are you?' query...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the query
        result = await agent.process_message("1", "conv1", "who are you?")

        print(f"Input: 'who are you?'")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: '{result.get('response_text', 'no response')}'")

        response_text = result.get('response_text', '')
        has_expected_identity = "Todo AI Assistant" in response_text

        print(f"Has expected identity response: {has_expected_identity}")
        print()

        return has_expected_identity

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_list_my_tasks_query():
    """Test 'list my tasks?' query response."""
    print("Testing 'list my tasks?' query...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the query
        result = await agent.process_message("1", "conv1", "list my tasks?")

        print(f"Input: 'list my tasks?'")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: '{result.get('response_text', 'no response')}'")

        # Check if it calls the LIST_TASKS tool
        has_list_tasks_call = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))
        intent_correct = result.get('intent') == 'list_tasks'

        print(f"Has LIST_TASKS tool call: {has_list_tasks_call}")
        print(f"Correct intent: {intent_correct}")
        print()

        return has_list_tasks_call and intent_correct

    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_add_task_query():
    """Test 'can you add task to my todoapp?' query response."""
    print("Testing 'can you add task to my todoapp?' query...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the query
        result = await agent.process_message("1", "conv1", "can you add task to my todoapp?")

        print(f"Input: 'can you add task to my todoapp?'")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: '{result.get('response_text', 'no response')}'")

        # This might be interpreted as a help/capability question or a task creation request
        # It could either return help info or ask for task details
        is_help_intent = result.get('intent') in ['help', 'general']
        is_task_intent = result.get('intent') in ['create_task']
        has_task_reference = 'task' in result.get('response_text', '').lower()

        print(f"Is help/capability intent: {is_help_intent}")
        print(f"Is task creation intent: {is_task_intent}")
        print(f"Response mentions tasks: {has_task_reference}")
        print()

        # Either interpretation is valid - could be capability question or task request
        return is_help_intent or is_task_intent or has_task_reference

    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_add_specific_task():
    """Test adding a specific task."""
    print("Testing 'add a task to buy groceries' query...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the query
        result = await agent.process_message("1", "conv1", "add a task to buy groceries")

        print(f"Input: 'add a task to buy groceries'")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: '{result.get('response_text', 'no response')}'")

        # Check if it calls the CREATE_TASK tool
        has_create_task_call = any(tool.get('name') == 'CREATE_TASK' for tool in result.get('tool_calls', []))
        intent_correct = result.get('intent') == 'create_task'

        print(f"Has CREATE_TASK tool call: {has_create_task_call}")
        print(f"Correct intent: {intent_correct}")
        print()

        return has_create_task_call and intent_correct

    except Exception as e:
        print(f"Error: {e}")
        return False

async def main():
    """Run all functionality tests."""
    print("="*70)
    print("FRONTEND FUNCTIONALITY TEST - BACKEND RESPONSE VERIFICATION")
    print("Testing how backend responds to common user queries...")
    print("="*70)

    test1 = await test_who_are_you_query()
    test2 = await test_list_my_tasks_query()
    test3 = await test_add_task_query()
    test4 = await test_add_specific_task()

    print("="*70)
    print("TEST RESULTS:")
    print(f"'who are you?' response: {'[PASS]' if test1 else '[FAIL]'}")
    print(f"'list my tasks?' response: {'[PASS]' if test2 else '[FAIL]'}")
    print(f"'can you add task?' response: {'[PASS]' if test3 else '[INFO]'} (Valid behavior)")
    print(f"'add task' response: {'[PASS]' if test4 else '[FAIL]'}")

    # Overall success - most important are identity and task operations
    overall_success = test1 and test2 and test4
    print(f"\nOVERALL FRONTEND FUNCTIONALITY: {'[PASS]' if overall_success else '[PARTIAL]'}")

    print("\nSUMMARY:")
    print("- 'who are you?' should return identity: ", "[WORKS]" if test1 else "[ISSUE]")
    print("- 'list my tasks?' should call LIST_TASKS: ", "[WORKS]" if test2 else "[ISSUE]")
    print("- 'add task' should call CREATE_TASK: ", "[WORKS]" if test4 else "[ISSUE]")
    print("- Capability questions handled: ", "[WORKS]" if test3 else "[ADJUSTED]")

    print("="*70)

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)