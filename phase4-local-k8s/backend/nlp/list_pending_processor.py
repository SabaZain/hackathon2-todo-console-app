"""
List Pending Task Processor for Todo AI Chatbot

This module processes natural language commands for listing pending tasks.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


class ListPendingTaskProcessor:
    """Processes natural language commands for listing pending tasks."""

    def __init__(self):
        """Initialize the list pending task processor."""
        self.patterns = self._define_patterns()

    def _define_patterns(self) -> Dict[str, str]:
        """
        Define patterns for identifying list pending task commands.

        Returns:
            Dictionary of regex patterns for different list pending task variations
        """
        return {
            'list_pending_tasks': r'\b(list|show|display|view|see|give me|tell me)\s+(pending|incomplete|todo|to-do|open|active|not done|not completed)\s+(tasks|todos|to-dos|items|my\s+tasks|my\s+todos)\b',
            'list_not_done': r'\b(list|show|display|view)\s+(what\s+i\s+haven\'t\s+done|what\'s\s+not\s+done|what\'s\s+left|what\s+remains|what\'s\s+left\s+to\s+do)\b',
            'what_is_left': r'\b(what\'s\s+(left|remaining|to\s+do|yet\s+to\s+be\s+done|outstanding)|what\s+do\s+i\s+still\s+have\s+to\s+do)\b',
            'pending_basic': r'\b(pending|incomplete|todo|to-do|open|active|not done|not completed)\s+(tasks|todos|to-dos|items)\b',
            'show_pending': r'\b(show|list|display|view)\s+(my\s+)?(pending|incomplete|todo|to-do|open|active|not done|not completed)\s+(tasks|todos|to-dos|items)\b',
            'what_do_i_need_to_do': r'\b(what\s+(do\s+i\s+need\s+to\s+do|should\s+i\s+do|am\s+i\s+supposed\s+to\s+do|need\s+to\s+complete))\b',
            'unfinished_tasks': r'\b(list|show|display|view)\s+(unfinished|uncompleted|incomplete|pending|remaining)\s+(tasks|todos|to-dos|items)\b',
            'incomplete_tasks': r'\b(incomplete|uncompleted|unfinished|pending|todo)\s+(tasks|todos|to-dos|items)\s+(that|which)\s+(are|still)\s+(left|remaining|to\s+do)\b'
        }

    def process(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Process a user input to extract pending task listing information.

        Args:
            user_input: The user's natural language command

        Returns:
            Dictionary containing listing parameters for pending tasks, or None if not a list pending command
        """
        user_input = user_input.strip()

        # Check if this is a list pending task command
        if not self._is_list_pending_command(user_input):
            return None

        # Extract listing parameters
        list_params = self._extract_list_params(user_input)

        # Normalize the listing parameters
        normalized_params = self._normalize_params(list_params)

        return normalized_params

    def _is_list_pending_command(self, user_input: str) -> bool:
        """
        Check if the user input is a list pending task command.

        Args:
            user_input: The user's input

        Returns:
            Boolean indicating if this is a list pending task command
        """
        lower_input = user_input.lower()

        # Check against list pending task patterns
        for pattern in [
            self.patterns['list_pending_tasks'],
            self.patterns['list_not_done'],
            self.patterns['what_is_left'],
            self.patterns['pending_basic'],
            self.patterns['show_pending'],
            self.patterns['what_do_i_need_to_do'],
            self.patterns['unfinished_tasks'],
            self.patterns['incomplete_tasks']
        ]:
            if re.search(pattern, lower_input):
                return True

        return False

    def _extract_list_params(self, user_input: str) -> Dict[str, Any]:
        """
        Extract listing parameters from user input for pending tasks.

        Args:
            user_input: The user's input

        Returns:
            Dictionary containing extracted listing parameters
        """
        lower_input = user_input.lower()
        params = {
            'filter': 'pending',  # Specifically for pending tasks
            'sort_by': 'created',  # Default sort
            'sort_order': 'asc',  # Default sort order
            'limit': None,  # No limit by default
            'category': None,
            'priority': None,
            'search_term': None,
            'include_overdue': True  # Include overdue tasks in pending
        }

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
        category_match = re.search(r'(work|personal|shopping|home|school|urgent|chores)\s+(pending|incomplete|todo)\s+(tasks|todos|to-dos)', lower_input)
        if category_match:
            params['category'] = category_match.group(1)

        # Check for priority
        if 'high priority' in lower_input or 'high-priority' in lower_input:
            params['priority'] = 'high'
        elif 'low priority' in lower_input or 'low-priority' in lower_input:
            params['priority'] = 'low'

        # Check for overdue-specific requests
        if 'overdue' in lower_input:
            params['include_overdue'] = True
            params['filter'] = 'overdue'

        # Extract any search terms
        search_terms = []
        exclude_terms = [
            'list', 'show', 'display', 'view', 'pending', 'incomplete', 'todo', 'to-do',
            'open', 'active', 'not', 'done', 'completed', 'tasks', 'todos', 'to-dos',
            'items', 'my', 'the', 'what', 'i', 'have', 'to', 'do', 'should', 'need',
            'am', 'supposed', 'left', 'remaining', 'unfinished', 'uncompleted'
        ]

        words = re.findall(r'\b\w+\b', lower_input)
        for word in words:
            if word not in exclude_terms and len(word) > 2:
                search_terms.append(word)

        if search_terms:
            params['search_term'] = ' '.join(search_terms)

        return params

    def _normalize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the listing parameters for pending tasks.

        Args:
            params: Dictionary containing raw listing parameters

        Returns:
            Normalized listing parameters
        """
        normalized = {
            'filter': params.get('filter', 'pending'),
            'sort_by': params.get('sort_by', 'created'),
            'sort_order': params.get('sort_order', 'asc'),
            'limit': params.get('limit'),
            'category': params.get('category'),
            'priority': params.get('priority'),
            'search_term': params.get('search_term'),
            'include_overdue': params.get('include_overdue', True),
            'processed_at': datetime.utcnow().isoformat()
        }

        return normalized

    def get_default_params(self) -> Dict[str, Any]:
        """
        Get default listing parameters for pending tasks.

        Returns:
            Dictionary with default parameters for listing pending tasks
        """
        return {
            'filter': 'pending',
            'sort_by': 'created',
            'sort_order': 'asc',
            'limit': None,
            'category': None,
            'priority': None,
            'search_term': None,
            'include_overdue': True,
            'processed_at': datetime.utcnow().isoformat()
        }

    def get_pending_filters(self) -> Dict[str, str]:
        """
        Get specific filters for pending tasks.

        Returns:
            Dictionary of filter descriptions for pending tasks
        """
        return {
            'all_pending': 'All tasks that are not yet completed',
            'overdue': 'Tasks that are past their due date',
            'due_soon': 'Tasks with due dates approaching',
            'high_priority_pending': 'High priority tasks that are not completed',
            'low_priority_pending': 'Low priority tasks that are not completed'
        }


def get_list_pending_processor() -> ListPendingTaskProcessor:
    """
    Get an instance of the list pending task processor.

    Returns:
        ListPendingTaskProcessor instance
    """
    return ListPendingTaskProcessor()