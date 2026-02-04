"""
Validation Module for Todo AI Chatbot API.

This module handles request validation and sanitization for the chat API.
"""

import re
from typing import Dict, Any, Tuple, Optional
from urllib.parse import urlparse


def validate_chat_request(request_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate a chat request.

    Args:
        request_data: The request data to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for required fields
    required_fields = ["message"]
    for field in required_fields:
        if field not in request_data:
            return False, f"Missing required field: {field}"

    # Validate message field
    message = request_data.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return False, "Message must be a non-empty string"

    # Validate message length
    if len(message) > 2000:  # Arbitrary limit for now
        return False, "Message is too long (max 2000 characters)"

    # Sanitize message
    sanitized_message = sanitize_input(message)
    if sanitized_message != message:
        # Update the request data with sanitized message
        request_data["message"] = sanitized_message

    # Validate conversation_id if provided
    conversation_id = request_data.get("conversation_id")
    if conversation_id is not None:
        if not isinstance(conversation_id, str) or not conversation_id.strip():
            return False, "Conversation ID must be a non-empty string if provided"

        # Basic validation for conversation ID format
        if not re.match(r'^[a-zA-Z0-9_-]+$', conversation_id):
            return False, "Invalid conversation ID format"

    # Validate user_id if provided in request (though it's typically from path)
    user_id = request_data.get("user_id")
    if user_id is not None:
        if not isinstance(user_id, str) or not user_id.strip():
            return False, "User ID must be a non-empty string if provided"

        # Basic validation for user ID format
        if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
            return False, "Invalid user ID format"

    return True, None


def validate_user_id(user_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a user ID.

    Args:
        user_id: The user ID to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not user_id or not user_id.strip():
        return False, "User ID cannot be empty"

    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        return False, "Invalid user ID format. Only alphanumeric characters, hyphens, and underscores are allowed"

    # Check length
    if len(user_id) > 100:
        return False, "User ID is too long (max 100 characters)"

    return True, None


def validate_conversation_id(conversation_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a conversation ID.

    Args:
        conversation_id: The conversation ID to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not conversation_id or not conversation_id.strip():
        return False, "Conversation ID cannot be empty"

    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9_-]+$', conversation_id):
        return False, "Invalid conversation ID format. Only alphanumeric characters, hyphens, and underscores are allowed"

    # Check length
    if len(conversation_id) > 100:
        return False, "Conversation ID is too long (max 100 characters)"

    return True, None


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by removing potentially harmful content.

    Args:
        input_str: The input string to sanitize

    Returns:
        Sanitized string
    """
    if not input_str:
        return input_str

    # Remove potentially dangerous characters/patterns
    # This is a basic implementation - in a real app, you'd want more robust sanitization

    # Remove null bytes
    sanitized = input_str.replace('\x00', '')

    # Remove control characters (except tab, newline, carriage return)
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')

    # Escape HTML-sensitive characters (basic protection)
    sanitized = sanitized.replace('<', '&lt;').replace('>', '&gt;')

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    return sanitized


def validate_message_content(message: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the content of a message.

    Args:
        message: The message to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Message cannot be empty"

    # Check for potential SQL injection patterns
    sql_patterns = [
        r'\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b',
        r"'(?:--|#|/\*|\\)",
        r';\s*(?:--|#|/\*)'
    ]

    for pattern in sql_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return False, "Message contains potentially unsafe content"

    # Check for potential XSS patterns
    xss_patterns = [
        r'<script[^>]*>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>'
    ]

    for pattern in xss_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return False, "Message contains potentially unsafe content"

    return True, None


def validate_api_request_headers(headers: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """
    Validate API request headers.

    Args:
        headers: Dictionary of request headers

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for common security headers
    content_type = headers.get('content-type', '').lower()
    if content_type and not content_type.startswith('application/json'):
        return False, "Invalid content type. Expected application/json"

    # Check for suspicious headers
    suspicious_headers = [
        'x-forwarded-for',
        'x-real-ip',
        'x-client-ip'
    ]

    for header in suspicious_headers:
        if header in headers:
            # In a real implementation, you'd want to validate these properly
            # For now, just log that they exist
            pass

    return True, None


class RequestValidator:
    """Class-based validator for API requests."""

    @staticmethod
    def validate_and_sanitize_request(request_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """
        Validate and sanitize a complete request.

        Args:
            request_data: The request data to validate and sanitize

        Returns:
            Tuple of (is_valid, error_message, sanitized_data)
        """
        # Create a copy to avoid modifying the original
        sanitized_data = request_data.copy()

        # Validate the request
        is_valid, error_msg = validate_chat_request(sanitized_data)
        if not is_valid:
            return False, error_msg, sanitized_data

        # Additional validations can be added here
        message = sanitized_data.get("message", "")
        is_content_valid, content_error = validate_message_content(message)
        if not is_content_valid:
            return False, content_error, sanitized_data

        return True, None, sanitized_data


def get_validator() -> RequestValidator:
    """
    Get an instance of the request validator.

    Returns:
        RequestValidator instance
    """
    return RequestValidator()