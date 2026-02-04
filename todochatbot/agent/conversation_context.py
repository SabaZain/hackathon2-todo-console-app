"""
Conversation Context for Todo AI Chatbot Agent.

This module implements conversation context management, drawing inspiration
from .claude/agents/conversation-context-agent.md
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class ConversationContext:
    """Manages context for a specific conversation."""

    def __init__(self, conversation_id: str, user_id: str):
        """
        Initialize conversation context.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user
        """
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.last_updated = datetime.utcnow()

        # Core context components
        self.participants = [user_id]
        self.shared_state = {}
        self.topic_history = []
        self.action_log = []
        self.entity_resolution = {}
        self.user_preferences = {}
        self.temporal_context = {}
        self.semantic_memory = []

    def update_context(self, **kwargs):
        """
        Update the conversation context with new information.

        Args:
            **kwargs: Key-value pairs to update in the context
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.last_updated = datetime.utcnow()

    def add_to_shared_state(self, key: str, value: Any):
        """
        Add information to the shared state of the conversation.

        Args:
            key: The key for the state item
            value: The value to store
        """
        self.shared_state[key] = value

    def get_from_shared_state(self, key: str, default: Any = None) -> Any:
        """
        Retrieve information from the shared state.

        Args:
            key: The key to look up
            default: Default value if key not found

        Returns:
            The value from shared state or default
        """
        return self.shared_state.get(key, default)

    def log_action(self, action_type: str, details: Dict[str, Any]):
        """
        Log an action in the conversation's action log.

        Args:
            action_type: Type of action (e.g., 'message_sent', 'task_created')
            details: Details about the action
        """
        action = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": action_type,
            "details": details
        }
        self.action_log.append(action)

    def update_topic(self, topic: str):
        """
        Update the current topic of the conversation.

        Args:
            topic: The current topic
        """
        if not self.topic_history or self.topic_history[-1]["topic"] != topic:
            topic_entry = {
                "topic": topic,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.topic_history.append(topic_entry)

    def resolve_entity(self, reference: str, actual_value: str):
        """
        Resolve an entity reference to its actual value.

        Args:
            reference: The reference used (e.g., "it", "that task")
            actual_value: The actual value it refers to
        """
        self.entity_resolution[reference] = actual_value

    def get_resolved_entity(self, reference: str) -> Optional[str]:
        """
        Get the resolved value for an entity reference.

        Args:
            reference: The reference to resolve

        Returns:
            The resolved value or None
        """
        return self.entity_resolution.get(reference)

    def update_user_preference(self, preference_key: str, value: Any):
        """
        Update a user preference in the context.

        Args:
            preference_key: The preference to update
            value: The new value
        """
        self.user_preferences[preference_key] = value

    def get_user_preference(self, preference_key: str, default: Any = None) -> Any:
        """
        Get a user preference from the context.

        Args:
            preference_key: The preference to retrieve
            default: Default value if preference not set

        Returns:
            The preference value or default
        """
        return self.user_preferences.get(preference_key, default)

    def update_temporal_context(self, **temporal_info):
        """
        Update temporal context information.

        Args:
            **temporal_info: Temporal information like dates, timeframes
        """
        self.temporal_context.update(temporal_info)

    def get_temporal_context(self) -> Dict[str, Any]:
        """
        Get the current temporal context.

        Returns:
            Dictionary of temporal context information
        """
        return self.temporal_context.copy()

    def add_semantic_memory(self, memory_item: Dict[str, Any]):
        """
        Add a semantic memory item to the conversation context.

        Args:
            memory_item: Dictionary containing memory information
        """
        memory_entry = {
            "content": memory_item,
            "timestamp": datetime.utcnow().isoformat(),
            "importance": memory_item.get("importance", 0.5)
        }
        self.semantic_memory.append(memory_entry)

    def get_relevant_memories(self, importance_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Get relevant memories based on importance threshold.

        Args:
            importance_threshold: Minimum importance score to include

        Returns:
            List of relevant memory items
        """
        return [
            mem for mem in self.semantic_memory
            if mem["importance"] >= importance_threshold
        ]

    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current conversation context.

        Returns:
            Dictionary containing context summary
        """
        return {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "participants": self.participants,
            "shared_state_keys": list(self.shared_state.keys()),
            "topic_history_length": len(self.topic_history),
            "action_log_length": len(self.action_log),
            "entity_resolution_count": len(self.entity_resolution),
            "user_preferences_set": list(self.user_preferences.keys()),
            "temporal_context_keys": list(self.temporal_context.keys()),
            "semantic_memory_count": len(self.semantic_memory)
        }

    def serialize(self) -> str:
        """
        Serialize the conversation context to JSON string.

        Returns:
            JSON string representation of the context
        """
        context_dict = {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "participants": self.participants,
            "shared_state": self.shared_state,
            "topic_history": self.topic_history,
            "action_log": self.action_log,
            "entity_resolution": self.entity_resolution,
            "user_preferences": self.user_preferences,
            "temporal_context": self.temporal_context,
            "semantic_memory": self.semantic_memory
        }
        return json.dumps(context_dict, default=str)

    @classmethod
    def deserialize(cls, serialized_context: str) -> 'ConversationContext':
        """
        Deserialize a JSON string to a ConversationContext object.

        Args:
            serialized_context: JSON string representation of context

        Returns:
            ConversationContext instance
        """
        data = json.loads(serialized_context)
        context = cls(data["conversation_id"], data["user_id"])

        # Restore all properties
        context.created_at = datetime.fromisoformat(data["created_at"])
        context.last_updated = datetime.fromisoformat(data["last_updated"])
        context.participants = data["participants"]
        context.shared_state = data["shared_state"]
        context.topic_history = data["topic_history"]
        context.action_log = data["action_log"]
        context.entity_resolution = data["entity_resolution"]
        context.user_preferences = data["user_preferences"]
        context.temporal_context = data["temporal_context"]
        context.semantic_memory = data["semantic_memory"]

        return context


def create_conversation_context(conversation_id: str, user_id: str) -> ConversationContext:
    """
    Factory function to create a new conversation context.

    Args:
        conversation_id: The ID of the conversation
        user_id: The ID of the user

    Returns:
        ConversationContext instance
    """
    return ConversationContext(conversation_id, user_id)