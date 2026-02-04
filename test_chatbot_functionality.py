#!/usr/bin/env python3
"""
Test script to verify chatbot functionality with proper conversation handling.
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_chatbot_functionality():
    """Test the chatbot functionality with proper conversation handling."""
    try:
        # Import the chat endpoint to access the conversation creation function
        from backend.api.chat_endpoint import db_create_conversation

        print("[SUCCESS] Successfully imported conversation creation function")

        # Create a proper conversation
        user_id = "1"
        conversation_id = db_create_conversation(user_id)

        print(f"[SUCCESS] Created conversation: {conversation_id}")

        # Import the agent connector
        from backend.api.agent_connector import get_agent_connector

        print("[SUCCESS] Successfully imported agent connector")

        # Create and initialize the agent connector
        connector = get_agent_connector()
        await connector.initialize_agent()

        print("[SUCCESS] Successfully initialized chat agent")

        # Test processing a simple message
        # This simulates what happens when a user sends a message through the chatbot
        message = "add task test chatbot functionality"

        print(f"Testing message: '{message}'")

        result = await connector.process_message(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            session=None  # We'll test without a session first
        )

        print(f"[SUCCESS] Successfully processed message")
        print(f"Response: {result.get('response_text', 'No response text')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Intent: {result.get('intent', 'unknown')}")

        # Test list tasks
        message = "list my tasks"
        print(f"\nTesting message: '{message}'")

        result = await connector.process_message(
            user_id=user_id,
            conversation_id=conversation_id,
            message=message,
            session=None
        )

        print(f"[SUCCESS] Successfully processed message")
        print(f"Response: {result.get('response_text', 'No response text')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Intent: {result.get('intent', 'unknown')}")

        print("\n[SUCCESS] Chatbot functionality test completed successfully!")
        return True

    except ImportError as e:
        print(f"[ERROR] Failed to import required modules: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error during chatbot functionality test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing chatbot functionality with proper conversation handling...")
    success = asyncio.run(test_chatbot_functionality())

    if success:
        print("\n[ALL TESTS PASSED] Chatbot functionality is working correctly.")
    else:
        print("\n[TESTS FAILED] Some tests failed. Please check the implementation.")
        sys.exit(1)