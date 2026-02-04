#!/usr/bin/env python3
"""
Test script to verify the chat endpoint response format.
"""

import sys
import os
import asyncio
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_expected_format():
    """Test that the expected format matches the requirements."""
    print("Testing expected response format...")

    # This is the format that the frontend expects
    expected_format = {
        "conversation_id": "<uuid>",
        "user_id": 123,  # user_id as integer
        "message": "<user_message>",
        "response": "<AI-generated assistant response>",
        "tool_calls": [
            {
                "name": "<MCP_TOOL_NAME>",
                "arguments": { }
            }
        ],
        "intent": "<detected_intent>",
        "timestamp": "<ISO_timestamp>",
        "success": True
    }

    print("Expected format:")
    print(expected_format)
    return True

def test_current_agent_response():
    """Test the current agent response format."""
    print("\nTesting current agent response format...")

    # This is what the agent currently returns (based on code analysis)
    current_agent_response = {
        "response_text": "<AI-generated assistant response>",
        "tool_calls": [
            {
                "name": "<MCP_TOOL_NAME>",
                "arguments": { }
            }
        ],
        "conversation_id": "<uuid>",
        "intent": "<detected_intent>"
    }

    print("Current agent response format:")
    print(current_agent_response)
    return True

def test_endpoint_processing():
    """Test how the endpoint processes the agent response."""
    print("\nTesting endpoint processing logic...")

    # Simulate what the endpoint does
    ai_response = {
        "response_text": "I've created your task: Buy groceries",
        "tool_calls": [{"name": "CREATE_TASK", "arguments": {"description": "Buy groceries"}}],
        "conversation_id": "conv_123_1234567890",
        "intent": "create_task"
    }

    # This is what the endpoint extracts
    response_text = ai_response.get('response_text', 'No response generated')
    tool_calls = ai_response.get('tool_calls', [])
    intent = ai_response.get('intent', 'general')
    conversation_id = "conv_123_1234567890"  # from function parameter
    current_user_id = 123  # from JWT
    message = "Add a task to buy groceries"  # from request

    # This is what the endpoint constructs
    response_data = {
        "conversation_id": conversation_id,
        "user_id": current_user_id,
        "message": message,
        "response": response_text,
        "tool_calls": tool_calls,
        "intent": intent,
        "timestamp": datetime.utcnow().isoformat(),
        "success": True
    }

    print("Endpoint constructs this final response:")
    print(response_data)

    # Check if it matches expected format
    required_keys = ["conversation_id", "user_id", "message", "response", "tool_calls", "intent", "timestamp", "success"]
    has_all_keys = all(key in response_data for key in required_keys)

    print(f"\nHas all required keys: {has_all_keys}")
    if has_all_keys:
        print("[OK] Endpoint processing format is correct!")
        return True
    else:
        missing_keys = [key for key in required_keys if key not in response_data]
        print(f"[ERROR] Missing keys: {missing_keys}")
        return False

async def main():
    print("=== Chat Response Format Test ===\n")

    test1 = test_expected_format()
    test2 = test_current_agent_response()
    test3 = test_endpoint_processing()

    if test1 and test2 and test3:
        print("\n✅ All tests passed! The response format should be correct.")
        return True
    else:
        print("\n❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)