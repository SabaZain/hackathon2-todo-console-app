"""
Chat Endpoint for Todo AI Chatbot API.

This module implements the FastAPI routes for chat communication with JWT authentication.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
import asyncio
from datetime import datetime

# Import the authentication function
try:
    from ..auth import get_current_user_id
except (ImportError, ValueError):
    # Fallback to absolute import if relative import fails
    from auth import get_current_user_id

# Import the agent connector to process messages with AI
try:
    from .agent_connector import get_agent_connector
except ImportError:
    # Fallback to absolute import if relative import fails
    from backend.api.agent_connector import get_agent_connector

# Import database functions for conversation persistence
try:
    from ..database.conversations import (
        save_message,
        create_conversation as db_create_conversation,
        get_user_conversations as db_get_user_conversations,
        load_conversation as db_load_conversation,
        delete_conversation as db_delete_conversation
    )
    from ..db import get_session
except (ImportError, ValueError):
    # Fallback to absolute import if relative import fails
    try:
        from database.conversations import (
            save_message,
            create_conversation as db_create_conversation,
            get_user_conversations as db_get_user_conversations,
            load_conversation as db_load_conversation,
            delete_conversation as db_delete_conversation
        )
        from db import get_session
    except ImportError:
        # Last resort: import directly
        from backend.database.conversations import (
            save_message,
            create_conversation as db_create_conversation,
            get_user_conversations as db_get_user_conversations,
            load_conversation as db_load_conversation,
            delete_conversation as db_delete_conversation
        )
        from backend.db import get_session

router = APIRouter()


@router.post("/{user_id}/chat")
async def handle_chat_request(user_id: str, request_data: Dict[str, Any], current_user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    FastAPI endpoint for handling chat requests with JWT authentication.

    Args:
        user_id: The ID of the requesting user (path parameter)
        request_data: The request payload (JSON body)
        current_user_id: User ID from JWT token (via dependency)
        session: Database session dependency

    Returns:
        JSON response with chat response
    """
    try:
        # Verify that the user_id in the URL matches the one in the token
        path_user_id = int(user_id)

        if path_user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        # Extract message from request data
        message = request_data.get('message', '')
        conversation_id = request_data.get('conversation_id')

        # If no conversation_id provided, create a new conversation
        if not conversation_id:
            conversation_id = db_create_conversation(str(current_user_id))
        else:
            # Ensure conversation exists before saving messages
            from ..database.conversations import db_manager
            db_manager.ensure_conversation_exists(conversation_id, str(current_user_id))

        # Get the agent connector and process the message through the AI agent
        agent_connector = get_agent_connector()

        # Process the message with the AI agent, passing the database session
        ai_response = await agent_connector.process_message(
            user_id=str(current_user_id),
            conversation_id=conversation_id,
            message=message,
            session=session
        )

        # Extract response text and other data from AI response
        response_text = ai_response.get('response_text', 'No response generated')
        tool_calls = ai_response.get('tool_calls', [])
        intent = ai_response.get('intent', 'general')

        # Save user message to database with error handling
        try:
            save_message(user_id=str(current_user_id), conversation_id=conversation_id, content=message, role='user')

            # Only save AI response if user message was saved successfully
            save_message(user_id=str(current_user_id), conversation_id=conversation_id, content=response_text, role='assistant')

            # Create the response data with proper structure (after successful save)
            response_data = {
                "conversation_id": conversation_id,
                "user_id": current_user_id,
                "message": message,
                "response": response_text,
                "tool_calls": tool_calls,
                "intent": intent,
                "timestamp": datetime.utcnow().isoformat(),
                "success": True,
                "message_saved": True,
                "ai_response_saved": True
            }

        except Exception as e:
            # If saving user message fails, log the error but don't attempt to save assistant message
            print(f"Error saving messages to database: {str(e)}")

            # Create the response data with proper structure (even when save fails)
            response_data = {
                "conversation_id": conversation_id,
                "user_id": current_user_id,
                "message": message,
                "response": response_text,
                "tool_calls": tool_calls,
                "intent": intent,
                "timestamp": datetime.utcnow().isoformat(),
                "success": True,
                "message_saved": False,
                "ai_response_saved": False,
                "db_error": str(e)
            }
            return response_data

        # Create the response data with proper structure
        response_data = {
            "conversation_id": conversation_id,
            "user_id": current_user_id,
            "message": message,
            "response": response_text,
            "tool_calls": tool_calls,
            "intent": intent,
            "timestamp": datetime.utcnow().isoformat(),
            "success": True
        }

        return response_data

    except ValueError:
        # Return proper JSON response format for frontend with meaningful response
        # Detect if the input was in Urdu for appropriate response
        is_urdu = _is_urdu_text(message if 'message' in locals() else '')

        if is_urdu:
            response_text = "Maaf kijeye, main aapki request ko samajh nahi pa raha. Kripya sahi tarah se poochhen."
        else:
            response_text = "I encountered an issue processing your request. Please try again with a different phrasing."

        response_data = {
            "conversation_id": conversation_id if 'conversation_id' in locals() else f"conv_{current_user_id}_{int(asyncio.get_event_loop().time())}",
            "user_id": current_user_id,
            "message": message if 'message' in locals() else '',
            "response": response_text,
            "tool_calls": [],
            "intent": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "success": False
        }
        return response_data
    except Exception as e:
        # Return proper JSON response with meaningful response
        is_urdu = _is_urdu_text(message if 'message' in locals() else '')

        if is_urdu:
            response_text = "Maaf kijeye, main aapki request ko samajh nahi pa raha. Kripya sahi tarah se poochhen."
        else:
            response_text = "I encountered an issue processing your request. Please try again with a different phrasing."

        response_data = {
            "conversation_id": conversation_id if 'conversation_id' in locals() else f"conv_{current_user_id}_{int(asyncio.get_event_loop().time())}",
            "user_id": current_user_id,
            "message": message if 'message' in locals() else '',
            "response": response_text,
            "tool_calls": [],
            "intent": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "success": False
        }
        return response_data


def _is_urdu_text(text: str) -> bool:
    """
    Detect if the input text contains Urdu characters.

    Args:
        text: Input text to check

    Returns:
        Boolean indicating if Urdu text is detected
    """
    # Urdu Unicode range: U+0600-U+06FF (Arabic/Persian characters used in Urdu)
    urdu_chars = [char for char in text if '\u0600' <= char <= '\u06FF']
    # If more than 20% of the characters are Urdu, consider it Urdu text
    if len(text.strip()) == 0:
        return False
    return len(urdu_chars) / len(text.replace(' ', '')) > 0.2


@router.get("/{user_id}/conversations")
async def get_user_conversations(user_id: str, current_user_id: int = Depends(get_current_user_id)):
    """
    Get a list of conversation IDs for a user.

    Args:
        user_id: The ID of the user (path parameter)
        current_user_id: User ID from JWT token (via dependency)

    Returns:
        List of conversation IDs
    """
    try:
        # Verify that the user_id in the URL matches the one in the token
        path_user_id = int(user_id)

        if path_user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        # Get conversations from database
        conversations = db_get_user_conversations(str(current_user_id))

        return {
            "user_id": current_user_id,
            "conversations": conversations,
            "total_count": len(conversations),
            "success": True
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id: must be a number")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_history(user_id: str, conversation_id: str, current_user_id: int = Depends(get_current_user_id)):
    """
    Get the history of a specific conversation.

    Args:
        user_id: The ID of the user (path parameter)
        conversation_id: The ID of the conversation (path parameter)
        current_user_id: User ID from JWT token (via dependency)

    Returns:
        List of messages in the conversation
    """
    try:
        # Verify that the user_id in the URL matches the one in the token
        path_user_id = int(user_id)

        if path_user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        # Get conversation history from database
        messages = db_load_conversation(str(current_user_id), conversation_id)

        return {
            "conversation_id": conversation_id,
            "user_id": current_user_id,
            "messages": messages,
            "message_count": len(messages),
            "success": True
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id: must be a number")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{user_id}/conversations/{conversation_id}")
async def delete_conversation(user_id: str, conversation_id: str, current_user_id: int = Depends(get_current_user_id)):
    """
    Delete a specific conversation.

    Args:
        user_id: The ID of the user (path parameter)
        conversation_id: The ID of the conversation to delete (path parameter)
        current_user_id: User ID from JWT token (via dependency)

    Returns:
        Deletion confirmation
    """
    try:
        # Verify that the user_id in the URL matches the one in the token
        path_user_id = int(user_id)

        if path_user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        # Delete conversation from database
        success = db_delete_conversation(str(current_user_id), conversation_id)

        if not success:
            raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")

        return {
            "conversation_id": conversation_id,
            "user_id": current_user_id,
            "deleted": True,
            "message": f"Conversation {conversation_id} deleted successfully",
            "success": True
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id: must be a number")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{user_id}/history")
async def get_user_history(user_id: str, current_user_id: int = Depends(get_current_user_id)):
    """
    Get the complete history of interactions for a user.

    Args:
        user_id: The ID of the user (path parameter)
        current_user_id: User ID from JWT token (via dependency)

    Returns:
        Complete history of interactions
    """
    try:
        # Verify that the user_id in the URL matches the one in the token
        path_user_id = int(user_id)

        if path_user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Forbidden: user ID mismatch")

        # Get all conversations from database to build history
        conversations = db_get_user_conversations(str(current_user_id))

        # Build history from all conversations
        interactions = []
        total_interactions = 0

        for conv in conversations:
            messages = db_load_conversation(str(current_user_id), conv['id'])
            for msg in messages:
                interactions.append({
                    "id": msg['id'],
                    "type": "chat" if msg['role'] == 'user' else 'response',
                    "conversation_id": conv['id'],
                    "summary": f"{msg['role']}: {msg['content'][:50]}...",
                    "timestamp": msg['timestamp']
                })
            total_interactions += len(messages)

        history = {
            "user_id": current_user_id,
            "interactions": interactions,
            "total_interactions": total_interactions,
            "success": True
        }

        return history

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id: must be a number")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")




# Create and return the router
def get_router() -> APIRouter:
    """
    Get the FastAPI router for the chat endpoints.

    Returns:
        APIRouter instance containing the chat routes
    """
    return router