"""
API Contract for Todo AI Chatbot.

This module defines the contract for the chat API endpoint.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ChatRequest:
    """Contract for chat API request."""
    conversation_id: Optional[str] = None
    message: str = ""
    user_id: str = ""


@dataclass
class ChatResponse:
    """Contract for chat API response."""
    conversation_id: str = ""
    response: str = ""
    success: bool = True
    error: Optional[str] = None


class ChatAPIContract:
    """Defines the contract for the chat API endpoint."""

    @staticmethod
    def get_endpoint_path() -> str:
        """
        Get the endpoint path for the chat API.

        Returns:
            String representing the API endpoint path
        """
        return "/api/{user_id}/chat"

    @staticmethod
    def get_supported_methods() -> list:
        """
        Get the supported HTTP methods for the chat API.

        Returns:
            List of supported HTTP methods
        """
        return ["POST"]

    @staticmethod
    def validate_request(request_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate the incoming request data.

        Args:
            request_data: Dictionary containing request data

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ["message"]

        for field in required_fields:
            if field not in request_data:
                return False, f"Missing required field: {field}"

        if not isinstance(request_data["message"], str) or not request_data["message"].strip():
            return False, "Message field must be a non-empty string"

        return True, None

    @staticmethod
    def create_response(conversation_id: str, response_text: str, success: bool = True, error: Optional[str] = None) -> ChatResponse:
        """
        Create a standardized response object.

        Args:
            conversation_id: The ID of the conversation
            response_text: The response text from the AI
            success: Whether the operation was successful
            error: Optional error message

        Returns:
            ChatResponse object
        """
        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            success=success,
            error=error
        )


def get_chat_contract() -> ChatAPIContract:
    """
    Get an instance of the chat API contract.

    Returns:
        ChatAPIContract instance
    """
    return ChatAPIContract()