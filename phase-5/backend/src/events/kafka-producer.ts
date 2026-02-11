import { Kafka, Producer, ProducerRecord, RecordMetadata } from 'kafkajs';
import { v4 as uuidv4 } from 'uuid';
import logger from '../logger';

export interface EventPayload {
  eventId: string;
  eventType: string;
  timestamp: string;
  userId: string;
  taskId?: string;
  correlationId: string;
  payload: Record<string, any>;
  metadata: {
    sourceService: string;
    version: string;
  };
}

class KafkaProducerService {
  private kafka: Kafka;
  private producer: Producer;
  private isConnected: boolean = false;

  constructor() {
    this.kafka = new Kafka({
      clientId: 'phase5-backend',
      brokers: [process.env.KAFKA_BROKERS || 'localhost:9092'],
      retry: {
        initialRetryTime: 100,
        retries: 2, // Reduced retries for faster startup when Kafka is unavailable
      },
    });

    this.producer = this.kafka.producer({
      allowAutoTopicCreation: false,
      transactionTimeout: 30000,
    });
  }

  async connect(): Promise<void> {
    try {
      await this.producer.connect();
      this.isConnected = true;
      logger.info('Kafka producer connected successfully');
    } catch (error) {
      logger.error('Failed to connect Kafka producer:', error);
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    try {
      await this.producer.disconnect();
      this.isConnected = false;
      logger.info('Kafka producer disconnected');
    } catch (error) {
      logger.error('Failed to disconnect Kafka producer:', error);
      throw error;
    }
  }

  async publishEvent(
    topic: string,
    eventType: string,
    userId: string,
    payload: Record<string, any>,
    taskId?: string,
    correlationId?: string
  ): Promise<RecordMetadata[]> {
    if (!this.isConnected) {
      logger.debug(`Kafka not connected - skipping event publish to ${topic}:`, {
        eventType,
        taskId,
        userId,
      });
      return []; // Return empty array instead of throwing error
    }

    const event: EventPayload = {
      eventId: uuidv4(),
      eventType,
      timestamp: new Date().toISOString(),
      userId,
      taskId,
      correlationId: correlationId || uuidv4(),
      payload,
      metadata: {
        sourceService: 'backend-api',
        version: '1.0',
      },
    };

    const record: ProducerRecord = {
      topic,
      messages: [
        {
          key: taskId || userId,
          value: JSON.stringify(event),
          headers: {
            'event-type': eventType,
            'correlation-id': event.correlationId,
          },
        },
      ],
    };

    try {
      const metadata = await this.producer.send(record);
      logger.info(`Event published to ${topic}:`, {
        eventId: event.eventId,
        eventType,
        taskId,
      });
      return metadata;
    } catch (error) {
      logger.error(`Failed to publish event to ${topic}:`, error);
      // Don't throw - just log the error and continue
      return [];
    }
  }

  async publishTaskEvent(
    eventType: 'task.created' | 'task.updated' | 'task.deleted' | 'task.completed',
    userId: string,
    taskId: string,
    task: Record<string, any>,
    correlationId?: string
  ): Promise<RecordMetadata[]> {
    return this.publishEvent('task-events', eventType, userId, { task }, taskId, correlationId);
  }

  async publishTaskUpdate(
    userId: string,
    taskId: string,
    changes: Record<string, any>,
    correlationId?: string
  ): Promise<RecordMetadata[]> {
    return this.publishEvent(
      'task-updates',
      'task.updated',
      userId,
      { changes },
      taskId,
      correlationId
    );
  }

  async publishReminder(
    userId: string,
    taskId: string,
    reminder: Record<string, any>,
    correlationId?: string
  ): Promise<RecordMetadata[]> {
    return this.publishEvent(
      'reminders',
      'reminder.scheduled',
      userId,
      { reminder },
      taskId,
      correlationId
    );
  }

  async publishReminderEvent(
    eventType: 'reminder.scheduled' | 'reminder.updated' | 'reminder.sent' | 'reminder.failed' | 'reminder.deleted',
    userId: string,
    reminderId: string,
    reminder: Record<string, any>,
    correlationId?: string
  ): Promise<RecordMetadata[]> {
    return this.publishEvent('reminders', eventType, userId, { reminder }, reminderId, correlationId);
  }

  async publishAuditLog(
    userId: string,
    taskId: string | undefined,
    operationType: string,
    beforeState: Record<string, any> | null,
    afterState: Record<string, any> | null,
    correlationId?: string
  ): Promise<RecordMetadata[]> {
    return this.publishEvent(
      'audit-logs',
      `audit.${operationType}`,
      userId,
      { operationType, beforeState, afterState },
      taskId,
      correlationId
    );
  }
}

export const kafkaProducer = new KafkaProducerService();
