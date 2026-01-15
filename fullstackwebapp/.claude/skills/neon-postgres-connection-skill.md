# Neon PostgreSQL Connection Skill

This skill defines how to connect and configure Neon PostgreSQL database in FastAPI backend.

## Responsibilities

- Establish connection to Neon PostgreSQL
- Manage environment-based configuration
- Ensure secure connection without hardcoded credentials
- Support transactions and session management

## Scope Limitations

- Do not define SQLModel models
- Do not implement API endpoints
- Do not handle frontend logic

## Core Guidelines

1. **Environment Variables**: Use DATABASE_URL from environment
2. **Secure Connections**: Avoid hardcoded credentials
3. **Session Management**: Handle connection sessions efficiently
4. **Reusability**: Provide a reusable database session for other backend skills

## Reusability

Reusable for any FastAPI backend requiring Neon PostgreSQL connectivity.

## Implementation Constraints

- No frontend/UI code
- No JWT/auth logic
- Implementation-agnostic connection handling