"""
Error Handlers for Todo AI Chatbot API.

This module implements graceful error handling for AI agent failures.
"""

from typing import Dict, Any, Optional, Callable
from enum import Enum
import logging
import traceback
from datetime import datetime


class ErrorType(Enum):
    """Enumeration of different error types."""
    AGENT_CONNECTION_ERROR = "agent_connection_error"
    AGENT_TIMEOUT_ERROR = "agent_timeout_error"
    INVALID_REQUEST_ERROR = "invalid_request_error"
    DATABASE_ERROR = "database_error"
    MCP_TOOL_ERROR = "mcp_tool_error"
    CONVERSATION_ERROR = "conversation_error"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN_ERROR = "unknown_error"


class ErrorHandler:
    """Handles different types of errors gracefully."""

    def __init__(self):
        """Initialize the error handler."""
        self.error_handlers = {}
        self.setup_default_handlers()

    def setup_default_handlers(self):
        """Set up default error handlers for common error types."""
        self.error_handlers = {
            ErrorType.AGENT_CONNECTION_ERROR: self.handle_agent_connection_error,
            ErrorType.AGENT_TIMEOUT_ERROR: self.handle_agent_timeout_error,
            ErrorType.INVALID_REQUEST_ERROR: self.handle_invalid_request_error,
            ErrorType.DATABASE_ERROR: self.handle_database_error,
            ErrorType.MCP_TOOL_ERROR: self.handle_mcp_tool_error,
            ErrorType.CONVERSATION_ERROR: self.handle_conversation_error,
            ErrorType.VALIDATION_ERROR: self.handle_validation_error,
            ErrorType.UNKNOWN_ERROR: self.handle_unknown_error,
        }

    def handle_error(self, error: Exception, error_type: ErrorType, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle an error based on its type.

        Args:
            error: The exception that occurred
            error_type: The type of error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        if error_type in self.error_handlers:
            return self.error_handlers[error_type](error, context)
        else:
            return self.handle_unknown_error(error, context)

    def handle_agent_connection_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle agent connection errors.

        Args:
            error: The connection error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.error(f"Agent connection error: {str(error)}", exc_info=True)

        return {
            "success": False,
            "error_type": "agent_connection_error",
            "message": "Unable to connect to the AI agent. Please try again later.",
            "timestamp": datetime.utcnow().isoformat(),
            "debug_info": {
                "error": str(error),
                "traceback": traceback.format_exc() if context and context.get("include_traceback", False) else None
            } if context and context.get("include_debug_info", False) else None
        }

    def handle_agent_timeout_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle agent timeout errors.

        Args:
            error: The timeout error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.warning(f"Agent timeout error: {str(error)}")

        return {
            "success": False,
            "error_type": "agent_timeout_error",
            "message": "The AI agent is taking too long to respond. Please try again.",
            "timestamp": datetime.utcnow().isoformat()
        }

    def handle_invalid_request_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle invalid request errors.

        Args:
            error: The validation error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.info(f"Invalid request error: {str(error)}")

        return {
            "success": False,
            "error_type": "invalid_request_error",
            "message": "The request is invalid. Please check your input and try again.",
            "timestamp": datetime.utcnow().isoformat()
        }

    def handle_database_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle database errors.

        Args:
            error: The database error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.error(f"Database error: {str(error)}", exc_info=True)

        return {
            "success": False,
            "error_type": "database_error",
            "message": "A database error occurred. Our team has been notified.",
            "timestamp": datetime.utcnow().isoformat()
        }

    def handle_mcp_tool_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle MCP tool errors.

        Args:
            error: The MCP tool error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.error(f"MCP tool error: {str(error)}", exc_info=True)

        return {
            "success": False,
            "error_type": "mcp_tool_error",
            "message": "There was an issue with the task management tools. Please try again later.",
            "timestamp": datetime.utcnow().isoformat()
        }

    def handle_conversation_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle conversation-related errors.

        Args:
            error: The conversation error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.error(f"Conversation error: {str(error)}", exc_info=True)

        return {
            "success": False,
            "error_type": "conversation_error",
            "message": "There was an issue with your conversation. Please start a new conversation.",
            "timestamp": datetime.utcnow().isoformat()
        }

    def handle_validation_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle validation errors.

        Args:
            error: The validation error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.info(f"Validation error: {str(error)}")

        return {
            "success": False,
            "error_type": "validation_error",
            "message": f"Validation failed: {str(error)}",
            "timestamp": datetime.utcnow().isoformat()
        }

    def handle_unknown_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle unknown errors.

        Args:
            error: The unknown error
            context: Additional context information

        Returns:
            Dictionary with error response details
        """
        logging.error(f"Unknown error: {str(error)}", exc_info=True)

        return {
            "success": False,
            "error_type": "unknown_error",
            "message": "An unexpected error occurred. Our team has been notified.",
            "timestamp": datetime.utcnow().isoformat(),
            "debug_info": {
                "error": str(error),
                "traceback": traceback.format_exc() if context and context.get("include_traceback", False) else None
            } if context and context.get("include_debug_info", False) else None
        }

    def register_custom_handler(self, error_type: ErrorType, handler: Callable[[Exception, Optional[Dict[str, Any]]], Dict[str, Any]]):
        """
        Register a custom error handler.

        Args:
            error_type: The type of error to handle
            handler: The handler function
        """
        self.error_handlers[error_type] = handler

    def log_error(self, error: Exception, error_type: ErrorType, context: Optional[Dict[str, Any]] = None):
        """
        Log an error with appropriate level based on error type.

        Args:
            error: The error to log
            error_type: The type of error
            context: Additional context information
        """
        if error_type in [ErrorType.AGENT_CONNECTION_ERROR, ErrorType.DATABASE_ERROR, ErrorType.MCP_TOOL_ERROR, ErrorType.UNKNOWN_ERROR]:
            logging.error(f"Critical error [{error_type.value}]: {str(error)}", exc_info=True)
        elif error_type in [ErrorType.AGENT_TIMEOUT_ERROR, ErrorType.CONVERSATION_ERROR]:
            logging.warning(f"Warning error [{error_type.value}]: {str(error)}")
        else:
            logging.info(f"Info error [{error_type.value}]: {str(error)}")


class APIErrorHandler:
    """Error handler specifically for API endpoints."""

    def __init__(self):
        """Initialize the API error handler."""
        self.generic_handler = ErrorHandler()

    def handle_endpoint_error(self, error: Exception, request_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle an error in an API endpoint.

        Args:
            error: The error that occurred
            request_context: Context about the request

        Returns:
            Dictionary with error response
        """
        # Determine error type based on exception
        error_type = self._determine_error_type(error)

        # Log the error
        self.generic_handler.log_error(error, error_type, request_context)

        # Handle the error
        return self.generic_handler.handle_error(error, error_type, request_context)

    def _determine_error_type(self, error: Exception) -> ErrorType:
        """
        Determine the type of error based on the exception.

        Args:
            error: The exception to classify

        Returns:
            The determined ErrorType
        """
        error_str = str(error).lower()

        if "connection" in error_str or "connect" in error_str:
            return ErrorType.AGENT_CONNECTION_ERROR
        elif "timeout" in error_str or "timed out" in error_str:
            return ErrorType.AGENT_TIMEOUT_ERROR
        elif "database" in error_str or "db" in error_str:
            return ErrorType.DATABASE_ERROR
        elif "validation" in error_str or "invalid" in error_str:
            return ErrorType.VALIDATION_ERROR
        elif "mcp" in error_str or "tool" in error_str:
            return ErrorType.MCP_TOOL_ERROR
        elif "conversation" in error_str:
            return ErrorType.CONVERSATION_ERROR
        else:
            return ErrorType.UNKNOWN_ERROR


def get_error_handler() -> ErrorHandler:
    """
    Get an instance of the error handler.

    Returns:
        ErrorHandler instance
    """
    return ErrorHandler()


def get_api_error_handler() -> APIErrorHandler:
    """
    Get an instance of the API error handler.

    Returns:
        APIErrorHandler instance
    """
    return APIErrorHandler()