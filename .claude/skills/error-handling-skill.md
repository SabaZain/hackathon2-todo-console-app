# Error Handling Skill

This skill ensures graceful handling of errors during todo operations.

## Responsibilities

- Handle task not found scenarios
- Handle invalid or missing input data
- Convert system and tool errors into user-safe signals
- Prevent crashes or unhandled exceptions

## Scope Limitations

- Do not retry failed operations
- Do not expose system or database error details
- Do not perform task operations

## Core Guidelines

1. Never leak internal error details
2. Always provide a clear error reason
3. Suggest corrective action when possible
4. Keep error handling consistent across actions

## Reusability

This skill can be reused in any application requiring robust and user-friendly error handling.

## Implementation Constraints

- Stateless logic
- No UI logic