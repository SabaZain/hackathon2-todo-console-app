"""
Chat Endpoint for Todo AI Chatbot API.

This module implements the FastAPI/FastHTML route for chat communication with JWT authentication.
"""

import os
from jose import jwt
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
import asyncio

from .request_models import ChatRequestModel
from .response_models import ChatResponseModel, ErrorResponseModel
from .validation import validate_chat_request
from .agent_connector import AgentConnector
from .conversation_manager import ConversationManager
from .user_messages import get_user_friendly_error
try:
    # Try relative import first (when running as part of the package)
    from ..security.auth_handler import get_auth_handler
except (ImportError, ValueError):
    # Handle direct execution by adding the parent to the path
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    from todochatbot.security.auth_handler import get_auth_handler


router = APIRouter(prefix="/api")
auth_handler = get_auth_handler(os.getenv("JWT_SECRET"))


def verify_jwt_token(authorization: str = Header(None)):
    """
    Verify the JWT token from the Authorization header.

    Args:
        authorization: The Authorization header value

    Returns:
        User ID if token is valid

    Raises:
        HTTPException if token is invalid
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: no user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


class ChatEndpoint:
    """Implementation of the chat API endpoint."""

    def __init__(self):
        """Initialize the chat endpoint with required services."""
        self.agent_connector = AgentConnector()
        self.conversation_manager = ConversationManager()

    async def chat_handler(self, user_id: str, request_data: Dict[str, Any], token_user_id: str = Depends(verify_jwt_token)) -> Dict[str, Any]:
        """
        Handle chat requests from users.

        Args:
            user_id: The ID of the requesting user
            request_data: The request payload
            token_user_id: User ID from JWT token (via dependency)

        Returns:
            Dictionary containing the API response
        """
        # Verify that the user_id in the URL matches the one in the token
        if user_id != token_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        try:
            # Validate the request
            is_valid, error_msg = validate_chat_request(request_data)
            if not is_valid:
                return ErrorResponseModel(error=error_msg).__dict__

            # Create request model from validated data
            chat_request = ChatRequestModel(
                conversation_id=request_data.get('conversation_id'),
                message=request_data['message'],
                user_id=user_id
            )

            # Create or get conversation ID
            conversation_id = chat_request.conversation_id or await self.conversation_manager.create_conversation(chat_request.user_id)

            # Process the message with the AI agent
            ai_response = await self.agent_connector.process_message(
                user_id=chat_request.user_id,
                conversation_id=conversation_id,
                message=chat_request.message
            )

            # Create response model
            response_model = ChatResponseModel(
                conversation_id=conversation_id,
                response=ai_response.get('response_text', 'I processed your message'),
                success=True,
                user_id=chat_request.user_id,
                intent=ai_response.get('intent', 'general')
            )

            # Store the interaction in conversation history using real database
            try:
                from ..database.conversations import save_message
            except (ImportError, ValueError):
                import sys
                import os
                current_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(current_dir)
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)

                from todochatbot.database.conversations import save_message

            save_message(user_id, conversation_id, chat_request.message, "user")
            save_message(user_id, conversation_id, response_model.response, "assistant")

            return response_model.__dict__

        except Exception as e:
            error_response = ErrorResponseModel(
                error=get_user_friendly_error(str(e)),
                success=False
            )
            return error_response.__dict__

    async def get_user_conversations(self, user_id: str, token_user_id: str = Depends(verify_jwt_token)):
        """
        Get a list of conversation IDs for a user.

        Args:
            user_id: The ID of the user
            token_user_id: User ID from JWT token (via dependency)

        Returns:
            List of conversation IDs
        """
        # Verify that the user_id in the URL matches the one in the token
        if user_id != token_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        try:
            from ..database.conversations import get_user_conversations as db_get_user_conversations
        except (ImportError, ValueError):
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            from todochatbot.database.conversations import get_user_conversations as db_get_user_conversations
        return db_get_user_conversations(user_id)

    async def get_conversation(self, user_id: str, conversation_id: str, token_user_id: str = Depends(verify_jwt_token)):
        """
        Get a specific conversation's history.

        Args:
            user_id: The ID of the user
            conversation_id: The conversation ID
            token_user_id: User ID from JWT token (via dependency)

        Returns:
            List of messages in the conversation
        """
        # Verify that the user_id in the URL matches the one in the token
        if user_id != token_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        try:
            from ..database.conversations import load_conversation
        except (ImportError, ValueError):
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            from todochatbot.database.conversations import load_conversation
        messages = load_conversation(user_id, conversation_id)
        return {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "messages": messages
        }

    async def delete_conversation(self, user_id: str, conversation_id: str, token_user_id: str = Depends(verify_jwt_token)):
        """
        Delete a specific conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The conversation ID to delete
            token_user_id: User ID from JWT token (via dependency)

        Returns:
            Deletion confirmation
        """
        # Verify that the user_id in the URL matches the one in the token
        if user_id != token_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        try:
            from ..database.conversations import delete_conversation as db_delete_conversation
        except (ImportError, ValueError):
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            from todochatbot.database.conversations import delete_conversation as db_delete_conversation
        success = db_delete_conversation(user_id, conversation_id)

        if success:
            return {
                "success": True,
                "message": f"Conversation {conversation_id} deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")


# Create an instance of the chat endpoint
chat_endpoint = ChatEndpoint()


@router.post("/{user_id}/chat")
async def handle_chat_request(user_id: str, request_data: Dict[str, Any], token_user_id: str = Depends(verify_jwt_token)):
    """
    FastAPI endpoint for handling chat requests.

    Args:
        user_id: The ID of the requesting user (path parameter)
        request_data: The request payload (JSON body)
        token_user_id: User ID from JWT token (via dependency)

    Returns:
        JSON response with chat response
    """
    return await chat_endpoint.chat_handler(user_id, request_data, token_user_id)


@router.get("/{user_id}/conversations")
async def get_user_conversations(user_id: str, token_user_id: str = Depends(verify_jwt_token)):
    """
    Get a list of conversation IDs for a user.

    Args:
        user_id: The ID of the user
        token_user_id: User ID from JWT token (via dependency)

    Returns:
        List of conversation IDs
    """
    return await chat_endpoint.get_user_conversations(user_id, token_user_id)


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation(user_id: str, conversation_id: str, token_user_id: str = Depends(verify_jwt_token)):
    """
    Get a specific conversation's history.

    Args:
        user_id: The ID of the user
        conversation_id: The conversation ID
        token_user_id: User ID from JWT token (via dependency)

    Returns:
        List of messages in the conversation
    """
    return await chat_endpoint.get_conversation(user_id, conversation_id, token_user_id)


@router.delete("/{user_id}/conversations/{conversation_id}")
async def delete_conversation(user_id: str, conversation_id: str, token_user_id: str = Depends(verify_jwt_token)):
    """
    Delete a specific conversation.

    Args:
        user_id: The ID of the user
        conversation_id: The conversation ID to delete
        token_user_id: User ID from JWT token (via dependency)

    Returns:
        Deletion confirmation
    """
    return await chat_endpoint.delete_conversation(user_id, conversation_id, token_user_id)


@router.get("/{user_id}/health")
async def health_check(user_id: str, token_user_id: str = Depends(verify_jwt_token)):
    """
    Health check endpoint for the chat API.

    Args:
        user_id: The ID of the requesting user (path parameter)
        token_user_id: User ID from JWT token (via dependency)

    Returns:
        Health status
    """
    # Verify that the user_id in the URL matches the one in the token
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

    return {
        "status": "healthy",
        "service": "chat-api",
        "user_id": user_id,
        "timestamp": asyncio.get_event_loop().time()
    }


def get_router() -> APIRouter:
    """
    Get the FastAPI router for the chat endpoints.

    Returns:
        APIRouter instance containing the chat routes
    """
    return router


def create_chat_endpoint() -> ChatEndpoint:
    """
    Create and return a new instance of the chat endpoint.

    Returns:
        ChatEndpoint instance
    """
    return ChatEndpoint()