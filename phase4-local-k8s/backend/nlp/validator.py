"""
Validator for Todo AI Chatbot

This module validates extracted task information.
"""

import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime


class Validator:
    """Validates extracted task information."""

    def __init__(self):
        """Initialize the validator."""
        self.validation_rules = self._define_validation_rules()

    def _define_validation_rules(self) -> Dict[str, callable]:
        """
        Define validation rules.

        Returns:
            Dictionary of field names to validation functions
        """
        return {
            'description': self._validate_description,
            'due_date': self._validate_due_date,
            'priority': self._validate_priority,
            'category': self._validate_category,
            'tags': self._validate_tags,
            'status': self._validate_status,
            'estimated_time': self._validate_estimated_time,
            'assigned_to': self._validate_assigned_to
        }

    def validate_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a task dictionary.

        Args:
            task_data: Dictionary containing task information

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'validated_data': {}
        }

        for field, value in task_data.items():
            if field in self.validation_rules:
                result = self.validation_rules[field](value)
                if not result['valid']:
                    validation_results['valid'] = False
                    validation_results['errors'].extend(result['errors'])
                elif result.get('warnings'):
                    validation_results['warnings'].extend(result['warnings'])

                # Store validated/cleaned value
                validation_results['validated_data'][field] = result.get('value', value)
            else:
                # For fields without specific validation rules, just store the value
                validation_results['validated_data'][field] = value

        return validation_results

    def _validate_description(self, description: Any) -> Dict[str, Any]:
        """
        Validate task description.

        Args:
            description: The description to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': description}

        if description is None:
            result['valid'] = False
            result['errors'].append('Description cannot be None')
            return result

        if not isinstance(description, str):
            try:
                description = str(description)
            except:
                result['valid'] = False
                result['errors'].append('Description must be convertible to string')
                return result

        # Trim whitespace
        description = description.strip()

        if not description:
            result['valid'] = False
            result['errors'].append('Description cannot be empty')
        elif len(description) > 500:
            result['valid'] = False
            result['errors'].append('Description is too long (max 500 characters)')
        elif len(description) < 2:
            result['warnings'] = ['Description is very short']

        result['value'] = description
        return result

    def _validate_due_date(self, due_date: Any) -> Dict[str, Any]:
        """
        Validate task due date.

        Args:
            due_date: The due date to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': due_date}

        if due_date is None:
            # Due date is optional, so None is valid
            return result

        if isinstance(due_date, str):
            # Check if it's in YYYY-MM-DD format
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(date_pattern, due_date):
                try:
                    parsed_date = datetime.strptime(due_date, '%Y-%m-%d')
                    # Check if date is not in the past
                    today = datetime.now().date()
                    if parsed_date.date() < today:
                        result['warnings'] = ['Due date is in the past']
                    result['value'] = due_date
                except ValueError:
                    result['valid'] = False
                    result['errors'].append('Invalid date format, expected YYYY-MM-DD')
            else:
                result['valid'] = False
                result['errors'].append('Invalid date format, expected YYYY-MM-DD')
        else:
            result['valid'] = False
            result['errors'].append('Due date must be a string in YYYY-MM-DD format')

        return result

    def _validate_priority(self, priority: Any) -> Dict[str, Any]:
        """
        Validate task priority.

        Args:
            priority: The priority to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': priority}

        if priority is None:
            # Priority is optional, default to 'medium'
            result['value'] = 'medium'
            return result

        if isinstance(priority, str):
            priority = priority.lower().strip()
            valid_priorities = ['low', 'medium', 'high']

            if priority in valid_priorities:
                result['value'] = priority
            else:
                result['valid'] = False
                result['errors'].append(f'Invalid priority value: {priority}. Must be one of {valid_priorities}')
        else:
            result['valid'] = False
            result['errors'].append('Priority must be a string')

        return result

    def _validate_category(self, category: Any) -> Dict[str, Any]:
        """
        Validate task category.

        Args:
            category: The category to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': category}

        if category is None:
            # Category is optional
            result['value'] = 'general'
            return result

        if isinstance(category, str):
            category = category.lower().strip()

            if len(category) > 50:
                result['valid'] = False
                result['errors'].append('Category name is too long (max 50 characters)')
            elif not re.match(r'^[a-z0-9\s\-_]+$', category):
                result['valid'] = False
                result['errors'].append('Category can only contain lowercase letters, numbers, spaces, hyphens, and underscores')
            else:
                result['value'] = category
        else:
            result['valid'] = False
            result['errors'].append('Category must be a string')

        return result

    def _validate_tags(self, tags: Any) -> Dict[str, Any]:
        """
        Validate task tags.

        Args:
            tags: The tags to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': tags}

        if tags is None:
            # Tags are optional
            result['value'] = []
            return result

        if isinstance(tags, str):
            # If it's a string, split it by commas or spaces
            tags = [tag.strip() for tag in re.split(r'[,\s]+', tags) if tag.strip()]
        elif not isinstance(tags, list):
            result['valid'] = False
            result['errors'].append('Tags must be a list or comma-separated string')
            return result

        validated_tags = []
        for i, tag in enumerate(tags):
            if not isinstance(tag, str):
                try:
                    tag = str(tag)
                except:
                    result['valid'] = False
                    result['errors'].append(f'Tag at index {i} must be convertible to string')
                    continue

            tag = tag.strip().lower()
            if not tag:
                continue  # Skip empty tags

            if len(tag) > 30:
                result['valid'] = False
                result['errors'].append(f'Tag "{tag}" is too long (max 30 characters)')
                continue

            if not re.match(r'^[a-z0-9_\-]+$', tag):
                result['valid'] = False
                result['errors'].append(f'Tag "{tag}" contains invalid characters. Only lowercase letters, numbers, hyphens, and underscores allowed.')
                continue

            validated_tags.append(tag)

        result['value'] = validated_tags
        return result

    def _validate_status(self, status: Any) -> Dict[str, Any]:
        """
        Validate task status.

        Args:
            status: The status to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': status}

        if status is None:
            # Status is optional, default to 'pending'
            result['value'] = 'pending'
            return result

        if isinstance(status, str):
            status = status.lower().strip()
            valid_statuses = ['pending', 'completed', 'active', 'inactive', 'todo', 'done']

            if status in valid_statuses:
                result['value'] = status
            else:
                result['valid'] = False
                result['errors'].append(f'Invalid status value: {status}. Must be one of {valid_statuses}')
        else:
            result['valid'] = False
            result['errors'].append('Status must be a string')

        return result

    def _validate_estimated_time(self, estimated_time: Any) -> Dict[str, Any]:
        """
        Validate estimated time for task completion.

        Args:
            estimated_time: The estimated time to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': estimated_time}

        if estimated_time is None:
            # Estimated time is optional
            return result

        # Check if it's a valid time format (e.g., "2h 30m", "1.5 hours", etc.)
        if isinstance(estimated_time, (int, float)):
            # If it's a number, assume it's in minutes
            if estimated_time < 0:
                result['valid'] = False
                result['errors'].append('Estimated time cannot be negative')
            elif estimated_time > 1440 * 30:  # More than 30 days in minutes
                result['valid'] = False
                result['errors'].append('Estimated time is unrealistically large (>30 days)')
            else:
                result['value'] = float(estimated_time)
        elif isinstance(estimated_time, str):
            # Parse time string like "2h 30m", "1.5 hours", etc.
            time_pattern = r'(\d+(?:\.\d+)?)\s*(h|hr|hour|hours|m|min|minute|minutes|d|day|days|w|week|weeks|mo|month|months)\b'
            matches = re.findall(time_pattern, estimated_time.lower())

            if not matches:
                result['valid'] = False
                result['errors'].append('Invalid time format. Use formats like "2h 30m", "1.5 hours", etc.')
            else:
                # Convert to minutes for validation
                total_minutes = 0
                for value, unit in matches:
                    val = float(value)
                    if unit.startswith(('h', 'hr')):
                        total_minutes += val * 60
                    elif unit.startswith(('m', 'min')):
                        total_minutes += val
                    elif unit.startswith('d'):
                        total_minutes += val * 24 * 60
                    elif unit.startswith('w'):
                        total_minutes += val * 7 * 24 * 60
                    elif unit.startswith(('mo', 'month')):
                        total_minutes += val * 30 * 24 * 60  # Approximate

                if total_minutes < 0:
                    result['valid'] = False
                    result['errors'].append('Estimated time cannot be negative')
                elif total_minutes > 1440 * 30:  # More than 30 days in minutes
                    result['valid'] = False
                    result['errors'].append('Estimated time is unrealistically large (>30 days)')
                else:
                    result['value'] = total_minutes
        else:
            result['valid'] = False
            result['errors'].append('Estimated time must be a number (minutes) or time string (e.g., "2h 30m")')

        return result

    def _validate_assigned_to(self, assigned_to: Any) -> Dict[str, Any]:
        """
        Validate who the task is assigned to.

        Args:
            assigned_to: The assignee to validate

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': [], 'value': assigned_to}

        if assigned_to is None:
            # Assignee is optional
            return result

        if isinstance(assigned_to, str):
            assigned_to = assigned_to.strip()

            if not assigned_to:
                result['valid'] = False
                result['errors'].append('Assigned to cannot be empty')
            elif len(assigned_to) > 100:
                result['valid'] = False
                result['errors'].append('Assigned to name is too long (max 100 characters)')
            else:
                result['value'] = assigned_to
        else:
            result['valid'] = False
            result['errors'].append('Assigned to must be a string')

        return result

    def validate_multiple_tasks(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate multiple tasks at once.

        Args:
            tasks: List of task dictionaries to validate

        Returns:
            Dictionary with validation results for all tasks
        """
        results = {
            'all_valid': True,
            'task_results': [],
            'total_errors': 0,
            'total_warnings': 0
        }

        for i, task in enumerate(tasks):
            task_result = self.validate_task(task)
            results['task_results'].append({
                'index': i,
                'original_task': task,
                'validation_result': task_result
            })

            if not task_result['valid']:
                results['all_valid'] = False

            results['total_errors'] += len(task_result['errors'])
            results['total_warnings'] += len(task_result.get('warnings', []))

        return results

    def validate_conversation_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate conversation context data.

        Args:
            context: Dictionary containing conversation context

        Returns:
            Dictionary with validation results
        """
        result = {'valid': True, 'errors': []}

        required_fields = ['user_id', 'conversation_id']
        for field in required_fields:
            if field not in context:
                result['valid'] = False
                result['errors'].append(f'Missing required field: {field}')

        return result

    def sanitize_input(self, text: str) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            text: The input text to sanitize

        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""

        # Remove potentially dangerous characters
        sanitized = text.replace('\0', '')  # Null bytes
        sanitized = sanitized.replace('<script', '&lt;script')  # Prevent script tags
        sanitized = sanitized.replace('javascript:', 'javascript&#58;')  # Prevent JS execution
        sanitized = sanitized.replace('vbscript:', 'vbscript&#58;')  # Prevent VBScript execution

        return sanitized


def get_validator() -> Validator:
    """
    Get an instance of the validator.

    Returns:
        Validator instance
    """
    return Validator()