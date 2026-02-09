---
name: RealTimeSyncAgent
description: Handles real-time synchronization of tasks across multiple connected clients. Consumes events from Kafka's task-updates topic and broadcasts updates via WebSocket to all active clients. Supports immediate propagation of task changes, ensuring every client has the latest task state without manual refresh. Integrates with Dapr for event-driven pub/sub.
---

# RealTimeSyncAgent

This agent handles real-time synchronization of tasks across multiple connected clients. It consumes events from Kafka's task-updates topic and broadcasts updates via WebSocket to all active clients. The agent supports immediate propagation of task changes, ensuring every client has the latest task state without manual refresh. It integrates with Dapr for event-driven pub/sub.
