"""
Retriever for Todo AI Chatbot

This module retrieves conversation history for existing conversations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .storage import StorageManager


class Retriever:
    """Retrieves conversation history for existing conversations."""

    def __init__(self, storage_manager: StorageManager):
        """
        Initialize the retriever.

        Args:
            storage_manager: Instance of StorageManager to use for data access
        """
        self.storage_manager = storage_manager

    def retrieve_conversation_history(
        self,
        user_id: str,
        conversation_id: str,
        limit: Optional[int] = None,
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Retrieve the full history of a conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            limit: Maximum number of messages to retrieve
            from_timestamp: Only retrieve messages after this time
            to_timestamp: Only retrieve messages before this time

        Returns:
            Dictionary containing conversation history and metadata
        """
        # Get messages from storage
        all_messages = self.storage_manager.get_conversation_history(
            user_id, conversation_id, limit
        )

        # Filter by timestamp if specified
        if from_timestamp or to_timestamp:
            filtered_messages = []
            for msg in all_messages:
                msg_time = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))

                if from_timestamp and msg_time < from_timestamp:
                    continue
                if to_timestamp and msg_time > to_timestamp:
                    continue

                filtered_messages.append(msg)

            all_messages = filtered_messages

        # Get conversation metadata
        recent_convs = self.storage_manager.get_recent_conversations(user_id, limit=1)
        conv_metadata = {}
        if recent_convs:
            for conv in recent_convs:
                if conv['conversation_id'] == conversation_id:
                    conv_metadata = conv['metadata']
                    break

        return {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'messages': all_messages,
            'message_count': len(all_messages),
            'conversation_metadata': conv_metadata,
            'has_more': limit is not None and len(all_messages) == limit
        }

    def retrieve_recent_conversations(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve a list of recent conversations for a user.

        Args:
            user_id: The user's ID
            limit: Maximum number of conversations to retrieve

        Returns:
            List of conversation dictionaries
        """
        return self.storage_manager.get_recent_conversations(user_id, limit)

    def retrieve_last_n_messages(
        self,
        user_id: str,
        conversation_id: str,
        n: int
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the last N messages from a conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            n: Number of messages to retrieve

        Returns:
            List of message dictionaries
        """
        return self.storage_manager.get_conversation_history(
            user_id, conversation_id, limit=n, order='DESC'
        )

    def retrieve_conversations_by_date_range(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversations within a specific date range.

        Args:
            user_id: The user's ID
            start_date: Start of date range
            end_date: End of date range

        Returns:
            List of conversation dictionaries
        """
        all_conversations = self.storage_manager.get_recent_conversations(user_id, limit=None)

        filtered_conversations = []
        for conv in all_conversations:
            conv_start = datetime.fromisoformat(conv['created_at'].replace('Z', '+00:00'))
            if start_date <= conv_start <= end_date:
                filtered_conversations.append(conv)

        return filtered_conversations

    def retrieve_conversations_with_unread_messages(
        self,
        user_id: str,
        last_read_timestamp: datetime
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversations with messages after the last read timestamp.

        Args:
            user_id: The user's ID
            last_read_timestamp: Timestamp of last read message

        Returns:
            List of conversation dictionaries with unread messages
        """
        all_conversations = self.storage_manager.get_recent_conversations(user_id, limit=None)

        conversations_with_unread = []
        for conv in all_conversations:
            # Get the last message in the conversation
            last_messages = self.storage_manager.get_conversation_history(
                user_id, conv['conversation_id'], limit=1, order='DESC'
            )

            if last_messages:
                last_msg_time = datetime.fromisoformat(
                    last_messages[0]['timestamp'].replace('Z', '+00:00')
                )

                if last_msg_time > last_read_timestamp:
                    # Add unread message count
                    all_msgs = self.storage_manager.get_conversation_history(
                        user_id, conv['conversation_id']
                    )

                    unread_count = 0
                    for msg in all_msgs:
                        msg_time = datetime.fromisoformat(
                            msg['timestamp'].replace('Z', '+00:00')
                        )
                        if msg_time > last_read_timestamp:
                            unread_count += 1

                    conv['unread_count'] = unread_count
                    conversations_with_unread.append(conv)

        return conversations_with_unread

    def retrieve_conversations_by_participants(
        self,
        user_id: str,
        participants: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversations involving specific participants.

        Args:
            user_id: The user's ID
            participants: List of participant identifiers to search for

        Returns:
            List of conversation dictionaries
        """
        all_conversations = self.storage_manager.get_recent_conversations(user_id, limit=None)

        matching_conversations = []
        for conv in all_conversations:
            # Search for participants in the conversation messages
            messages = self.storage_manager.get_conversation_history(
                user_id, conv['conversation_id']
            )

            found_participant = False
            for msg in messages:
                for participant in participants:
                    if participant.lower() in msg['content'].lower():
                        found_participant = True
                        break
                if found_participant:
                    break

            if found_participant:
                matching_conversations.append(conv)

        return matching_conversations

    def retrieve_conversation_statistics(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve statistics for a specific conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Dictionary containing conversation statistics
        """
        messages = self.storage_manager.get_conversation_history(
            user_id, conversation_id
        )

        if not messages:
            return {
                'message_count': 0,
                'user_message_count': 0,
                'ai_message_count': 0,
                'first_message_time': None,
                'last_message_time': None,
                'average_message_length': 0,
                'estimated_duration_minutes': 0
            }

        # Count message types
        user_messages = [m for m in messages if m['role'] == 'user']
        ai_messages = [m for m in messages if m['role'] == 'assistant']

        # Calculate statistics
        first_time = datetime.fromisoformat(messages[0]['timestamp'].replace('Z', '+00:00'))
        last_time = datetime.fromisoformat(messages[-1]['timestamp'].replace('Z', '+00:00'))
        duration = (last_time - first_time).total_seconds() / 60  # in minutes

        avg_length = sum(len(m['content']) for m in messages) / len(messages) if messages else 0

        return {
            'message_count': len(messages),
            'user_message_count': len(user_messages),
            'ai_message_count': len(ai_messages),
            'first_message_time': messages[0]['timestamp'],
            'last_message_time': messages[-1]['timestamp'],
            'average_message_length': avg_length,
            'estimated_duration_minutes': duration
        }

    def retrieve_conversations_by_topic(
        self,
        user_id: str,
        topic_keywords: List[str],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversations containing specific topic keywords.

        Args:
            user_id: The user's ID
            topic_keywords: List of keywords related to the topic
            limit: Maximum number of conversations to retrieve

        Returns:
            List of conversation dictionaries matching the topic
        """
        all_conversations = self.storage_manager.get_recent_conversations(user_id, limit=None)

        topic_conversations = []
        for conv in all_conversations:
            # Get sample messages to check for topic keywords
            sample_messages = self.storage_manager.get_conversation_history(
                user_id, conv['conversation_id'], limit=5
            )

            # Check if any topic keyword appears in the messages
            topic_found = False
            for msg in sample_messages:
                content_lower = msg['content'].lower()
                for keyword in topic_keywords:
                    if keyword.lower() in content_lower:
                        topic_found = True
                        break
                if topic_found:
                    break

            if topic_found:
                topic_conversations.append(conv)

        # Return up to the limit
        return topic_conversations[:limit]

    def retrieve_conversation_summaries(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve summaries of recent conversations.

        Args:
            user_id: The user's ID
            limit: Maximum number of conversation summaries to retrieve

        Returns:
            List of conversation summary dictionaries
        """
        conversations = self.storage_manager.get_recent_conversations(user_id, limit)

        summaries = []
        for conv in conversations:
            # Get the last few messages to create a summary
            recent_messages = self.storage_manager.get_conversation_history(
                user_id, conv['conversation_id'], limit=3, order='DESC'
            )

            # Create a brief summary from the last message
            summary_text = ""
            if recent_messages:
                last_msg = recent_messages[0]['content']
                summary_text = last_msg[:100] + "..." if len(last_msg) > 100 else last_msg

            summary = {
                'conversation_id': conv['conversation_id'],
                'last_updated': conv['updated_at'],
                'summary': summary_text,
                'message_count': self.storage_manager.get_message_count(user_id, conv['conversation_id']),
                'participants': ['user', 'assistant']  # Simplified for this implementation
            }

            summaries.append(summary)

        return summaries

    def search_conversation_content(
        self,
        user_id: str,
        search_query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for specific content within conversations.

        Args:
            user_id: The user's ID
            search_query: Query string to search for
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing search results
        """
        # This would normally use a more sophisticated search mechanism
        # For now, we'll use the storage manager's search functionality
        return self.storage_manager.search_conversations(user_id, search_query, limit)


def get_retriever(storage_manager: StorageManager) -> Retriever:
    """
    Get an instance of the retriever.

    Args:
        storage_manager: Instance of StorageManager to use

    Returns:
        Retriever instance
    """
    return Retriever(storage_manager)