"""
Resumer for Todo AI Chatbot

This module supports conversation continuation after interruptions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .state_reconstructor import StateReconstructor
from .storage import StorageManager
from .retriever import Retriever
from .context_preserver import ContextPreserver


class Resumer:
    """Supports conversation continuation after interruptions."""

    def __init__(
        self,
        state_reconstructor: StateReconstructor,
        storage_manager: StorageManager,
        retriever: Retriever,
        context_preserver: ContextPreserver
    ):
        """
        Initialize the resumer.

        Args:
            state_reconstructor: Instance of StateReconstructor
            storage_manager: Instance of StorageManager
            retriever: Instance of Retriever
            context_preserver: Instance of ContextPreserver
        """
        self.state_reconstructor = state_reconstructor
        self.storage_manager = storage_manager
        self.retriever = retriever
        self.context_preserver = context_preserver
        self.interruption_threshold = 3600  # 1 hour threshold for interruption

    def resume_conversation(
        self,
        user_id: str,
        conversation_id: str,
        current_message: str,
        max_context_messages: int = 10
    ) -> Dict[str, Any]:
        """
        Resume a conversation after a potential interruption.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            current_message: The current message that triggered the resume
            max_context_messages: Maximum number of previous messages to include

        Returns:
            Dictionary with resume information and context
        """
        # Check if conversation was interrupted
        was_interrupted, interruption_duration = self._was_conversation_interrupted(
            user_id, conversation_id
        )

        # Get conversation history
        conversation_history = self.retriever.retrieve_conversation_history(
            user_id, conversation_id, limit=max_context_messages
        )

        # Get preserved context
        preserved_context = self.context_preserver.get_preserved_context(
            user_id, conversation_id
        )

        resume_info = {
            'was_interrupted': was_interrupted,
            'interruption_duration_seconds': interruption_duration,
            'conversation_history': conversation_history,
            'preserved_context': preserved_context,
            'should_summarize': was_interrupted or len(conversation_history['messages']) > max_context_messages,
            'resumed_at': datetime.now().isoformat(),
            'recommendation': self._get_resume_recommendation(
                was_interrupted, conversation_history, current_message
            )
        }

        # Log the resume event
        self._log_resume_event(user_id, conversation_id, resume_info)

        return resume_info

    def _was_conversation_interrupted(
        self,
        user_id: str,
        conversation_id: str
    ) -> tuple[bool, int]:
        """
        Determine if a conversation was interrupted based on time since last activity.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Tuple of (was_interrupted: bool, interruption_duration: int in seconds)
        """
        # Get the last message in the conversation
        last_messages = self.storage_manager.get_conversation_history(
            user_id, conversation_id, limit=1, order='DESC'
        )

        if not last_messages:
            # New conversation, not interrupted
            return False, 0

        last_message_time = datetime.fromisoformat(
            last_messages[0]['timestamp'].replace('Z', '+00:00')
        )
        time_since_last = datetime.now() - last_message_time

        # Consider interrupted if longer than threshold
        is_interrupted = time_since_last.total_seconds() > self.interruption_threshold

        return is_interrupted, int(time_since_last.total_seconds())

    def _get_resume_recommendation(
        self,
        was_interrupted: bool,
        conversation_history: Dict[str, Any],
        current_message: str
    ) -> str:
        """
        Get a recommendation for how to handle the conversation resume.

        Args:
            was_interrupted: Whether the conversation was interrupted
            conversation_history: The conversation history
            current_message: The current message

        Returns:
            Recommendation string
        """
        if was_interrupted:
            if conversation_history['message_count'] > 5:
                return "summarize_and_continue"
            else:
                return "simple_greeting_and_continue"
        elif self._message_refers_to_past_content(current_message, conversation_history):
            return "recall_context_and_respond"
        else:
            return "continue_normally"

    def _message_refers_to_past_content(
        self,
        current_message: str,
        conversation_history: Dict[str, Any]
    ) -> bool:
        """
        Check if the current message refers to content from earlier in the conversation.

        Args:
            current_message: The current message
            conversation_history: The conversation history

        Returns:
            Boolean indicating if message refers to past content
        """
        # Look for references to previous topics or tasks
        current_lower = current_message.lower()

        # Check for reference words
        reference_words = ['that', 'previous', 'earlier', 'before', 'above', 'mentioned', 'said', 'asked']

        if any(ref_word in current_lower for ref_word in reference_words):
            return True

        # Check for task-specific references
        task_refs = ['task', 'the task', 'it', 'that task', 'the thing']
        if any(task_ref in current_lower for task_ref in task_refs):
            return True

        return False

    def get_interruption_summary(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Get a summary of the interruption.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Dictionary with interruption summary
        """
        was_interrupted, duration = self._was_conversation_interrupted(user_id, conversation_id)

        if not was_interrupted:
            return {
                'was_interrupted': False,
                'duration_since_last_interaction': duration,
                'summary_needed': False
            }

        # Get conversation context before interruption
        messages_before = self.storage_manager.get_conversation_history(
            user_id, conversation_id, limit=5, order='DESC'
        )

        # Identify the main topics discussed
        topics = self._identify_topics_in_messages(messages_before)

        # Identify any tasks that were in progress
        active_tasks = self._identify_active_tasks(messages_before)

        return {
            'was_interrupted': True,
            'interruption_duration_seconds': duration,
            'summary_needed': True,
            'topics_discussed_before': topics,
            'active_tasks_before': active_tasks,
            'context_before_interruption': self._create_context_summary(messages_before)
        }

    def _identify_topics_in_messages(self, messages: List[Dict[str, Any]]) -> List[str]:
        """
        Identify main topics discussed in messages.

        Args:
            messages: List of message dictionaries

        Returns:
            List of identified topics
        """
        all_content = " ".join([msg['content'] for msg in messages])
        content_lower = all_content.lower()

        # Identify task-related topics
        topics = []
        if any(word in content_lower for word in ['add', 'create', 'task', 'todo']):
            topics.append('task_creation')
        if any(word in content_lower for word in ['list', 'show', 'display', 'view']):
            topics.append('task_listing')
        if any(word in content_lower for word in ['update', 'change', 'modify', 'edit']):
            topics.append('task_modification')
        if any(word in content_lower for word in ['complete', 'finish', 'done']):
            topics.append('task_completion')
        if any(word in content_lower for word in ['delete', 'remove', 'cancel']):
            topics.append('task_deletion')

        return topics

    def _identify_active_tasks(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Identify tasks that were in progress based on conversation.

        Args:
            messages: List of message dictionaries

        Returns:
            List of active tasks
        """
        active_tasks = []

        for msg in messages:
            content_lower = msg['content'].lower()

            # Look for task creation or modification
            if any(word in content_lower for word in ['add', 'create', 'new task']):
                # Extract potential task description
                import re
                task_match = re.search(r'(?:add|create|make)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:to|for)\s+(.+?)(?:\s+for|\s+by|\s+on|\s+with|\s+tomorrow|\s+today|$)', content_lower)
                if task_match:
                    active_tasks.append({
                        'type': 'creation',
                        'description': task_match.group(1).strip(),
                        'status': 'pending'
                    })

        return active_tasks

    def _create_context_summary(self, messages: List[Dict[str, Any]]) -> str:
        """
        Create a brief summary of the conversation context.

        Args:
            messages: List of message dictionaries

        Returns:
            Context summary string
        """
        if not messages:
            return "No conversation history available."

        # Take the last few messages to create a summary
        recent_messages = messages[-3:]  # Last 3 messages
        summary_parts = []

        for msg in recent_messages:
            role_prefix = "User" if msg['role'] == 'user' else "AI"
            content_preview = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
            summary_parts.append(f"{role_prefix}: {content_preview}")

        return " | ".join(summary_parts)

    def _log_resume_event(
        self,
        user_id: str,
        conversation_id: str,
        resume_info: Dict[str, Any]
    ):
        """
        Log the resume event for analytics.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            resume_info: The resume information
        """
        # In a real implementation, this would log to a proper logging system
        # For now, we'll store as metadata in the conversation
        metadata = {
            'last_resumed_at': resume_info['resumed_at'],
            'was_interrupted': resume_info['was_interrupted'],
            'interruption_duration': resume_info['interruption_duration_seconds']
        }

        self.storage_manager.update_conversation_metadata(
            user_id, conversation_id, metadata
        )

    def handle_interruption_greeting(
        self,
        user_id: str,
        conversation_id: str
    ) -> str:
        """
        Generate an appropriate greeting when resuming after an interruption.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Appropriate greeting message
        """
        was_interrupted, duration = self._was_conversation_interrupted(user_id, conversation_id)

        if not was_interrupted:
            return ""

        hours_ago = int(duration / 3600)
        if hours_ago >= 24:
            days_ago = hours_ago // 24
            if days_ago == 1:
                return "Welcome back! I see you were away for a day. How can I help you today?"
            else:
                return f"Welcome back! I see you were away for {days_ago} days. How can I help you today?"
        elif hours_ago >= 1:
            return f"Welcome back! I see you were away for {hours_ago} hour{'s' if hours_ago > 1 else ''}. How can I help you today?"
        else:
            minutes_ago = int(duration / 60)
            return f"Welcome back! I see you were away for {minutes_ago} minutes. How can I help you continue with your tasks?"

    def get_context_for_continuation(
        self,
        user_id: str,
        conversation_id: str,
        max_messages: int = 5
    ) -> Dict[str, Any]:
        """
        Get the appropriate context for continuing a conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            max_messages: Maximum number of messages to include

        Returns:
            Dictionary with context for continuation
        """
        # Get recent messages
        recent_messages = self.retriever.retrieve_last_n_messages(
            user_id, conversation_id, max_messages
        )

        # Get conversation statistics
        stats = self.retriever.retrieve_conversation_statistics(user_id, conversation_id)

        # Get any active tasks from preserved context
        preserved_context = self.context_preserver.get_preserved_context(user_id, conversation_id)

        return {
            'recent_messages': recent_messages,
            'conversation_stats': stats,
            'active_tasks': preserved_context.get('active_tasks', []),
            'referenced_items': preserved_context.get('referenced_items', {}),
            'context_summary': preserved_context.get('context_summary', {}),
            'should_provide_summary': len(recent_messages) < stats['message_count']
        }

    def mark_conversation_active(
        self,
        user_id: str,
        conversation_id: str
    ):
        """
        Mark a conversation as active again after interruption.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
        """
        # Update metadata to indicate the conversation is active again
        metadata = {
            'marked_active_at': datetime.now().isoformat(),
            'was_interrupted': False,
            'interruption_duration': 0
        }

        self.storage_manager.update_conversation_metadata(user_id, conversation_id, metadata)

        # Clear any interruption-related context
        self.context_preserver.clear_context_cache(user_id, conversation_id)


def get_resumer(
    state_reconstructor: StateReconstructor,
    storage_manager: StorageManager,
    retriever: Retriever,
    context_preserver: ContextPreserver
) -> Resumer:
    """
    Get an instance of the resumer.

    Args:
        state_reconstructor: Instance of StateReconstructor
        storage_manager: Instance of StorageManager
        retriever: Instance of Retriever
        context_preserver: Instance of ContextPreserver

    Returns:
        Resumer instance
    """
    return Resumer(
        state_reconstructor,
        storage_manager,
        retriever,
        context_preserver
    )