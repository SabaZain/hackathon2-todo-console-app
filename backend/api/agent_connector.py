"""
Agent Connector for Todo AI Chatbot API.

This module handles connection and communication with the AI agent.
"""

import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import os

# Get the Cohere API key from environment variables
cohere_api_key = os.getenv('COHERE_API_KEY')
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required. Please set it in your deployment environment.")
os.environ['COHERE_API_KEY'] = cohere_api_key

import sys

# Determine the correct path for imports depending on execution context
current_dir = os.path.dirname(os.path.abspath(__file__))  # This is backend/api/
parent_dir = os.path.dirname(current_dir)  # This is backend/
grandparent_dir = os.path.dirname(parent_dir)  # This is hackathontwo/

# Add the backend directory to path to ensure we import from backend/agent/
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Add the hackathontwo directory to path as well for comprehensive access
if grandparent_dir not in sys.path:
    sys.path.insert(0, grandparent_dir)

# Try importing the backend agent first (the merged version with proper task integration)
# Use absolute imports to avoid relative import issues
current_dir = os.path.dirname(os.path.abspath(__file__))  # This is backend/api/
parent_dir = os.path.dirname(current_dir)  # This is backend/

# Add debugging to see which imports are working
print("Attempting to import backend.agent modules...")

# Add the hackathontwo directory to the path as well for comprehensive access
grandparent_dir = os.path.dirname(parent_dir)  # This is hackathontwo/

# Add the backend directory to path to ensure we import from backend/agent/
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if grandparent_dir not in sys.path:
    sys.path.insert(0, grandparent_dir)

# Prioritize backend modules
try:
    from backend.agent.chat_agent import ChatAgent, create_chat_agent
    from backend.agent.conversation_context import create_conversation_context
    from backend.agent.history_manager import get_history_manager
    print("Using backend.agent module import")
except ImportError as e:
    print(f"Could not import backend.agent: {e}")
    # Fallback to different import style if needed
    try:
        from agent.chat_agent import ChatAgent, create_chat_agent
        from agent.conversation_context import create_conversation_context
        from agent.history_manager import get_history_manager
        print("Using backend agent implementation")
    except ImportError as e2:
        print(f"Could not import agent: {e2}")
        # Last resort: try todochatbot import
        try:
            from todochatbot.agent.chat_agent import ChatAgent, create_chat_agent
            from todochatbot.agent.conversation_context import create_conversation_context
            from todochatbot.agent.history_manager import get_history_manager
            print("Using todochatbot fallback agent")
        except ImportError as e3:
            print(f"All import attempts failed: {e}, {e2}, {e3}")
            raise


class AgentConnector:
    """Connects the API to the AI agent for message processing."""

    def __init__(self):
        """Initialize the agent connector with required services."""
        self.chat_agent = None
        self.history_manager = get_history_manager()

    async def initialize_agent(self):
        """Initialize the chat agent asynchronously."""
        if self.chat_agent is None:
            try:
                self.chat_agent = await create_chat_agent()
            except ValueError as e:
                # Handle configuration errors like missing API keys
                print(f"Configuration error during agent initialization: {str(e)}")
                raise e
            except Exception as e:
                # Handle other initialization errors
                print(f"Error initializing chat agent: {str(e)}")
                raise e

    async def process_message(self, user_id: str, conversation_id: str, message: str, session=None) -> Dict[str, Any]:
        """
        Process a user message through the AI agent.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The message to process
            session: Optional database session to pass to the agent for tool operations

        Returns:
            Dictionary containing the agent's response
        """
        # Ensure agent is initialized
        if self.chat_agent is None:
            try:
                await self.initialize_agent()
            except ValueError as e:
                # Handle configuration errors like missing API keys with meaningful response
                is_urdu = self._is_urdu_text(message) if 'message' in locals() else False
                error_result = {
                    "response_text": "Maaf kijeye, main aapki request ko samajh nahi pa raha. Kripya sahi tarah se poochhen." if is_urdu else "I encountered a configuration issue. Please try again.",
                    "tool_calls": [],
                    "conversation_id": conversation_id,
                    "intent": "error",
                    "success": False,
                    "error": str(e)
                }

                # Save error response to history (only if conversation exists)
                try:
                    if "response_text" in error_result:
                        self.history_manager.save_ai_response(user_id, conversation_id, error_result["response_text"])
                except Exception as save_error:
                    print(f"Could not save error response to history: {save_error}")

                return error_result

        try:
            # CRITICAL FIX: Ensure conversation exists BEFORE saving any messages
            # This prevents foreign key constraint violations
            try:
                # Check if conversation exists, if not it will be created
                from database.conversations import db_manager
                db_manager.ensure_conversation_exists(conversation_id, user_id)
            except Exception as conv_error:
                print(f"Error ensuring conversation exists: {conv_error}")
                # Create conversation with the specific ID if it doesn't exist
                from database.conversations import create_new_conversation
                # If the conversation doesn't exist and ensure_conversation_exists fails,
                # we might need to create it differently
                pass

            # Save user message to history - wrapped in try/except to avoid FK errors
            try:
                self.history_manager.save_user_message(user_id, conversation_id, message)
            except Exception as user_msg_error:
                print(f"Error saving user message: {user_msg_error}")
                # Continue processing even if user message fails to save

            # Process the message with the agent, passing the session if available
            result = await self.chat_agent.process_message(user_id, conversation_id, message, session=session)

            # Save AI response to history - only if user message was saved successfully
            # and we have a response to save
            if "response_text" in result:
                try:
                    self.history_manager.save_ai_response(user_id, conversation_id, result["response_text"])
                except Exception as ai_msg_error:
                    print(f"Error saving AI response: {ai_msg_error}")
                    # Still return the result even if saving fails

            # Return the agent's response to ensure it's passed back to the frontend
            return result

        except Exception as e:
            # Handle any errors in agent processing with proper response format
            # Detect if the input was in Urdu and provide appropriate error message
            is_urdu = self._is_urdu_text(message) if 'message' in locals() else False

            # Provide meaningful response instead of generic fallback
            if is_urdu:
                response_text = "Maaf kijeye, main aapki request ko samajh nahi pa raha. Kripya sahi tarah se poochhen."
            else:
                response_text = "I encountered an issue processing your request. Please try again with a different phrasing."

            error_result = {
                "response_text": response_text,
                "tool_calls": [],
                "conversation_id": conversation_id,
                "intent": "error",
                "success": False,
                "error": str(e)
            }

            # Save error response to history - only if safe to do so
            try:
                if "response_text" in error_result:
                    self.history_manager.save_ai_response(user_id, conversation_id, error_result["response_text"])
            except Exception as save_error:
                print(f"Could not save error response to history: {save_error}")

            # Return the error result to ensure response goes back to frontend
            return error_result

    def _is_urdu_text(self, text: str) -> bool:
        """
        Detect if the input text contains Urdu characters.

        Args:
            text: Input text to check

        Returns:
            Boolean indicating if Urdu text is detected
        """
        # Urdu Unicode range: U+0600-U+06FF (Arabic/Persian characters used in Urdu)
        urdu_chars = [char for char in text if '\u0600' <= char <= '\u06FF']
        # If more than 20% of the characters are Urdu, consider it Urdu text
        if len(text.strip()) == 0:
            return False
        return len(urdu_chars) / len(text.replace(' ', '')) > 0.2

    async def create_conversation_context(self, user_id: str, conversation_id: str) -> Any:
        """
        Create a conversation context for the agent.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            Conversation context object
        """
        # Get recent conversation history for context
        recent_messages = self.history_manager.get_messages_for_context(user_id, conversation_id, limit=5)

        # Create and return conversation context
        return create_conversation_context(conversation_id, user_id)

    async def get_conversation_state(self, user_id: str, conversation_id: str) -> Dict[str, Any]:
        """
        Get the current state of a conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            Dictionary containing conversation state
        """
        # Get conversation history
        history = self.history_manager.get_conversation_history(user_id, conversation_id)

        # Get recent messages for context
        recent_messages = self.history_manager.get_messages_for_context(user_id, conversation_id, limit=3)

        return {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message_count": len(history),
            "recent_messages": recent_messages,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def reset_conversation_context(self, conversation_id: str):
        """
        Reset the context for a specific conversation.

        Args:
            conversation_id: The ID of the conversation to reset
        """
        # In a real implementation, this would clear any stored context
        # For now, this is a placeholder
        pass

    async def batch_process_messages(self, user_id: str, conversation_id: str, messages: list) -> list:
        """
        Process multiple messages in sequence.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            messages: List of messages to process

        Returns:
            List of responses corresponding to each message
        """
        responses = []
        for message in messages:
            response = await self.process_message(user_id, conversation_id, message)
            responses.append(response)

        return responses


def get_agent_connector() -> AgentConnector:
    """
    Get an instance of the agent connector.

    Returns:
        AgentConnector instance
    """
    return AgentConnector()


async def create_agent_connector() -> AgentConnector:
    """
    Create and initialize an agent connector.

    Returns:
        Initialized AgentConnector instance
    """
    connector = AgentConnector()
    await connector.initialize_agent()
    return connector