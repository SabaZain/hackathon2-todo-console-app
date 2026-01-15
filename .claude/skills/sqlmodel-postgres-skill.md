# SQLModel PostgreSQL Skill

This skill defines how to model and interact with PostgreSQL using SQLModel.

## Responsibilities

- Define SQLModel models for tasks and related entities
- Manage CRUD operations with user-level scoping
- Handle relationships, indexes, and constraints
- Implement queries for filtering, sorting, and task ownership

## Scope Limitations

- Do not implement API endpoints
- Do not handle frontend logic
- Do not manage JWT authentication

## Core Guidelines

1. **SQLModel Best Practices**: Use SQLModel for all database operations
2. **User Ownership Enforcement**: All queries respect the authenticated user
3. **Data Integrity**: Maintain constraints and consistency
4. **Indexes**: Optimize common queries with appropriate indexes
5. **Connection via DB Skill**: Use database connection patterns from DB connection skill

## Reusability

Can be reused for any FastAPI + PostgreSQL project requiring SQLModel-based database access.

## Implementation Constraints

- No UI logic
- No endpoint definitions
- Implementation-agnostic SQLModel usage