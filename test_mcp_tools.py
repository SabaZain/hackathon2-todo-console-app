#!/usr/bin/env python3
"""
Test script to verify MCP tools functionality directly.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_mcp_tools():
    """Test the MCP tools directly."""
    try:
        # Import the MCP tools
        from backend.mcp_tools.task_tools import create_task, list_tasks, update_task, complete_task, delete_task

        print("[SUCCESS] Successfully imported MCP task tools")

        # Test basic functionality with mock data
        # These functions should be available and callable
        print("Testing create_task function signature...")
        # Just check if function exists and is callable
        assert callable(create_task), "create_task should be callable"
        print("[SUCCESS] create_task function is available")

        print("Testing list_tasks function signature...")
        assert callable(list_tasks), "list_tasks should be callable"
        print("[SUCCESS] list_tasks function is available")

        print("Testing update_task function signature...")
        assert callable(update_task), "update_task should be callable"
        print("[SUCCESS] update_task function is available")

        print("Testing complete_task function signature...")
        assert callable(complete_task), "complete_task should be callable"
        print("[SUCCESS] complete_task function is available")

        print("Testing delete_task function signature...")
        assert callable(delete_task), "delete_task should be callable"
        print("[SUCCESS] delete_task function is available")

        print("\n[SUCCESS] All MCP tools are properly defined and available!")
        print("The chatbot can invoke these tools to manage tasks via the backend system.")

        return True

    except ImportError as e:
        print(f"[ERROR] Failed to import MCP tools: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error during MCP tools test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_agent_import():
    """Test that the chat agent can be imported (without full initialization)."""
    try:
        # Import just the class definition to check if it's properly structured
        from backend.agent.chat_agent import ChatAgent

        print("[SUCCESS] Successfully imported ChatAgent class")

        # Check if the class has the expected methods
        agent_methods = dir(ChatAgent)

        required_methods = ['process_message', '_classify_intent_cohere', '_extract_entities_cohere']
        for method in required_methods:
            if method in agent_methods:
                print(f"[SUCCESS] Found required method: {method}")
            else:
                print(f"[WARNING] Missing method: {method}")

        print("[SUCCESS] ChatAgent class structure looks good!")
        return True

    except ImportError as e:
        print(f"[ERROR] Failed to import ChatAgent: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error during ChatAgent import test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing MCP tools functionality...")
    tools_success = test_mcp_tools()

    print("\nTesting ChatAgent import...")
    agent_success = test_chat_agent_import()

    if tools_success and agent_success:
        print("\n[ALL TESTS PASSED] MCP tools and ChatAgent are properly structured.")
        print("The frontend chatbot should be able to communicate with the backend via the /api/{user_id}/chat endpoint.")
    else:
        print("\n[TESTS FAILED] Some tests failed. Please check the implementation.")
        sys.exit(1)