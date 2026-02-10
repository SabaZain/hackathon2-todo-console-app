import express from 'express';
import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';
import { PrismaClient } from '@prisma/client';
import {
  tracer,
  createSpan,
  finishSpan,
  logger,
  createContextLogger,
  register,
  trackKafkaEvent,
  trackAgentOperation,
  closeTracer,
} from '../shared/observability';
import promClient from 'prom-client';

const app = express();
const prisma = new PrismaClient();

const SERVICE_NAME = 'recurring-task-agent';
const PORT = process.env.PORT || 3103;

// Additional metrics specific to recurring task agent
const recurringTaskGenerated = new promClient.Counter({
  name: 'recurring_task_generated_total',
  help: 'Total number of recurring tasks generated',
  labelNames: ['pattern'],
  registers: [register],
});

const recurringTaskGenerationDuration = new promClient.Histogram({
  name: 'recurring_task_generation_duration_seconds',
  help: 'Duration of recurring task generation in seconds',
  labelNames: ['pattern'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1],
  registers: [register],
});

// Kafka configuration
const kafka = new Kafka({
  clientId: SERVICE_NAME,
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092'],
});

const consumer: Consumer = kafka.consumer({
  groupId: `${SERVICE_NAME}-group`,
});

const producer = kafka.producer();

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: SERVICE_NAME,
    timestamp: new Date().toISOString(),
  });
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (error: any) {
    logger.error('Failed to generate metrics', { error: error.message });
    res.status(500).end(error.message);
  }
});

// Calculate next occurrence based on recurrence pattern
const calculateNextOccurrence = (
  completedDate: Date,
  pattern: string
): Date | null => {
  const next = new Date(completedDate);

  switch (pattern) {
    case 'daily':
      next.setDate(next.getDate() + 1);
      break;
    case 'weekly':
      next.setDate(next.getDate() + 7);
      break;
    case 'monthly':
      next.setMonth(next.getMonth() + 1);
      break;
    case 'yearly':
      next.setFullYear(next.getFullYear() + 1);
      break;
    default:
      return null;
  }

  return next;
};

// Generate next recurring task
const generateNextTask = async (
  originalTask: any,
  span: any
): Promise<void> => {
  const start = Date.now();
  const childSpan = tracer.startSpan('generate_next_task', { childOf: span });

  try {
    const nextDueDate = calculateNextOccurrence(
      new Date(originalTask.completedAt),
      originalTask.recurrencePattern
    );

    if (!nextDueDate) {
      throw new Error(`Invalid recurrence pattern: ${originalTask.recurrencePattern}`);
    }

    // Create new task in database
    const newTask = await prisma.task.create({
      data: {
        title: originalTask.title,
        description: originalTask.description,
        userId: originalTask.userId,
        dueDate: nextDueDate,
        priority: originalTask.priority,
        tags: originalTask.tags,
        isRecurring: true,
        recurrencePattern: originalTask.recurrencePattern,
        parentTaskId: originalTask.id,
      },
    });

    // Publish task created event
    await producer.send({
      topic: 'task-events',
      messages: [
        {
          key: newTask.id,
          value: JSON.stringify({
            type: 'task.created',
            taskId: newTask.id,
            userId: newTask.userId,
            timestamp: new Date().toISOString(),
            data: newTask,
          }),
        },
      ],
    });

    const duration = (Date.now() - start) / 1000;
    recurringTaskGenerated.inc({ pattern: originalTask.recurrencePattern });
    recurringTaskGenerationDuration.observe(
      { pattern: originalTask.recurrencePattern },
      duration
    );

    childSpan.setTag('generation.success', true);
    childSpan.setTag('new_task.id', newTask.id);
    childSpan.finish();
  } catch (error: any) {
    childSpan.setTag('error', true);
    childSpan.log({ event: 'error', message: error.message });
    childSpan.finish();

    throw error;
  }
};

// Process task completed event
const processTaskCompletedEvent = async (payload: EachMessagePayload) => {
  const start = Date.now();
  const span = createSpan('process_task_completed');
  const contextLogger = createContextLogger({
    service: SERVICE_NAME,
    topic: payload.topic,
    partition: payload.partition,
    offset: payload.message.offset,
  });

  try {
    const event = JSON.parse(payload.message.value?.toString() || '{}');

    // Only process if task is recurring
    if (!event.data?.isRecurring) {
      contextLogger.debug('Skipping non-recurring task', {
        taskId: event.taskId,
      });
      return;
    }

    contextLogger.info('Processing recurring task completion', {
      eventType: event.type,
      taskId: event.taskId,
      pattern: event.data.recurrencePattern,
    });

    span.setTag('event.type', event.type);
    span.setTag('task.id', event.taskId);
    span.setTag('recurrence.pattern', event.data.recurrencePattern);

    // Generate next occurrence
    await generateNextTask(event.data, span);

    const duration = (Date.now() - start) / 1000;
    trackKafkaEvent(payload.topic, event.type, 'success', duration);
    trackAgentOperation('generate_recurring_task', 'success', duration);

    contextLogger.info('Recurring task generated successfully', {
      originalTaskId: event.taskId,
      pattern: event.data.recurrencePattern,
      duration,
    });

    finishSpan(span);
  } catch (error: any) {
    const duration = (Date.now() - start) / 1000;
    trackKafkaEvent(payload.topic, 'unknown', 'error', duration);
    trackAgentOperation('generate_recurring_task', 'error', duration);

    contextLogger.error('Failed to generate recurring task', {
      error: error.message,
      stack: error.stack,
    });

    finishSpan(span, error);
    throw error;
  }
};

// Start Kafka consumer and producer
const startConsumer = async () => {
  await producer.connect();
  await consumer.connect();
  await consumer.subscribe({ topic: 'task-events', fromBeginning: false });

  await consumer.run({
    eachMessage: processTaskCompletedEvent,
  });

  logger.info('Recurring task agent started', {
    service: SERVICE_NAME,
    topics: ['task-events'],
  });
};

// Start HTTP server
app.listen(PORT, () => {
  logger.info('Recurring task agent HTTP server started', {
    port: PORT,
    service: SERVICE_NAME,
  });
});

// Graceful shutdown
const gracefulShutdown = async (signal: string) => {
  logger.info(`Received ${signal}, starting graceful shutdown`);

  await consumer.disconnect();
  await producer.disconnect();
  await prisma.$disconnect();
  await closeTracer();

  logger.info('Graceful shutdown complete');
  process.exit(0);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Start the agent
startConsumer().catch((error) => {
  logger.error('Failed to start recurring task agent', {
    error: error.message,
    stack: error.stack,
  });
  process.exit(1);
});
