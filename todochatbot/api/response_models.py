"""
Response Models for Todo AI Chatbot API.

This module defines the data models for API responses.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatResponseModel:
    """Model for chat API response body."""
    conversation_id: str
    response: str
    success: bool = True
    error: Optional[str] = None
    timestamp: str = ""
    user_id: Optional[str] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ErrorResponseModel:
    """Model for error responses."""
    error: str
    success: bool = False
    timestamp: str = ""
    error_code: Optional[str] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class HealthCheckResponseModel:
    """Model for health check API response."""
    status: str = "healthy"
    timestamp: str = ""
    version: Optional[str] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ConversationHistoryResponseModel:
    """Model for conversation history response."""
    conversation_id: str
    messages: List[Dict[str, Any]]
    success: bool = True
    error: Optional[str] = None
    user_id: Optional[str] = None


class ResponseModels:
    """Container for all response models."""

    @staticmethod
    def get_chat_response_model(**kwargs) -> ChatResponseModel:
        """
        Create a ChatResponseModel with provided parameters.

        Args:
            **kwargs: Parameters for the model

        Returns:
            ChatResponseModel instance
        """
        return ChatResponseModel(**kwargs)

    @staticmethod
    def get_error_response_model(error: str, error_code: Optional[str] = None) -> ErrorResponseModel:
        """
        Create an ErrorResponseModel with provided parameters.

        Args:
            error: Error message
            error_code: Optional error code

        Returns:
            ErrorResponseModel instance
        """
        return ErrorResponseModel(error=error, error_code=error_code)

    @staticmethod
    def get_health_check_response_model(status: str = "healthy", version: Optional[str] = None) -> HealthCheckResponseModel:
        """
        Create a HealthCheckResponseModel with provided parameters.

        Args:
            status: Health status
            version: Optional version info

        Returns:
            HealthCheckResponseModel instance
        """
        return HealthCheckResponseModel(status=status, version=version)

    @staticmethod
    def get_conversation_history_response_model(conversation_id: str, messages: List[Dict[str, Any]]) -> ConversationHistoryResponseModel:
        """
        Create a ConversationHistoryResponseModel with provided parameters.

        Args:
            conversation_id: ID of the conversation
            messages: List of messages in the conversation

        Returns:
            ConversationHistoryResponseModel instance
        """
        return ConversationHistoryResponseModel(conversation_id=conversation_id, messages=messages)


def get_response_models() -> ResponseModels:
    """
    Get an instance of the response models container.

    Returns:
        ResponseModels instance
    """
    return ResponseModels()