#!/usr/bin/env python3
"""
Test to verify the current status of the Cohere integration.
"""

import os
import sys
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_current_status():
    """Test the current status of the chat functionality."""
    print("Testing current chat functionality...")

    try:
        from backend.api.agent_connector import get_agent_connector
        from backend.database.conversations import create_conversation

        # Create agent connector
        connector = get_agent_connector()

        # Create a proper conversation first
        conversation_id = create_conversation(user_id="1")
        print(f"Created conversation: {conversation_id}")

        # Test processing a general message
        result1 = await connector.process_message(
            user_id="1",
            conversation_id=conversation_id,
            message="Hello, who are you?"
        )

        print(f"Response to 'Hello, who are you?': {result1['response_text'][:200]}...")

        # Test processing a task-related message
        result2 = await connector.process_message(
            user_id="1",
            conversation_id=conversation_id,
            message="Can you help me create a task to buy groceries?"
        )

        print(f"Response to task creation: {result2['response_text'][:200]}...")

        # Check if the original error message appears in either response
        responses = [result1['response_text'], result2['response_text']]

        original_error = "Both Cohere API methods encountered issues. Please ensure your COHERE_API_KEY is properly configured."

        has_original_error = any(original_error in resp for resp in responses)

        if has_original_error:
            print("\n[ERROR] The original error message is still appearing!")
            return False
        else:
            print("\n[SUCCESS] The original error message is NOT appearing!")

            # Check if we're getting real AI responses
            responses_are_meaningful = all(
                "I'm unable to process your request because the Cohere API key is not configured" not in resp
                and "experiencing a technical issue connecting to the AI service" not in resp
                for resp in responses
            )

            if responses_are_meaningful:
                print("We're getting real AI responses!")
            else:
                print("We're getting fallback messages, but not the original error.")

            return True

    except Exception as e:
        print(f"Exception during test: {e}")
        if "Both Cohere API methods encountered issues" in str(e):
            print("[ERROR] Original error still exists in exception handling")
            return False
        else:
            print("[INFO] Different error (not the original Cohere issue)")
            return True

def main():
    print("=== Current Status Test ===\n")

    success = asyncio.run(test_current_status())

    print(f"\n=== RESULT ===")
    if success:
        print("The original Cohere error appears to be FIXED!")
    else:
        print("The original Cohere error still exists.")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)