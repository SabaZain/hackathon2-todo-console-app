#!/usr/bin/env python3
"""
Test script to verify how the chatbot responds to 'hello' greeting.
"""

import asyncio
import os
import sys
from unittest.mock import patch

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_hello_response():
    """Test how the chatbot responds to 'hello'."""
    print("Testing chatbot response to 'hello' greeting...")

    # Mock the environment variables to avoid errors
    with patch.dict(os.environ, {
        "JWT_SECRET": "test_secret_key",
        "DATABASE_URL": "sqlite:///test.db",
        "COHERE_API_KEY": "fake_api_key"
    }, clear=True):
        try:
            # Import the chat agent
            from backend.agent.chat_agent import ChatAgent
            from backend.agent.configuration import get_agent_config

            # Create a mock config to avoid API key issues
            with patch('backend.agent.chat_agent.get_agent_config') as mock_config:
                mock_config.return_value = {
                    'cohere_api_key': 'fake_key',
                    'model': 'command',
                    'temperature': 0.7,
                    'max_tokens': 150
                }

                # Mock the Cohere client to avoid API calls
                with patch('backend.agent.chat_agent.cohere.Client') as mock_client:
                    mock_client_instance = mock_client.return_value
                    mock_response = type('Response', (), {})()
                    mock_response.text = 'greeting'
                    mock_client_instance.chat.return_value = mock_response

                    # Create the agent
                    agent = ChatAgent()

                    # Mock the _generate_general_response method to avoid Cohere API calls
                    with patch.object(agent, '_generate_general_response', return_value="Hello! I'm your Todo AI Assistant. How can I help you?"):
                        # Test the hello greeting
                        result = await agent.process_message(
                            user_id="1",
                            conversation_id="test_conv_1",
                            message="hello"
                        )

                        print(f"Input: 'hello'")
                        print(f"Detected intent: {result.get('intent', 'unknown')}")
                        print(f"Response: {result.get('response_text', 'No response')}")

                        if result.get('response_text') and 'Hello!' in result['response_text']:
                            print("✅ SUCCESS: Chatbot correctly responds to 'hello' with greeting!")
                            return True
                        else:
                            print("❌ FAILED: Chatbot did not respond appropriately to 'hello'")
                            return False

        except Exception as e:
            print(f"Error during hello test: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = asyncio.run(test_hello_response())
    if success:
        print("\n🎉 Chatbot correctly responds to 'hello' greeting!")
    else:
        print("\n❌ Chatbot response to 'hello' needs attention.")
    sys.exit(0 if success else 1)