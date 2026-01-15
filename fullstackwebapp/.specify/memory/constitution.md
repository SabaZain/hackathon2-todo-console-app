# Phase II Frontend Constitution

## Purpose
This constitution governs all frontend work for Phase II of the Hackathon II Todo application.

## Scope
- Applies ONLY to Phase II
- Applies ONLY to frontend development
- Backend, AI chatbot, and deployment concerns are explicitly out of scope

## Core Principles

### 1. Spec-Driven Development
- No frontend code may be written without an approved specification
- All features must originate from /sp.specify
- Rationale: Ensures organized, planned development with clear requirements

### 2. No Manual Coding
- All implementation must be generated via Claude CLI
- Human-written code is not allowed
- Rationale: Maintains consistency and leverages AI-assisted development practices

### 3. Phase Discipline
- Only Phase II features are allowed
- Reject features from Phase III, IV, or V (chatbot, AI agents, Kubernetes, etc.)
- Rationale: Prevents scope creep and maintains focus on current phase objectives

### 4. Separation of Concerns
- Frontend handles UI, UX, and API consumption only
- Business logic lives in backend
- Authentication is consumed, not implemented, in frontend
- Rationale: Maintains clean architecture and proper layer separation

### 5. Security & User Isolation
- Frontend assumes JWT-based authentication
- API calls must always be user-scoped
- No hardcoded secrets or tokens
- Rationale: Ensures secure, isolated user experiences with proper authentication

### 6. Reusable Intelligence
- Use all global agents and skills from fullstackwebapp/.claude/agents and fullstackwebapp/.claude/skills
- Do not duplicate architectural or spec logic locally
- Rationale: Promotes reuse of established patterns and avoids redundancy

### 7. Consistency
- Follow patterns defined in frontend/CLAUDE.md
- Use consistent naming, structure, and layout patterns
- Rationale: Ensures uniformity across the codebase for maintainability

## Required Artifacts
- /sp.specify : Feature specifications (user stories + acceptance criteria)
- /sp.plan : Execution plans derived strictly from specs
- /sp.tasks : Concrete tasks generated only after plan approval

## Forbidden Actions
- Writing JSX, TS, or CSS without a spec
- Mixing backend logic into frontend
- Skipping acceptance criteria
- Implementing chatbot or AI features

## Approval Rule
No /sp.plan, /sp.tasks, or /sp.implementation may proceed unless this constitution is accepted and active.

## Confirmation
This constitution is acknowledged and active. Ready to proceed with Phase II frontend specifications.

## Notes
- All files will be generated inside fullstackwebapp/
- Reusable agents and skills are referenced from fullstackwebapp/.claude/