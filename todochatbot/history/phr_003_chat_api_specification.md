# Prompt History Record (PHR)

**Date:** 2026-01-22

**Command Executed:** Create Chat API Specification for Todo AI Chatbot

**Original Prompt:**
/sp.spec chat-api

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

**Agents Involved:**
- None

**Skills Used:**
- File creation skill

**Changes Introduced:**
- Created chat-api-specification.md file in the specs directory
- Defined the chat API endpoint specification
- Specified path parameters and request body structure
- Provided example request format

**Summary:**
Created the detailed specification for the chat API endpoint that will handle communication between the frontend chat interface and the AI agent. The API allows users to send natural language messages that will be processed by the AI to perform todo operations via MCP tools.

**Status:** Completed