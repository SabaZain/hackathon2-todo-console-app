"""
Intent Mapper for Todo AI Chatbot Agent.

This module maps recognized intents to appropriate MCP tools for execution.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from .intent_recognizer import Intent


class IntentMapper:
    """Maps intents to appropriate MCP tool calls."""

    def __init__(self):
        """Initialize the intent mapper with intent-to-tool mappings."""
        self.intent_to_tool = {
            Intent.ADD_TASK: "create_task",
            Intent.LIST_TASKS: "list_tasks",
            Intent.LIST_PENDING_TASKS: "list_tasks",
            Intent.LIST_COMPLETED_TASKS: "list_tasks",
            Intent.UPDATE_TASK: "update_task",
            Intent.COMPLETE_TASK: "complete_task",
            Intent.DELETE_TASK: "delete_task"
        }

    def map_intent_to_tool(self, intent: Intent, entities: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Map an intent and entities to an appropriate MCP tool call.

        Args:
            intent: The recognized intent
            entities: Extracted entities from the user input

        Returns:
            Dictionary containing the tool name and parameters, or None if no mapping exists
        """
        if intent not in self.intent_to_tool:
            return None

        tool_name = self.intent_to_tool[intent]
        tool_params = self._build_tool_parameters(intent, entities)

        return {
            "tool_name": tool_name,
            "parameters": tool_params
        }

    def _build_tool_parameters(self, intent: Intent, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build appropriate parameters for the MCP tool based on intent and entities.

        Args:
            intent: The recognized intent
            entities: Extracted entities from the user input

        Returns:
            Dictionary of parameters for the MCP tool
        """
        params = {}

        if intent == Intent.ADD_TASK:
            params["description"] = entities.get("task_description", "")
            if "due_date" in entities:
                params["due_date"] = entities["due_date"]
            if "priority" in entities:
                params["priority"] = entities["priority"]

        elif intent == Intent.LIST_TASKS:
            params["filter"] = "all"

        elif intent == Intent.LIST_PENDING_TASKS:
            params["filter"] = "pending"

        elif intent == Intent.LIST_COMPLETED_TASKS:
            params["filter"] = "completed"

        elif intent == Intent.UPDATE_TASK:
            params["task_id"] = entities.get("task_id", "")
            if "task_description" in entities:
                params["description"] = entities["task_description"]
            if "due_date" in entities:
                params["due_date"] = entities["due_date"]
            if "priority" in entities:
                params["priority"] = entities["priority"]

        elif intent == Intent.COMPLETE_TASK:
            params["task_id"] = entities.get("task_id", "")

        elif intent == Intent.DELETE_TASK:
            params["task_id"] = entities.get("task_id", "")

        # Add user context if available
        if "user_id" in entities:
            params["user_id"] = entities["user_id"]

        return params

    def get_available_intents(self) -> List[Intent]:
        """
        Get a list of all supported intents.

        Returns:
            List of supported Intent values
        """
        return list(self.intent_to_tool.keys())


def get_intent_mapper() -> IntentMapper:
    """
    Get an instance of the intent mapper.

    Returns:
        IntentMapper instance
    """
    return IntentMapper()


def map_intent_to_response_template(intent: Intent) -> str:
    """
    Get an appropriate response template for the given intent.

    Args:
        intent: The intent to get a response template for

    Returns:
        String template for the response
    """
    templates = {
        Intent.ADD_TASK: "I've added the task '{task_description}' to your list.",
        Intent.LIST_TASKS: "Here are your tasks: {task_list}",
        Intent.LIST_PENDING_TASKS: "Here are your pending tasks: {task_list}",
        Intent.LIST_COMPLETED_TASKS: "Here are your completed tasks: {task_list}",
        Intent.UPDATE_TASK: "I've updated the task as requested.",
        Intent.COMPLETE_TASK: "I've marked the task as completed.",
        Intent.DELETE_TASK: "I've removed the task from your list.",
        Intent.UNKNOWN: "I'm not sure how to handle that request. Could you please rephrase?"
    }

    return templates.get(intent, templates[Intent.UNKNOWN])