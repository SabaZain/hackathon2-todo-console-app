# FastAPI REST Skill

This skill defines how to implement RESTful API endpoints using FastAPI based on project specs.

## Responsibilities

- Implement CRUD operations for tasks
- Handle request validation and response schemas
- Integrate JWT authentication dependencies
- Enforce HTTP status codes and error handling
- Ensure endpoints strictly follow spec-driven development

## Scope Limitations

- Do not design frontend UI
- Do not handle database schema beyond API interaction
- Do not implement authentication logic itself

## Core Guidelines

1. **RESTful Design**: Follow REST conventions (verbs, resource-based URLs)
2. **Spec-Driven Implementation**: Implement endpoints as described in specifications
3. **Validation**: Use Pydantic models for input/output
4. **Error Handling**: Proper HTTP exceptions for all edge cases
5. **Authentication Integration**: Use dependencies/middleware from Auth skill

## Reusability

This skill can be applied to any FastAPI project needing spec-driven REST endpoints.

## Implementation Constraints

- No frontend/UI logic
- No database model creation beyond access through DB skill