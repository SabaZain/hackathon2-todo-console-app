"""
User Messages for Todo AI Chatbot API.

This module provides user-friendly error messages for the chatbot API.
"""

from typing import Dict, Any, Optional
from enum import Enum


class UserMessageType(Enum):
    """Enumeration of different types of user messages."""
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SYSTEM = "system"


def get_user_friendly_error(error_code: str) -> str:
    """
    Get a user-friendly error message based on the error code.

    Args:
        error_code: The error code or message from the system

    Returns:
        User-friendly error message
    """
    error_mappings = {
        # Connection and network errors
        "connection refused": "We're having trouble connecting to our services. Please check your internet connection and try again.",
        "timeout": "The request took too long to process. Please try again in a moment.",
        "network error": "There's a network issue preventing us from processing your request. Please check your connection and try again.",

        # Agent-related errors
        "agent unavailable": "The AI assistant is currently busy. Please try again in a moment.",
        "agent timeout": "The AI assistant is taking too long to respond. Please try rephrasing your request.",

        # Database errors
        "database connection failed": "We're experiencing database issues. Our team has been notified and is working on fixing the problem.",
        "database error": "There was an issue accessing your data. Please try again later.",

        # Validation errors
        "invalid request": "Your request seems to have some issues. Please check your input and try again.",
        "validation failed": "Some information in your request is not quite right. Please verify and try again.",

        # Authorization errors
        "unauthorized": "You don't have permission to perform this action. Please make sure you're logged in.",
        "authentication failed": "We couldn't verify your identity. Please log in again.",

        # Conversation errors
        "conversation not found": "We couldn't find your conversation. Please start a new chat.",
        "conversation expired": "Your conversation has expired. Please start a new chat.",

        # Task-related errors
        "task not found": "We couldn't find that task. Please check the task details and try again.",
        "task creation failed": "There was an issue creating your task. Please try again.",
        "task update failed": "There was an issue updating your task. Please try again.",

        # MCP tool errors
        "mcp tool unavailable": "The task management system is temporarily unavailable. Please try again later.",
        "tool execution failed": "There was an issue processing your request. Please try again.",
    }

    # Normalize the error code for comparison
    normalized_error = error_code.lower().strip()

    # Check for exact matches first
    if normalized_error in error_mappings:
        return error_mappings[normalized_error]

    # Check for partial matches
    for error_key, user_message in error_mappings.items():
        if error_key in normalized_error:
            return user_message

    # Default generic message
    return "We encountered an unexpected issue while processing your request. Please try again or rephrase your request."


def get_success_message(operation: str, details: Optional[Dict[str, Any]] = None) -> str:
    """
    Get a user-friendly success message based on the operation performed.

    Args:
        operation: The operation that was successful
        details: Optional details about the operation

    Returns:
        User-friendly success message
    """
    success_messages = {
        "create_task": "Your task has been successfully added!",
        "update_task": "Your task has been successfully updated!",
        "complete_task": "Great job! The task has been marked as completed.",
        "delete_task": "The task has been successfully removed.",
        "list_tasks": "Here are your tasks:",
        "start_conversation": "Hello! I'm ready to help you manage your tasks. What would you like to do?",
        "continue_conversation": "I understand. How else can I help you?",
    }

    return success_messages.get(operation, "Operation completed successfully!")


def get_info_message(info_type: str, details: Optional[Dict[str, Any]] = None) -> str:
    """
    Get an informative message for the user.

    Args:
        info_type: The type of information message
        details: Optional details to include

    Returns:
        Informative message
    """
    info_messages = {
        "loading": "Processing your request...",
        "thinking": "Thinking about your request...",
        "searching": "Looking up information for you...",
        "connecting": "Connecting to the task management system...",
        "saving": "Saving your information...",
        "processing": "Processing your request...",
    }

    return info_messages.get(info_type, "Processing...")


def get_warning_message(warning_type: str, details: Optional[Dict[str, Any]] = None) -> str:
    """
    Get a user-friendly warning message.

    Args:
        warning_type: The type of warning
        details: Optional details about the warning

    Returns:
        User-friendly warning message
    """
    warning_messages = {
        "rate_limit": "You're sending requests very quickly. Please slow down a bit.",
        "deprecated_feature": "This feature is being updated. Please use the new method instead.",
        "temporary_issue": "We're experiencing a temporary issue with this function. Please try again later.",
        "data_privacy": "Your data is safe with us. We don't store personal information unnecessarily.",
    }

    return warning_messages.get(warning_type, "Please note: This function is still being improved.")


def format_user_message(message_type: UserMessageType, content: str,
                       details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Format a user message with appropriate styling and structure.

    Args:
        message_type: The type of message
        content: The message content
        details: Optional additional details

    Returns:
        Formatted message dictionary
    """
    message_formats = {
        UserMessageType.SUCCESS: {
            "type": "success",
            "icon": "✅",
            "style_class": "message-success",
            "content": content
        },
        UserMessageType.INFO: {
            "type": "info",
            "icon": "ℹ️",
            "style_class": "message-info",
            "content": content
        },
        UserMessageType.WARNING: {
            "type": "warning",
            "icon": "⚠️",
            "style_class": "message-warning",
            "content": content
        },
        UserMessageType.ERROR: {
            "type": "error",
            "icon": "❌",
            "style_class": "message-error",
            "content": content
        },
        UserMessageType.SYSTEM: {
            "type": "system",
            "icon": "🤖",
            "style_class": "message-system",
            "content": content
        }
    }

    formatted_message = message_formats.get(message_type, message_formats[UserMessageType.INFO]).copy()

    if details:
        formatted_message["details"] = details

    return formatted_message


def get_common_responses(intent: str) -> str:
    """
    Get common responses for specific intents.

    Args:
        intent: The detected intent

    Returns:
        Appropriate response for the intent
    """
    common_responses = {
        "greeting": "Hello! I'm your AI assistant for managing tasks. How can I help you today?",
        "goodbye": "Goodbye! Feel free to come back anytime you need help with your tasks.",
        "thank_you": "You're welcome! Is there anything else I can help you with?",
        "help": "I can help you manage your tasks. You can ask me to add, list, update, or complete tasks. What would you like to do?",
        "unknown": "I'm not sure I understood that. I can help with managing your tasks - like adding, listing, or updating them. Could you please rephrase?",
        "add_task": "Sure! What task would you like to add?",
        "list_tasks": "I can list your tasks for you. Would you like to see all tasks, pending tasks, or completed tasks?",
        "update_task": "What task would you like to update, and what changes would you like to make?",
        "complete_task": "Which task would you like to mark as completed?",
    }

    return common_responses.get(intent, common_responses["unknown"])


def get_conversation_starter() -> str:
    """
    Get a message to start a conversation.

    Returns:
        Conversation starter message
    """
    starters = [
        "Hi there! I'm your AI assistant for managing tasks. What would you like to do today?",
        "Hello! I'm here to help you manage your tasks. Just tell me what you'd like to do.",
        "Greetings! I can help you add, list, update, or complete tasks. How can I assist you?",
    ]

    return starters[0]  # Returning first option, in a real app could randomize


def get_typical_user_errors() -> Dict[str, str]:
    """
    Get common user errors and suggested corrections.

    Returns:
        Dictionary mapping common errors to suggestions
    """
    return {
        "vague_request": {
            "error": "Your request is a bit vague",
            "suggestion": "Try being more specific. For example: 'Add a task to buy groceries' or 'List my pending tasks'"
        },
        "missing_task_details": {
            "error": "Missing details for the task",
            "suggestion": "Please provide more information about the task you want to create"
        },
        "unclear_reference": {
            "error": "Unclear reference to a task",
            "suggestion": "Please specify which task you mean by providing more details or the task number"
        }
    }