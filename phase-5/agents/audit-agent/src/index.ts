import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';
import { PrismaClient } from '@prisma/client';
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'audit-agent.log' }),
  ],
});

const prisma = new PrismaClient();

class AuditAgent {
  private kafka: Kafka;
  private consumer: Consumer;

  constructor() {
    this.kafka = new Kafka({
      clientId: 'audit-agent',
      brokers: [process.env.KAFKA_BROKERS || 'localhost:9092'],
    });

    this.consumer = this.kafka.consumer({ groupId: 'audit-agent-group' });
  }

  async start(): Promise<void> {
    try {
      await this.consumer.connect();
      logger.info('AuditAgent connected to Kafka');

      await this.consumer.subscribe({ topic: 'task-events', fromBeginning: false });
      logger.info('AuditAgent subscribed to task-events topic');

      await this.consumer.run({
        eachMessage: async (payload: EachMessagePayload) => {
          await this.handleMessage(payload);
        },
      });
    } catch (error) {
      logger.error('Failed to start AuditAgent:', error);
      throw error;
    }
  }

  private async handleMessage(payload: EachMessagePayload): Promise<void> {
    const { topic, partition, message } = payload;

    try {
      const event = JSON.parse(message.value?.toString() || '{}');

      logger.info('Processing event:', {
        topic,
        partition,
        offset: message.offset,
        eventType: event.eventType,
        eventId: event.eventId,
      });

      // Store audit log in database
      await prisma.auditLog.create({
        data: {
          userId: event.userId,
          taskId: event.taskId,
          operationType: this.mapEventTypeToOperation(event.eventType),
          beforeState: event.payload?.beforeState || null,
          afterState: event.payload?.afterState || event.payload?.task || null,
          correlationId: event.correlationId,
          metadata: event.metadata,
        },
      });

      logger.info('Audit log created successfully:', {
        eventId: event.eventId,
        taskId: event.taskId,
      });
    } catch (error) {
      logger.error('Failed to process message:', error);
      // In production, send to dead letter queue
    }
  }

  private mapEventTypeToOperation(eventType: string): string {
    const mapping: Record<string, string> = {
      'task.created': 'CREATE',
      'task.updated': 'UPDATE',
      'task.deleted': 'DELETE',
      'task.completed': 'COMPLETE',
      'task.restored': 'RESTORE',
    };
    return mapping[eventType] || 'UPDATE';
  }

  async stop(): Promise<void> {
    await this.consumer.disconnect();
    await prisma.$disconnect();
    logger.info('AuditAgent stopped');
  }
}

const agent = new AuditAgent();

process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, shutting down');
  await agent.stop();
  process.exit(0);
});

process.on('SIGINT', async () => {
  logger.info('SIGINT received, shutting down');
  await agent.stop();
  process.exit(0);
});

agent.start().catch((error) => {
  logger.error('Failed to start AuditAgent:', error);
  process.exit(1);
});
