import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';
import { PrismaClient, ReminderChannel } from '@prisma/client';
import winston from 'winston';
import cron from 'node-cron';
import { NotificationSender } from './notification-sender';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'reminder-agent.log' }),
  ],
});

const prisma = new PrismaClient();

class ReminderAgent {
  private kafka: Kafka;
  private consumer: Consumer;
  private notificationSender: NotificationSender;
  private cronJob?: cron.ScheduledTask;

  constructor() {
    this.kafka = new Kafka({
      clientId: 'reminder-agent',
      brokers: [process.env.KAFKA_BROKERS || 'localhost:9092'],
    });

    this.consumer = this.kafka.consumer({ groupId: 'reminder-agent-group' });
    this.notificationSender = new NotificationSender();
  }

  async start(): Promise<void> {
    try {
      // Connect to Kafka
      await this.consumer.connect();
      logger.info('ReminderAgent connected to Kafka');

      // Subscribe to reminders topic
      await this.consumer.subscribe({ topic: 'reminders', fromBeginning: false });
      logger.info('ReminderAgent subscribed to reminders topic');

      // Start consuming messages
      await this.consumer.run({
        eachMessage: async (payload: EachMessagePayload) => {
          await this.handleMessage(payload);
        },
      });

      // Start cron job to check for pending reminders every minute
      this.startReminderCheckCron();

      logger.info('ReminderAgent started successfully');
    } catch (error) {
      logger.error('Failed to start ReminderAgent:', error);
      throw error;
    }
  }

  private startReminderCheckCron(): void {
    // Run every minute to check for pending reminders
    this.cronJob = cron.schedule('* * * * *', async () => {
      try {
        await this.checkAndSendPendingReminders();
      } catch (error) {
        logger.error('Error in reminder check cron job:', error);
      }
    });

    logger.info('Reminder check cron job started (runs every minute)');
  }

  private async checkAndSendPendingReminders(): Promise<void> {
    try {
      const now = new Date();

      // Get all pending reminders that should be sent now
      const pendingReminders = await prisma.reminder.findMany({
        where: {
          status: 'PENDING',
          reminderTime: {
            lte: now,
          },
        },
        include: {
          task: {
            include: {
              user: true,
            },
          },
        },
        take: 100, // Process in batches
      });

      if (pendingReminders.length === 0) {
        return;
      }

      logger.info(`Found ${pendingReminders.length} pending reminders to send`);

      // Process each reminder
      for (const reminder of pendingReminders) {
        try {
          await this.sendReminder(reminder);
        } catch (error) {
          logger.error(`Failed to send reminder ${reminder.id}:`, error);

          // Mark as failed
          await prisma.reminder.update({
            where: { id: reminder.id },
            data: { status: 'FAILED' },
          });
        }
      }
    } catch (error) {
      logger.error('Failed to check pending reminders:', error);
    }
  }

  private async sendReminder(reminder: any): Promise<void> {
    const { task, channels } = reminder;
    const user = task.user;

    logger.info(`Sending reminder ${reminder.id} for task ${task.id} to user ${user.id}`);

    // Send notification via each channel
    const results = await Promise.allSettled(
      channels.map((channel: ReminderChannel) =>
        this.notificationSender.send(channel, user, task, reminder)
      )
    );

    // Check if all notifications were sent successfully
    const allSuccessful = results.every((result) => result.status === 'fulfilled');

    if (allSuccessful) {
      // Mark reminder as sent
      await prisma.reminder.update({
        where: { id: reminder.id },
        data: {
          status: 'SENT',
          sentAt: new Date(),
        },
      });

      logger.info(`Reminder ${reminder.id} sent successfully via all channels`);
    } else {
      // Mark as failed
      await prisma.reminder.update({
        where: { id: reminder.id },
        data: { status: 'FAILED' },
      });

      logger.error(`Reminder ${reminder.id} failed to send via some channels`);
    }
  }

  private async handleMessage(payload: EachMessagePayload): Promise<void> {
    const { topic, partition, message } = payload;

    try {
      const event = JSON.parse(message.value?.toString() || '{}');

      logger.info('Processing reminder event:', {
        topic,
        partition,
        offset: message.offset,
        eventType: event.eventType,
        eventId: event.eventId,
      });

      // Handle different reminder event types
      switch (event.eventType) {
        case 'reminder.scheduled':
          await this.handleReminderScheduled(event);
          break;
        case 'reminder.updated':
          await this.handleReminderUpdated(event);
          break;
        case 'reminder.deleted':
          await this.handleReminderDeleted(event);
          break;
        default:
          logger.warn(`Unknown event type: ${event.eventType}`);
      }
    } catch (error) {
      logger.error('Failed to process reminder message:', error);
      // In production, send to dead letter queue
    }
  }

  private async handleReminderScheduled(event: any): Promise<void> {
    logger.info('Reminder scheduled:', {
      reminderId: event.payload.reminder.id,
      taskId: event.payload.reminder.taskId,
      reminderTime: event.payload.reminder.reminderTime,
    });

    // Additional processing if needed (e.g., pre-scheduling notifications)
  }

  private async handleReminderUpdated(event: any): Promise<void> {
    logger.info('Reminder updated:', {
      reminderId: event.payload.reminder.id,
      taskId: event.payload.reminder.taskId,
    });

    // Handle reminder updates (e.g., reschedule if time changed)
  }

  private async handleReminderDeleted(event: any): Promise<void> {
    logger.info('Reminder deleted:', {
      reminderId: event.payload.reminder.id,
      taskId: event.payload.reminder.taskId,
    });

    // Handle reminder deletion (e.g., cancel scheduled notifications)
  }

  async stop(): Promise<void> {
    if (this.cronJob) {
      this.cronJob.stop();
      logger.info('Cron job stopped');
    }

    await this.consumer.disconnect();
    await prisma.$disconnect();
    logger.info('ReminderAgent stopped');
  }
}

const agent = new ReminderAgent();

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
  logger.error('Failed to start ReminderAgent:', error);
  process.exit(1);
});
