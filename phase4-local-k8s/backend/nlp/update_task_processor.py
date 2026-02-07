"""
Update Task Processor for Todo AI Chatbot

This module processes natural language commands for updating tasks.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class UpdateTaskProcessor:
    """Processes natural language commands for updating tasks."""

    def __init__(self):
        """Initialize the update task processor."""
        self.patterns = self._define_patterns()

    def _define_patterns(self) -> Dict[str, str]:
        """
        Define patterns for identifying update task commands.

        Returns:
            Dictionary of regex patterns for different update task variations
        """
        return {
            'update_task_by_id': r'\b(update|change|modify|edit|adjust|revise|alter)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this|it)\s*(?P<task_id>\d+)?\s*(with|to|and)\s+(?P<updates>[^.!?]+)',
            'update_task_description': r'\b(update|change|modify|edit|adjust|revise|alter)\s+(?P<action>[^.!?]+?)\s+(to|with)\s+(?P<new_description>[^.!?]+)',
            'change_task_detail': r'\b(change|update|modify|edit|adjust|revise|alter)\s+(the\s+)?(description|details?|info|information|title|name|text)\s+(of|for)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)?\s*(?P<task_id>\d+)?\s*(to|with)\s*(?P<new_value>[^.!?]+)',
            'update_task_property': r'\b(update|change|modify|edit|adjust|revise|alter)\s+(the\s+)?(due date|priority|status|category|assignee|time|estimate)\s+(of|for)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)?\s*(?P<task_id>\d+)?\s*(to|with)\s*(?P<new_value>[^.!?]+)',
            'update_task_simple': r'\b(update|change|modify|edit|adjust|revise|alter)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)\s*(?P<task_id>\d+)?\s+(?P<updates>[^.!?]+)',
            'change_task': r'\b(change|update|modify|edit|adjust|revise|alter)\s+(?P<task_ref>task|todo|to-do|item)\s+(#|\d+|the|that|this)?\s*(?P<task_id>\d+)?\s+(?P<action>[^.!?]+)',
            'set_task_property': r'\b(set|make|assign|put)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)?\s*(?P<task_id>\d+)?\s+(?P<property>\w+)\s+(to|as)\s+(?P<value>[^.!?]+)',
            'update_specific_field': r'\b(make|set|change|update)\s+(the\s+)?(?P<field>description|title|due date|priority|status|category)\s+(of|for)\s+(task|todo|to-do|item)\s+(#|\d+|the|that|this)?\s*(?P<task_id>\d+)?\s+(to|as)\s+(?P<new_value>[^.!?]+)'
        }

    def process(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Process a user input to extract task update information.

        Args:
            user_input: The user's natural language command

        Returns:
            Dictionary containing update parameters, or None if not an update task command
        """
        user_input = user_input.strip()

        # Check if this is an update task command
        if not self._is_update_task_command(user_input):
            return None

        # Extract update parameters
        update_params = self._extract_update_params(user_input)

        # Normalize the update parameters
        normalized_params = self._normalize_params(update_params)

        return normalized_params

    def _is_update_task_command(self, user_input: str) -> bool:
        """
        Check if the user input is an update task command.

        Args:
            user_input: The user's input

        Returns:
            Boolean indicating if this is an update task command
        """
        lower_input = user_input.lower()

        # Check against update task patterns
        update_keywords = ['update', 'change', 'modify', 'edit', 'adjust', 'revise', 'alter', 'set', 'make']

        # At least one update keyword should be present
        has_update_keyword = any(keyword in lower_input for keyword in update_keywords)

        # And it should refer to a task
        has_task_reference = any(word in lower_input for word in ['task', 'todo', 'to-do', 'item'])

        return has_update_keyword and has_task_reference

    def _extract_update_params(self, user_input: str) -> Dict[str, Any]:
        """
        Extract update parameters from user input.

        Args:
            user_input: The user's input

        Returns:
            Dictionary containing extracted update parameters
        """
        lower_input = user_input.lower()
        params = {
            'task_id': None,
            'updates': {},
            'field_updates': {},
            'raw_updates': user_input
        }

        # Try to extract task ID
        id_match = re.search(r'#(\d+)|task\s+(\d+)|number\s+(\d+)', lower_input)
        if id_match:
            params['task_id'] = id_match.group(1) or id_match.group(2) or id_match.group(3)

        # Extract updates based on different patterns
        # Check for specific field updates
        property_patterns = [
            (r'due date.*?(to|as)\s*(?P<value>[^.!?]+)', 'due_date'),
            (r'priority.*?(to|as)\s*(?P<value>high|low|medium|urgent|normal)', 'priority'),
            (r'status.*?(to|as)\s*(?P<value>pending|completed|active|inactive)', 'status'),
            (r'category.*?(to|as)\s*(?P<value>[^.!?]+)', 'category'),
            (r'description.*?(to|as)\s*(?P<value>[^.!?]+)', 'description'),
            (r'title.*?(to|as)\s*(?P<value>[^.!?]+)', 'title'),
            (r'name.*?(to|as)\s*(?P<value>[^.!?]+)', 'name')
        ]

        for pattern, field in property_patterns:
            match = re.search(pattern, lower_input)
            if match:
                value = match.group('value').strip()
                params['field_updates'][field] = self._normalize_field_value(field, value)

        # Extract general updates
        update_match = re.search(r'(update|change|modify|edit|adjust|revise|alter).*?(to|with|and)\s+(?P<update>[^.!?]+)', lower_input)
        if update_match:
            general_update = update_match.group('update').strip()
            if general_update:
                params['updates']['general'] = general_update

        # Extract task description updates
        desc_match = re.search(r'(description|title|name|text)\s+(to|as)\s+(?P<desc>[^.!?]+)', lower_input)
        if desc_match:
            params['updates']['description'] = desc_match.group('desc').strip()

        # Extract due date updates
        date_match = re.search(r'(due date|deadline|by|before|on)\s+(?P<date>[^.!?]+)', lower_input)
        if date_match:
            parsed_date = self._parse_date(date_match.group('date'))
            if parsed_date:
                params['updates']['due_date'] = parsed_date

        # Extract priority updates
        priority_match = re.search(r'(priority|importance)\s+(to|as)\s+(?P<priority>high|low|medium|urgent|normal)', lower_input)
        if priority_match:
            params['updates']['priority'] = self._normalize_priority(priority_match.group('priority'))

        # Extract status updates
        status_match = re.search(r'(status|state)\s+(to|as)\s+(?P<status>pending|completed|active|inactive|done|todo)', lower_input)
        if status_match:
            params['updates']['status'] = self._normalize_status(status_match.group('status'))

        return params

    def _parse_date(self, date_string: str) -> Optional[str]:
        """
        Parse a date string and convert to ISO format.

        Args:
            date_string: The date string to parse

        Returns:
            ISO formatted date string, or None if parsing fails
        """
        date_string = date_string.strip().lower()

        # Handle relative dates
        if 'today' in date_string:
            return datetime.now().date().isoformat()
        elif 'tomorrow' in date_string:
            return (datetime.now() + timedelta(days=1)).date().isoformat()
        elif 'yesterday' in date_string:
            return (datetime.now() - timedelta(days=1)).date().isoformat()

        # Handle 'next week', 'next month', etc.
        if 'next week' in date_string:
            return (datetime.now() + timedelta(weeks=1)).date().isoformat()
        elif 'next month' in date_string:
            return (datetime.now() + timedelta(days=30)).date().isoformat()
        elif 'next year' in date_string:
            return (datetime.now() + timedelta(days=365)).date().isoformat()

        # Handle day names
        days = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        for day, day_num in days.items():
            if day in date_string:
                today = datetime.now()
                days_ahead = day_num - today.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                return (today + timedelta(days_ahead)).date().isoformat()

        # Handle numerical dates (MM/DD, DD/MM, etc.)
        date_patterns = [
            r'(\d{1,2})[/\-](\d{1,2})(?:[/\-](\d{2,4}))?',  # MM/DD or MM/DD/YYYY
        ]

        for pattern in date_patterns:
            match = re.search(pattern, date_string)
            if match:
                month, day, year = match.groups()
                if year is None:
                    # Assume current year
                    year = str(datetime.now().year)
                elif len(year) == 2:
                    # Two-digit year, assume 20xx
                    year = '20' + year

                try:
                    parsed_date = datetime(int(year), int(month), int(day))
                    return parsed_date.date().isoformat()
                except ValueError:
                    continue

        # If no pattern matches, return None
        return None

    def _normalize_field_value(self, field: str, value: str) -> str:
        """
        Normalize a field value based on the field type.

        Args:
            field: The field name
            value: The raw value

        Returns:
            Normalized field value
        """
        value = value.strip().lower()

        if field == 'priority':
            return self._normalize_priority(value)
        elif field == 'status':
            return self._normalize_status(value)
        elif field == 'due_date':
            return self._parse_date(value) or value
        else:
            return value

    def _normalize_priority(self, priority: str) -> str:
        """
        Normalize priority value.

        Args:
            priority: Raw priority value

        Returns:
            Normalized priority (high, medium, low)
        """
        priority = priority.lower().strip()

        if priority in ['high', 'urgent', 'important', 'critical', 'top']:
            return 'high'
        elif priority in ['low', 'minor', 'trivial', 'bottom']:
            return 'low'
        else:
            return 'medium'

    def _normalize_status(self, status: str) -> str:
        """
        Normalize status value.

        Args:
            status: Raw status value

        Returns:
            Normalized status (pending, completed)
        """
        status = status.lower().strip()

        if status in ['completed', 'done', 'finished', 'closed', 'complete']:
            return 'completed'
        else:
            return 'pending'

    def _normalize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the update parameters.

        Args:
            params: Dictionary containing raw update parameters

        Returns:
            Normalized update parameters
        """
        normalized = {
            'task_id': params.get('task_id'),
            'updates': {**params.get('updates', {}), **params.get('field_updates', {})},
            'raw_command': params.get('raw_updates'),
            'processed_at': datetime.utcnow().isoformat()
        }

        # Combine updates and field_updates
        all_updates = {**params.get('updates', {}), **params.get('field_updates', {})}
        normalized['updates'] = all_updates

        return normalized

    def get_default_params(self) -> Dict[str, Any]:
        """
        Get default update parameters.

        Returns:
            Dictionary with default parameters for updating tasks
        """
        return {
            'task_id': None,
            'updates': {},
            'raw_command': '',
            'processed_at': datetime.utcnow().isoformat()
        }


def get_update_task_processor() -> UpdateTaskProcessor:
    """
    Get an instance of the update task processor.

    Returns:
        UpdateTaskProcessor instance
    """
    return UpdateTaskProcessor()