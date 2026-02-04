"""
Multi-Step Handler for Todo AI Chatbot Agent.

This module handles multi-step operations that require multiple interactions
or complex task creation processes.
"""

from typing import Dict, Any, Optional, List
from .intent_recognizer import Intent
from .conversation_context import ConversationContext


class MultiStepHandler:
    """Handles multi-step operations that require more than one interaction."""

    def __init__(self):
        """Initialize the multi-step handler."""
        self.active_operations = {}  # Maps conversation_id to operation state

    def start_multi_step_operation(self, conversation_id: str, intent: Intent, initial_params: Dict[str, Any]):
        """
        Start a multi-step operation for a conversation.

        Args:
            conversation_id: The ID of the conversation
            intent: The initial intent that started the multi-step operation
            initial_params: Initial parameters gathered so far
        """
        operation_state = {
            "intent": intent,
            "current_step": 0,
            "total_steps": self._get_total_steps(intent),
            "params": initial_params,
            "required_params": self._get_required_params(intent),
            "collected_params": list(initial_params.keys())
        }

        self.active_operations[conversation_id] = operation_state

    def continue_multi_step_operation(self, conversation_id: str, user_input: str) -> Dict[str, Any]:
        """
        Continue a multi-step operation with user input.

        Args:
            conversation_id: The ID of the conversation
            user_input: The user's input for the current step

        Returns:
            Dictionary containing operation status and next steps
        """
        if conversation_id not in self.active_operations:
            return {
                "completed": False,
                "needs_more_info": False,
                "response": "No active multi-step operation found for this conversation."
            }

        operation_state = self.active_operations[conversation_id]

        # Determine what parameter to collect based on current step
        missing_params = [param for param in operation_state["required_params"]
                         if param not in operation_state["collected_params"]]

        if missing_params:
            param_to_collect = missing_params[0]

            # Try to extract the needed parameter from user input
            extracted_param = self._extract_param_from_input(param_to_collect, user_input)

            if extracted_param is not None:
                operation_state["params"][param_to_collect] = extracted_param
                operation_state["collected_params"].append(param_to_collect)

                # Check if all required parameters are now collected
                if all(p in operation_state["collected_params"] for p in operation_state["required_params"]):
                    # Operation is complete
                    del self.active_operations[conversation_id]
                    return {
                        "completed": True,
                        "params": operation_state["params"],
                        "response": self._generate_completion_response(operation_state["intent"])
                    }
                else:
                    # Need more parameters
                    next_missing = [p for p in operation_state["required_params"]
                                   if p not in operation_state["collected_params"]]
                    return {
                        "completed": False,
                        "needs_more_info": True,
                        "request_param": next_missing[0],
                        "response": self._generate_request_for_param(next_missing[0])
                    }
            else:
                # Could not extract the needed parameter, ask again
                return {
                    "completed": False,
                    "needs_more_info": True,
                    "request_param": param_to_collect,
                    "response": self._generate_request_for_param(param_to_collect)
                }
        else:
            # All parameters collected, operation complete
            del self.active_operations[conversation_id]
            return {
                "completed": True,
                "params": operation_state["params"],
                "response": self._generate_completion_response(operation_state["intent"])
            }

    def cancel_multi_step_operation(self, conversation_id: str):
        """
        Cancel an active multi-step operation.

        Args:
            conversation_id: The ID of the conversation
        """
        if conversation_id in self.active_operations:
            del self.active_operations[conversation_id]

    def has_active_operation(self, conversation_id: str) -> bool:
        """
        Check if there's an active multi-step operation for a conversation.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            Boolean indicating if an operation is active
        """
        return conversation_id in self.active_operations

    def _get_total_steps(self, intent: Intent) -> int:
        """
        Get the total number of steps required for an intent.

        Args:
            intent: The intent to check

        Returns:
            Number of steps required
        """
        step_counts = {
            Intent.ADD_TASK: 3,  # Description, due date, priority
            Intent.UPDATE_TASK: 2,  # Task ID, update details
            Intent.UNKNOWN: 1
        }
        return step_counts.get(intent, 1)

    def _get_required_params(self, intent: Intent) -> List[str]:
        """
        Get the required parameters for an intent.

        Args:
            intent: The intent to check

        Returns:
            List of required parameter names
        """
        required_params = {
            Intent.ADD_TASK: ["description"],
            Intent.UPDATE_TASK: ["task_id"],
            Intent.COMPLETE_TASK: ["task_id"],
            Intent.DELETE_TASK: ["task_id"]
        }
        return required_params.get(intent, [])

    def _extract_param_from_input(self, param_name: str, user_input: str) -> Optional[Any]:
        """
        Extract a specific parameter from user input.

        Args:
            param_name: Name of the parameter to extract
            user_input: The user's input text

        Returns:
            Extracted parameter value or None if not found
        """
        import re

        if param_name == "description":
            # For description, return the input as-is (or extract relevant part)
            return user_input.strip()
        elif param_name == "due_date":
            # Look for date patterns in the input
            date_pattern = r"\b(\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|\d{4}-\d{2}-\d{2}|today|tomorrow|yesterday|tonight|(?:next|this)\s+\w+)\b"
            match = re.search(date_pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1)
        elif param_name == "priority":
            # Look for priority keywords
            priority_pattern = r"\b(high|medium|low|urgent|important)\b"
            match = re.search(priority_pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1)
        elif param_name == "task_id":
            # Look for numeric task IDs
            id_pattern = r"\b(\d+|[A-Za-z0-9-]+)\b"
            match = re.search(id_pattern, user_input)
            if match:
                return match.group(1)

        return None

    def _generate_request_for_param(self, param_name: str) -> str:
        """
        Generate a request message for a specific parameter.

        Args:
            param_name: Name of the parameter to request

        Returns:
            Request message string
        """
        requests = {
            "description": "Could you please provide the task description?",
            "due_date": "When is this task due? (e.g., today, tomorrow, or a specific date)",
            "priority": "What priority should I set for this task? (high, medium, low)",
            "task_id": "Which task would you like to update? Please provide the task ID or name."
        }
        return requests.get(param_name, f"What is the {param_name} for this task?")

    def _generate_completion_response(self, intent: Intent) -> str:
        """
        Generate a completion response for an intent.

        Args:
            intent: The intent that was completed

        Returns:
            Completion response string
        """
        responses = {
            Intent.ADD_TASK: "I've added the task with all the details you provided.",
            Intent.UPDATE_TASK: "I've updated the task with the new information.",
            Intent.COMPLETE_TASK: "I've marked the task as completed.",
            Intent.DELETE_TASK: "I've removed the task from your list."
        }
        return responses.get(intent, "Operation completed successfully.")


def get_multi_step_handler() -> MultiStepHandler:
    """
    Get an instance of the multi-step handler.

    Returns:
        MultiStepHandler instance
    """
    return MultiStepHandler()