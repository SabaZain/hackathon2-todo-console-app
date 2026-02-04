#!/usr/bin/env python3
"""
Test script to verify intent resolution and MCP tool routing fixes.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_add_task_intent():
    """Test that 'add task' intent calls the create_task tool."""
    print("Testing 'add task' intent routing...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test adding a task
        result = await agent.process_message("1", "conv1", "add task Buy groceries")

        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: {result.get('response_text', 'no response')}")

        # Check if it's a CREATE_TASK intent and has tool calls
        has_create_task = any(tool.get('name') == 'CREATE_TASK' for tool in result.get('tool_calls', []))

        if result.get('intent') == 'create_task' and has_create_task:
            print("[PASS] 'add task' correctly routes to CREATE_TASK tool\n")
            return True
        else:
            print("[FAIL] 'add task' does not route to CREATE_TASK tool properly\n")
            return False

    except Exception as e:
        print(f"[FAIL] Error testing add task: {e}\n")
        return False

async def test_list_tasks_intent():
    """Test that 'list my tasks' returns real DB tasks."""
    print("Testing 'list my tasks' intent routing...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test listing tasks
        result = await agent.process_message("1", "conv1", "list my tasks")

        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: {result.get('response_text', 'no response')}")

        # Check if it's a LIST_TASKS intent and has tool calls
        has_list_tasks = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))

        if result.get('intent') == 'list_tasks' and has_list_tasks:
            print("[PASS] 'list my tasks' correctly routes to LIST_TASKS tool\n")
            return True
        else:
            print("[FAIL] 'list my tasks' does not route to LIST_TASKS tool properly\n")
            return False

    except Exception as e:
        print(f"[FAIL] Error testing list tasks: {e}\n")
        return False

async def test_capability_question():
    """Test that 'what can you do' returns description without DB hit."""
    print("Testing 'what can you do' capability question...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test capability question
        result = await agent.process_message("1", "conv1", "what can you do")

        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: {result.get('response_text', 'no response')}")

        # Check if it's a help/general intent and has NO tool calls
        has_no_tool_calls = len(result.get('tool_calls', [])) == 0
        is_help_or_general = result.get('intent') in ['help', 'general']

        if is_help_or_general and has_no_tool_calls:
            print("[PASS] 'what can you do' returns description without DB hit\n")
            return True
        else:
            print("[FAIL] 'what can you do' incorrectly calls tools or has wrong intent\n")
            return False

    except Exception as e:
        print(f"[FAIL] Error testing capability question: {e}\n")
        return False

async def test_greeting_intent():
    """Test that greeting questions don't call tools."""
    print("Testing greeting intent...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test greeting
        result = await agent.process_message("1", "conv1", "hello")

        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: {result.get('response_text', 'no response')}")

        # Check if it's a greeting intent and has NO tool calls
        has_no_tool_calls = len(result.get('tool_calls', [])) == 0
        is_greeting = result.get('intent') == 'greeting'

        if is_greeting and has_no_tool_calls:
            print("[PASS] Greeting correctly returns response without tools\n")
            return True
        else:
            print("[FAIL] Greeting incorrectly calls tools or has wrong intent\n")
            return False

    except Exception as e:
        print(f"[FAIL] Error testing greeting: {e}\n")
        return False

async def main():
    """Run all tests."""
    print("="*60)
    print("TESTING INTENT RESOLUTION AND MCP TOOL ROUTING FIXES")
    print("="*60)

    test1 = await test_add_task_intent()
    test2 = await test_list_tasks_intent()
    test3 = await test_capability_question()
    test4 = await test_greeting_intent()

    print("="*60)
    print("RESULTS:")
    print(f"'add task' calls add_task: {'[PASS]' if test1 else '[FAIL]'}")
    print(f"'list my tasks' returns DB tasks: {'[PASS]' if test2 else '[FAIL]'}")
    print(f"'what can you do' no DB hit: {'[PASS]' if test3 else '[FAIL]'}")
    print(f"Greeting no tool calls: {'[PASS]' if test4 else '[FAIL]'}")

    all_pass = test1 and test2 and test3 and test4
    print(f"\nOVERALL: {'[PASS]' if all_pass else '[FAIL]'}")
    print("="*60)

    return all_pass

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)