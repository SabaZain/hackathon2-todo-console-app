"""
Conversation Manager for Todo AI Chatbot API.

This module handles conversation state management via the database layer.
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

from database.conversations import (
    save_message,
    load_conversation,
    get_user_conversations,
    create_new_conversation,
    get_conversation_summary
)


class ConversationManager:
    """Manages conversation state using the database layer."""

    def __init__(self):
        """Initialize the conversation manager."""
        pass

    async def create_conversation(self, user_id: str) -> str:
        """
        Create a new conversation for a user.

        Args:
            user_id: The ID of the user

        Returns:
            The ID of the new conversation
        """
        # In a real implementation, this would call the database asynchronously
        # For now, we'll use the synchronous version from the database module
        conversation_id = create_new_conversation(user_id)

        # Save an initial system message to establish the conversation
        save_message(
            user_id=user_id,
            conversation_id=conversation_id,
            content="Conversation started",
            role="system"
        )

        return conversation_id

    async def get_conversation(self, user_id: str, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get a specific conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            List of messages in the conversation
        """
        # Load conversation from database
        messages = load_conversation(user_id, conversation_id)
        return messages

    async def save_interaction(self, user_id: str, conversation_id: str, user_message: str, ai_response: str) -> bool:
        """
        Save a complete interaction (user message + AI response) to the conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            user_message: The message from the user
            ai_response: The response from the AI

        Returns:
            True if successfully saved
        """
        try:
            # Save user message
            save_message(
                user_id=user_id,
                conversation_id=conversation_id,
                content=user_message,
                role="user"
            )

            # Save AI response
            save_message(
                user_id=user_id,
                conversation_id=conversation_id,
                content=ai_response,
                role="assistant"
            )

            return True
        except Exception:
            return False

    async def get_user_conversations(self, user_id: str) -> List[str]:
        """
        Get all conversation IDs for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List of conversation IDs
        """
        return get_user_conversations(user_id)

    async def get_conversation_summary(self, user_id: str, conversation_id: str) -> Dict[str, Any]:
        """
        Get a summary of a conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            Dictionary with conversation summary information
        """
        return get_conversation_summary(user_id, conversation_id)

    async def get_recent_conversations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversations for a user.

        Args:
            user_id: The ID of the user
            limit: Maximum number of conversations to return

        Returns:
            List of conversation summaries
        """
        conversation_ids = get_user_conversations(user_id)

        # Get summaries for all conversations
        summaries = []
        for conv_id in conversation_ids:
            summary = get_conversation_summary(user_id, conv_id)
            summaries.append(summary)

        # Sort by last message time (most recent first)
        summaries.sort(
            key=lambda x: x.get('last_message_time', ''),
            reverse=True
        )

        return summaries[:limit]

    async def update_conversation_metadata(self, user_id: str, conversation_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update metadata for a conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            metadata: Metadata to update

        Returns:
            True if successfully updated
        """
        try:
            # In a real implementation, this would store metadata in a structured way
            # For now, we'll just store it as a special message type
            metadata_message = f"METADATA_UPDATE: {str(metadata)}"
            save_message(
                user_id=user_id,
                conversation_id=conversation_id,
                content=metadata_message,
                role="system"
            )

            return True
        except Exception:
            return False

    async def clear_conversation(self, user_id: str, conversation_id: str) -> bool:
        """
        Clear all messages from a conversation while preserving the conversation record.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            True if successfully cleared
        """
        from database.conversations import clear_conversation
        try:
            clear_conversation(user_id, conversation_id)
            return True
        except Exception:
            return False

    async def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        """
        Delete a conversation entirely.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            True if successfully deleted
        """
        from database.conversations import delete_conversation
        try:
            delete_conversation(user_id, conversation_id)
            return True
        except Exception:
            return False

    async def get_conversation_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics about a user's conversations.

        Args:
            user_id: The ID of the user

        Returns:
            Dictionary with conversation statistics
        """
        conversation_ids = get_user_conversations(user_id)

        total_conversations = len(conversation_ids)
        total_messages = 0

        for conv_id in conversation_ids:
            messages = load_conversation(user_id, conv_id)
            total_messages += len(messages)

        stats = {
            "user_id": user_id,
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "average_messages_per_conversation": total_messages // total_conversations if total_conversations > 0 else 0,
            "timestamp": datetime.utcnow().isoformat()
        }

        return stats


def get_conversation_manager() -> ConversationManager:
    """
    Get an instance of the conversation manager.

    Returns:
        ConversationManager instance
    """
    return ConversationManager()


async def create_conversation_manager() -> ConversationManager:
    """
    Create and initialize a conversation manager.

    Returns:
        Initialized ConversationManager instance
    """
    return ConversationManager()