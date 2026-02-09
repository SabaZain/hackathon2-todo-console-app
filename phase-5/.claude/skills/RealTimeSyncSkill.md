---
name: RealTimeSyncSkill
description: Ensures real-time synchronization of task updates across all connected clients. Subscribes to Kafka's task-updates topic and pushes changes via WebSocket or Dapr service invocation, so that any modification from one client instantly reflects on all other clients. Supports high concurrency and is decoupled from the main backend logic, enabling scalable multi-client collaboration.
---

# RealTimeSyncSkill

This skill ensures real-time synchronization of task updates across all connected clients. It subscribes to Kafka's task-updates topic and pushes changes via WebSocket or Dapr service invocation, so that any modification from one client instantly reflects on all other clients. The skill supports high concurrency and is decoupled from the main backend logic, enabling scalable multi-client collaboration.
