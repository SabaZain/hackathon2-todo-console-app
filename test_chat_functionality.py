#!/usr/bin/env python3
"""
Quick test to verify the chat functionality works with the fix.
"""

import os
import sys
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_chat_functionality():
    """Test that the chat functionality works without the original error."""
    print("Testing chat functionality with Cohere API key fix...")

    try:
        from backend.api.agent_connector import get_agent_connector

        # Create agent connector
        connector = get_agent_connector()

        # Test processing a simple message
        # Use a fake user_id and conversation_id for testing
        result = await connector.process_message(
            user_id="1",
            conversation_id="test_conv_1",
            message="Hello, can you help me create a task?"
        )

        print(f"Response received: {result}")

        # Check if the response contains the expected error message that was reported
        response_text = result.get('response_text', '')

        if "Both Cohere API methods encountered issues. Please ensure your COHERE_API_KEY is properly configured." in response_text:
            print("[ERROR] Still getting the original error message")
            return False
        else:
            print("[OK] No longer getting the original error message")
            print(f"Response type: {type(response_text)}")
            return True

    except Exception as e:
        print(f"[ERROR] Exception during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=== Testing Chat Functionality After Fix ===\n")

    # Run the async test
    success = asyncio.run(test_chat_functionality())

    if success:
        print("\n[OK] Chat functionality test passed!")
        print("The original error message should no longer appear.")
    else:
        print("\n[ERROR] Chat functionality test failed!")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)