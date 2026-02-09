---
name: ReminderAgent
description: Handles task reminders and notifications. When a task with a due date or reminder is created, updated, or approaching its scheduled time, this agent consumes the relevant event from Kafka and triggers notifications to the user via push, email, or in-app channels. It ensures that all reminders are sent reliably and on time, supports recurring reminders, and integrates with Dapr for scheduled bindings and event-driven workflows.
---

# ReminderAgent

This agent handles task reminders and notifications. When a task with a due date or reminder is created, updated, or approaching its scheduled time, this agent consumes the relevant event from Kafka and triggers notifications to the user via push, email, or in-app channels. It ensures that all reminders are sent reliably and on time, supports recurring reminders, and integrates with Dapr for scheduled bindings and event-driven workflows.
