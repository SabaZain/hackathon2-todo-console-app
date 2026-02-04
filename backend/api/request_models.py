"""
Request Models for Todo AI Chatbot API.

This module defines the data models for API requests.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class ChatRequestModel:
    """Model for chat API request body."""
    conversation_id: Optional[str] = None
    message: str = ""
    user_id: Optional[str] = None

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate the request model.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.message or not self.message.strip():
            return False, "Message cannot be empty"

        if not self.user_id:
            return False, "User ID is required"

        return True, None


@dataclass
class HealthCheckRequestModel:
    """Model for health check API request."""
    timestamp: Optional[str] = None


@dataclass
class ConversationStartRequestModel:
    """Model for starting a new conversation."""
    user_id: str = ""
    initial_message: Optional[str] = None

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate the conversation start request model.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.user_id:
            return False, "User ID is required"

        return True, None


class RequestModels:
    """Container for all request models."""

    @staticmethod
    def get_chat_request_model(**kwargs) -> ChatRequestModel:
        """
        Create a ChatRequestModel with provided parameters.

        Args:
            **kwargs: Parameters for the model

        Returns:
            ChatRequestModel instance
        """
        return ChatRequestModel(**kwargs)

    @staticmethod
    def get_health_check_request_model(**kwargs) -> HealthCheckRequestModel:
        """
        Create a HealthCheckRequestModel with provided parameters.

        Args:
            **kwargs: Parameters for the model

        Returns:
            HealthCheckRequestModel instance
        """
        return HealthCheckRequestModel(**kwargs)

    @staticmethod
    def get_conversation_start_request_model(**kwargs) -> ConversationStartRequestModel:
        """
        Create a ConversationStartRequestModel with provided parameters.

        Args:
            **kwargs: Parameters for the model

        Returns:
            ConversationStartRequestModel instance
        """
        return ConversationStartRequestModel(**kwargs)


def get_request_models() -> RequestModels:
    """
    Get an instance of the request models container.

    Returns:
        RequestModels instance
    """
    return RequestModels()