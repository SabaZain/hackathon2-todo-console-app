import { PrismaClient, Reminder, ReminderStatus, ReminderChannel } from '@prisma/client';
import { v4 as uuidv4 } from 'uuid';
import { kafkaProducer } from '../events/kafka-producer';
import logger from '../config/logger';

const prisma = new PrismaClient();

export interface CreateReminderInput {
  taskId: string;
  userId: string;
  reminderTime: Date;
  channels: ReminderChannel[];
}

export interface UpdateReminderInput {
  reminderTime?: Date;
  channels?: ReminderChannel[];
  status?: ReminderStatus;
}

export class ReminderService {
  /**
   * Create a new reminder for a task
   */
  async createReminder(input: CreateReminderInput): Promise<Reminder> {
    const correlationId = uuidv4();

    try {
      // Verify task exists and belongs to user
      const task = await prisma.task.findFirst({
        where: {
          id: input.taskId,
          userId: input.userId,
        },
      });

      if (!task) {
        throw new Error('Task not found or access denied');
      }

      // Create reminder
      const reminder = await prisma.reminder.create({
        data: {
          taskId: input.taskId,
          reminderTime: input.reminderTime,
          channels: input.channels,
          status: ReminderStatus.PENDING,
        },
        include: {
          task: true,
        },
      });

      // Publish reminder.scheduled event
      await kafkaProducer.publishReminderEvent(
        'reminder.scheduled',
        input.userId,
        reminder.id,
        {
          id: reminder.id,
          taskId: reminder.taskId,
          taskTitle: task.title,
          reminderTime: reminder.reminderTime.toISOString(),
          channels: reminder.channels,
          status: reminder.status,
          createdAt: reminder.createdAt.toISOString(),
        },
        correlationId
      );

      logger.info('Reminder created:', {
        reminderId: reminder.id,
        taskId: input.taskId,
        userId: input.userId,
        reminderTime: reminder.reminderTime,
        correlationId,
      });

      return reminder;
    } catch (error) {
      logger.error('Failed to create reminder:', error);
      throw error;
    }
  }

  /**
   * Get reminder by ID
   */
  async getReminderById(reminderId: string, userId: string): Promise<Reminder | null> {
    try {
      const reminder = await prisma.reminder.findFirst({
        where: {
          id: reminderId,
          task: {
            userId,
          },
        },
        include: {
          task: true,
        },
      });

      return reminder;
    } catch (error) {
      logger.error('Failed to get reminder:', error);
      throw error;
    }
  }

  /**
   * Get all reminders for a task
   */
  async getTaskReminders(taskId: string, userId: string): Promise<Reminder[]> {
    try {
      const reminders = await prisma.reminder.findMany({
        where: {
          taskId,
          task: {
            userId,
          },
        },
        orderBy: {
          reminderTime: 'asc',
        },
      });

      return reminders;
    } catch (error) {
      logger.error('Failed to get task reminders:', error);
      throw error;
    }
  }

  /**
   * Get all reminders for a user
   */
  async getUserReminders(userId: string, status?: ReminderStatus): Promise<Reminder[]> {
    try {
      const where: any = {
        task: {
          userId,
        },
      };

      if (status) {
        where.status = status;
      }

      const reminders = await prisma.reminder.findMany({
        where,
        include: {
          task: true,
        },
        orderBy: {
          reminderTime: 'asc',
        },
      });

      return reminders;
    } catch (error) {
      logger.error('Failed to get user reminders:', error);
      throw error;
    }
  }

  /**
   * Get pending reminders that should be sent now
   */
  async getPendingReminders(beforeTime: Date): Promise<Reminder[]> {
    try {
      const reminders = await prisma.reminder.findMany({
        where: {
          status: ReminderStatus.PENDING,
          reminderTime: {
            lte: beforeTime,
          },
        },
        include: {
          task: {
            include: {
              user: true,
            },
          },
        },
        orderBy: {
          reminderTime: 'asc',
        },
      });

      return reminders;
    } catch (error) {
      logger.error('Failed to get pending reminders:', error);
      throw error;
    }
  }

  /**
   * Update a reminder
   */
  async updateReminder(
    reminderId: string,
    userId: string,
    input: UpdateReminderInput
  ): Promise<Reminder> {
    const correlationId = uuidv4();

    try {
      // Verify reminder exists and belongs to user
      const existingReminder = await this.getReminderById(reminderId, userId);
      if (!existingReminder) {
        throw new Error('Reminder not found or access denied');
      }

      // Update reminder
      const reminder = await prisma.reminder.update({
        where: {
          id: reminderId,
        },
        data: input,
        include: {
          task: true,
        },
      });

      // Publish reminder.updated event
      await kafkaProducer.publishReminderEvent(
        'reminder.updated',
        userId,
        reminder.id,
        {
          id: reminder.id,
          taskId: reminder.taskId,
          taskTitle: reminder.task.title,
          reminderTime: reminder.reminderTime.toISOString(),
          channels: reminder.channels,
          status: reminder.status,
          updatedAt: reminder.updatedAt.toISOString(),
        },
        correlationId
      );

      logger.info('Reminder updated:', {
        reminderId: reminder.id,
        userId,
        correlationId,
      });

      return reminder;
    } catch (error) {
      logger.error('Failed to update reminder:', error);
      throw error;
    }
  }

  /**
   * Mark reminder as sent
   */
  async markReminderAsSent(reminderId: string): Promise<Reminder> {
    const correlationId = uuidv4();

    try {
      const reminder = await prisma.reminder.update({
        where: {
          id: reminderId,
        },
        data: {
          status: ReminderStatus.SENT,
          sentAt: new Date(),
        },
        include: {
          task: {
            include: {
              user: true,
            },
          },
        },
      });

      // Publish reminder.sent event
      await kafkaProducer.publishReminderEvent(
        'reminder.sent',
        reminder.task.userId,
        reminder.id,
        {
          id: reminder.id,
          taskId: reminder.taskId,
          taskTitle: reminder.task.title,
          reminderTime: reminder.reminderTime.toISOString(),
          channels: reminder.channels,
          status: reminder.status,
          sentAt: reminder.sentAt?.toISOString(),
        },
        correlationId
      );

      logger.info('Reminder marked as sent:', {
        reminderId: reminder.id,
        correlationId,
      });

      return reminder;
    } catch (error) {
      logger.error('Failed to mark reminder as sent:', error);
      throw error;
    }
  }

  /**
   * Mark reminder as failed
   */
  async markReminderAsFailed(reminderId: string, errorMessage?: string): Promise<Reminder> {
    const correlationId = uuidv4();

    try {
      const reminder = await prisma.reminder.update({
        where: {
          id: reminderId,
        },
        data: {
          status: ReminderStatus.FAILED,
        },
        include: {
          task: {
            include: {
              user: true,
            },
          },
        },
      });

      // Publish reminder.failed event
      await kafkaProducer.publishReminderEvent(
        'reminder.failed',
        reminder.task.userId,
        reminder.id,
        {
          id: reminder.id,
          taskId: reminder.taskId,
          taskTitle: reminder.task.title,
          reminderTime: reminder.reminderTime.toISOString(),
          channels: reminder.channels,
          status: reminder.status,
          error: errorMessage,
        },
        correlationId
      );

      logger.error('Reminder marked as failed:', {
        reminderId: reminder.id,
        error: errorMessage,
        correlationId,
      });

      return reminder;
    } catch (error) {
      logger.error('Failed to mark reminder as failed:', error);
      throw error;
    }
  }

  /**
   * Delete a reminder
   */
  async deleteReminder(reminderId: string, userId: string): Promise<void> {
    const correlationId = uuidv4();

    try {
      // Verify reminder exists and belongs to user
      const reminder = await this.getReminderById(reminderId, userId);
      if (!reminder) {
        throw new Error('Reminder not found or access denied');
      }

      // Delete reminder
      await prisma.reminder.delete({
        where: {
          id: reminderId,
        },
      });

      // Publish reminder.deleted event
      await kafkaProducer.publishReminderEvent(
        'reminder.deleted',
        userId,
        reminderId,
        {
          id: reminder.id,
          taskId: reminder.taskId,
          taskTitle: reminder.task.title,
          reminderTime: reminder.reminderTime.toISOString(),
          channels: reminder.channels,
          status: reminder.status,
        },
        correlationId
      );

      logger.info('Reminder deleted:', {
        reminderId,
        userId,
        correlationId,
      });
    } catch (error) {
      logger.error('Failed to delete reminder:', error);
      throw error;
    }
  }
}

export const reminderService = new ReminderService();
