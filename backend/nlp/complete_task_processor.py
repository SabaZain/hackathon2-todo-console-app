"""
Complete Task Processor for Todo AI Chatbot

This module processes natural language commands for completing tasks.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


class CompleteTaskProcessor:
    """Processes natural language commands for completing tasks."""

    def __init__(self):
        """Initialize the complete task processor."""
        self.patterns = self._define_patterns()

    def _define_patterns(self) -> Dict[str, str]:
        """
        Define patterns for identifying complete task commands.

        Returns:
            Dictionary of regex patterns for different complete task variations
        """
        return {
            'complete_task_by_id': r'\b(mark|set|complete|finish|done|close|accomplish|achieve|tick off|check off)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)\s*(?P<task_id>\d+)?\s*(as)?\s*(completed?|done|finished|closed)\b',
            'complete_task_by_description': r'\b(mark|set|complete|finish|done|close|accomplish|achieve)\s+(?P<description>[^.!?]+?)\s+(as\s+)?(completed?|done|finished|closed)\b',
            'complete_task_simple': r'\b(done|completed?|finished|complete|finish|tick|check)\s+(#|\d+|the|that|this)\s*(?P<task_id>\d+)?\s*(task|todo|to-do|item)\b',
            'task_is_done': r'\b(the\s+)?(?P<description>[^.!?]+?)\s+(is\s+)?(done|completed?|finished)\b',
            'i_did_task': r'\b(i\s+(did|completed?|finished|have\s+done|have\s+completed|have\s+finished))\s+(?P<description>[^.!?]+)\b',
            'i_finished_task': r'\b(i\s+(just\s+)?(finished|completed?|done))\s+(?P<description>[^.!?]+)\b',
            'completed_task': r'\b(i\s+)?(just\s+)?(completed?|finished|done)\s+(?P<description>[^.!?]+)\b',
            'tick_off_task': r'\b(tick|check)\s+(off|as\s+done)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)\s*(?P<task_id>\d+)?\s*(?P<description>[^.!?]*)',
            'set_task_complete': r'\b(set|mark|make)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)\s*(?P<task_id>\d+)?\s+(as\s+)?(completed?|done|finished|closed)\b'
        }

    def process(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Process a user input to extract task completion information.

        Args:
            user_input: The user's natural language command

        Returns:
            Dictionary containing completion parameters, or None if not a complete task command
        """
        user_input = user_input.strip()

        # Check if this is a complete task command
        if not self._is_complete_task_command(user_input):
            return None

        # Extract completion parameters
        completion_params = self._extract_completion_params(user_input)

        # Normalize the completion parameters
        normalized_params = self._normalize_params(completion_params)

        return normalized_params

    def _is_complete_task_command(self, user_input: str) -> bool:
        """
        Check if the user input is a complete task command.

        Args:
            user_input: The user's input

        Returns:
            Boolean indicating if this is a complete task command
        """
        lower_input = user_input.lower()

        # Check for completion keywords
        completion_keywords = [
            'mark', 'set', 'complete', 'finish', 'done', 'close', 'accomplish',
            'achieve', 'tick', 'check', 'completed', 'finished', 'done with',
            'just finished', 'just completed', 'have completed', 'have finished',
            'is done', 'was done', 'got done', 'tick off', 'check off'
        ]

        # Check for task references
        task_keywords = ['task', 'todo', 'to-do', 'item', 'it', 'that']

        # Check if it has both completion and task keywords
        has_completion_word = any(keyword in lower_input for keyword in completion_keywords)

        # Check if it refers to a specific task or has a task-like description
        has_task_ref = any(word in lower_input for word in task_keywords)
        has_task_structure = bool(re.search(r'\b(i\s+(did|completed?|finished|have\s+done|have\s+completed|have\s+finished))\s+', lower_input))

        return has_completion_word and (has_task_ref or has_task_structure)

    def _extract_completion_params(self, user_input: str) -> Dict[str, Any]:
        """
        Extract completion parameters from user input.

        Args:
            user_input: The user's input

        Returns:
            Dictionary containing extracted completion parameters
        """
        lower_input = user_input.lower()
        params = {
            'task_id': None,
            'description': None,
            'completion_method': 'unknown',
            'raw_command': user_input
        }

        # Try to extract task ID
        id_match = re.search(r'#(\d+)|task\s+(\d+)|number\s+(\d+)', lower_input)
        if id_match:
            params['task_id'] = id_match.group(1) or id_match.group(2) or id_match.group(3)

        # Try to extract description
        # Check for explicit description patterns
        desc_match = re.search(r'(?:i\s+(?:did|completed?|finished|have\s+done|have\s+completed|have\s+finished))\s+(?P<desc>[^.!?]+)', lower_input)
        if desc_match:
            params['description'] = desc_match.group('desc').strip()
            params['completion_method'] = 'i_did'

        # Check for "task is done" pattern
        is_done_match = re.search(r'(?:the\s+)?(?P<desc>[^.!?]+?)\s+(?:is\s+)?(?:done|completed?|finished)', lower_input)
        if is_done_match and not params['description']:
            params['description'] = is_done_match.group('desc').strip()
            params['completion_method'] = 'is_done'

        # Check for "mark task as complete" pattern
        mark_complete_match = re.search(r'(?:mark|set|complete|finish|done|close)\s+(?P<desc>[^.!?]+?)\s+(?:as\s+)?(?:completed?|done|finished)', lower_input)
        if mark_complete_match and not params['description']:
            params['description'] = mark_complete_match.group('desc').strip()
            params['completion_method'] = 'mark_complete'

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
        Normalize the completion parameters.

        Args:
            params: Dictionary containing raw completion parameters

        Returns:
            Normalized completion parameters
        """
        normalized = {
            'task_id': params.get('task_id'),
            'description': params.get('description'),
            'completion_method': params.get('completion_method', 'unknown'),
            'raw_command': params.get('raw_command'),
            'completed_at': datetime.utcnow().isoformat(),
            'status': 'completed'
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
        Get default completion parameters.

        Returns:
            Dictionary with default parameters for completing tasks
        """
        return {
            'task_id': None,
            'description': None,
            'completion_method': 'unknown',
            'raw_command': '',
            'completed_at': datetime.utcnow().isoformat(),
            'status': 'completed'
        }

    def extract_task_identifier(self, user_input: str) -> Optional[str]:
        """
        Extract a task identifier (ID or description) from user input.

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
        params = self._extract_completion_params(user_input)
        return params.get('description')


def get_complete_task_processor() -> CompleteTaskProcessor:
    """
    Get an instance of the complete task processor.

    Returns:
        CompleteTaskProcessor instance
    """
    return CompleteTaskProcessor()