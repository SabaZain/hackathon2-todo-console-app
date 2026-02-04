# Task Extraction Skill

This skill extracts task-related information from user messages for todo operations.

## Responsibilities

- Extract task title from natural language input
- Extract task_id when mentioned by the user
- Extract task description if provided
- Extract task status filters (all, pending, completed)

## Scope Limitations

- Do not detect user intent
- Do not call MCP tools
- Do not access the database
- Do not generate responses for the user

## Core Guidelines

1. Extract only information explicitly mentioned by the user
2. Do not invent or assume missing values
3. Return structured data suitable for MCP tools
4. If required data is missing, notify the calling agent

## Reusability

This skill can be reused in any task-based or CRUD-oriented conversational system.

## Implementation Constraints

- Stateless execution
- No business logic