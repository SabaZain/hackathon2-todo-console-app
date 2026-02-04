# Prompt History Record (PHR)

**Date:** 2026-01-22

**Command Executed:** Create Phase 3 Constitution for Todo AI Chatbot Integration

**Original Prompt:**
/sp.constitution

# Phase 3 Constitution: Todo AI Chatbot Integration

This constitution governs Phase 3 of the Todo Web Application. Phase 3 focuses exclusively on integrating an AI-powered chatbot into an already working Todo system without breaking or modifying existing functionality.

---

## Project Context

The Todo Web Application frontend and backend are already implemented, deployed, and fully functional.

### Critical Rule

The existing Todo Web Application MUST remain stable and functional at all times.

Any chatbot-related functionality must be added in a way that does NOT disrupt or refactor existing todo features.

---

## Phase 3 Objective

The objective of Phase 3 is to integrate a stateless AI-powered chatbot that allows users to manage their todos using natural language.

The chatbot must:
- Add tasks
- List tasks
- Update tasks
- Complete tasks
- Delete tasks

All via conversational interaction.

---

## Frontend Integration Rule (Chatbot UI)

The chatbot MUST be integrated as an optional UI enhancement.

### Rules

- The chatbot must appear as a floating icon or button on the Todo web application
- Clicking the icon opens a chat interface (drawer, modal, or overlay)
- Closing the chat must not affect the main Todo UI
- Existing Todo UI screens, flows, and components MUST NOT be modified
- The Todo application must function normally even if the chatbot is not used

The chatbot is an enhancement layer, not a core dependency.

---

## Backend Integration Rule

- A dedicated chat API endpoint must be introduced for chatbot communication
- Existing todo APIs MUST NOT be modified
- Chatbot logic must interact with todo data ONLY via MCP tools
- No direct database access by AI agents is allowed

---

## Folder Isolation Rule

All Phase 3 chatbot-related development MUST live inside a dedicated folder:

/todo-chatbot

This folder will exist inside the hackathontwo root directory.

### Rules

- Existing frontend and backend folders MUST NOT be modified
- All chatbot-related backend logic, MCP server, chat APIs, specs, and runners must live inside /todo-chatbot
- The /todo-chatbot folder represents Phase 3 only
- Integration with the existing Todo application must occur only via APIs or MCP tools

---

## Architecture Principles

1. **Additive Architecture**
   - Chatbot features are added without altering existing systems

2. **Stateless Server Design**
   - Each chat request is independent
   - All conversation state is stored in the database

3. **Spec-Driven Development**
   - All chatbot behavior must be implemented strictly through specs
   - No undocumented logic is allowed

---

## Agent & Skill Reuse Policy

Reusable agents and skills already exist inside the `.claude/` directory.

### Mandatory Rules

- Existing reusable agents MUST be used where applicable
- Existing reusable skills MUST be used where applicable
- Duplication of logic is forbidden
- Agents and skills may be extended but not rewritten without spec approval

---

## MCP Usage Rules

- All task operations must be performed through MCP tools
- MCP tools must be stateless
- MCP tools must persist state in the database
- AI agents must never manipulate task data directly

---

## Conversation & Persistence Rules

- Conversation history must be stored in the database
- Messages must be persisted for every user and conversation
- The server must not retain in-memory state between requests
- Conversations must resume correctly after server restarts

---

## History Folder Requirement

A `/history` directory MUST be maintained.

### Rules

- Every Spec-Kit Plus command execution must generate a history file
- History files must document:
  - The command executed
  - Agents and skills involved
  - Changes introduced
- History files act as an audit trail and learning reference

---

## Quality, Safety & Stability Rules

- Existing Todo functionality always takes priority over chatbot features
- Errors must be handled gracefully
- No breaking changes are allowed
- The system must be restart-safe and reliable

---

## Final Authority Rule

If any conflict arises between:
- Existing working Todo functionality
- New chatbot features

The existing working functionality ALWAYS takes priority.

Phase 3 exists to enhance the application, not to destabilize it.

**Agents Involved:**
- None

**Skills Used:**
- File creation skill

**Changes Introduced:**
- Created constitution.md file in the todo-chatbot directory
- Defined governance rules for Phase 3 Todo AI Chatbot Integration
- Established principles for maintaining existing functionality while adding chatbot features
- Specified folder isolation rule requiring all Phase 3 work to be in /todo-chatbot
- Outlined agent and skill reuse policies
- Defined MCP usage rules
- Established conversation and persistence requirements

**Summary:**
Created the foundational governance document for Phase 3 of the Todo Web Application. The constitution establishes rules for integrating an AI-powered chatbot while ensuring existing functionality remains stable and unmodified. It defines architectural principles, integration rules, and quality standards for the project.

**Status:** Completed