"""
Response Formatter for Todo AI Chatbot

This module applies response formatting using skills.
"""

from typing import Dict, Any, List, Union
import re
from datetime import datetime


class ResponseFormatter:
    """Applies response formatting using skills."""

    def __init__(self):
        """Initialize the response formatter."""
        self.formatters = {
            'task_creation': self._format_task_creation_response,
            'task_list': self._format_task_list_response,
            'task_update': self._format_task_update_response,
            'task_completion': self._format_task_completion_response,
            'task_deletion': self._format_task_deletion_response,
            'error': self._format_error_response,
            'confirmation': self._format_confirmation_response,
            'greeting': self._format_greeting_response,
            'help': self._format_help_response
        }

    def format_response(self, response_type: str, data: Dict[str, Any], user_preferences: Dict[str, Any] = None) -> str:
        """
        Format a response based on its type.

        Args:
            response_type: The type of response to format
            data: The data to format
            user_preferences: Optional user formatting preferences

        Returns:
            Formatted response string
        """
        if response_type in self.formatters:
            return self.formatters[response_type](data, user_preferences or {})
        else:
            # Default formatting
            return str(data)

    def _format_task_creation_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a task creation response.

        Args:
            data: Task creation data
            user_preferences: User formatting preferences

        Returns:
            Formatted task creation response
        """
        task = data.get('task', data)

        if not task:
            return "Task was created successfully."

        description = task.get('description', 'unnamed task')
        due_date = task.get('due_date')
        priority = task.get('priority', 'medium')
        task_id = task.get('id', 'unknown')

        # Format based on user preferences
        if user_preferences.get('concise', False):
            return f"✓ Added: {description}"
        elif user_preferences.get('detailed', False):
            details = [f"Task '{description}' has been created with ID {task_id}."]
            if due_date:
                details.append(f"Due date: {due_date}.")
            if priority and priority != 'medium':
                details.append(f"Priority: {priority}.")
            return " ".join(details)
        else:
            response = f"Task '{description}' has been added."
            if due_date:
                response += f" It's due on {due_date}."
            if priority and priority != 'medium':
                response += f" Priority set to {priority}."
            return response

    def _format_task_list_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a task list response.

        Args:
            data: Task list data
            user_preferences: User formatting preferences

        Returns:
            Formatted task list response
        """
        tasks = data.get('tasks', [])
        filter_type = data.get('filter', 'all')

        if not tasks:
            filter_text = {
                'pending': 'pending',
                'completed': 'completed',
                'all': ''
            }.get(filter_type, '')

            if filter_text:
                return f"You have no {filter_text} tasks."
            else:
                return "You have no tasks."

        if user_preferences.get('concise', False):
            task_list = [f"{i+1}. {task.get('description', 'unnamed')}" for i, task in enumerate(tasks)]
            return f"Your tasks:\n" + "\n".join(task_list)
        elif user_preferences.get('detailed', False):
            task_details = []
            for i, task in enumerate(tasks):
                task_info = [
                    f"Task #{i+1}: {task.get('description', 'unnamed')}",
                    f"  ID: {task.get('id', 'N/A')}",
                    f"  Status: {task.get('status', 'N/A')}",
                    f"  Priority: {task.get('priority', 'N/A')}"
                ]
                if task.get('due_date'):
                    task_info.append(f"  Due: {task.get('due_date')}")
                task_details.append("\n".join(task_info))
            return "\n\n".join(task_details)
        else:
            task_list = []
            for i, task in enumerate(tasks):
                status_marker = "✓" if task.get('status') == 'completed' else "○"
                priority_marker = {
                    'high': '❗',
                    'low': '⬇️',
                    'medium': ''
                }.get(task.get('priority', 'medium'), '')

                task_desc = f"{status_marker}{priority_marker} {task.get('description', 'unnamed')}"
                if task.get('due_date'):
                    task_desc += f" (due {task['due_date']})"

                task_list.append(task_desc)

            filter_text = {
                'pending': 'pending',
                'completed': 'completed',
                'all': 'current'
            }.get(filter_type, 'current')

            return f"Here are your {filter_text} tasks:\n" + "\n".join([f"  {task}" for task in task_list])

    def _format_task_update_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a task update response.

        Args:
            data: Task update data
            user_preferences: User formatting preferences

        Returns:
            Formatted task update response
        """
        task = data.get('task', data)
        updated_fields = data.get('updated_fields', [])

        if not task:
            return "Task was updated successfully."

        description = task.get('description', 'unnamed task')
        task_id = task.get('id', 'unknown')

        if user_preferences.get('concise', False):
            if updated_fields:
                return f"✓ Updated: {description} ({', '.join(updated_fields)})"
            else:
                return f"✓ Updated: {description}"
        else:
            if updated_fields:
                return f"Task '{description}' (ID: {task_id}) has been updated with changes to: {', '.join(updated_fields)}."
            else:
                return f"Task '{description}' has been updated."

    def _format_task_completion_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a task completion response.

        Args:
            data: Task completion data
            user_preferences: User formatting preferences

        Returns:
            Formatted task completion response
        """
        task = data.get('task', data)

        if not task:
            return "Task was marked as completed."

        description = task.get('description', 'unnamed task')

        if user_preferences.get('concise', False):
            return f"✓ Completed: {description}"
        else:
            return f"Great job! Task '{description}' has been marked as completed."

    def _format_task_deletion_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a task deletion response.

        Args:
            data: Task deletion data
            user_preferences: User formatting preferences

        Returns:
            Formatted task deletion response
        """
        task_id = data.get('task_id', data.get('id', 'unknown'))
        description = data.get('description', 'unnamed task')

        if user_preferences.get('concise', False):
            return f"✓ Deleted task #{task_id}"
        else:
            return f"Task '{description}' (ID: {task_id}) has been deleted."

    def _format_error_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format an error response.

        Args:
            data: Error data
            user_preferences: User formatting preferences

        Returns:
            Formatted error response
        """
        error_code = data.get('code', 'UNKNOWN_ERROR')
        error_message = data.get('message', 'An unknown error occurred')
        suggestion = data.get('suggestion', 'Please try again.')

        if user_preferences.get('concise', False):
            return f"❌ Error: {error_message}"
        else:
            return f"Sorry, I encountered an issue: {error_message} (Code: {error_code}). {suggestion}"

    def _format_confirmation_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a confirmation response.

        Args:
            data: Confirmation data
            user_preferences: User formatting preferences

        Returns:
            Formatted confirmation response
        """
        action = data.get('action', 'completed')
        result = data.get('result', 'successfully')

        if user_preferences.get('concise', False):
            return f"✓ {action.title()} {result}"
        else:
            return f"Action '{action}' was {result}."

    def _format_greeting_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a greeting response.

        Args:
            data: Greeting data
            user_preferences: User formatting preferences

        Returns:
            Formatted greeting response
        """
        time_based = data.get('time_based', True)
        task_summary = data.get('task_summary', {})

        if time_based:
            current_hour = datetime.now().hour
            if current_hour < 12:
                greeting = "Good morning"
            elif current_hour < 17:
                greeting = "Good afternoon"
            else:
                greeting = "Good evening"
        else:
            greeting = "Hello"

        if task_summary:
            pending_count = task_summary.get('pending_count', 0)
            if pending_count > 0:
                task_text = f"You have {pending_count} pending task{'s' if pending_count != 1 else ''}."
                return f"{greeting}! {task_text} How can I help you today?"
            else:
                return f"{greeting}! You have no pending tasks. How can I help you?"
        else:
            return f"{greeting}! How can I help you today?"

    def _format_help_response(self, data: Dict[str, Any], user_preferences: Dict[str, Any]) -> str:
        """
        Format a help response.

        Args:
            data: Help data
            user_preferences: User formatting preferences

        Returns:
            Formatted help response
        """
        commands = data.get('commands', [
            "Add a task: 'Add a task to buy groceries'",
            "List tasks: 'Show me my tasks'",
            "Update task: 'Update task #1 to high priority'",
            "Complete task: 'Mark task #1 as done'",
            "Delete task: 'Delete task #1'"
        ])

        if user_preferences.get('concise', False):
            return "Commands: " + ", ".join(commands[:3]) + "..."
        else:
            help_text = "I can help you manage your tasks. Try these commands:\n"
            for cmd in commands:
                help_text += f"• {cmd}\n"
            help_text += "\nJust talk to me naturally!"
            return help_text

    def format_for_accessibility(self, response: str, accessibility_prefs: Dict[str, Any]) -> str:
        """
        Format a response for accessibility.

        Args:
            response: The response to format
            accessibility_prefs: Accessibility preferences

        Returns:
            Accessibility-enhanced response
        """
        # Increase contrast by emphasizing important information
        if accessibility_prefs.get('high_contrast', False):
            # Convert emphasis markers to more explicit text
            response = re.sub(r'\b([✗✓❗○⬇️])\b', r'[EMPHASIS: \1]', response)

        # Add more verbose descriptions if needed
        if accessibility_prefs.get('screen_reader_friendly', False):
            response = response.replace('✓', '(completed)').replace('✗', '(not completed)')
            response = response.replace('❗', '(high priority)').replace('⬇️', '(low priority)')

        return response

    def format_multilingual(self, response: str, target_language: str = 'en') -> str:
        """
        Format a response for multilingual support.

        Args:
            response: The response to format
            target_language: Target language code

        Returns:
            Language-appropriate response
        """
        # In a real implementation, this would translate the response
        # For now, we'll return the English response
        return response

    def format_for_channel(self, response: str, channel: str = 'web') -> str:
        """
        Format a response for a specific communication channel.

        Args:
            response: The response to format
            channel: The communication channel ('web', 'mobile', 'voice', etc.)

        Returns:
            Channel-appropriate response
        """
        if channel == 'voice':
            # Remove visual elements for voice interfaces
            response = re.sub(r'[✗✓❗○⬇️]', '', response)
            response = re.sub(r'\([^)]*\)', '', response)  # Remove parenthetical info
        elif channel == 'mobile':
            # Possibly shorten for mobile screens
            if len(response) > 200:
                sentences = response.split('. ')
                shortened = []
                char_count = 0
                for sentence in sentences:
                    if char_count + len(sentence) < 180:
                        shortened.append(sentence)
                        char_count += len(sentence) + 2
                    else:
                        break
                response = '. '.join(shortened) + '.' if shortened else response

        return response

    def add_rich_formatting(self, response: str, formatting_options: Dict[str, Any]) -> str:
        """
        Add rich formatting to a response.

        Args:
            response: The response to format
            formatting_options: Options for rich formatting

        Returns:
            Richly formatted response
        """
        if formatting_options.get('bold_keywords', False):
            # Make certain keywords bold (in markdown format)
            keywords = ['task', 'complete', 'add', 'delete', 'update']
            for keyword in keywords:
                response = re.sub(
                    r'\b(' + keyword + r')\b',
                    r'**\1**',
                    response,
                    flags=re.IGNORECASE
                )

        if formatting_options.get('highlight_values', False):
            # Highlight values like dates, numbers
            # Highlight dates
            response = re.sub(
                r'(\d{4}-\d{2}-\d{2})',
                r'*\1*',
                response
            )
            # Highlight task IDs
            response = re.sub(
                r'(?:#|task\s)(\d+)',
                r'*#\1*',
                response,
                flags=re.IGNORECASE
            )

        return response


def get_response_formatter() -> ResponseFormatter:
    """
    Get an instance of the response formatter.

    Returns:
        ResponseFormatter instance
    """
    return ResponseFormatter()


def format_task_creation_response(task_data: Dict[str, Any], user_prefs: Dict[str, Any] = None) -> str:
    """
    Convenience function to format task creation responses.

    Args:
        task_data: Task creation data
        user_prefs: Optional user preferences

    Returns:
        Formatted task creation response
    """
    formatter = get_response_formatter()
    return formatter.format_response('task_creation', task_data, user_prefs or {})


def format_task_list_response(task_list_data: Dict[str, Any], user_prefs: Dict[str, Any] = None) -> str:
    """
    Convenience function to format task list responses.

    Args:
        task_list_data: Task list data
        user_prefs: Optional user preferences

    Returns:
        Formatted task list response
    """
    formatter = get_response_formatter()
    return formatter.format_response('task_list', task_list_data, user_prefs or {})