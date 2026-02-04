# MCP Tools for Todo AI Chatbot

This directory contains the Model Context Protocol (MCP) tools that enable AI agents to manage todo tasks through natural language interactions.

## Overview

The MCP tools provide a standardized interface for AI agents to interact with the todo management system. These tools are stateless and operate through database operations, ensuring all task data is persisted properly.

## Available Tools

### `add_task`
Create a new task for a user.

**Parameters:**
- `user_id` (string): The user's ID
- `title` (string): The task title
- `description` (string, optional): The task description

**Returns:**
- `task_id`: The ID of the created task
- `status`: "created"
- `title`: The title of the created task

### `list_tasks`
Retrieve tasks for a user.

**Parameters:**
- `user_id` (string): The user's ID
- `status` (string, optional): Filter by status ('all', 'pending', 'completed')

**Returns:**
- List of task objects with `id`, `title`, and `completed` status

### `complete_task`
Mark a task as completed.

**Parameters:**
- `user_id` (string): The user's ID
- `task_id` (integer): The ID of the task to complete

**Returns:**
- `task_id`: The ID of the completed task
- `status`: "completed"
- `title`: The title of the completed task

### `delete_task`
Delete a task.

**Parameters:**
- `user_id` (string): The user's ID
- `task_id` (integer): The ID of the task to delete

**Returns:**
- `task_id`: The ID of the deleted task
- `status`: "deleted"
- `title`: The title of the deleted task

### `update_task`
Update task title or description.

**Parameters:**
- `user_id` (string): The user's ID
- `task_id` (integer): The ID of the task to update
- `title` (string, optional): New task title
- `description` (string, optional): New task description

**Returns:**
- `task_id`: The ID of the updated task
- `status`: "updated"
- `title`: The title of the updated task

## Architecture

The MCP tools interact with the existing backend system:
- All data is stored in the same database used by the web application
- Authentication and user isolation are maintained
- Tools are stateless and rely on database persistence
- Error handling is implemented for robust operation

## Usage

The tools are designed to be used by AI agents via the MCP protocol. The server (`mcp_server.py`) handles incoming requests and routes them to the appropriate tool functions.

## Testing

Run the test suite to verify all tools work correctly:

```bash
python test_mcp_tools.py
```

## Security

- User isolation is enforced - users can only operate on their own tasks
- Input validation is performed on all parameters
- Proper error handling prevents information disclosure

## Dependencies

- fastapi
- sqlmodel
- uvicorn
- pydantic
- SQLAlchemy
- psycopg2-binary (for PostgreSQL)