"""
Input Validation Module for Todo AI Chatbot

This module verifies input sanitization and validation in all components for security.
"""

from typing import Dict, Any, Optional
import re
import html


class InputValidation:
    """Verifies input sanitization and validation in all components for security."""

    def __init__(self):
        """Initialize the input validation module."""
        # Define security patterns
        self.sql_injection_patterns = [
            r"(?i)(union\s+select|drop\s+\w+|create\s+\w+|exec\s*\(|';\s*--)",
            r"(?i)(delete\s+from|update\s+\w+\s+set|insert\s+into)",
            r"(?i)(declare\s+@|\-\-|\#|/\*|\*/)"
        ]

        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>",
            r"<object[^>]*>.*?</object>"
        ]

        self.command_injection_patterns = [
            r"[;&|]",
            r"\$\(",
            r"`.*?`",
            r"eval\s*\(",
            r"exec\s*\("
        ]

    def validate_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Validate user input for security vulnerabilities.

        Args:
            user_input: The raw user input to validate

        Returns:
            Dictionary containing validation results
        """
        result = {
            'is_valid': True,
            'sanitized_input': user_input,
            'security_issues': [],
            'original_input': user_input
        }

        # Check for SQL injection patterns
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, user_input):
                result['is_valid'] = False
                result['security_issues'].append({
                    'type': 'sql_injection',
                    'pattern': pattern,
                    'found_in': user_input
                })

        # Check for XSS patterns
        for pattern in self.xss_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                result['is_valid'] = False
                result['security_issues'].append({
                    'type': 'xss',
                    'pattern': pattern,
                    'found_in': user_input
                })

        # Check for command injection patterns
        for pattern in self.command_injection_patterns:
            if re.search(pattern, user_input):
                result['is_valid'] = False
                result['security_issues'].append({
                    'type': 'command_injection',
                    'pattern': pattern,
                    'found_in': user_input
                })

        # Sanitize the input
        result['sanitized_input'] = self.sanitize_input(user_input)

        return result

    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            user_input: The raw user input to sanitize

        Returns:
            Sanitized input string
        """
        if not isinstance(user_input, str):
            return ""

        # Escape HTML entities
        sanitized = html.escape(user_input)

        # Remove potentially dangerous patterns
        # Remove script tags (case insensitive)
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)

        # Remove javascript: URIs
        sanitized = re.sub(r'javascript:', 'javascript&#58;', sanitized, flags=re.IGNORECASE)

        # Remove data URIs that could contain scripts
        sanitized = re.sub(r'data:text/html', 'data&#58;text/html', sanitized, flags=re.IGNORECASE)

        return sanitized

    def validate_user_id(self, user_id: str) -> Dict[str, Any]:
        """
        Validate user ID for security compliance.

        Args:
            user_id: The user ID to validate

        Returns:
            Dictionary containing validation results
        """
        result = {
            'is_valid': True,
            'sanitized_id': user_id,
            'security_issues': []
        }

        # Check for invalid characters in user ID
        if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
            result['is_valid'] = False
            result['security_issues'].append({
                'type': 'invalid_user_id_format',
                'description': 'User ID contains invalid characters',
                'value': user_id
            })

        # Ensure user ID length is reasonable
        if len(user_id) > 100 or len(user_id) < 1:
            result['is_valid'] = False
            result['security_issues'].append({
                'type': 'invalid_user_id_length',
                'description': 'User ID length is invalid',
                'value': user_id,
                'length': len(user_id)
            })

        return result

    def validate_conversation_id(self, conversation_id: str) -> Dict[str, Any]:
        """
        Validate conversation ID for security compliance.

        Args:
            conversation_id: The conversation ID to validate

        Returns:
            Dictionary containing validation results
        """
        result = {
            'is_valid': True,
            'sanitized_id': conversation_id,
            'security_issues': []
        }

        # Check for invalid characters in conversation ID
        if not re.match(r'^[a-zA-Z0-9_-]+$', conversation_id):
            result['is_valid'] = False
            result['security_issues'].append({
                'type': 'invalid_conversation_id_format',
                'description': 'Conversation ID contains invalid characters',
                'value': conversation_id
            })

        # Ensure conversation ID length is reasonable
        if len(conversation_id) > 100 or len(conversation_id) < 1:
            result['is_valid'] = False
            result['security_issues'].append({
                'type': 'invalid_conversation_id_length',
                'description': 'Conversation ID length is invalid',
                'value': conversation_id,
                'length': len(conversation_id)
            })

        return result

    def validate_api_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an API request for security compliance.

        Args:
            request_data: The API request data to validate

        Returns:
            Dictionary containing validation results
        """
        result = {
            'is_valid': True,
            'validated_data': {},
            'security_issues': []
        }

        # Validate user ID if present
        if 'user_id' in request_data:
            user_validation = self.validate_user_id(str(request_data['user_id']))
            if not user_validation['is_valid']:
                result['is_valid'] = False
                result['security_issues'].extend(user_validation['security_issues'])

            result['validated_data']['user_id'] = user_validation['sanitized_id']

        # Validate conversation ID if present
        if 'conversation_id' in request_data:
            conv_validation = self.validate_conversation_id(str(request_data['conversation_id']))
            if not conv_validation['is_valid']:
                result['is_valid'] = False
                result['security_issues'].extend(conv_validation['security_issues'])

            result['validated_data']['conversation_id'] = conv_validation['sanitized_id']

        # Validate message content if present
        if 'message' in request_data:
            message_validation = self.validate_user_input(str(request_data['message']))
            if not message_validation['is_valid']:
                result['is_valid'] = False
                result['security_issues'].extend(message_validation['security_issues'])

            result['validated_data']['message'] = message_validation['sanitized_input']

        return result

    def validate_database_query_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate database query parameters for security compliance.

        Args:
            params: The database query parameters to validate

        Returns:
            Dictionary containing validation results
        """
        result = {
            'is_valid': True,
            'validated_params': {},
            'security_issues': []
        }

        for key, value in params.items():
            if isinstance(value, str):
                # Validate string parameters
                validation = self.validate_user_input(value)
                if not validation['is_valid']:
                    result['is_valid'] = False
                    # Add context to security issues
                    for issue in validation['security_issues']:
                        issue['param_key'] = key
                        result['security_issues'].append(issue)

                result['validated_params'][key] = validation['sanitized_input']
            else:
                # For non-string parameters, just pass through
                result['validated_params'][key] = value

        return result

    def scan_for_sensitive_data(self, text: str) -> Dict[str, Any]:
        """
        Scan text for potential sensitive data.

        Args:
            text: The text to scan for sensitive data

        Returns:
            Dictionary containing scan results
        """
        patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b|\b(?:\d{4}[-\s]?){2}\d{7}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'password': r'(?i)(password|pwd|pass)\s*[=:]\s*\S+'
        }

        findings = {}
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                findings[pattern_name] = matches

        return {
            'has_sensitive_data': len(findings) > 0,
            'findings': findings,
            'text_length': len(text)
        }


def get_input_validator() -> InputValidation:
    """
    Get an instance of the input validator.

    Returns:
        InputValidation instance
    """
    return InputValidation()