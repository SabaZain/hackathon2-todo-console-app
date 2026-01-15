# JWT Verification Skill

This skill defines how to validate JWT tokens in the FastAPI backend.

## Responsibilities

- Verify JWT tokens issued by Better Auth
- Decode token to extract user ID and claims
- Enforce authorization for protected endpoints
- Reject invalid or expired tokens

## Scope Limitations

- Do not implement API endpoints
- Do not create frontend authentication logic
- Do not manage database models

## Core Guidelines

1. **Security**: Validate signatures using the shared secret
2. **User Isolation**: Ensure only authenticated user accesses their resources
3. **Expiration Handling**: Reject expired tokens with proper HTTP status
4. **Reusability**: Implement as reusable dependency or middleware for FastAPI

## Reusability

This skill can be reused across all protected API routes in FastAPI projects using JWT.

## Implementation Constraints

- No frontend code
- No database creation
- Implementation-agnostic JWT verification