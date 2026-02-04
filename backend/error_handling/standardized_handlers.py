"""
Standardized Error Handlers for Todo AI Chatbot

This module adds standardized error handling using skills.
"""

from typing import Dict, Any, Optional, Union
import logging
from functools import wraps
import traceback
from enum import Enum


class ErrorType(Enum):
    """Enumeration of error types."""
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    NOT_FOUND_ERROR = "not_found_error"
    CONFLICT_ERROR = "conflict_error"
    INTERNAL_ERROR = "internal_error"
    TIMEOUT_ERROR = "timeout_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    SERVICE_UNAVAILABLE_ERROR = "service_unavailable_error"


class StandardizedErrorHandler:
    """Standardized error handlers using skills."""

    def __init__(self):
        """Initialize the standardized error handler."""
        self.logger = logging.getLogger(__name__)
        self.error_templates = {
            ErrorType.VALIDATION_ERROR: {
                'message': 'Invalid input provided',
                'code': 'VALIDATION_ERROR',
                'status_code': 400
            },
            ErrorType.AUTHENTICATION_ERROR: {
                'message': 'Authentication required or invalid token',
                'code': 'AUTHENTICATION_ERROR',
                'status_code': 401
            },
            ErrorType.AUTHORIZATION_ERROR: {
                'message': 'Insufficient permissions',
                'code': 'AUTHORIZATION_ERROR',
                'status_code': 403
            },
            ErrorType.NOT_FOUND_ERROR: {
                'message': 'Requested resource not found',
                'code': 'NOT_FOUND_ERROR',
                'status_code': 404
            },
            ErrorType.CONFLICT_ERROR: {
                'message': 'Resource conflict detected',
                'code': 'CONFLICT_ERROR',
                'status_code': 409
            },
            ErrorType.INTERNAL_ERROR: {
                'message': 'An internal error occurred',
                'code': 'INTERNAL_ERROR',
                'status_code': 500
            },
            ErrorType.TIMEOUT_ERROR: {
                'message': 'Request timed out',
                'code': 'TIMEOUT_ERROR',
                'status_code': 408
            },
            ErrorType.RATE_LIMIT_ERROR: {
                'message': 'Rate limit exceeded',
                'code': 'RATE_LIMIT_ERROR',
                'status_code': 429
            },
            ErrorType.SERVICE_UNAVAILABLE_ERROR: {
                'message': 'Service temporarily unavailable',
                'code': 'SERVICE_UNAVAILABLE_ERROR',
                'status_code': 503
            }
        }

    def handle_error(self, error_type: ErrorType, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle an error according to standardized format.

        Args:
            error_type: The type of error
            details: Additional error details

        Returns:
            Standardized error response
        """
        template = self.error_templates[error_type]

        error_response = {
            'success': False,
            'error': {
                'code': template['code'],
                'message': template['message'],
                'type': error_type.value
            }
        }

        if details:
            error_response['error']['details'] = details

        # Log the error
        self.logger.error(f"{template['code']}: {template['message']}", extra={
            'error_type': error_type.value,
            'details': details
        })

        return error_response

    def handle_validation_error(self, field: str, message: str, value: Any = None) -> Dict[str, Any]:
        """
        Handle a validation error.

        Args:
            field: The field that failed validation
            message: The validation error message
            value: The value that failed validation

        Returns:
            Standardized validation error response
        """
        details = {
            'field': field,
            'message': message
        }
        if value is not None:
            details['value'] = str(value)

        return self.handle_error(ErrorType.VALIDATION_ERROR, details)

    def handle_authentication_error(self, reason: str = "Invalid or missing token") -> Dict[str, Any]:
        """
        Handle an authentication error.

        Args:
            reason: Reason for authentication failure

        Returns:
            Standardized authentication error response
        """
        return self.handle_error(ErrorType.AUTHENTICATION_ERROR, {'reason': reason})

    def handle_authorization_error(self, resource: str = "resource", action: str = "access") -> Dict[str, Any]:
        """
        Handle an authorization error.

        Args:
            resource: The resource that was accessed
            action: The action that was attempted

        Returns:
            Standardized authorization error response
        """
        details = {
            'resource': resource,
            'action': action
        }
        return self.handle_error(ErrorType.AUTHORIZATION_ERROR, details)

    def handle_not_found_error(self, resource_type: str, resource_id: str) -> Dict[str, Any]:
        """
        Handle a not found error.

        Args:
            resource_type: Type of resource (e.g., 'task', 'conversation')
            resource_id: ID of the resource

        Returns:
            Standardized not found error response
        """
        details = {
            'resource_type': resource_type,
            'resource_id': resource_id
        }
        return self.handle_error(ErrorType.NOT_FOUND_ERROR, details)

    def handle_internal_error(self, exception: Exception, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle an internal error.

        Args:
            exception: The exception that occurred
            context: Additional context about where the error occurred

        Returns:
            Standardized internal error response
        """
        # Log the full exception with traceback
        self.logger.exception("Internal error occurred", exc_info=True, extra={
            'context': context,
            'exception_type': type(exception).__name__,
            'exception_message': str(exception)
        })

        details = {
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'context': context or 'Unknown context'
        }

        return self.handle_error(ErrorType.INTERNAL_ERROR, details)

    def handle_service_unavailable_error(self, service_name: str, reason: str = "") -> Dict[str, Any]:
        """
        Handle a service unavailable error.

        Args:
            service_name: Name of the unavailable service
            reason: Reason for unavailability

        Returns:
            Standardized service unavailable error response
        """
        details = {
            'service': service_name,
            'reason': reason
        }
        return self.handle_error(ErrorType.SERVICE_UNAVAILABLE_ERROR, details)

    def handle_timeout_error(self, operation: str, timeout_duration: float) -> Dict[str, Any]:
        """
        Handle a timeout error.

        Args:
            operation: The operation that timed out
            timeout_duration: Duration that was waited before timeout

        Returns:
            Standardized timeout error response
        """
        details = {
            'operation': operation,
            'timeout_duration_seconds': timeout_duration
        }
        return self.handle_error(ErrorType.TIMEOUT_ERROR, details)

    def handle_rate_limit_error(self, limit: int, window: str, retry_after: Optional[float] = None) -> Dict[str, Any]:
        """
        Handle a rate limit error.

        Args:
            limit: The rate limit that was exceeded
            window: Time window for the rate limit
            retry_after: Seconds after which request can be retried

        Returns:
            Standardized rate limit error response
        """
        details = {
            'limit': limit,
            'window': window
        }
        if retry_after:
            details['retry_after_seconds'] = retry_after

        return self.handle_error(ErrorType.RATE_LIMIT_ERROR, details)

    def create_error_handler_decorator(self, error_type: ErrorType):
        """
        Create a decorator for handling specific error types.

        Args:
            error_type: The type of error to handle

        Returns:
            Decorator function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Log the exception
                    self.logger.exception(f"Error in {func.__name__}", exc_info=True)

                    # Handle based on error type
                    if error_type == ErrorType.INTERNAL_ERROR:
                        return self.handle_internal_error(e, f"Function: {func.__name__}")
                    else:
                        return self.handle_error(error_type, {
                            'function': func.__name__,
                            'exception': str(e),
                            'args': str(args)[:100],  # Limit length
                            'kwargs': str(kwargs)[:100]  # Limit length
                        })
            return wrapper
        return decorator

    def log_error_with_context(self, error: Exception, context: Dict[str, Any]):
        """
        Log an error with additional context information.

        Args:
            error: The error to log
            context: Additional context information
        """
        self.logger.error(
            f"Error: {str(error)}",
            extra={
                'exception_type': type(error).__name__,
                'context': context,
                'traceback': traceback.format_exc()
            }
        )

    def format_error_response(self, error: Union[Exception, str], error_type: Optional[ErrorType] = None) -> Dict[str, Any]:
        """
        Format an error response based on the error and optional error type.

        Args:
            error: The error (exception or string message)
            error_type: Optional specific error type

        Returns:
            Formatted error response
        """
        if isinstance(error, Exception):
            error_str = str(error)
            exc_type = type(error).__name__
        else:
            error_str = error
            exc_type = "GenericError"

        if error_type:
            return self.handle_error(error_type, {
                'message': error_str,
                'exception_type': exc_type
            })
        else:
            # Try to determine error type based on error message
            error_lower = error_str.lower()

            if 'validation' in error_lower or 'invalid' in error_lower:
                return self.handle_validation_error('unknown', error_str)
            elif 'auth' in error_lower:
                return self.handle_authentication_error(error_str)
            elif 'not found' in error_lower or 'does not exist' in error_lower:
                return self.handle_not_found_error('unknown', 'unknown')
            elif 'timeout' in error_lower:
                return self.handle_timeout_error('unknown_operation', 30.0)
            else:
                return self.handle_internal_error(error if isinstance(error, Exception) else Exception(error_str))

    def register_error_callback(self, error_type: ErrorType, callback_func):
        """
        Register a callback function to be called when a specific error occurs.

        Args:
            error_type: The type of error
            callback_func: Function to call when error occurs
        """
        # In a real implementation, this would store callbacks to be executed
        # when specific errors occur
        pass


def get_standardized_error_handler() -> StandardizedErrorHandler:
    """
    Get an instance of the standardized error handler.

    Returns:
        StandardizedErrorHandler instance
    """
    return StandardizedErrorHandler()


# Global error handler instance
global_error_handler = get_standardized_error_handler()


def handle_api_error(error_type: ErrorType, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to handle API errors using the global error handler.

    Args:
        error_type: The type of error
        details: Additional error details

    Returns:
        Standardized error response
    """
    return global_error_handler.handle_error(error_type, details)


def handle_validation_error(field: str, message: str, value: Any = None) -> Dict[str, Any]:
    """
    Convenience function to handle validation errors using the global error handler.

    Args:
        field: The field that failed validation
        message: The validation error message
        value: The value that failed validation

    Returns:
        Standardized validation error response
    """
    return global_error_handler.handle_validation_error(field, message, value)