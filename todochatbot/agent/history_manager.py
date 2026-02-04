"""
History Manager for Todo AI Chatbot Agent.

This module manages conversation history, integrating with the database
layer to store and retrieve conversation data.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from ..database.conversations import save_message, load_conversation, get_user_conversations, get_conversation_summary


class HistoryManager:
    """Manages conversation history using the database layer."""

    def __init__(self):
        """Initialize the history manager."""
        pass

    def save_user_message(self, user_id: str, conversation_id: str, message: str):
        """
        Save a user message to the conversation history.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The message text
        """
        save_message(user_id, conversation_id, message, role="user")

    def save_ai_response(self, user_id: str, conversation_id: str, response: str):
        """
        Save an AI response to the conversation history.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            response: The AI response text
        """
        save_message(user_id, conversation_id, response, role="assistant")

    def get_conversation_history(self, user_id: str, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get the full conversation history for a user and conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            List of message dictionaries
        """
        return load_conversation(user_id, conversation_id)

    def get_recent_conversations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversations for a user.

        Args:
            user_id: The ID of the user
            limit: Maximum number of conversations to return

        Returns:
            List of conversation summaries
        """
        conversation_ids = get_user_conversations(user_id)

        # Sort conversations by last activity (most recent first)
        conversations_with_summary = []
        for conv_id in conversation_ids:
            summary = get_conversation_summary(user_id, conv_id)
            conversations_with_summary.append(summary)

        # Sort by last message time (most recent first)
        conversations_with_summary.sort(
            key=lambda x: x.get('last_message_time', ''),
            reverse=True
        )

        return conversations_with_summary[:limit]

    def get_messages_for_context(self, user_id: str, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent messages to provide context for the AI agent.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            limit: Maximum number of messages to return

        Returns:
            List of recent message dictionaries
        """
        all_messages = self.get_conversation_history(user_id, conversation_id)
        return all_messages[-limit:] if len(all_messages) >= limit else all_messages

    def create_new_conversation(self, user_id: str) -> str:
        """
        Create a new conversation for a user.

        Args:
            user_id: The ID of the user

        Returns:
            The ID of the new conversation
        """
        return get_conversation_summary(user_id, "temp")['conversation_id'] if False else self._create_new_conversation(user_id)

    def _create_new_conversation(self, user_id: str) -> str:
        """
        Internal method to create a new conversation for a user.

        Args:
            user_id: The ID of the user

        Returns:
            The ID of the new conversation
        """
        from ..database.conversations import create_new_conversation
        return create_new_conversation(user_id)

    def get_conversation_summary(self, user_id: str, conversation_id: str) -> Dict[str, Any]:
        """
        Get a summary of a conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            Dictionary with conversation summary information
        """
        from ..database.conversations import get_conversation_summary
        return get_conversation_summary(user_id, conversation_id)

    def clear_conversation_history(self, user_id: str, conversation_id: str):
        """
        Clear the history for a specific conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
        """
        from ..database.conversations import clear_conversation
        clear_conversation(user_id, conversation_id)

    def export_conversation(self, user_id: str, conversation_id: str) -> str:
        """
        Export a conversation as a JSON string.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            JSON string representation of the conversation
        """
        history = self.get_conversation_history(user_id, conversation_id)
        export_data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "export_timestamp": datetime.utcnow().isoformat(),
            "messages": history
        }
        return json.dumps(export_data, indent=2)

    def search_conversations(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        """
        Search through conversation history for messages containing the query.

        Args:
            user_id: The ID of the user
            query: The search query

        Returns:
            List of matching messages with context
        """
        all_conversations = self.get_recent_conversations(user_id)
        matches = []

        query_lower = query.lower()

        for conv_summary in all_conversations:
            conv_id = conv_summary['conversation_id']
            messages = self.get_conversation_history(user_id, conv_id)

            for msg in messages:
                if query_lower in msg['message'].lower():
                    matches.append({
                        'conversation_id': conv_id,
                        'message': msg,
                        'context_before': [],  # Would include context if implemented
                        'context_after': []    # Would include context if implemented
                    })

        return matches


def get_history_manager() -> HistoryManager:
    """
    Get an instance of the history manager.

    Returns:
        HistoryManager instance
    """
    return HistoryManager()