# Intent Detection Skill

This skill is responsible for identifying the user's intent from natural language input in the Todo AI Chatbot.

## Responsibilities

- Analyze user messages written in natural language
- Detect the intended action related to todo management
- Map user intent to predefined task actions
- Provide a clear intent label to the calling agent

## Supported Intents

- add_task
- list_tasks
- complete_task
- delete_task
- update_task

## Scope Limitations

- Do not call MCP tools
- Do not access the database
- Do not format user-facing responses
- Do not manage conversation history

## Core Guidelines

1. Always infer intent based on meaning, not exact keywords
2. Handle variations in phrasing (e.g. "remember", "add", "create")
3. If intent is unclear, signal ambiguity to the agent
4. Return only one primary intent per message

## Reusability

This skill can be reused in any conversational AI system that requires intent detection from natural language input.

## Implementation Constraints

- Stateless processing only
- No external API calls