"""
Reference Resolver for Todo AI Chatbot Agent.

This module handles follow-up questions and references to previous statements
in the conversation.
"""

from typing import Dict, Any, List, Optional
from .history_manager import HistoryManager
import re


class ReferenceResolver:
    """Resolves references to previous statements and entities in conversations."""

    def __init__(self, history_manager: HistoryManager):
        """
        Initialize the reference resolver.

        Args:
            history_manager: Instance of HistoryManager to access conversation history
        """
        self.history_manager = history_manager

    def resolve_references(self, user_id: str, conversation_id: str, message: str) -> Dict[str, Any]:
        """
        Resolve references in the user's message to previous statements or entities.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The user's current message

        Returns:
            Dictionary containing resolved references and enriched context
        """
        resolved_context = {
            "original_message": message,
            "resolved_references": {},
            "enriched_message": message,
            "referenced_entities": [],
            "previous_topic": None
        }

        # Get recent conversation history
        recent_messages = self.history_manager.get_messages_for_context(
            user_id, conversation_id, limit=5
        )

        # Resolve pronoun references (it, that, this, etc.)
        resolved_context = self._resolve_pronouns(recent_messages, resolved_context)

        # Resolve temporal references (before, after, yesterday, etc.)
        resolved_context = self._resolve_temporal_references(recent_messages, resolved_context)

        # Resolve task references (the task, that task, etc.)
        resolved_context = self._resolve_task_references(recent_messages, resolved_context)

        return resolved_context

    def _resolve_pronouns(self, recent_messages: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve pronoun references in the message to previous entities.

        Args:
            recent_messages: List of recent messages in the conversation
            context: Current resolution context

        Returns:
            Updated resolution context
        """
        message = context["enriched_message"].lower()
        pronoun_patterns = [
            (r'\b(it|that|this)\b', ['task', 'item', 'thing']),
            (r'\b(them|those)\b', ['tasks', 'items', 'things'])
        ]

        # Look for task-related entities in recent messages
        for msg in reversed(recent_messages):
            if msg["sender"] == "ai":
                # Look for task IDs or descriptions in AI responses
                task_id_match = re.search(r'task\s+(\d+|[A-Za-z0-9-]+)', msg["message"])
                if task_id_match:
                    context["resolved_references"]["recent_task_id"] = task_id_match.group(1)

                task_desc_match = re.search(r'task\s+"([^"]+)"', msg["message"])
                if task_desc_match:
                    context["resolved_references"]["recent_task_desc"] = task_desc_match.group(1)

        # Replace pronouns in message if we have context
        if "recent_task_id" in context["resolved_references"]:
            message = re.sub(r'\b(it|that|this)\b', f'task {context["resolved_references"]["recent_task_id"]}', message)
            context["enriched_message"] = message

        return context

    def _resolve_temporal_references(self, recent_messages: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve temporal references like 'before', 'after', 'yesterday', etc.

        Args:
            recent_messages: List of recent messages in the conversation
            context: Current resolution context

        Returns:
            Updated resolution context
        """
        message = context["enriched_message"]

        # Look for temporal context in recent messages
        for msg in reversed(recent_messages):
            # Check for dates mentioned in previous messages
            date_match = re.search(r'\b(\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|today|tomorrow|yesterday|(?:next|this)\s+\w+)\b',
                                 msg["message"], re.IGNORECASE)
            if date_match:
                context["resolved_references"]["recent_date"] = date_match.group(1)
                break

        return context

    def _resolve_task_references(self, recent_messages: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve references to tasks like 'the task', 'that task', etc.

        Args:
            recent_messages: List of recent messages in the conversation
            context: Current resolution context

        Returns:
            Updated resolution context
        """
        message = context["enriched_message"]

        # Look for specific task references
        task_reference_patterns = [
            r'the\s+task',
            r'that\s+task',
            r'previous\s+task',
            r'earlier\s+task'
        ]

        # Find recent task-related context
        for msg in reversed(recent_messages):
            # Look for task descriptions in previous messages
            task_desc_match = re.search(r'(?:add|create|update|complete|delete)\s+(?:a\s+|the\s+|an\s+)?(.+?)(?:\.|$|,)',
                                      msg["message"], re.IGNORECASE)
            if task_desc_match:
                context["resolved_references"]["recent_task"] = task_desc_match.group(1).strip()
                break

        # Look for task IDs in previous messages
        for msg in reversed(recent_messages):
            task_id_match = re.search(r'task\s+(\d+|[A-Za-z0-9-]+)', msg["message"], re.IGNORECASE)
            if task_id_match:
                context["resolved_references"]["recent_task_id"] = task_id_match.group(1)
                break

        return context

    def infer_intent_from_context(self, user_id: str, conversation_id: str, message: str) -> Optional[str]:
        """
        Infer the likely intent based on conversation context and references.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The user's current message

        Returns:
            Inferred intent or None if unclear
        """
        recent_messages = self.history_manager.get_messages_for_context(
            user_id, conversation_id, limit=3
        )

        # Analyze the conversation flow to infer intent
        if len(recent_messages) >= 2:
            last_ai_msg = None
            for msg in reversed(recent_messages):
                if msg["sender"] == "ai":
                    last_ai_msg = msg
                    break

            if last_ai_msg:
                # If the last AI message was about adding a task and user says "yes", likely confirming
                if "added" in last_ai_msg["message"] and message.lower() in ["yes", "ok", "sure", "confirm"]:
                    return "confirm_addition"

                # If the last AI asked for more info and user is providing it
                if "could you" in last_ai_msg["message"] or "what is" in last_ai_msg["message"]:
                    return "provide_details"

        return None

    def extract_referenced_entities(self, user_id: str, conversation_id: str, message: str) -> List[Dict[str, Any]]:
        """
        Extract entities referenced in the message that relate to previous conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The user's current message

        Returns:
            List of referenced entities with context
        """
        entities = []
        resolved = self.resolve_references(user_id, conversation_id, message)

        if "recent_task_id" in resolved["resolved_references"]:
            entities.append({
                "type": "task_id",
                "value": resolved["resolved_references"]["recent_task_id"],
                "confidence": 0.9
            })

        if "recent_task_desc" in resolved["resolved_references"]:
            entities.append({
                "type": "task_description",
                "value": resolved["resolved_references"]["recent_task_desc"],
                "confidence": 0.8
            })

        return entities

    def get_conversation_topic(self, user_id: str, conversation_id: str) -> Optional[str]:
        """
        Determine the current topic of conversation based on recent exchanges.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation

        Returns:
            Current conversation topic or None
        """
        recent_messages = self.history_manager.get_messages_for_context(
            user_id, conversation_id, limit=5
        )

        # Analyze recent messages to determine topic
        topics = []
        for msg in recent_messages:
            if "task" in msg["message"].lower() or "todo" in msg["message"].lower():
                topics.append("task_management")
            elif "complete" in msg["message"].lower() or "done" in msg["message"].lower():
                topics.append("task_completion")
            elif "add" in msg["message"].lower() or "create" in msg["message"].lower():
                topics.append("task_creation")

        # Return the most frequent topic
        if topics:
            # Simple majority vote - in practice, this could be more sophisticated
            return max(set(topics), key=topics.count)

        return None


def get_reference_resolver(history_manager: HistoryManager) -> ReferenceResolver:
    """
    Get an instance of the reference resolver.

    Args:
        history_manager: Instance of HistoryManager to use

    Returns:
        ReferenceResolver instance
    """
    return ReferenceResolver(history_manager)