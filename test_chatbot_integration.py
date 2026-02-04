"""
Test script to verify the AI Chatbot integration with the existing task system.
"""
import asyncio
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agent.chat_agent import create_chat_agent
from backend.api.agent_connector import get_agent_connector


async def test_chatbot_integration():
    """Test the chatbot integration with the task system."""
    print("Testing AI Chatbot Integration...")

    # Test creating an agent connector
    print("\n1. Testing agent connector initialization...")
    try:
        connector = get_agent_connector()
        print("✓ Agent connector created successfully")

        # Initialize the agent
        await connector.initialize_agent()
        print("✓ Agent initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing agent: {e}")
        return

    # Test various chat interactions
    print("\n2. Testing chat interactions...")
    test_cases = [
        "Add a task to buy groceries",
        "Show my tasks",
        "Complete task 1",
        "Delete task 1"
    ]

    user_id = "1"  # Test user ID
    conversation_id = "test_conv_1"

    for i, message in enumerate(test_cases):
        print(f"\n  Test {i+1}: {message}")
        try:
            response = await connector.process_message(
                user_id=user_id,
                conversation_id=conversation_id,
                message=message
            )
            print(f"  Response: {response.get('response_text', 'No response')}")
            print(f"  Tool calls: {response.get('tool_calls', [])}")
        except Exception as e:
            print(f"  ✗ Error processing message '{message}': {e}")

    print("\n✓ Chatbot integration test completed!")


if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.getenv("COHERE_API_KEY"):
        print("Warning: COHERE_API_KEY not set. Some functionality may be limited.")
        print("Please set COHERE_API_KEY environment variable for full AI capabilities.")

    if not os.getenv("DATABASE_URL"):
        print("Error: DATABASE_URL not set. Database integration will not work.")
        print("Please set DATABASE_URL environment variable.")
        sys.exit(1)

    # Run the test
    asyncio.run(test_chatbot_integration())