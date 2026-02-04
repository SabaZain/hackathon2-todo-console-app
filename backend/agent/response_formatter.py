"""
Response Formatter for Todo AI Chatbot Agent.

This module formats responses for the todo chatbot, drawing inspiration
from .claude/agents/response-formatter-agent.md
"""

from typing import Dict, Any, List, Union
from enum import Enum


class ResponseStyle(Enum):
    """Enumeration of possible response styles."""
    CONCISE = "concise"
    DETAILED = "detailed"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    HELPFUL = "helpful"


class ResponseFormatter:
    """Formats responses for the todo chatbot according to specified styles and requirements."""

    def __init__(self, style: ResponseStyle = ResponseStyle.HELPFUL):
        """
        Initialize the response formatter.

        Args:
            style: The default response style to use
        """
        self.style = style

    def format_response(self, content: Union[str, Dict[str, Any]], **kwargs) -> str:
        """
        Format a response according to the specified style and content.

        Args:
            content: The content to format (string or dict with structured data)
            **kwargs: Additional formatting options

        Returns:
            Formatted response string
        """
        if isinstance(content, dict):
            return self._format_structured_response(content, **kwargs)
        else:
            return self._format_simple_response(content, **kwargs)

    def _format_simple_response(self, content: str, **kwargs) -> str:
        """
        Format a simple text response.

        Args:
            content: The text content to format
            **kwargs: Additional formatting options

        Returns:
            Formatted response string
        """
        # Apply basic formatting based on style
        if self.style == ResponseStyle.CONCISE:
            return self._apply_concise_formatting(content)
        elif self.style == ResponseStyle.DETAILED:
            return self._apply_detailed_formatting(content)
        elif self.style == ResponseStyle.FRIENDLY:
            return self._apply_friendly_formatting(content)
        elif self.style == ResponseStyle.FORMAL:
            return self._apply_formal_formatting(content)
        else:  # HELPFUL (default)
            return self._apply_helpful_formatting(content)

    def _format_structured_response(self, content: Dict[str, Any], **kwargs) -> str:
        """
        Format a structured response from a dictionary.

        Args:
            content: Dictionary containing structured response data
            **kwargs: Additional formatting options

        Returns:
            Formatted response string
        """
        response_parts = []

        # Add title if present
        if "title" in content:
            response_parts.append(f"## {content['title']}")

        # Add main message
        if "message" in content:
            response_parts.append(content["message"])

        # Add list of items if present
        if "items" in content and isinstance(content["items"], list):
            response_parts.append("")
            for i, item in enumerate(content["items"], 1):
                if isinstance(item, dict):
                    # Format as key-value pairs
                    item_parts = []
                    for key, value in item.items():
                        item_parts.append(f"- {key}: {value}")
                    response_parts.extend(item_parts)
                else:
                    response_parts.append(f"{i}. {item}")

        # Add suggestions if present
        if "suggestions" in content and isinstance(content["suggestions"], list):
            response_parts.append("")
            response_parts.append("**Suggestions:**")
            for suggestion in content["suggestions"]:
                response_parts.append(f"- {suggestion}")

        # Join all parts with appropriate spacing
        return "\n".join(response_parts)

    def format_task_list_response(self, tasks: List[Dict[str, Any]], filter_type: str = "all") -> str:
        """
        Format a response containing a list of tasks.

        Args:
            tasks: List of task dictionaries
            filter_type: Type of filter applied ("all", "pending", "completed")

        Returns:
            Formatted response string with task list
        """
        if not tasks:
            if filter_type == "pending":
                return "You don't have any pending tasks right now."
            elif filter_type == "completed":
                return "You haven't completed any tasks yet."
            else:
                return "You don't have any tasks on your list."

        response_parts = [f"Here are your {filter_type} tasks:"]
        response_parts.append("")  # Empty line for spacing

        for i, task in enumerate(tasks, 1):
            status_marker = "✓" if task.get("completed", False) else "○"
            task_line = f"{status_marker} {i}. {task.get('description', 'Unnamed task')}"

            # Add due date if available
            if task.get("due_date"):
                task_line += f" (Due: {task['due_date']})"

            # Add priority if available
            if task.get("priority"):
                task_line += f" [Priority: {task['priority']}]"

            response_parts.append(task_line)

        return "\n".join(response_parts)

    def format_task_operation_response(self, operation: str, task_details: Dict[str, Any]) -> str:
        """
        Format a response for a task operation (create, update, complete, delete).

        Args:
            operation: The operation performed
            task_details: Details about the task involved

        Returns:
            Formatted response string
        """
        if operation == "create":
            desc = task_details.get("description", "unnamed task")
            response = f"I've added '{desc}' to your task list."

            if task_details.get("due_date"):
                response += f" It's due on {task_details['due_date']}."
            if task_details.get("priority"):
                response += f" Priority set to {task_details['priority']}."

            return response

        elif operation == "update":
            desc = task_details.get("description", "the task")
            response = f"I've updated '{desc}'."

            changes = []
            if task_details.get("due_date"):
                changes.append(f"due date to {task_details['due_date']}")
            if task_details.get("priority"):
                changes.append(f"priority to {task_details['priority']}")
            if task_details.get("completed") is True:
                changes.append("marked as completed")

            if changes:
                response += f" Set {', '.join(changes)}."

            return response

        elif operation == "complete":
            desc = task_details.get("description", "the task")
            return f"I've marked '{desc}' as completed. Great job!"

        elif operation == "delete":
            desc = task_details.get("description", "the task")
            return f"I've removed '{desc}' from your task list."

        return "Task operation completed."

    def _apply_concise_formatting(self, content: str) -> str:
        """Apply concise formatting to the content."""
        # Remove extra whitespace and keep it simple
        return " ".join(content.split())

    def _apply_detailed_formatting(self, content: str) -> str:
        """Apply detailed formatting to the content."""
        # Add more descriptive elements
        return f"Details: {content}"

    def _apply_friendly_formatting(self, content: str) -> str:
        """Apply friendly formatting to the content."""
        # Add friendly elements
        friendly_prefixes = ["Hey there! ", "Hi! ", "Hello! "]
        return f"{friendly_prefixes[0]}{content}"

    def _apply_formal_formatting(self, content: str) -> str:
        """Apply formal formatting to the content."""
        # Make it more formal
        return f"Notification: {content.capitalize()}"

    def _apply_helpful_formatting(self, content: str) -> str:
        """Apply helpful formatting to the content."""
        # Add helpful elements
        return f"{content} Is there anything else I can help you with?"

    def set_style(self, style: ResponseStyle):
        """
        Change the response formatting style.

        Args:
            style: The new response style to use
        """
        self.style = style

    def format_error_response(self, error_message: str, user_friendly: bool = True) -> str:
        """
        Format an error response in a user-friendly way.

        Args:
            error_message: The raw error message
            user_friendly: Whether to format as user-friendly message

        Returns:
            Formatted error response
        """
        if user_friendly:
            return "I'm sorry, but I encountered an issue processing your request. Could you please try rephrasing or ask me to do something else?"
        else:
            return f"Error: {error_message}"


def get_response_formatter(style: ResponseStyle = ResponseStyle.HELPFUL) -> ResponseFormatter:
    """
    Get an instance of the response formatter.

    Args:
        style: The response style to use

    Returns:
        ResponseFormatter instance
    """
    return ResponseFormatter(style)