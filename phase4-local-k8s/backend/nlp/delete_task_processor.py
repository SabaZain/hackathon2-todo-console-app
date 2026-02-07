"""
Delete Task Processor for Todo AI Chatbot

This module processes natural language commands for deleting tasks.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


class DeleteTaskProcessor:
    """Processes natural language commands for deleting tasks."""

    def __init__(self):
        """Initialize the delete task processor."""
        self.patterns = self._define_patterns()

    def _define_patterns(self) -> Dict[str, str]:
        """
        Define patterns for identifying delete task commands.

        Returns:
            Dictionary of regex patterns for different delete task variations
        """
        return {
            'delete_task_by_id': r'\b(remove|delete|erase|cancel|eliminate|purge|get rid of|dispose of)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)\s*(?P<task_id>\d+)?\b',
            'delete_task_by_description': r'\b(remove|delete|erase|cancel|eliminate|purge|get rid of|dispose of)\s+(?P<description>[^.!?]+?)\s+(task|todo|to-do|item)\b',
            'delete_simple': r'\b(delete|remove|erase|cancel|eliminate|purge)\s+(#|\d+|the|that|this)\s*(?P<task_id>\d+)?\s*(task|todo|to-do|item)\b',
            'remove_task': r'\b(remove|delete|erase|cancel|eliminate|purge|get rid of|dispose of)\s+(task|todo|to-do|item)\s+(?P<description>[^.!?]+)\b',
            'kill_task': r'\b(kill|destroy|obliterate|wipe out|scratch|drop|abort)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)?\s*(?P<task_id>\d+)?\s*(?P<description>[^.!?]*)',
            'toss_task': r'\b(toss|throw out|discard|bin|trash|dump)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)?\s*(?P<task_id>\d+)?\s*(?P<description>[^.!?]*)',
            'clear_task': r'\b(clear|clean up|remove|delete)\s+(?P<description>[^.!?]+?)\s+(from|off)\s+(my\s+)?(tasks?|todos?|to-dos?|list|board)\b',
            'delete_from_list': r'\b(delete|remove|erase)\s+(?P<description>[^.!?]+?)\s+(from|off)\s+(my\s+)?(tasks?|todos?|to-dos?|list|board)\b'
        }

    def process(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Process a user input to extract task deletion information.

        Args:
            user_input: The user's natural language command

        Returns:
            Dictionary containing deletion parameters, or None if not a delete task command
        """
        user_input = user_input.strip()

        # Check if this is a delete task command
        if not self._is_delete_task_command(user_input):
            return None

        # Extract deletion parameters
        deletion_params = self._extract_deletion_params(user_input)

        # Normalize the deletion parameters
        normalized_params = self._normalize_params(deletion_params)

        return normalized_params

    def _is_delete_task_command(self, user_input: str) -> bool:
        """
        Check if the user input is a delete task command.

        Args:
            user_input: The user's input

        Returns:
            Boolean indicating if this is a delete task command
        """
        lower_input = user_input.lower()

        # Check for deletion keywords
        deletion_keywords = [
            'remove', 'delete', 'erase', 'cancel', 'eliminate', 'purge',
            'get rid of', 'dispose of', 'kill', 'destroy', 'obliterate',
            'wipe out', 'scratch', 'drop', 'abort', 'toss', 'throw out',
            'discard', 'bin', 'trash', 'dump', 'clear', 'clean up'
        ]

        # Check for task references
        task_keywords = ['task', 'todo', 'to-do', 'item', 'list', 'board']

        # Check if it has deletion keywords
        has_deletion_word = any(keyword in lower_input for keyword in deletion_keywords)

        # Check if it refers to tasks in some way
        has_task_ref = any(word in lower_input for word in task_keywords)
        has_task_structure = bool(re.search(r'\b(from|off)\s+(my\s+)?(tasks?|todos?|to-dos?|list|board)\b', lower_input))

        return has_deletion_word and (has_task_ref or has_task_structure)

    def _extract_deletion_params(self, user_input: str) -> Dict[str, Any]:
        """
        Extract deletion parameters from user input.

        Args:
            user_input: The user's input

        Returns:
            Dictionary containing extracted deletion parameters
        """
        lower_input = user_input.lower()
        params = {
            'task_id': None,
            'description': None,
            'deletion_method': 'unknown',
            'raw_command': user_input
        }

        # Try to extract task ID
        id_match = re.search(r'#(\d+)|task\s+(\d+)|number\s+(\d+)', lower_input)
        if id_match:
            params['task_id'] = id_match.group(1) or id_match.group(2) or id_match.group(3)

        # Try to extract description
        # Check for explicit description patterns
        desc_match = re.search(r'(?:remove|delete|erase|cancel|eliminate|purge|get rid of|dispose of|kill|destroy|toss|throw out|discard|bin|trash|dump)\s+(?P<desc>[^.!?]+?)\s+(?:task|todo|to-do|item|from|off)', lower_input)
        if desc_match:
            desc = desc_match.group('desc').strip()
            if desc and not desc.endswith(' ') and not desc.startswith(' '):
                params['description'] = desc
                params['deletion_method'] = 'explicit_description'

        # Check for "delete from list" pattern
        from_list_match = re.search(r'(?:delete|remove|erase)\s+(?P<desc>[^.!?]+?)\s+(?:from|off)\s+(?:my\s+)?(?:tasks?|todos?|to-dos?|list|board)', lower_input)
        if from_list_match and not params['description']:
            params['description'] = from_list_match.group('desc').strip()
            params['deletion_method'] = 'from_list'

        # Check for "remove task by description" pattern
        remove_match = re.search(r'(?:remove|delete|erase|cancel)\s+(?P<desc>[^.!?]+?)\s+(?:task|todo|to-do|item)', lower_input)
        if remove_match and not params['description']:
            desc = remove_match.group('desc').strip()
            if len(desc) > 2:  # Avoid single letters or words
                params['description'] = desc
                params['deletion_method'] = 'remove_task'

        # If no description found but we have a task ID, create a placeholder
        if not params['description'] and params['task_id']:
            params['description'] = f'Task #{params["task_id"]}'

        # If no ID found but we have description, try to infer
        if not params['task_id'] and params['description']:
            # Look for any number near the description that might be an ID
            desc_pos = lower_input.find(params['description'].lower())
            if desc_pos != -1:
                # Look for numbers nearby
                nearby_text = lower_input[max(0, desc_pos-10):desc_pos+len(params['description'])+10]
                num_match = re.search(r'#?(\d+)', nearby_text)
                if num_match:
                    params['task_id'] = num_match.group(1)

        return params

    def _normalize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the deletion parameters.

        Args:
            params: Dictionary containing raw deletion parameters

        Returns:
            Normalized deletion parameters
        """
        normalized = {
            'task_id': params.get('task_id'),
            'description': params.get('description'),
            'deletion_method': params.get('deletion_method', 'unknown'),
            'raw_command': params.get('raw_command'),
            'deleted_at': datetime.utcnow().isoformat(),
            'status': 'deleted'
        }

        # Ensure description is not empty
        if not normalized['description']:
            if normalized['task_id']:
                normalized['description'] = f'Task #{normalized["task_id"]}'
            else:
                normalized['description'] = 'Unspecified task'

        return normalized

    def get_default_params(self) -> Dict[str, Any]:
        """
        Get default deletion parameters.

        Returns:
            Dictionary with default parameters for deleting tasks
        """
        return {
            'task_id': None,
            'description': None,
            'deletion_method': 'unknown',
            'raw_command': '',
            'deleted_at': datetime.utcnow().isoformat(),
            'status': 'deleted'
        }

    def extract_task_identifier(self, user_input: str) -> Optional[str]:
        """
        Extract a task identifier (ID or description) from user input for deletion.

        Args:
            user_input: The user's input

        Returns:
            Task identifier or None if not found
        """
        lower_input = user_input.lower()

        # Try to find a task ID first
        id_match = re.search(r'#(\d+)|task\s+(\d+)|number\s+(\d+)', lower_input)
        if id_match:
            return id_match.group(1) or id_match.group(2) or id_match.group(3)

        # If no ID found, return the extracted description
        params = self._extract_deletion_params(user_input)
        return params.get('description')

    def get_confirmation_needed(self) -> bool:
        """
        Determine if confirmation is needed for the deletion.

        Returns:
            Boolean indicating if confirmation is needed
        """
        # For safety, always return True to require confirmation
        return True


def get_delete_task_processor() -> DeleteTaskProcessor:
    """
    Get an instance of the delete task processor.

    Returns:
        DeleteTaskProcessor instance
    """
    return DeleteTaskProcessor()