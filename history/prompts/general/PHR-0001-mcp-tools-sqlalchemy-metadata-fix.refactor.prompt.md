---
id: PHR-0001
title: "MCP Tools SQLAlchemy Metadata Fix"
stage: refactor
date: 2026-02-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: /sp.implement
labels: ["mcp", "sqlalchemy", "metadata", "conflict", "refactor", "database"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - D:\hackathontwo\todochatbot\mcp_tools\task_tools.py
  - D:\hackathontwo\todochatbot\mcp_tools\mcp_server.py
tests:
  - none
---

# MCP Tools SQLAlchemy Metadata Fix

## PROMPT_TEXT

```
You are working inside an existing full-stack Todo application with:
- FastAPI backend (SQLModel + PostgreSQL)
- Next.js frontend
- An AI chatbot integrated with frontend + backend
- MCP tools used by the chatbot for task CRUD operations

IMPORTANT CONTEXT:
- Backend, frontend, auth, database, and direct task APIs are fully working.
- Chatbot intent detection works.
- The ONLY broken part is MCP task tools (create/list/update/delete).
- Error observed at runtime:
  "Table 'user' is already defined for this MetaData instance"
  caused by SQLModel models being registered more than once.

STRICT RULES:
1. DO NOT change existing API routes, frontend code, auth logic, or database schema.
2. DO NOT modify working task APIs or chatbot intent logic.
3. DO NOT use extend_existing=True as a workaround.
4. DO NOT duplicate SQLModel model definitions.
5. Keep behavior and responses exactly the same — only fix MCP tool execution.

TASK:
Refactor MCP task tools so they:
- Do NOT directly import or redefine SQLModel models in a way that re-registers tables.
- Reuse the already-initialized SQLModel engine, metadata, and session used by FastAPI.
- Use a single shared database session source (e.g., backend db/session utility).
- Safely execute CRUD operations without triggering SQLAlchemy metadata conflicts.

IMPLEMENTATION REQUIREMENTS:
- Ensure models are imported from a single source of truth.
- Ensure MCP tools only run queries using an existing Session.
- Prevent circular imports and duplicate metadata registration.
- Backend must start normally.
- Chatbot MCP tools must successfully create and list tasks.

OUTPUT:
- Apply minimal, surgical code changes.
- Show only the files that need changes with exact code.
- Do not rewrite unrelated files.
- Final result: chatbot can create and list tasks via MCP tools without errors.

Proceed carefully and conservatively.
```

## RESPONSE_TEXT

Successfully refactored MCP task tools to fix SQLAlchemy metadata conflicts by updating imports to use the existing db_utils module instead of directly importing models, eliminating duplicate table registrations.

## OUTCOME_IMPACT

Fixed the "Table 'user' is already defined for this MetaData instance" error by refactoring the MCP tools to use the existing db_utils module that handles model loading safely. MCP tools now work without metadata conflicts while maintaining all existing functionality.

## TESTS_SUMMARY

Created and ran test script that verified imports work without metadata conflicts. Confirmed backend still starts normally and MCP tools can perform CRUD operations.

## FILES_SUMMARY

Modified task_tools.py to use db_utils functions instead of direct model imports. Updated mcp_server.py to fix parameter mapping.

## NEXT_PROMPTS

none

## REFLECTION_NOTE

Using existing utility modules designed for safe database operations prevented the metadata re-registration issue while maintaining all functionality.

## FAILURE MODES OBSERVED

None observed - the solution worked effectively by leveraging the existing db_utils module that was already designed to handle model loading safely.

## NEXT EXPERIMENT TO IMPROVE PROMPT QUALITY

Consider adding more emphasis on checking for existing utility modules that may already solve the problem before implementing new solutions.