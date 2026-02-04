"""
Agent Connector for Todo AI Chatbot API.

This module handles connection and communication with the AI agent.
"""

import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

import sys
import os

# Determine the correct path for imports depending on execution context
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This is the todochatbot directory
grandparent_dir = os.path.dirname(parent_dir)  # This is the hackathontwo directory

# Add both parent and grandparent to path to handle different execution contexts
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if grandparent_dir not in sys.path:
    sys.path.insert(0, grandparent_dir)

# Try importing with the adjusted path
try:
    from agent.chat_agent import ChatAgent, create_chat_agent
    from agent.conversation_context import create_conversation_context
    from agent.history_manager import get_history_manager
except ImportError:
    # Fallback to different import style if needed
    from todochatbot.agent.chat_agent import ChatAgent, create_chat_agent
    from todochatbot.agent.conversation_context import create_conversation_context
    from todochatbot.agent.history_manager import get_history_manager


class AgentConnector:
    """Connects the API to the AI agent for message processing."""

    def __init__(self):
        """Initialize the agent connector with required services."""
        self.chat_agent = None
        self.history_manager = get_history_manager()

    async def initialize_agent(self):
        """Initialize the chat agent asynchronously."""
        if self.chat_agent is None:
            self.chat_agent = await create_chat_agent()

    async def process_message(self, user_id: str, conversation_id: str, message: str) -> Dict[str, Any]:
        """
        Process a user message through the AI agent.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The message to process

        Returns:
            Dictionary containing the agent's response
        """
        # Ensure agent is initialized
        if self.chat_agent is None:
            await self.initialize_agent()

        try:
            # Save user message to history
            self.history_manager.save_user_message(user_id, conversation_id, message)

            # Process the message with the agent
            result = await self.chat_agent.process_message(user_id, conversation_id, message)

            # Save AI response to history
            if "response_text" in result:
                self.history_manager.save_ai_response(user_id, conversation_id, result["response_text"])

            return result

        except Exception as e:
            # Handle any errors in agent processing
            error_result = {
                "response_text": f"Sorry, I encountered an issue processing your request: {str(e)}",
                "success": False,
                "error": str(e)
            }

            # Save error response to history
            if "response_text" in error_result:
                self.history_manager.save_ai_response(user_id, conversation_id, error_result["response_text"])

            return error_result

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