---
name: AuditAgent
description: Captures and maintains a full history of all task operations (create, update, complete, delete). Consumes events from Kafka's task-events topic and stores them in a database (e.g., Neon DB) for audit, analytics, and troubleshooting. Ensures traceability, immutable logging, and supports queries for user activity and task lifecycle.
---

# AuditAgent

This agent captures and maintains a full history of all task operations (create, update, complete, delete). It consumes events from Kafka's task-events topic and stores them in a database (e.g., Neon DB) for audit, analytics, and troubleshooting. The agent ensures traceability, immutable logging, and supports queries for user activity and task lifecycle.
