# Confirmation Message Skill

This skill generates confirmation messages after successful todo operations.

## Responsibilities

- Generate confirmation messages for task creation
- Generate confirmation messages for updates and deletions
- Generate confirmation messages for task completion
- Maintain a consistent and friendly response tone

## Scope Limitations

- Do not call MCP tools
- Do not detect user intent
- Do not manage conversation history
- Do not access the database

## Core Guidelines

1. Always confirm successful actions
2. Keep messages short and friendly
3. Avoid technical or system language
4. Use consistent phrasing patterns

## Reusability

This skill can be reused in any chatbot or assistant that requires action confirmations.

## Implementation Constraints

- Stateless execution
- No business logic