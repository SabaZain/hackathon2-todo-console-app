import { PrismaClient, Task, TaskStatus, RecurrenceFrequency } from '@prisma/client';
import { v4 as uuidv4 } from 'uuid';
import { recurrenceCalculator } from './recurrence-calculator.service';
import { kafkaProducer } from '../events/kafka-producer';
import logger from '../logger';

const prisma = new PrismaClient();

export interface CreateRecurringTaskInput {
  title: string;
  description?: string;
  userId: string;
  priority?: string;
  tags?: string[];
  dueDate?: Date;
  recurrencePattern: {
    frequency: string;
    interval: number;
    dayOfWeek?: number;
    dayOfMonth?: number;
    endDate?: Date;
    occurrencesCount?: number;
  };
}

export class RecurringTaskService {
  /**
   * Create a new recurring task with its pattern
   */
  async createRecurringTask(input: CreateRecurringTaskInput): Promise<Task> {
    const correlationId = uuidv4();

    try {
      // Validate recurrence pattern
      const validation = recurrenceCalculator.validatePattern({
        ...input.recurrencePattern,
        frequency: input.recurrencePattern.frequency as RecurrenceFrequency,
      });
      if (!validation.valid) {
        throw new Error(`Invalid recurrence pattern: ${validation.errors.join(', ')}`);
      }

      // Create recurrence pattern and task in a transaction
      const result = await prisma.$transaction(async (tx) => {
        // Create recurrence pattern
        const pattern = await tx.recurrencePattern.create({
          data: {
            frequency: input.recurrencePattern.frequency as RecurrenceFrequency,
            interval: input.recurrencePattern.interval,
            dayOfWeek: input.recurrencePattern.dayOfWeek,
            dayOfMonth: input.recurrencePattern.dayOfMonth,
            endDate: input.recurrencePattern.endDate,
            occurrencesCount: input.recurrencePattern.occurrencesCount,
          },
        });

        // Create the first task occurrence
        const task = await tx.task.create({
          data: {
            title: input.title,
            description: input.description,
            userId: input.userId,
            priority: input.priority as any,
            tags: input.tags || [],
            dueDate: input.dueDate,
            isRecurring: true,
            recurrencePatternId: pattern.id,
            status: TaskStatus.PENDING,
          },
          include: {
            recurrencePattern: true,
          },
        });

        return task;
      });

      // Publish task.created event
      await kafkaProducer.publishTaskEvent(
        'task.created',
        input.userId,
        result.id,
        {
          id: result.id,
          title: result.title,
          description: result.description || '',
          status: result.status,
          priority: result.priority,
          tags: result.tags,
          dueDate: result.dueDate?.toISOString(),
          isRecurring: result.isRecurring,
          recurrencePattern: result.recurrencePattern,
          createdAt: result.createdAt.toISOString(),
          updatedAt: result.updatedAt.toISOString(),
        },
        correlationId
      );

      logger.info('Recurring task created:', {
        taskId: result.id,
        userId: input.userId,
        correlationId,
      });

      return result;
    } catch (error) {
      logger.error('Failed to create recurring task:', error);
      throw error;
    }
  }

  /**
   * Generate the next occurrence of a recurring task
   */
  async generateNextOccurrence(completedTask: Task): Promise<Task | null> {
    const correlationId = uuidv4();

    try {
      if (!completedTask.isRecurring || !completedTask.recurrencePatternId) {
        logger.warn('Task is not recurring, cannot generate next occurrence:', {
          taskId: completedTask.id,
        });
        return null;
      }

      // Get recurrence pattern
      const pattern = await prisma.recurrencePattern.findUnique({
        where: { id: completedTask.recurrencePatternId },
      });

      if (!pattern) {
        logger.error('Recurrence pattern not found:', {
          patternId: completedTask.recurrencePatternId,
        });
        return null;
      }

      // Calculate next occurrence
      const calculation = recurrenceCalculator.calculateNextOccurrence(
        pattern,
        completedTask.dueDate || new Date()
      );

      if (!calculation.shouldCreateNext) {
        logger.info('Recurrence pattern has ended, no next occurrence:', {
          taskId: completedTask.id,
          patternId: pattern.id,
        });
        return null;
      }

      // Create next occurrence
      const nextTask = await prisma.task.create({
        data: {
          title: completedTask.title,
          description: completedTask.description,
          userId: completedTask.userId,
          priority: completedTask.priority,
          tags: completedTask.tags,
          dueDate: calculation.nextOccurrence,
          isRecurring: true,
          recurrencePatternId: pattern.id,
          parentTaskId: completedTask.id,
          status: TaskStatus.PENDING,
        },
        include: {
          recurrencePattern: true,
        },
      });

      // Publish task.created event for next occurrence
      await kafkaProducer.publishTaskEvent(
        'task.created',
        nextTask.userId,
        nextTask.id,
        {
          id: nextTask.id,
          title: nextTask.title,
          description: nextTask.description || '',
          status: nextTask.status,
          priority: nextTask.priority,
          tags: nextTask.tags,
          dueDate: nextTask.dueDate?.toISOString(),
          isRecurring: nextTask.isRecurring,
          recurrencePattern: nextTask.recurrencePattern,
          createdAt: nextTask.createdAt.toISOString(),
          updatedAt: nextTask.updatedAt.toISOString(),
        },
        correlationId
      );

      logger.info('Next occurrence generated:', {
        originalTaskId: completedTask.id,
        nextTaskId: nextTask.id,
        nextDueDate: calculation.nextOccurrence,
        correlationId,
      });

      return nextTask;
    } catch (error) {
      logger.error('Failed to generate next occurrence:', error);
      throw error;
    }
  }

  /**
   * Get all occurrences of a recurring task
   */
  async getTaskOccurrences(taskId: string): Promise<Task[]> {
    try {
      // Find the root task (task without parent)
      const task = await prisma.task.findUnique({
        where: { id: taskId },
      });

      if (!task) {
        throw new Error('Task not found');
      }

      // If this task has a parent, find the root
      let rootTaskId = task.parentTaskId || task.id;

      // Get all tasks in the chain
      const occurrences = await prisma.task.findMany({
        where: {
          OR: [
            { id: rootTaskId },
            { parentTaskId: rootTaskId },
          ],
        },
        orderBy: {
          dueDate: 'asc',
        },
        include: {
          recurrencePattern: true,
        },
      });

      return occurrences;
    } catch (error) {
      logger.error('Failed to get task occurrences:', error);
      throw error;
    }
  }
}

export const recurringTaskService = new RecurringTaskService();
