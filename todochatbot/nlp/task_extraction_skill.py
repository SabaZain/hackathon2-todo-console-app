"""
Task Extraction Skill for Todo AI Chatbot

This module extracts task details (dates, priorities) from user messages
inspired by the task extraction skill from .claude/skills/task-extraction-skill.md
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class TaskExtractionSkill:
    """Extracts task details like dates, priorities, and other attributes from user messages."""

    def __init__(self):
        """Initialize the task extraction skill."""
        self.date_patterns = self._define_date_patterns()
        self.priority_patterns = self._define_priority_patterns()
        self.category_patterns = self._define_category_patterns()
        self.duration_patterns = self._define_duration_patterns()

    def _define_date_patterns(self) -> Dict[str, str]:
        """
        Define patterns for extracting dates from text.

        Returns:
            Dictionary of date-related regex patterns
        """
        return {
            'relative_dates': r'\b(today|tomorrow|yesterday|tonight|now)\b',
            'day_names': r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b',
            'day_abbreviations': r'\b(mon|tue|tues|wed|thu|thur|thurs|fri|sat|sun)\b',
            'absolute_dates': r'\b(\d{1,2}[\/\-]\d{1,2}(?:[\/\-]\d{2,4})?|\d{4}-\d{2}-\d{2})\b',
            'time_expressions': r'\b(at\s+)?(\d{1,2}(:\d{2})?\s*(am|pm|AM|PM)?)\b',
            'relative_time': r'\b(in\s+\d+\s+(minutes?|hours?|days?|weeks?|months?|years?))\b',
            'this_week': r'\b(this\s+(week|monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b',
            'next_week': r'\b(next\s+(week|monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b',
            'last_week': r'\b(last\s+(week|monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b'
        }

    def _define_priority_patterns(self) -> Dict[str, str]:
        """
        Define patterns for extracting priority levels.

        Returns:
            Dictionary of priority-related regex patterns
        """
        return {
            'high_priority': r'\b(highest|high|urgent|critical|immediate|asap|ASAP|top priority|top-priority|very important|vital|essential|crucial)\b',
            'medium_priority': r'\b(medium|normal|regular|standard|usual|typical|routine|average|moderate)\b',
            'low_priority': r'\b(low|lowest|low priority|low-priority|not urgent|non-urgent|when possible|whenever convenient|optional|nice to have)\b'
        }

    def _define_category_patterns(self) -> Dict[str, str]:
        """
        Define patterns for extracting task categories.

        Returns:
            Dictionary of category-related regex patterns
        """
        return {
            'work': r'\b(work|job|office|meeting|project|task|assignment|duty|responsibility|professional|career|business)\b',
            'personal': r'\b(personal|private|my own|home|family|me|myself|individual|own business)\b',
            'shopping': r'\b(shopping|buy|purchase|grocery|store|market|shop|retail|errand)\b',
            'health': r'\b(health|medical|doctor|appointment|exercise|fitness|wellness|hospital|clinic|medicine|medication)\b',
            'finance': r'\b(finance|financial|money|bank|bill|payment|tax|expense|budget|account|investment)\b',
            'education': r'\b(education|study|learning|school|college|university|course|homework|assignment|exam|test|research)\b',
            'leisure': r'\b(leisure|fun|entertainment|movie|game|play|relax|vacation|hobby|sport|outing)\b'
        }

    def _define_duration_patterns(self) -> Dict[str, str]:
        """
        Define patterns for extracting time durations.

        Returns:
            Dictionary of duration-related regex patterns
        """
        return {
            'minutes': r'\b(\d+)\s*(minutes?|mins?)\b',
            'hours': r'\b(\d+)\s*(hours?|hrs?)\b',
            'days': r'\b(\d+)\s*(days?)\b',
            'weeks': r'\b(\d+)\s*(weeks?)\b',
            'months': r'\b(\d+)\s*(months?)\b',
            'years': r'\b(\d+)\s*(years?)\b'
        }

    def extract_task_details(self, text: str) -> Dict[str, Any]:
        """
        Extract task details from a text message.

        Args:
            text: The text to extract details from

        Returns:
            Dictionary containing extracted task details
        """
        text_lower = text.lower()

        details = {
            'dates': self._extract_dates(text_lower),
            'priorities': self._extract_priorities(text_lower),
            'categories': self._extract_categories(text_lower),
            'durations': self._extract_durations(text_lower),
            'assigned_to': self._extract_assignments(text_lower),
            'tags': self._extract_tags(text_lower),
            'location': self._extract_location(text_lower),
            'recurrence': self._extract_recurrence(text_lower)
        }

        return details

    def _extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract date information from text.

        Args:
            text: The text to extract dates from

        Returns:
            List of dictionaries containing date information
        """
        dates = []

        # Relative dates
        relative_matches = re.finditer(self.date_patterns['relative_dates'], text)
        for match in relative_matches:
            date_val = self._convert_relative_date(match.group(1))
            if date_val:
                dates.append({
                    'type': 'relative',
                    'value': match.group(1),
                    'parsed_date': date_val,
                    'position': match.span()
                })

        # Absolute dates
        abs_matches = re.finditer(self.date_patterns['absolute_dates'], text)
        for match in abs_matches:
            date_val = self._parse_absolute_date(match.group(1))
            if date_val:
                dates.append({
                    'type': 'absolute',
                    'value': match.group(1),
                    'parsed_date': date_val,
                    'position': match.span()
                })

        # Day names
        day_matches = re.finditer(self.date_patterns['day_names'], text)
        for match in day_matches:
            date_val = self._convert_day_name(match.group(1))
            if date_val:
                dates.append({
                    'type': 'day_name',
                    'value': match.group(1),
                    'parsed_date': date_val,
                    'position': match.span()
                })

        # Relative time expressions
        rel_time_matches = re.finditer(self.date_patterns['relative_time'], text)
        for match in rel_time_matches:
            dates.append({
                'type': 'relative_time',
                'value': match.group(1),
                'parsed_date': None,  # Would need more complex parsing
                'position': match.span()
            })

        return dates

    def _convert_relative_date(self, date_str: str) -> Optional[str]:
        """
        Convert relative date strings to actual dates.

        Args:
            date_str: The relative date string

        Returns:
            ISO formatted date string or None
        """
        today = datetime.now().date()

        if date_str == 'today':
            return today.isoformat()
        elif date_str == 'tomorrow':
            return (today + timedelta(days=1)).isoformat()
        elif date_str == 'yesterday':
            return (today - timedelta(days=1)).isoformat()
        elif date_str == 'tonight':
            return today.isoformat()  # Same day, but contextually evening
        elif date_str == 'now':
            return today.isoformat()

        return None

    def _parse_absolute_date(self, date_str: str) -> Optional[str]:
        """
        Parse absolute date strings.

        Args:
            date_str: The absolute date string

        Returns:
            ISO formatted date string or None
        """
        # Handle YYYY-MM-DD format
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            try:
                parsed = datetime.strptime(date_str, '%Y-%m-%d')
                return parsed.date().isoformat()
            except ValueError:
                pass

        # Handle MM/DD or MM/DD/YYYY or DD/MM or DD/MM/YYYY
        for fmt in ['%m/%d', '%m/%d/%Y', '%d/%m', '%d/%m/%Y', '%m-%d', '%m-%d-%Y', '%d-%m', '%d-%m-%Y']:
            try:
                # For formats without year, add current year
                if fmt in ['%m/%d', '%d/%m', '%m-%d', '%d-%m']:
                    date_str_with_year = date_str + '/' + str(datetime.now().year)
                    fmt_with_year = fmt + '/%Y'
                    parsed = datetime.strptime(date_str_with_year, fmt_with_year)
                else:
                    parsed = datetime.strptime(date_str, fmt)

                return parsed.date().isoformat()
            except ValueError:
                continue

        return None

    def _convert_day_name(self, day_str: str) -> Optional[str]:
        """
        Convert day name to actual date.

        Args:
            day_str: The day name string

        Returns:
            ISO formatted date string or None
        """
        today = datetime.now()
        days = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        if day_str in days:
            target_day = days[day_str]
            days_ahead = target_day - today.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return (today + timedelta(days_ahead)).date().isoformat()

        return None

    def _extract_priorities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract priority information from text.

        Args:
            text: The text to extract priorities from

        Returns:
            List of dictionaries containing priority information
        """
        priorities = []

        for priority_level, pattern in self.priority_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                priority_value = self._normalize_priority(match.group(1))
                priorities.append({
                    'level': priority_level,
                    'value': match.group(1),
                    'normalized': priority_value,
                    'position': match.span()
                })

        return priorities

    def _normalize_priority(self, priority_str: str) -> str:
        """
        Normalize priority string to standard values.

        Args:
            priority_str: The raw priority string

        Returns:
            Normalized priority value (high, medium, low)
        """
        priority_str = priority_str.lower()

        if any(word in priority_str for word in ['highest', 'high', 'urgent', 'critical', 'immediate', 'asap', 'top priority', 'very important', 'vital', 'essential', 'crucial']):
            return 'high'
        elif any(word in priority_str for word in ['low', 'lowest', 'not urgent', 'non-urgent', 'optional', 'nice to have']):
            return 'low'
        else:
            return 'medium'

    def _extract_categories(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract category information from text.

        Args:
            text: The text to extract categories from

        Returns:
            List of dictionaries containing category information
        """
        categories = []

        for category, pattern in self.category_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                categories.append({
                    'category': category,
                    'value': match.group(1),
                    'position': match.span()
                })

        return categories

    def _extract_durations(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract duration information from text.

        Args:
            text: The text to extract durations from

        Returns:
            List of dictionaries containing duration information
        """
        durations = []

        for unit, pattern in self.duration_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                quantity = int(match.group(1))
                durations.append({
                    'unit': unit,
                    'quantity': quantity,
                    'value': match.group(0),
                    'position': match.span()
                })

        return durations

    def _extract_assignments(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract assignment information from text.

        Args:
            text: The text to extract assignments from

        Returns:
            List of dictionaries containing assignment information
        """
        assignments = []

        # Look for patterns like "assign to John" or "for Sarah"
        assign_patterns = [
            r'assign\s+(?:to\s+)?(\w+)',
            r'for\s+(\w+)',
            r'give\s+(?:to\s+)?(\w+)',
            r'let\s+(\w+)\s+do',
            r'have\s+(\w+)\s+do'
        ]

        for pattern in assign_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                assignments.append({
                    'person': match.group(1),
                    'value': match.group(0),
                    'position': match.span()
                })

        return assignments

    def _extract_tags(self, text: str) -> List[str]:
        """
        Extract tags from text (words preceded by #).

        Args:
            text: The text to extract tags from

        Returns:
            List of tag strings
        """
        tag_pattern = r'#(\w+)'
        tags = re.findall(tag_pattern, text)
        return tags

    def _extract_location(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract location information from text.

        Args:
            text: The text to extract locations from

        Returns:
            List of dictionaries containing location information
        """
        locations = []

        # Look for location indicators
        location_patterns = [
            r'at\s+([^.!,?]+?)(?=\s|$|[.!?])',
            r'in\s+([^.!,?]+?)(?=\s|$|[.!?])',
            r'to\s+([^.!,?]+?)(?=\s|$|[.!?])',
            r'from\s+([^.!,?]+?)(?=\s|$|[.!?])'
        ]

        for pattern in location_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                location = match.group(1).strip()
                if len(location) > 2:  # Avoid single letters
                    locations.append({
                        'location': location,
                        'value': match.group(0),
                        'position': match.span()
                    })

        return locations

    def _extract_recurrence(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract recurrence information from text.

        Args:
            text: The text to extract recurrence from

        Returns:
            List of dictionaries containing recurrence information
        """
        recurrences = []

        # Look for recurrence patterns
        recurrence_patterns = [
            r'\b(every\s+\w+)\b',
            r'\b(daily|weekly|monthly|yearly|annually)\b',
            r'\b(repeat|recurring|recurrent)\b',
            r'\b(each\s+\w+)\b'
        ]

        for pattern in recurrence_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                recurrences.append({
                    'recurrence': match.group(0),
                    'value': match.group(0),
                    'position': match.span()
                })

        return recurrences

    def get_most_likely_date(self, text: str) -> Optional[str]:
        """
        Get the most likely date from a text.

        Args:
            text: The text to extract date from

        Returns:
            ISO formatted date string or None
        """
        dates = self._extract_dates(text.lower())
        if dates:
            # Return the first date found as the most likely one
            return dates[0]['parsed_date']
        return None

    def get_priority_score(self, text: str) -> int:
        """
        Get a numeric priority score from text (higher is higher priority).

        Args:
            text: The text to analyze

        Returns:
            Priority score (1-3, where 3 is highest priority)
        """
        priorities = self._extract_priorities(text.lower())
        if not priorities:
            return 2  # Default to medium priority

        # Count priority indicators
        high_count = sum(1 for p in priorities if p['normalized'] == 'high')
        low_count = sum(1 for p in priorities if p['normalized'] == 'low')

        if high_count > low_count:
            return 3  # High priority
        elif low_count > high_count:
            return 1  # Low priority
        else:
            return 2  # Medium priority


def get_task_extraction_skill() -> TaskExtractionSkill:
    """
    Get an instance of the task extraction skill.

    Returns:
        TaskExtractionSkill instance
    """
    return TaskExtractionSkill()