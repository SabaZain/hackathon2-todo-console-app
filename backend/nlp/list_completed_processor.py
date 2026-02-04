"""
List Completed Task Processor for Todo AI Chatbot

This module processes natural language commands for listing completed tasks.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


class ListCompletedTaskProcessor:
    """Processes natural language commands for listing completed tasks."""

    def __init__(self):
        """Initialize the list completed task processor."""
        self.patterns = self._define_patterns()

    def _define_patterns(self) -> Dict[str, str]:
        """
        Define patterns for identifying list completed task commands.

        Returns:
            Dictionary of regex patterns for different list completed task variations
        """
        return {
            'list_completed_tasks': r'\b(list|show|display|view|see|give me|tell me)\s+(completed|done|finished|closed|completed\s+tasks|done\s+tasks|finished\s+tasks)\s+(tasks|todos|to-dos|items|my\s+tasks|my\s+todos)\b',
            'list_done_tasks': r'\b(list|show|display|view)\s+(done|completed|finished|closed)\s+(tasks|todos|to-dos|items)\b',
            'what_have_i_done': r'\b(what\s+(have\s+i\s+done|did\s+i\s+do|have\s+i\s+completed|did\s+i\s+finish))\b',
            'completed_basic': r'\b(completed|done|finished|closed)\s+(tasks|todos|to-dos|items)\b',
            'show_completed': r'\b(show|list|display|view)\s+(my\s+)?(completed|done|finished|closed)\s+(tasks|todos|to-dos|items)\b',
            'view_completed': r'\b(view|check|browse|look at)\s+(completed|done|finished|closed)\s+(tasks|todos|to-dos|items)\b',
            'completed_tasks_history': r'\b(my\s+)?(completed|done|finished|closed)\s+(tasks|todos|to-dos|items)\s+(history|record|log|list)\b',
            'what_i_ve_finished': r'\b(what\s+i\'ve\s+(done|completed|finished|closed)|what\s+have\s+i\s+(done|completed|finished|closed))\b'
        }

    def process(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Process a user input to extract completed task listing information.

        Args:
            user_input: The user's natural language command

        Returns:
            Dictionary containing listing parameters for completed tasks, or None if not a list completed command
        """
        user_input = user_input.strip()

        # Check if this is a list completed task command
        if not self._is_list_completed_command(user_input):
            return None

        # Extract listing parameters
        list_params = self._extract_list_params(user_input)

        # Normalize the listing parameters
        normalized_params = self._normalize_params(list_params)

        return normalized_params

    def _is_list_completed_command(self, user_input: str) -> bool:
        """
        Check if the user input is a list completed task command.

        Args:
            user_input: The user's input

        Returns:
            Boolean indicating if this is a list completed task command
        """
        lower_input = user_input.lower()

        # Check against list completed task patterns
        for pattern in [
            self.patterns['list_completed_tasks'],
            self.patterns['list_done_tasks'],
            self.patterns['what_have_i_done'],
            self.patterns['completed_basic'],
            self.patterns['show_completed'],
            self.patterns['view_completed'],
            self.patterns['completed_tasks_history'],
            self.patterns['what_i_ve_finished']
        ]:
            if re.search(pattern, lower_input):
                return True

        return False

    def _extract_list_params(self, user_input: str) -> Dict[str, Any]:
        """
        Extract listing parameters from user input for completed tasks.

        Args:
            user_input: The user's input

        Returns:
            Dictionary containing extracted listing parameters
        """
        lower_input = user_input.lower()
        params = {
            'filter': 'completed',  # Specifically for completed tasks
            'sort_by': 'completed_date',  # Default sort for completed tasks
            'sort_order': 'desc',  # Default to most recent first
            'limit': None,  # No limit by default
            'category': None,
            'priority': None,
            'search_term': None,
            'date_range': None  # For filtering by completion date range
        }

        # Check for sorting preferences
        if 'sort by' in lower_input or 'order by' in lower_input:
            if 'date' in lower_input or 'time' in lower_input or 'completed' in lower_input:
                params['sort_by'] = 'completed_date'
            elif 'original' in lower_input or 'creation' in lower_input or 'created' in lower_input:
                params['sort_by'] = 'created'
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
        category_match = re.search(r'(work|personal|shopping|home|school|urgent|chores)\s+(completed|done|finished)\s+(tasks|todos|to-dos)', lower_input)
        if category_match:
            params['category'] = category_match.group(1)

        # Check for priority
        if 'high priority' in lower_input or 'high-priority' in lower_input:
            params['priority'] = 'high'
        elif 'low priority' in lower_input or 'low-priority' in lower_input:
            params['priority'] = 'low'

        # Check for date ranges
        if 'today' in lower_input:
            params['date_range'] = 'today'
        elif 'yesterday' in lower_input:
            params['date_range'] = 'yesterday'
        elif 'this week' in lower_input:
            params['date_range'] = 'this_week'
        elif 'this month' in lower_input:
            params['date_range'] = 'this_month'
        elif 'this year' in lower_input:
            params['date_range'] = 'this_year'

        # Extract any search terms
        search_terms = []
        exclude_terms = [
            'list', 'show', 'display', 'view', 'completed', 'done', 'finished', 'closed',
            'tasks', 'todos', 'to-dos', 'items', 'my', 'the', 'what', 'i', 'have',
            'to', 'do', 'did', 'completed', 'finished', 'history', 'record', 'log',
            'view', 'check', 'browse', 'look', 'at', 'by', 'in', 'on', 'since', 'ago'
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
        Normalize the listing parameters for completed tasks.

        Args:
            params: Dictionary containing raw listing parameters

        Returns:
            Normalized listing parameters
        """
        normalized = {
            'filter': params.get('filter', 'completed'),
            'sort_by': params.get('sort_by', 'completed_date'),
            'sort_order': params.get('sort_order', 'desc'),
            'limit': params.get('limit'),
            'category': params.get('category'),
            'priority': params.get('priority'),
            'search_term': params.get('search_term'),
            'date_range': params.get('date_range'),
            'processed_at': datetime.utcnow().isoformat()
        }

        return normalized

    def get_default_params(self) -> Dict[str, Any]:
        """
        Get default listing parameters for completed tasks.

        Returns:
            Dictionary with default parameters for listing completed tasks
        """
        return {
            'filter': 'completed',
            'sort_by': 'completed_date',
            'sort_order': 'desc',
            'limit': None,
            'category': None,
            'priority': None,
            'search_term': None,
            'date_range': None,
            'processed_at': datetime.utcnow().isoformat()
        }

    def get_completed_filters(self) -> Dict[str, str]:
        """
        Get specific filters for completed tasks.

        Returns:
            Dictionary of filter descriptions for completed tasks
        """
        return {
            'all_completed': 'All tasks that have been completed',
            'completed_today': 'Tasks completed today',
            'completed_yesterday': 'Tasks completed yesterday',
            'completed_this_week': 'Tasks completed in the last 7 days',
            'completed_this_month': 'Tasks completed in the current month',
            'high_priority_completed': 'High priority tasks that have been completed',
            'low_priority_completed': 'Low priority tasks that have been completed'
        }


def get_list_completed_processor() -> ListCompletedTaskProcessor:
    """
    Get an instance of the list completed task processor.

    Returns:
        ListCompletedTaskProcessor instance
    """
    return ListCompletedTaskProcessor()