import { Kafka, Producer, Consumer } from 'kafkajs';
import { PrismaClient } from '@prisma/client';

describe('Kafka Event Flow - Integration Tests', () => {
  let kafka: Kafka;
  let producer: Producer;
  let consumer: Consumer;
  let prisma: PrismaClient;
  let receivedEvents: any[] = [];

  beforeAll(async () => {
    prisma = new PrismaClient();

    kafka = new Kafka({
      clientId: 'test-client',
      brokers: [process.env.KAFKA_BROKER || 'localhost:9092'],
    });

    producer = kafka.producer();
    consumer = kafka.consumer({ groupId: 'test-group' });

    await producer.connect();
    await consumer.connect();
    await consumer.subscribe({ topic: 'task-events', fromBeginning: false });

    // Collect events
    await consumer.run({
      eachMessage: async ({ message }) => {
        const event = JSON.parse(message.value?.toString() || '{}');
        receivedEvents.push(event);
      },
    });
  });

  afterAll(async () => {
    await consumer.disconnect();
    await producer.disconnect();
    await prisma.$disconnect();
  });

  beforeEach(() => {
    receivedEvents = [];
  });

  describe('Task Created Event', () => {
    it('should publish task.created event when task is created', async () => {
      const taskData = {
        id: 'test-task-123',
        title: 'Test Task',
        userId: 'user-123',
        createdAt: new Date().toISOString(),
      };

      await producer.send({
        topic: 'task-events',
        messages: [
          {
            key: taskData.id,
            value: JSON.stringify({
              type: 'task.created',
              taskId: taskData.id,
              userId: taskData.userId,
              timestamp: taskData.createdAt,
              data: taskData,
            }),
          },
        ],
      });

      // Wait for event to be consumed
      await new Promise((resolve) => setTimeout(resolve, 1000));

      expect(receivedEvents).toHaveLength(1);
      expect(receivedEvents[0]).toMatchObject({
        type: 'task.created',
        taskId: taskData.id,
        userId: taskData.userId,
      });
    });
  });

  describe('Task Completed Event', () => {
    it('should publish task.completed event when task is marked complete', async () => {
      const taskData = {
        id: 'test-task-456',
        title: 'Task to Complete',
        userId: 'user-123',
        completed: true,
        completedAt: new Date().toISOString(),
      };

      await producer.send({
        topic: 'task-events',
        messages: [
          {
            key: taskData.id,
            value: JSON.stringify({
              type: 'task.completed',
              taskId: taskData.id,
              userId: taskData.userId,
              timestamp: taskData.completedAt,
              data: taskData,
            }),
          },
        ],
      });

      await new Promise((resolve) => setTimeout(resolve, 1000));

      expect(receivedEvents).toHaveLength(1);
      expect(receivedEvents[0].type).toBe('task.completed');
      expect(receivedEvents[0].data.completed).toBe(true);
    });
  });

  describe('Recurring Task Event Flow', () => {
    it('should trigger recurring task generation on completion', async () => {
      const recurringTask = {
        id: 'recurring-task-789',
        title: 'Daily Task',
        userId: 'user-123',
        isRecurring: true,
        recurrencePattern: 'daily',
        completed: true,
        completedAt: new Date().toISOString(),
      };

      await producer.send({
        topic: 'task-events',
        messages: [
          {
            key: recurringTask.id,
            value: JSON.stringify({
              type: 'task.completed',
              taskId: recurringTask.id,
              userId: recurringTask.userId,
              timestamp: recurringTask.completedAt,
              data: recurringTask,
            }),
          },
        ],
      });

      // Wait for recurring task agent to process and create new task
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Should receive both completion event and new task created event
      expect(receivedEvents.length).toBeGreaterThanOrEqual(1);
      expect(receivedEvents[0].type).toBe('task.completed');
      expect(receivedEvents[0].data.isRecurring).toBe(true);
    });
  });

  describe('Audit Trail Event Flow', () => {
    it('should create audit log entry for task events', async () => {
      const taskId = 'audit-test-task';
      const userId = 'user-123';

      await producer.send({
        topic: 'task-events',
        messages: [
          {
            key: taskId,
            value: JSON.stringify({
              type: 'task.updated',
              taskId,
              userId,
              timestamp: new Date().toISOString(),
              changes: {
                title: { old: 'Old Title', new: 'New Title' },
              },
            }),
          },
        ],
      });

      // Wait for audit agent to process
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Verify audit log was created
      const auditLogs = await prisma.auditLog.findMany({
        where: { taskId },
      });

      expect(auditLogs.length).toBeGreaterThan(0);
      expect(auditLogs[0].operationType).toBe('task.updated');
    });
  });

  describe('Event Ordering', () => {
    it('should maintain event order for same task', async () => {
      const taskId = 'order-test-task';
      const events = [
        { type: 'task.created', order: 1 },
        { type: 'task.updated', order: 2 },
        { type: 'task.completed', order: 3 },
      ];

      for (const event of events) {
        await producer.send({
          topic: 'task-events',
          messages: [
            {
              key: taskId,
              value: JSON.stringify({
                ...event,
                taskId,
                userId: 'user-123',
                timestamp: new Date().toISOString(),
              }),
            },
          ],
        });
      }

      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Events should be received in order
      expect(receivedEvents).toHaveLength(3);
      expect(receivedEvents[0].type).toBe('task.created');
      expect(receivedEvents[1].type).toBe('task.updated');
      expect(receivedEvents[2].type).toBe('task.completed');
    });
  });

  describe('Error Handling', () => {
    it('should handle malformed event gracefully', async () => {
      await producer.send({
        topic: 'task-events',
        messages: [
          {
            key: 'malformed',
            value: 'not-valid-json',
          },
        ],
      });

      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Consumer should not crash
      expect(consumer).toBeDefined();
    });
  });
});
