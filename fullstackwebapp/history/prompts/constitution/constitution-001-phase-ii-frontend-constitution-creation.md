---
id: constitution-001
title: Phase II Frontend Constitution Creation
stage: constitution
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-frontend-todo-app
user: Saba Zain
command: /sp.constitution
labels: ["constitution", "frontend", "governance", "specification"]
links_spec: null
links_ticket: null
links_adr: null
links_pr: null
files_yaml:
 - .specify/memory/constitution.md
tests_yaml:
 - none
---

# Prompt Text

create "Phase II Frontend Constitution"

Purpose:
This constitution governs all frontend work for Phase II of the Hackathon II Todo application.

Scope:
- Applies ONLY to Phase II
- Applies ONLY to frontend development
- Backend, AI chatbot, and deployment concerns are explicitly out of scope

Core Principles:
1. Spec-Driven Development
   - No frontend code may be written without an approved specification
   - All features must originate from /sp.specify

2. No Manual Coding
   - All implementation must be generated via Claude CLI
   - Human-written code is not allowed

3. Phase Discipline
   - Only Phase II features are allowed
   - Reject features from Phase III, IV, or V (chatbot, AI agents, Kubernetes, etc.)

4. Separation of Concerns
   - Frontend handles UI, UX, and API consumption only
   - Business logic lives in backend
   - Authentication is consumed, not implemented, in frontend

5. Security & User Isolation
   - Frontend assumes JWT-based authentication
   - API calls must always be user-scoped
   - No hardcoded secrets or tokens

6. Reusable Intelligence
   - Use all global agents and skills from fullstackwebapp/.claude/agents and fullstackwebapp/.claude/skills
   - Do not duplicate architectural or spec logic locally

7. Consistency
   - Follow patterns defined in frontend/CLAUDE.md
   - Use consistent naming, structure, and layout patterns

Required Artifacts:
- /sp.specify : Feature specifications (user stories + acceptance criteria)
- /sp.plan : Execution plans derived strictly from specs
- /sp.tasks : Concrete tasks generated only after plan approval

Forbidden Actions:
- Writing JSX, TS, or CSS without a spec
- Mixing backend logic into frontend
- Skipping acceptance criteria
- Implementing chatbot or AI features

Approval Rule:
No /sp.plan, /sp.tasks, or /sp.implementation may proceed
unless this constitution is accepted and active.

Confirmation:
Acknowledge this constitution and confirm readiness to proceed
with Phase II frontend specifications.

Note:
- All files will be generated inside fullstackwebapp/
- Reusable agents and skills are referenced from fullstackwebapp/.claude/

# Response Text

Created the Phase II Frontend Constitution file at .specify/memory/constitution.md with all the specified principles and governance rules.

# Outcome Impact

Successfully established governance framework for Phase II frontend development, defining core principles, scope boundaries, and required workflows.

# Tests Summary

none

# Files Summary

.specify/memory/constitution.md - Created constitution file with all specified principles

# Next Prompts

Ready to proceed with Phase II frontend specifications using /sp.specify as required by the constitution.

# Reflection Note

The constitution provides clear boundaries and principles that will guide all future frontend development work for Phase II.

# Failure Modes Observed

None

# Next Experiment to Improve Prompt Quality

None needed
