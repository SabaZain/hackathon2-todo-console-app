"""
List Task Processor for Todo AI Chatbot

This module processes natural language commands for listing tasks.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


class ListTaskProcessor:
    """Processes natural language commands for listing tasks."""

    def __init__(self):
        """Initialize the list task processor."""
        self.patterns = self._define_patterns()

    def _define_patterns(self) -> Dict[str, str]:
        """
        Define patterns for identifying list task commands.

        Returns:
            Dictionary of regex patterns for different list task variations
        """
        return {
            'list_all_tasks': r'\b(list|show|display|view|see|give me|tell me|what are|what is)\s+(all\s+)?(the\s+)?(tasks|todos|to-dos|items|my\s+tasks|my\s+todos)\b',
            'list_tasks_basic': r'\b(tasks|todos|to-dos|items)\b',
            'show_my_tasks': r'\b(show|list|display|view)\s+(my\s+)?(tasks|todos|to-dos|items)\b',
            'what_do_i_have': r'\b(what\s+(do\s+i\s+have|should\s+i\s+do|am\s+i\s+supposed\s+to\s+do|need\s+to\s+do))\b',
            'what_are_my_tasks': r'\b(what\s+are\s+(my\s+)?(tasks|todos|to-dos|items))\b',
            'do_i_have_any': r'\b(do\s+i\s+have\s+(any|anything|some))\s+(tasks|todos|to-dos|items)\b',
            'list_with_filter': r'\b(list|show|display|view)\s+(all|completed|pending|incomplete|done|todo|to\s+do)\s+(tasks|todos|to-dos|items)',
            'view_tasks': r'\b(view|check|browse|look at)\s+(my\s+)?(tasks|todos|to-dos|items)\b'
        }

    def process(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Process a user input to extract task listing information.

        Args:
            user_input: The user's natural language command

        Returns:
            Dictionary containing listing parameters, or None if not a list task command
        """
        user_input = user_input.strip()

        # Check if this is a list task command
        if not self._is_list_task_command(user_input):
            return None

        # Extract listing parameters
        list_params = self._extract_list_params(user_input)

        # Normalize the listing parameters
        normalized_params = self._normalize_params(list_params)

        return normalized_params

    def _is_list_task_command(self, user_input: str) -> bool:
        """
        Check if the user input is a list task command.

        Args:
            user_input: The user's input

        Returns:
            Boolean indicating if this is a list task command
        """
        lower_input = user_input.lower()

        # Check against list task patterns
        for pattern in [
            self.patterns['list_all_tasks'],
            self.patterns['list_tasks_basic'],
            self.patterns['show_my_tasks'],
            self.patterns['what_do_i_have'],
            self.patterns['what_are_my_tasks'],
            self.patterns['do_i_have_any'],
            self.patterns['list_with_filter'],
            self.patterns['view_tasks']
        ]:
            if re.search(pattern, lower_input):
                return True

        return False

    def _extract_list_params(self, user_input: str) -> Dict[str, Any]:
        """
        Extract listing parameters from user input.

        Args:
            user_input: The user's input

        Returns:
            Dictionary containing extracted listing parameters
        """
        lower_input = user_input.lower()
        params = {
            'filter': 'all',  # Default to all tasks
            'sort_by': 'created',  # Default sort
            'sort_order': 'asc',  # Default sort order
            'limit': None,  # No limit by default
            'category': None,
            'priority': None,
            'search_term': None
        }

        # Check for specific filters
        if re.search(r'\b(completed|done|finished|closed)\s+(tasks|todos|to-dos|items?)\b', lower_input):
            params['filter'] = 'completed'
        elif re.search(r'\b(pending|incomplete|todo|to\s+do|not\s+done|open)\s+(tasks|todos|to-dos|items?)\b', lower_input):
            params['filter'] = 'pending'
        elif re.search(r'\ball\s+(tasks|todos|to-dos|items?)\b', lower_input):
            params['filter'] = 'all'
        elif re.search(r'\b(overdue|late)\s+(tasks|todos|to-dos|items?)\b', lower_input):
            params['filter'] = 'overdue'

        # Check for sorting preferences
        if 'sort by' in lower_input or 'order by' in lower_input:
            if 'date' in lower_input or 'time' in lower_input or 'created' in lower_input:
                params['sort_by'] = 'created'
            elif 'due' in lower_input or 'deadline' in lower_input:
                params['sort_by'] = 'due_date'
            elif 'priority' in lower_input or 'importance' in lower_input:
                params['sort_by'] = 'priority'
            elif 'alphabetical' in lower_input or 'name' in lower_input or 'title' in lower_input:
                params['sort_by'] = 'name'

        # Check for sort order
        if 'ascending' in lower_input or 'oldest first' in lower_input:
            params['sort_order'] = 'asc'
        elif 'descending' in lower_input or 'newest first' in lower_input or 'reverse' in lower_input:
            params['sort_order'] = 'desc'

        # Check for limits
        limit_match = re.search(r'(top|first|last|limit to)\s+(\d+)', lower_input)
        if limit_match:
            params['limit'] = int(limit_match.group(2))

        # Check for categories
        category_match = re.search(r'(work|personal|shopping|home|school|urgent|chores)\s+(tasks|todos|to-dos)', lower_input)
        if category_match:
            params['category'] = category_match.group(1)

        # Check for priority
        if 'high priority' in lower_input or 'high-priority' in lower_input:
            params['priority'] = 'high'
        elif 'low priority' in lower_input or 'low-priority' in lower_input:
            params['priority'] = 'low'

        # Extract any search terms
        search_terms = []
        exclude_terms = ['list', 'show', 'display', 'view', 'tasks', 'todos', 'to-dos', 'items', 'all', 'my', 'the']

        words = re.findall(r'\b\w+\b', lower_input)
        for word in words:
            if word not in exclude_terms and len(word) > 2:
                search_terms.append(word)

        if search_terms:
            params['search_term'] = ' '.join(search_terms)

        return params

    def _normalize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the listing parameters.

        Args:
            params: Dictionary containing raw listing parameters

        Returns:
            Normalized listing parameters
        """
        normalized = {
            'filter': params.get('filter', 'all'),
            'sort_by': params.get('sort_by', 'created'),
            'sort_order': params.get('sort_order', 'asc'),
            'limit': params.get('limit'),
            'category': params.get('category'),
            'priority': params.get('priority'),
            'search_term': params.get('search_term'),
            'processed_at': datetime.utcnow().isoformat()
        }

        return normalized

    def get_default_params(self) -> Dict[str, Any]:
        """
        Get default listing parameters.

        Returns:
            Dictionary with default parameters for listing tasks
        """
        return {
            'filter': 'all',
            'sort_by': 'created',
            'sort_order': 'asc',
            'limit': None,
            'category': None,
            'priority': None,
            'search_term': None,
            'processed_at': datetime.utcnow().isoformat()
        }


def get_list_task_processor() -> ListTaskProcessor:
    """
    Get an instance of the list task processor.

    Returns:
        ListTaskProcessor instance
    """
    return ListTaskProcessor()