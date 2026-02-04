# Phase 3 Chat API Specification: Todo AI Chatbot

This specification defines the chat API endpoint for the AI-powered chatbot integration into the existing Todo Web Application.

---

## Endpoint Overview

- **Endpoint URL**: /api/{user_id}/chat
- **HTTP Method**: POST
- **Purpose**: Receive user messages in natural language, pass them to the AI agent, and return responses including MCP tool actions.

---

## Request Specification

### Path Parameters
- **user_id** (string, required): The identifier of the current user.

### Request Body
- **conversation_id** (integer, optional): Existing conversation ID. If not provided, a new conversation is created.
- **message** (string, required): The user's natural language message.

### Example Request
```json
{
  "conversation_id": 12,
  "message": "Add a task to buy groceries"
}
```