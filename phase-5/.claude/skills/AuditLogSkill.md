---
name: AuditLogSkill
description: Maintains a complete audit trail of all task operations (create, update, delete, complete). Subscribes to Kafka's task-events topic and records every event to the database for accountability and analytics. Designed to work with Dapr for event-driven and decoupled processing, ensuring logs are consistent and reliable across distributed services.
---

# AuditLogSkill

This skill maintains a complete audit trail of all task operations (create, update, delete, complete). It subscribes to Kafka's task-events topic and records every event to the database for accountability and analytics. The skill is designed to work with Dapr for event-driven and decoupled processing, ensuring logs are consistent and reliable across distributed services.
