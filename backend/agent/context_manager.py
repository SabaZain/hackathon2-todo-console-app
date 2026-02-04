"""
Context Manager for Todo AI Chatbot Agent.

This module manages conversation context across multiple turns to maintain
coherence and track ongoing operations.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json


class ContextManager:
    """Manages conversation context across multiple interactions."""

    def __init__(self):
        """Initialize the context manager with storage for conversation contexts."""
        self.contexts = {}  # Maps conversation_id to context data

    def get_context(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get the context for a conversation, creating it if it doesn't exist.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            Dictionary containing the conversation context
        """
        if conversation_id not in self.contexts:
            self.contexts[conversation_id] = self._create_default_context(conversation_id)

        return self.contexts[conversation_id]

    def update_context(self, conversation_id: str, updates: Dict[str, Any]):
        """
        Update the context for a conversation with new information.

        Args:
            conversation_id: The ID of the conversation
            updates: Dictionary of updates to apply to the context
        """
        context = self.get_context(conversation_id)
        for key, value in updates.items():
            context[key] = value

    def add_message_to_context(self, conversation_id: str, role: str, content: str):
        """
        Add a message to the conversation context.

        Args:
            conversation_id: The ID of the conversation
            role: The role of the message sender ('user' or 'assistant')
            content: The content of the message
        """
        context = self.get_context(conversation_id)
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        context["messages"].append(message)

        # Limit message history to prevent growing indefinitely
        max_messages = 20
        if len(context["messages"]) > max_messages:
            context["messages"] = context["messages"][-max_messages:]

    def get_recent_messages(self, conversation_id: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Get the most recent messages from a conversation context.

        Args:
            conversation_id: The ID of the conversation
            count: Number of recent messages to retrieve

        Returns:
            List of recent message dictionaries
        """
        context = self.get_context(conversation_id)
        return context["messages"][-count:]

    def clear_context(self, conversation_id: str):
        """
        Clear the context for a specific conversation.

        Args:
            conversation_id: The ID of the conversation to clear
        """
        if conversation_id in self.contexts:
            del self.contexts[conversation_id]

    def clear_expired_contexts(self, hours: int = 24):
        """
        Clear contexts that haven't been updated in the specified number of hours.

        Args:
            hours: Number of hours after which contexts are considered expired
        """
        expired_ids = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        for conversation_id, context in self.contexts.items():
            if "last_updated" in context:
                last_update = datetime.fromisoformat(context["last_updated"])
                if last_update < cutoff_time:
                    expired_ids.append(conversation_id)

        for conversation_id in expired_ids:
            del self.contexts[conversation_id]

    def get_user_context(self, user_id: str) -> List[str]:
        """
        Get all conversation IDs associated with a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of conversation IDs for the user
        """
        user_conversations = []
        for conversation_id, context in self.contexts.items():
            if context.get("user_id") == user_id:
                user_conversations.append(conversation_id)
        return user_conversations

    def _create_default_context(self, conversation_id: str) -> Dict[str, Any]:
        """
        Create a default context for a new conversation.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            Dictionary containing the default context
        """
        default_context = {
            "conversation_id": conversation_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat(),
            "messages": [],
            "active_operations": {},
            "user_preferences": {},
            "context_variables": {},
            "summary": ""
        }
        return default_context

    def set_user_context(self, conversation_id: str, user_id: str):
        """
        Associate a user with a conversation context.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user
        """
        context = self.get_context(conversation_id)
        context["user_id"] = user_id

    def set_context_variable(self, conversation_id: str, key: str, value: Any):
        """
        Set a context variable for a conversation.

        Args:
            conversation_id: The ID of the conversation
            key: The variable name
            value: The variable value
        """
        context = self.get_context(conversation_id)
        context["context_variables"][key] = value

    def get_context_variable(self, conversation_id: str, key: str, default: Any = None) -> Any:
        """
        Get a context variable for a conversation.

        Args:
            conversation_id: The ID of the conversation
            key: The variable name
            default: Default value to return if key doesn't exist

        Returns:
            The variable value or default
        """
        context = self.get_context(conversation_id)
        return context["context_variables"].get(key, default)

    def update_last_accessed(self, conversation_id: str):
        """
        Update the last accessed timestamp for a conversation.

        Args:
            conversation_id: The ID of the conversation
        """
        context = self.get_context(conversation_id)
        context["last_updated"] = datetime.utcnow().isoformat()


def get_context_manager() -> ContextManager:
    """
    Get an instance of the context manager.

    Returns:
        ContextManager instance
    """
    return ContextManager()