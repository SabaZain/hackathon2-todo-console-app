# Backend Guidelines – Phase II

## Stack
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLModel or SQLAlchemy
- JWT-based Authentication

## Responsibilities
- API design and implementation
- Authentication and authorization
- Database schema and persistence
- Business logic enforcement
- API contracts for frontend

## Patterns
- Follow spec-driven development
- Do not mix frontend concerns
- Use routers for modular APIs
- Separate auth, domain, and infrastructure logic
- Validate all inputs using Pydantic models

## API Design
- RESTful endpoints
- JSON request/response only
- Proper HTTP status codes
- Version-ready structure (e.g. /api/v1)

## Authentication
- JWT access tokens
- Token verification middleware/dependency
- No frontend logic in backend

## Database
- User and Todo domain models
- Enforce ownership at query level
- No hardcoded credentials

## Agents & Skills
- Reference backend agents from root .claude/agents
- Reference backend skills from root .claude/skills

## Instructions for Claude
- Do NOT write any backend code yet
- Do NOT create database schemas yet
- Only create the folder and files
- Ensure correct placement inside fullstackwebapp/backend
- Confirm once the structure is created

## Prompt History Discipline
- After every `/sp.*` command, the full prompt must be saved
- Save location: backend/history/prompts/
- History is mandatory for all backend phases
- History is documentation, not source of truth