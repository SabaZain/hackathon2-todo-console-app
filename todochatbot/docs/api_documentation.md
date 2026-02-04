# Todo AI Chatbot API Documentation

## Overview
The Todo AI Chatbot provides a natural language interface to manage tasks through a RESTful API. The API allows users to interact with their todo lists using conversational language.

## Base URL
```
https://your-domain.com/api
```

## Authentication
All API requests require authentication using a Bearer token in the Authorization header:

```
Authorization: Bearer {your-jwt-token}
```

## Endpoints

### POST /{user_id}/chat
Send a message to the AI chatbot and receive a response.

#### Path Parameters
- `user_id` (string): The unique identifier for the user

#### Request Body
```json
{
  "conversation_id": "string",
  "message": "string",
  "timestamp": "string (optional)"
}
```

#### Response
```json
{
  "success": "boolean",
  "response": "string",
  "action": "string",
  "task_data": "object (optional)",
  "conversation_id": "string",
  "timestamp": "string"
}
```

#### Example Request
```bash
curl -X POST "https://your-domain.com/api/user123/chat" \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv456",
    "message": "Add a task to buy groceries tomorrow"
  }'
```

#### Example Response
```json
{
  "success": true,
  "response": "Task 'buy groceries' added for tomorrow.",
  "action": "create_task",
  "task_data": {
    "id": "task789",
    "description": "buy groceries",
    "due_date": "2026-01-24",
    "priority": "medium"
  },
  "conversation_id": "conv456",
  "timestamp": "2026-01-23T10:30:00Z"
}
```

### GET /{user_id}/conversations
Retrieve a list of user's conversations.

#### Path Parameters
- `user_id` (string): The unique identifier for the user

#### Query Parameters
- `limit` (integer, optional): Maximum number of conversations to return (default: 10)
- `offset` (integer, optional): Number of conversations to skip (default: 0)

#### Response
```json
{
  "success": "boolean",
  "conversations": [
    {
      "id": "string",
      "title": "string",
      "created_at": "string",
      "updated_at": "string",
      "message_count": "integer"
    }
  ],
  "total_count": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

### GET /{user_id}/conversations/{conversation_id}
Retrieve a specific conversation's history.

#### Path Parameters
- `user_id` (string): The unique identifier for the user
- `conversation_id` (string): The conversation identifier

#### Query Parameters
- `limit` (integer, optional): Maximum number of messages to return (default: 50)
- `offset` (integer, optional): Number of messages to skip (default: 0)

#### Response
```json
{
  "success": "boolean",
  "conversation": {
    "id": "string",
    "user_id": "string",
    "messages": [
      {
        "id": "string",
        "role": "string (user|assistant)",
        "content": "string",
        "timestamp": "string"
      }
    ],
    "created_at": "string",
    "updated_at": "string"
  }
}
```

### DELETE /{user_id}/conversations/{conversation_id}
Delete a specific conversation.

#### Path Parameters
- `user_id` (string): The unique identifier for the user
- `conversation_id` (string): The conversation identifier

#### Response
```json
{
  "success": "boolean",
  "message": "string"
}
```

## Task Management Endpoints

### GET /{user_id}/tasks
Retrieve user's tasks.

#### Query Parameters
- `status` (string, optional): Filter by status (all, pending, completed)
- `priority` (string, optional): Filter by priority (low, medium, high)
- `limit` (integer, optional): Maximum number of tasks to return
- `offset` (integer, optional): Number of tasks to skip

#### Response
```json
{
  "success": "boolean",
  "tasks": [
    {
      "id": "string",
      "description": "string",
      "status": "string",
      "priority": "string",
      "due_date": "string (optional)",
      "created_at": "string",
      "updated_at": "string"
    }
  ],
  "total_count": "integer"
}
```

### POST /{user_id}/tasks
Create a new task.

#### Request Body
```json
{
  "description": "string",
  "due_date": "string (optional)",
  "priority": "string (optional)",
  "category": "string (optional)"
}
```

#### Response
```json
{
  "success": "boolean",
  "task": {
    "id": "string",
    "description": "string",
    "status": "pending",
    "priority": "string",
    "due_date": "string (optional)",
    "created_at": "string",
    "updated_at": "string"
  }
}
```

## Error Responses

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

Common error codes:
- `AUTHENTICATION_ERROR`: Invalid or missing authentication token
- `VALIDATION_ERROR`: Invalid request parameters
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server-side error

## Rate Limits
- Requests are limited to 100 per hour per user
- Chat messages are limited to 10 per minute per conversation

## Webhook Events
The API can send webhook events to your configured endpoint for task updates. Events include:
- `task.created`
- `task.updated`
- `task.completed`
- `task.deleted`

## Client Libraries

### JavaScript/Node.js
```javascript
const { TodoChatClient } = require('@todo-chat/client');

const client = new TodoChatClient({
  baseUrl: 'https://your-domain.com/api',
  token: 'your-jwt-token'
});

// Send a message
const response = await client.sendMessage('user123', 'conv456', 'Add a task to buy groceries');
```

### Python
```python
from todo_chat_client import TodoChatClient

client = TodoChatClient(
    base_url='https://your-domain.com/api',
    token='your-jwt-token'
)

# Send a message
response = client.send_message('user123', 'conv456', 'Add a task to buy groceries')
```

## Best Practices

1. **Batch Requests**: When possible, batch multiple operations into a single conversation to reduce API calls.

2. **Handle Rate Limits**: Implement exponential backoff when encountering rate limit errors.

3. **Secure Token Storage**: Store JWT tokens securely and refresh them as needed.

4. **Validate Inputs**: Always validate user inputs before sending to the API to prevent injection attacks.

5. **Monitor Usage**: Monitor API usage to optimize performance and costs.

## Troubleshooting

### Common Issues
- **Slow Response Times**: May indicate heavy server load or complex natural language processing
- **Authentication Failures**: Verify token validity and proper header formatting
- **Unexpected Behavior**: Natural language processing may misinterpret complex or ambiguous requests

### Support
For API support, contact api-support@todo-chatbot.com with your user ID and request details.