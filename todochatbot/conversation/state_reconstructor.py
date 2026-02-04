"""
State Reconstructor for Todo AI Chatbot

This module reconstructs conversation state from stored messages.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from ..database.conversations import load_conversation, Message


class StateReconstructor:
    """Reconstructs conversation state from stored messages for AI context."""

    def __init__(self):
        """Initialize the state reconstructor."""
        pass

    def reconstruct_conversation_state(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Reconstruct conversation state from stored messages.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Dictionary containing reconstructed conversation state
        """
        # Load conversation messages from database
        messages = load_conversation(user_id, conversation_id)

        # Build conversation context from messages
        conversation_state = {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'messages': self._format_messages_for_ai(messages),
            'context_summary': self._build_context_summary(messages),
            'active_tasks': self._extract_active_tasks(messages),
            'referenced_items': self._extract_referenced_items(messages),
            'conversation_metadata': self._extract_metadata(messages)
        }

        return conversation_state

    def _format_messages_for_ai(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Format messages in a way suitable for AI context.

        Args:
            messages: List of Message objects

        Returns:
            List of formatted message dictionaries
        """
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat() if msg.timestamp else None
            })
        return formatted_messages

    def _build_context_summary(self, messages: List[Message]) -> Dict[str, Any]:
        """
        Build a summary of the conversation context.

        Args:
            messages: List of Message objects

        Returns:
            Dictionary containing context summary
        """
        if not messages:
            return {
                'started_at': None,
                'last_activity': None,
                'total_messages': 0,
                'user_messages': 0,
                'ai_messages': 0,
                'topic_summary': '',
                'active_intent': None
            }

        # Count different types of messages
        user_messages = [msg for msg in messages if msg.role == 'user']
        ai_messages = [msg for msg in messages if msg.role == 'assistant']

        # Determine topic from recent messages
        recent_messages = messages[-5:]  # Last 5 messages
        topic_summary = self._infer_topic_from_messages(recent_messages)

        # Infer active intent from last user message
        active_intent = None
        for msg in reversed(messages):
            if msg.role == 'user':
                active_intent = self._infer_intent_from_message(msg.content)
                break

        return {
            'started_at': messages[0].timestamp.isoformat() if messages[0].timestamp else None,
            'last_activity': messages[-1].timestamp.isoformat() if messages[-1].timestamp else None,
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'ai_messages': len(ai_messages),
            'topic_summary': topic_summary,
            'active_intent': active_intent
        }

    def _infer_topic_from_messages(self, messages: List[Message]) -> str:
        """
        Infer the main topic from a list of messages.

        Args:
            messages: List of Message objects

        Returns:
            String summary of the topic
        """
        # Look for keywords related to tasks
        task_related_keywords = [
            'task', 'add', 'create', 'delete', 'complete', 'update',
            'todo', 'list', 'priority', 'due', 'date', 'remind'
        ]

        combined_content = ' '.join([msg.content.lower() for msg in messages])

        # Count task-related keywords
        task_count = sum(1 for keyword in task_related_keywords if keyword in combined_content)

        if task_count > 0:
            return 'Task management conversation'
        else:
            # Return first 100 characters of last message as topic
            if messages:
                return messages[-1].content[:100] + ('...' if len(messages[-1].content) > 100 else '')
            else:
                return 'Empty conversation'

    def _infer_intent_from_message(self, message_content: str) -> Optional[str]:
        """
        Infer the user's intent from a message.

        Args:
            message_content: The message content to analyze

        Returns:
            String representing the inferred intent
        """
        content_lower = message_content.lower()

        # Define intent patterns
        intent_patterns = {
            'add_task': ['add', 'create', 'make', 'new', 'need to', 'want to'],
            'list_tasks': ['list', 'show', 'display', 'see', 'what'],
            'update_task': ['update', 'change', 'modify', 'edit'],
            'complete_task': ['complete', 'finish', 'done', 'mark'],
            'delete_task': ['delete', 'remove', 'erase', 'cancel'],
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'help': ['help', 'how', 'can you', 'what can', 'what do']
        }

        for intent, patterns in intent_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                return intent

        return None

    def _extract_active_tasks(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """
        Extract information about tasks mentioned in the conversation.

        Args:
            messages: List of Message objects

        Returns:
            List of active tasks mentioned in conversation
        """
        active_tasks = []

        # Look for task-related information in messages
        for i, msg in enumerate(messages):
            if msg.role == 'user':
                # Look for task creation or reference patterns
                task_info = self._extract_task_from_message(msg.content, messages[i+1:] if i+1 < len(messages) else [])
                if task_info:
                    active_tasks.append(task_info)

        return active_tasks

    def _extract_task_from_message(
        self,
        user_message: str,
        subsequent_messages: List[Message]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract task information from a user message and subsequent AI responses.

        Args:
            user_message: The user's message
            subsequent_messages: Subsequent messages in the conversation

        Returns:
            Dictionary containing extracted task information or None
        """
        # This is a simplified extraction - in a real implementation,
        # this would use more sophisticated NLP
        import re

        # Look for task creation patterns
        create_patterns = [
            r'(?:add|create|make)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:to|for)\s+(.+?)(?:\s+for|\s+by|\s+on|\s+with|\s+tomorrow|\s+today|$)',
            r'(?:i\s+need\s+to|i\s+want\s+to|should)\s+(.+?)(?:\s+for|\s+by|\s+on|\s+with|\s+tomorrow|\s+today|$)'
        ]

        for pattern in create_patterns:
            match = re.search(pattern, user_message.lower())
            if match:
                task_description = match.group(1).strip()
                return {
                    'description': task_description,
                    'status': 'pending',  # Assume pending until completed
                    'mentioned_at': 'user_message',
                    'estimated_priority': self._estimate_priority(task_description)
                }

        return None

    def _estimate_priority(self, task_description: str) -> str:
        """
        Estimate priority from task description.

        Args:
            task_description: The task description to analyze

        Returns:
            Estimated priority level (high, medium, low)
        """
        high_priority_keywords = ['urgent', 'asap', 'immediately', 'critical', 'important']
        low_priority_keywords = ['whenever', 'eventually', 'someday', 'maybe']

        desc_lower = task_description.lower()

        for keyword in high_priority_keywords:
            if keyword in desc_lower:
                return 'high'

        for keyword in low_priority_keywords:
            if keyword in desc_lower:
                return 'low'

        return 'medium'

    def _extract_referenced_items(self, messages: List[Message]) -> Dict[str, List[str]]:
        """
        Extract items referenced in the conversation (tasks, dates, etc.).

        Args:
            messages: List of Message objects

        Returns:
            Dictionary of referenced item types to lists of values
        """
        referenced_items = {
            'tasks': [],
            'dates': [],
            'times': [],
            'people': [],
            'locations': []
        }

        for msg in messages:
            # Extract dates (simple pattern matching)
            import re
            date_patterns = [
                r'\b\d{1,2}[\/\-]\d{1,2}(?:[\/\-]\d{2,4})?\b',  # MM/DD or MM/DD/YYYY
                r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
                r'\b(today|tomorrow|yesterday|tonight|now)\b',  # Relative dates
                r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'  # Days
            ]

            for pattern in date_patterns:
                matches = re.findall(pattern, msg.content.lower())
                referenced_items['dates'].extend(matches)

        # Remove duplicates while preserving order
        for key in referenced_items:
            seen = set()
            unique_items = []
            for item in referenced_items[key]:
                if item not in seen:
                    seen.add(item)
                    unique_items.append(item)
            referenced_items[key] = unique_items

        return referenced_items

    def _extract_metadata(self, messages: List[Message]) -> Dict[str, Any]:
        """
        Extract metadata about the conversation.

        Args:
            messages: List of Message objects

        Returns:
            Dictionary containing conversation metadata
        """
        if not messages:
            return {}

        # Calculate average response time if timestamps are available
        response_times = []
        user_msg_timestamps = []

        for msg in messages:
            if msg.role == 'user' and msg.timestamp:
                user_msg_timestamps.append(msg.timestamp)
            elif msg.role == 'assistant' and msg.timestamp and user_msg_timestamps:
                # Match assistant response to previous user message
                prev_user_time = user_msg_timestamps[-1]
                response_time = (msg.timestamp - prev_user_time).total_seconds()
                response_times.append(response_time)

        avg_response_time = sum(response_times) / len(response_times) if response_times else None

        return {
            'avg_response_time_seconds': avg_response_time,
            'total_duration_seconds': (
                (messages[-1].timestamp - messages[0].timestamp).total_seconds()
                if messages[0].timestamp and messages[-1].timestamp
                else None
            ),
            'message_density': len(messages) / 60 if avg_response_time else 0  # Messages per minute
        }


def get_state_reconstructor() -> StateReconstructor:
    """
    Get an instance of the state reconstructor.

    Returns:
        StateReconstructor instance
    """
    return StateReconstructor()