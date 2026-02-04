# MCP Tool Invocation Skill

This skill is responsible for invoking MCP task tools in a stateless and spec-compliant manner.

## Responsibilities

- Invoke MCP tools based on agent instructions
- Validate tool parameters before invocation
- Call MCP tools exactly as defined in specs
- Return structured tool responses to the agent

## Supported MCP Tools

- add_task
- list_tasks
- complete_task
- delete_task
- update_task

## Scope Limitations

- Do not interpret natural language
- Do not manage conversation state
- Do not format user-facing responses
- Do not directly manipulate database records

## Core Guidelines

1. Always follow MCP tool specifications
2. Never alter tool input or output formats
3. Handle tool-level errors safely
4. Maintain stateless behavior

## Reusability

This skill can be reused in any MCP-based system that requires tool invocation.

## Implementation Constraints

- No frontend logic
- No persistent state