---
name: NotificationSkill
description: Sends timely notifications (push/email) to users for due tasks or reminders. Listens to Kafka's reminders topic and triggers messages using the Notification Service. Integrated with Dapr for decoupled, event-driven execution. Ensures notifications are reliable, retrying if failures occur, and logs events for audit purposes.
---

# NotificationSkill

This skill sends timely notifications (push/email) to users for due tasks or reminders. It listens to Kafka's reminders topic and triggers messages using the Notification Service. The skill is integrated with Dapr for decoupled, event-driven execution. It ensures notifications are reliable, retrying if failures occur, and logs events for audit purposes.
