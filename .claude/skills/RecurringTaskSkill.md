---
name: RecurringTaskSkill
description: Automatically handles recurring tasks. When a task with recurrence is completed, this skill calculates the next occurrence and creates it. Consumes events from Kafka's task-events topic and triggers task creation without blocking main task workflow. Works with Dapr for event-driven execution.
---

# RecurringTaskSkill

This skill automatically handles recurring tasks. When a task with recurrence is completed, this skill calculates the next occurrence and creates it. It consumes events from Kafka's task-events topic and triggers task creation without blocking the main task workflow. The skill works with Dapr for event-driven execution.
