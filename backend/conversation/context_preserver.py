"""
Context Preserver for Todo AI Chatbot

This module preserves conversation context across multiple turns.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .state_reconstructor import StateReconstructor
from .storage import StorageManager
from .retriever import Retriever


class ContextPreserver:
    """Preserves conversation context across multiple turns."""

    def __init__(self, state_reconstructor: StateReconstructor, storage_manager: StorageManager):
        """
        Initialize the context preserver.

        Args:
            state_reconstructor: Instance of StateReconstructor
            storage_manager: Instance of StorageManager
        """
        self.state_reconstructor = state_reconstructor
        self.storage_manager = storage_manager
        self.retriever = Retriever(storage_manager)
        self.context_cache = {}  # Cache for frequently accessed context

    def preserve_context(
        self,
        user_id: str,
        conversation_id: str,
        current_message: Dict[str, Any],
        ai_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Preserve context after a conversation turn.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            current_message: The current user message
            ai_response: The AI's response

        Returns:
            Updated context dictionary
        """
        # Store both messages in the database
        self.storage_manager.store_message(
            user_id,
            conversation_id,
            current_message['role'],
            current_message['content'],
            current_message.get('metadata', {})
        )

        self.storage_manager.store_message(
            user_id,
            conversation_id,
            ai_response['role'],
            ai_response['content'],
            ai_response.get('metadata', {})
        )

        # Update context cache
        cache_key = f"{user_id}:{conversation_id}"
        if cache_key in self.context_cache:
            # Add new messages to cached context
            self.context_cache[cache_key]['messages'].extend([
                current_message,
                ai_response
            ])

            # Update context summary
            self.context_cache[cache_key]['context_summary'] = self._update_context_summary(
                self.context_cache[cache_key]['context_summary'],
                current_message,
                ai_response
            )
        else:
            # Reconstruct full context if not in cache
            self.context_cache[cache_key] = self.state_reconstructor.reconstruct_conversation_state(
                user_id, conversation_id
            )

        return self.context_cache[cache_key]

    def get_preserved_context(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve preserved context for a conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Context dictionary
        """
        cache_key = f"{user_id}:{conversation_id}"

        # Check if context is in cache
        if cache_key in self.context_cache:
            # Check if cache is still valid (not too old)
            if self._is_cache_valid(self.context_cache[cache_key]):
                return self.context_cache[cache_key]

        # If not in cache or cache is invalid, reconstruct
        context = self.state_reconstructor.reconstruct_conversation_state(
            user_id, conversation_id
        )

        # Store in cache
        self.context_cache[cache_key] = context

        return context

    def _is_cache_valid(self, cached_context: Dict[str, Any]) -> bool:
        """
        Check if cached context is still valid.

        Args:
            cached_context: The cached context to check

        Returns:
            Boolean indicating if cache is valid
        """
        if 'last_updated' not in cached_context:
            return False

        # Cache is valid for 10 minutes
        cache_duration = 600  # seconds
        last_updated = datetime.fromisoformat(cached_context['last_updated'])
        current_time = datetime.now()

        return (current_time - last_updated).total_seconds() < cache_duration

    def _update_context_summary(
        self,
        current_summary: Dict[str, Any],
        new_user_message: Dict[str, Any],
        new_ai_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update context summary with new messages.

        Args:
            current_summary: Current context summary
            new_user_message: New user message
            new_ai_response: New AI response

        Returns:
            Updated context summary
        """
        updated_summary = current_summary.copy()

        # Update message counts
        updated_summary['total_messages'] = updated_summary.get('total_messages', 0) + 2
        updated_summary['user_messages'] = updated_summary.get('user_messages', 0) + 1
        updated_summary['ai_messages'] = updated_summary.get('ai_messages', 0) + 1
        updated_summary['last_activity'] = datetime.now().isoformat()

        # Potentially update topic summary if new messages suggest a topic shift
        new_topic = self._infer_topic_from_messages([new_user_message, new_ai_response])
        if new_topic and new_topic != updated_summary.get('topic_summary'):
            updated_summary['topic_summary'] = new_topic

        # Update active intent based on the newest user message
        active_intent = self._infer_intent_from_message(new_user_message['content'])
        updated_summary['active_intent'] = active_intent

        return updated_summary

    def _infer_topic_from_messages(self, messages: List[Dict[str, Any]]) -> str:
        """
        Infer the main topic from a list of messages.

        Args:
            messages: List of message dictionaries

        Returns:
            String summary of the topic
        """
        # Look for keywords related to tasks
        task_related_keywords = [
            'task', 'add', 'create', 'delete', 'complete', 'update',
            'todo', 'list', 'priority', 'due', 'date', 'remind'
        ]

        combined_content = ' '.join([msg['content'].lower() for msg in messages])

        # Count task-related keywords
        task_count = sum(1 for keyword in task_related_keywords if keyword in combined_content)

        if task_count > 0:
            return 'Task management conversation'
        else:
            # Return first 100 characters of last message as topic
            if messages:
                last_content = messages[-1]['content']
                return last_content[:100] + ('...' if len(last_content) > 100 else '')
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

    def update_context_reference(
        self,
        user_id: str,
        conversation_id: str,
        reference_key: str,
        reference_value: Any
    ) -> bool:
        """
        Update a specific reference in the conversation context.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            reference_key: The key to update
            reference_value: The new value

        Returns:
            Boolean indicating success
        """
        context = self.get_preserved_context(user_id, conversation_id)

        # Update the specific reference
        context['referenced_items'] = context.get('referenced_items', {})
        context['referenced_items'][reference_key] = reference_value

        # Update cache
        cache_key = f"{user_id}:{conversation_id}"
        if cache_key in self.context_cache:
            self.context_cache[cache_key] = context

        # Update metadata in storage
        self.storage_manager.update_conversation_metadata(
            user_id,
            conversation_id,
            {reference_key: reference_value}
        )

        return True

    def get_context_references(
        self,
        user_id: str,
        conversation_id: str,
        reference_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get references from the conversation context.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            reference_type: Optional specific reference type to retrieve

        Returns:
            Dictionary of references
        """
        context = self.get_preserved_context(user_id, conversation_id)

        if reference_type:
            return context.get('referenced_items', {}).get(reference_type, [])
        else:
            return context.get('referenced_items', {})

    def clear_context_cache(
        self,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None
    ):
        """
        Clear context cache for specific conversation or all conversations.

        Args:
            user_id: Optional user ID to clear cache for
            conversation_id: Optional conversation ID to clear cache for
        """
        if user_id and conversation_id:
            # Clear cache for specific conversation
            cache_key = f"{user_id}:{conversation_id}"
            if cache_key in self.context_cache:
                del self.context_cache[cache_key]
        elif user_id:
            # Clear cache for all conversations of a user
            keys_to_remove = [key for key in self.context_cache.keys() if key.startswith(f"{user_id}:")]
            for key in keys_to_remove:
                del self.context_cache[key]
        else:
            # Clear entire cache
            self.context_cache.clear()

    def get_active_conversation_contexts(self) -> List[Dict[str, Any]]:
        """
        Get a list of active conversation contexts.

        Returns:
            List of dictionaries containing active conversation contexts
        """
        active_contexts = []

        for cache_key, context in self.context_cache.items():
            user_id, conversation_id = cache_key.split(':', 1)

            # Check if context is still valid
            if self._is_cache_valid(context):
                active_contexts.append({
                    'user_id': user_id,
                    'conversation_id': conversation_id,
                    'context_summary': context.get('context_summary', {}),
                    'last_activity': context.get('context_summary', {}).get('last_activity')
                })

        return active_contexts

    def get_conversation_depth(
        self,
        user_id: str,
        conversation_id: str
    ) -> int:
        """
        Get the depth of a conversation (number of message exchanges).

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Number of message exchanges (user-AI pairs)
        """
        context = self.get_preserved_context(user_id, conversation_id)
        return context.get('context_summary', {}).get('total_messages', 0) // 2

    def get_context_freshness(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Get information about how fresh the context is.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Dictionary with freshness information
        """
        context = self.get_preserved_context(user_id, conversation_id)
        context_summary = context.get('context_summary', {})

        last_activity_str = context_summary.get('last_activity')
        if last_activity_str:
            last_activity = datetime.fromisoformat(last_activity_str)
            time_since_last_activity = datetime.now() - last_activity

            return {
                'last_activity': last_activity_str,
                'seconds_since_last_activity': time_since_last_activity.total_seconds(),
                'is_fresh': time_since_last_activity.total_seconds() < 300,  # Less than 5 minutes
                'stale': time_since_last_activity.total_seconds() > 1800  # More than 30 minutes
            }
        else:
            return {
                'last_activity': None,
                'seconds_since_last_activity': float('inf'),
                'is_fresh': False,
                'stale': True
            }


def get_context_preserver(
    state_reconstructor: StateReconstructor,
    storage_manager: StorageManager
) -> ContextPreserver:
    """
    Get an instance of the context preserver.

    Args:
        state_reconstructor: Instance of StateReconstructor
        storage_manager: Instance of StorageManager

    Returns:
        ContextPreserver instance
    """
    return ContextPreserver(state_reconstructor, storage_manager)