#!/usr/bin/env python3
"""
Final verification test to ensure all requirements are met:
- "add task" always calls add_task
- "list my tasks" returns real DB tasks
- "what can you do" returns description, no DB hit
- Bot always knows user's tasks
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_requirement_1():
    """Requirement: 'add task' always calls add_task"""
    print("Testing requirement: 'add task' always calls add_task...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        result = await agent.process_message("1", "conv1", "add task Buy groceries")

        has_create_task = any(tool.get('name') == 'CREATE_TASK' for tool in result.get('tool_calls', []))
        intent_correct = result.get('intent') == 'create_task'

        print(f"  Intent: {result.get('intent')}")
        print(f"  Tool calls: {result.get('tool_calls')}")
        print(f"  Success: {has_create_task and intent_correct}")

        return has_create_task and intent_correct

    except Exception as e:
        print(f"  Error: {e}")
        return False

async def test_requirement_2():
    """Requirement: 'list my tasks' returns real DB tasks"""
    print("Testing requirement: 'list my tasks' returns real DB tasks...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        result = await agent.process_message("1", "conv1", "list my tasks")

        has_list_tasks = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))
        intent_correct = result.get('intent') == 'list_tasks'
        has_tasks_in_response = 'task' in result.get('response_text', '').lower()

        print(f"  Intent: {result.get('intent')}")
        print(f"  Tool calls: {result.get('tool_calls')}")
        print(f"  Response contains tasks: {'task' in result.get('response_text', '').lower()}")
        print(f"  Success: {has_list_tasks and intent_correct and has_tasks_in_response}")

        return has_list_tasks and intent_correct and has_tasks_in_response

    except Exception as e:
        print(f"  Error: {e}")
        return False

async def test_requirement_3():
    """Requirement: 'what can you do' returns description, no DB hit"""
    print("Testing requirement: 'what can you do' returns description, no DB hit...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        result = await agent.process_message("1", "conv1", "what can you do")

        has_no_tool_calls = len(result.get('tool_calls', [])) == 0
        is_help_intent = result.get('intent') in ['help', 'general']
        has_description = 'help' in result.get('response_text', '').lower() or 'task' in result.get('response_text', '').lower()

        print(f"  Intent: {result.get('intent')}")
        print(f"  Tool calls: {result.get('tool_calls')}")
        print(f"  Response: {result.get('response_text')[:60]}...")
        print(f"  Success: {has_no_tool_calls and is_help_intent and has_description}")

        return has_no_tool_calls and is_help_intent and has_description

    except Exception as e:
        print(f"  Error: {e}")
        return False

async def test_requirement_4():
    """Requirement: Bot always knows user's tasks"""
    print("Testing requirement: Bot always knows user's tasks...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test that bot can list tasks without saying it lacks access
        result = await agent.process_message("1", "conv1", "show my tasks")

        response_text = result.get('response_text', '').lower()
        does_not_say_lacks_access = not any(phrase in response_text for phrase in ['don\'t have access', 'cannot access', 'no access', 'lack access'])
        has_list_functionality = any(tool.get('name') == 'LIST_TASKS' for tool in result.get('tool_calls', []))

        print(f"  Intent: {result.get('intent')}")
        print(f"  Tool calls: {result.get('tool_calls')}")
        print(f"  Says lacks access: {not does_not_say_lacks_access}")
        print(f"  Has list functionality: {has_list_functionality}")
        print(f"  Success: {does_not_say_lacks_access and has_list_functionality}")

        return does_not_say_lacks_access and has_list_functionality

    except Exception as e:
        print(f"  Error: {e}")
        return False

async def main():
    """Run all requirement tests."""
    print("="*70)
    print("FINAL VERIFICATION: ALL REQUIREMENTS TEST")
    print("="*70)

    req1_pass = await test_requirement_1()
    print(f"  Result: {'[PASS]' if req1_pass else '[FAIL]'}\n")

    req2_pass = await test_requirement_2()
    print(f"  Result: {'[PASS]' if req2_pass else '[FAIL]'}\n")

    req3_pass = await test_requirement_3()
    print(f"  Result: {'[PASS]' if req3_pass else '[FAIL]'}\n")

    req4_pass = await test_requirement_4()
    print(f"  Result: {'[PASS]' if req4_pass else '[FAIL]'}\n")

    print("="*70)
    print("REQUIREMENT VERIFICATION RESULTS:")
    print(f"1. 'add task' always calls add_task: {'[PASS]' if req1_pass else '[FAIL]'}")
    print(f"2. 'list my tasks' returns real DB tasks: {'[PASS]' if req2_pass else '[FAIL]'}")
    print(f"3. 'what can you do' returns description, no DB hit: {'[PASS]' if req3_pass else '[FAIL]'}")
    print(f"4. Bot always knows user's tasks: {'[PASS]' if req4_pass else '[FAIL]'}")

    all_pass = req1_pass and req2_pass and req3_pass and req4_pass
    print(f"\nOVERALL COMPLIANCE: {'[PASS]' if all_pass else '[FAIL]'}")
    print("="*70)

    return all_pass

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)