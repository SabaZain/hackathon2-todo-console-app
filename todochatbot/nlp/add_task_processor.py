"""
Add Task Processor for Todo AI Chatbot

This module processes natural language commands for adding tasks.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid


class AddTaskProcessor:
    """Processes natural language commands for adding tasks."""

    def __init__(self):
        """Initialize the add task processor."""
        self.patterns = self._define_patterns()

    def _define_patterns(self) -> Dict[str, str]:
        """
        Define patterns for identifying add task commands.

        Returns:
            Dictionary of regex patterns for different add task variations
        """
        return {
            'add_task_basic': r'\b(add|create|make|new|put in|set up|establish)\s+(a\s+)?(task|todo|to-do|item)\b',
            'add_task_with_description': r'\b(add|create|make|new|put in|set up|establish)\s+(a\s+)?(task|todo|to-do|item)\s+(to|for|that|which|will)\s+(?P<description>[^.!?]+)',
            'simple_add': r'\b(need to|want to|must|should|going to|will)\s+(?P<action>[^.!?]+)',
            'remember_to': r'\bremember\s+to\s+(?P<action>[^.!?]+)',
            'add_imperative': r'\b(add|create|make|set|put)\s+(?P<action>[^.!?]+)\b',
            'task_with_due_date': r'\b(add|create|make)\s+(?P<action>[^.!?]+?)\s+(by|before|on|due)\s+(?P<due_date>[^.!?]+)',
            'task_with_priority': r'\b(add|create|make)\s+(?P<priority>high|low|medium|urgent|important)\s+(priority\s+)?(?P<action>[^.!?]+)',
            'task_with_date_and_priority': r'\b(add|create|make)\s+(?P<priority>high|low|medium|urgent|important)\s+(priority\s+)?(?P<action>[^.!?]+?)\s+(by|before|on|due)\s+(?P<due_date>[^.!?]+)'
        }

    def process(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Process a user input to extract task creation information.

        Args:
            user_input: The user's natural language command

        Returns:
            Dictionary containing task information, or None if not an add task command
        """
        user_input = user_input.strip()

        # Check if this is an add task command
        if not self._is_add_task_command(user_input):
            return None

        # Extract task information
        task_info = self._extract_task_info(user_input)

        if not task_info:
            return None

        # Normalize the task information
        normalized_task = self._normalize_task(task_info)

        return normalized_task

    def _is_add_task_command(self, user_input: str) -> bool:
        """
        Check if the user input is an add task command.

        Args:
            user_input: The user's input

        Returns:
            Boolean indicating if this is an add task command
        """
        lower_input = user_input.lower()

        # Check against basic add task patterns
        for pattern in [
            self.patterns['add_task_basic'],
            self.patterns['add_task_with_description'],
            self.patterns['simple_add'],
            self.patterns['remember_to'],
            self.patterns['add_imperative']
        ]:
            if re.search(pattern, lower_input):
                return True

        return False

    def _extract_task_info(self, user_input: str) -> Dict[str, Any]:
        """
        Extract task information from user input.

        Args:
            user_input: The user's input

        Returns:
            Dictionary containing extracted task information
        """
        lower_input = user_input.lower()
        task_info = {
            'description': '',
            'due_date': None,
            'priority': 'medium',
            'category': 'general',
            'tags': []
        }

        # Try to extract information using different patterns
        # Check for task with date and priority first (most specific)
        match = re.search(self.patterns['task_with_date_and_priority'], lower_input)
        if match:
            task_info['description'] = match.group('action').strip()
            task_info['priority'] = match.group('priority')
            task_info['due_date'] = self._parse_date(match.group('due_date'))
            return task_info

        # Check for task with due date
        match = re.search(self.patterns['task_with_due_date'], lower_input)
        if match:
            task_info['description'] = match.group('action').strip()
            task_info['due_date'] = self._parse_date(match.group('due_date'))
            return task_info

        # Check for task with priority
        match = re.search(self.patterns['task_with_priority'], lower_input)
        if match:
            task_info['description'] = match.group('action').strip()
            task_info['priority'] = match.group('priority')
            return task_info

        # Check for basic task with description
        match = re.search(self.patterns['add_task_with_description'], lower_input)
        if match:
            description = match.group('description').strip()
            if description:
                task_info['description'] = description
                return task_info

        # Check for simple add pattern
        match = re.search(self.patterns['simple_add'], lower_input)
        if match:
            action = match.group('action').strip()
            if action:
                task_info['description'] = action
                return task_info

        # Check for remember to pattern
        match = re.search(self.patterns['remember_to'], lower_input)
        if match:
            action = match.group('action').strip()
            if action:
                task_info['description'] = action
                return task_info

        # Check for imperative pattern
        match = re.search(self.patterns['add_imperative'], lower_input)
        if match:
            action = match.group('action').strip()
            if action:
                task_info['description'] = action
                return task_info

        # If no specific pattern matched, try to extract a basic description
        # Remove common add words and extract the rest
        cleaned_input = re.sub(r'\b(add|create|make|new|put in|set up|establish|need to|want to|must|should|going to|will|remember to)\s*', '', lower_input)
        cleaned_input = re.sub(r'\b(task|todo|to-do|item)\s*', '', cleaned_input)
        cleaned_input = cleaned_input.strip(' .,!?')

        if cleaned_input:
            task_info['description'] = cleaned_input
            return task_info

        return {}

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
        # This is a simplified version - in a real implementation, you'd want more robust date parsing
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

    def _normalize_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the task information.

        Args:
            task_info: Dictionary containing raw task information

        Returns:
            Normalized task information
        """
        normalized = {
            'id': str(uuid.uuid4()),
            'description': task_info.get('description', '').strip(),
            'due_date': task_info.get('due_date'),
            'priority': self._normalize_priority(task_info.get('priority', 'medium')),
            'category': task_info.get('category', 'general'),
            'tags': task_info.get('tags', []),
            'completed': False,
            'created_at': datetime.utcnow().isoformat()
        }

        # Ensure description is not empty
        if not normalized['description']:
            normalized['description'] = 'Untitled task'

        return normalized

    def _normalize_priority(self, priority: str) -> str:
        """
        Normalize priority value.

        Args:
            priority: Raw priority value

        Returns:
            Normalized priority (high, medium, low)
        """
        priority = priority.lower().strip()

        if priority in ['high', 'urgent', 'important', 'critical']:
            return 'high'
        elif priority in ['low', 'minor', 'trivial']:
            return 'low'
        else:
            return 'medium'


def get_add_task_processor() -> AddTaskProcessor:
    """
    Get an instance of the add task processor.

    Returns:
        AddTaskProcessor instance
    """
    return AddTaskProcessor()