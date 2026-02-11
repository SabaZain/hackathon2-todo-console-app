import { PrismaClient, Task, TaskStatus, TaskPriority } from '@prisma/client';
import { v4 as uuidv4 } from 'uuid';
import { kafkaProducer } from '../events/kafka-producer';
import { recurringTaskService } from './recurring-task.service';
import logger from '../logger';

const prisma = new PrismaClient();

export interface CreateTaskInput {
  title: string;
  description?: string;
  userId: string;
  priority?: TaskPriority;
  tags?: string[];
  dueDate?: Date;
}

export interface UpdateTaskInput {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  tags?: string[];
  dueDate?: Date;
  status?: TaskStatus;
}

export interface TaskFilters {
  userId: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  tags?: string[];
  search?: string;
  dueDateFrom?: Date;
  dueDateTo?: Date;
}

export class TaskService {
  /**
   * Create a new task
   */
  async createTask(input: CreateTaskInput): Promise<Task> {
    const correlationId = uuidv4();

    try {
      const task = await prisma.task.create({
        data: {
          title: input.title,
          description: input.description,
          userId: input.userId,
          priority: input.priority || TaskPriority.MEDIUM,
          tags: input.tags || [],
          dueDate: input.dueDate,
          status: TaskStatus.PENDING,
        },
      });

      // Publish task.created event
      await kafkaProducer.publishTaskEvent(
        'task.created',
        input.userId,
        task.id,
        {
          id: task.id,
          title: task.title,
          description: task.description || '',
          status: task.status,
          priority: task.priority,
          tags: task.tags,
          dueDate: task.dueDate?.toISOString(),
          isRecurring: task.isRecurring,
          createdAt: task.createdAt.toISOString(),
          updatedAt: task.updatedAt.toISOString(),
        },
        correlationId
      );

      // Publish to task-updates for real-time sync
      await kafkaProducer.publishTaskUpdate(
        input.userId,
        task.id,
        { action: 'created', task },
        correlationId
      );

      logger.info('Task created:', { taskId: task.id, userId: input.userId, correlationId });

      return task;
    } catch (error) {
      logger.error('Failed to create task:', error);
      throw error;
    }
  }

  /**
   * Get task by ID
   */
  async getTaskById(taskId: string, userId: string): Promise<Task | null> {
    try {
      const task = await prisma.task.findFirst({
        where: {
          id: taskId,
          userId,
        },
        include: {
          recurrencePattern: true,
          reminders: true,
        },
      });

      return task;
    } catch (error) {
      logger.error('Failed to get task:', error);
      throw error;
    }
  }

  /**
   * Get all tasks for a user with filters
   */
  async getTasks(filters: TaskFilters): Promise<Task[]> {
    try {
      const where: any = {
        userId: filters.userId,
      };

      if (filters.status) {
        where.status = filters.status;
      }

      if (filters.priority) {
        where.priority = filters.priority;
      }

      if (filters.tags && filters.tags.length > 0) {
        where.tags = {
          hasSome: filters.tags,
        };
      }

      if (filters.search) {
        where.OR = [
          { title: { contains: filters.search, mode: 'insensitive' } },
          { description: { contains: filters.search, mode: 'insensitive' } },
        ];
      }

      if (filters.dueDateFrom || filters.dueDateTo) {
        where.dueDate = {};
        if (filters.dueDateFrom) {
          where.dueDate.gte = filters.dueDateFrom;
        }
        if (filters.dueDateTo) {
          where.dueDate.lte = filters.dueDateTo;
        }
      }

      const tasks = await prisma.task.findMany({
        where,
        include: {
          recurrencePattern: true,
          reminders: true,
        },
        orderBy: [
          { dueDate: 'asc' },
          { createdAt: 'desc' },
        ],
      });

      return tasks;
    } catch (error) {
      logger.error('Failed to get tasks:', error);
      throw error;
    }
  }

  /**
   * Update a task
   */
  async updateTask(taskId: string, userId: string, input: UpdateTaskInput): Promise<Task> {
    const correlationId = uuidv4();

    try {
      // Get current task state
      const beforeState = await this.getTaskById(taskId, userId);
      if (!beforeState) {
        throw new Error('Task not found');
      }

      // Update task
      const task = await prisma.task.update({
        where: {
          id: taskId,
          userId,
        },
        data: input,
        include: {
          recurrencePattern: true,
        },
      });

      // Publish task.updated event
      await kafkaProducer.publishTaskEvent(
        'task.updated',
        userId,
        task.id,
        {
          id: task.id,
          title: task.title,
          description: task.description || '',
          status: task.status,
          priority: task.priority,
          tags: task.tags,
          dueDate: task.dueDate?.toISOString(),
          isRecurring: task.isRecurring,
          recurrencePattern: task.recurrencePattern,
          createdAt: task.createdAt.toISOString(),
          updatedAt: task.updatedAt.toISOString(),
        },
        correlationId
      );

      // Publish to task-updates for real-time sync
      await kafkaProducer.publishTaskUpdate(
        userId,
        task.id,
        { action: 'updated', changes: input, task },
        correlationId
      );

      logger.info('Task updated:', { taskId: task.id, userId, correlationId });

      return task;
    } catch (error) {
      logger.error('Failed to update task:', error);
      throw error;
    }
  }

  /**
   * Complete a task (and generate next occurrence if recurring)
   */
  async completeTask(taskId: string, userId: string): Promise<Task> {
    const correlationId = uuidv4();

    try {
      // Update task status
      const task = await prisma.task.update({
        where: {
          id: taskId,
          userId,
        },
        data: {
          status: TaskStatus.COMPLETED,
          completedAt: new Date(),
        },
        include: {
          recurrencePattern: true,
        },
      });

      // Publish task.completed event
      await kafkaProducer.publishTaskEvent(
        'task.completed',
        userId,
        task.id,
        {
          id: task.id,
          title: task.title,
          description: task.description || '',
          status: task.status,
          priority: task.priority,
          tags: task.tags,
          dueDate: task.dueDate?.toISOString(),
          completedAt: task.completedAt?.toISOString(),
          isRecurring: task.isRecurring,
          recurrencePattern: task.recurrencePattern,
          createdAt: task.createdAt.toISOString(),
          updatedAt: task.updatedAt.toISOString(),
        },
        correlationId
      );

      // Publish to task-updates for real-time sync
      await kafkaProducer.publishTaskUpdate(
        userId,
        task.id,
        { action: 'completed', task },
        correlationId
      );

      // If recurring, generate next occurrence
      // This will be handled by RecurringTaskAgent consuming the task.completed event
      // But we can also do it synchronously here for immediate response
      if (task.isRecurring) {
        await recurringTaskService.generateNextOccurrence(task);
      }

      logger.info('Task completed:', { taskId: task.id, userId, correlationId });

      return task;
    } catch (error) {
      logger.error('Failed to complete task:', error);
      throw error;
    }
  }

  /**
   * Delete a task
   */
  async deleteTask(taskId: string, userId: string): Promise<void> {
    const correlationId = uuidv4();

    try {
      // Get task before deletion
      const task = await this.getTaskById(taskId, userId);
      if (!task) {
        throw new Error('Task not found');
      }

      // Delete task
      await prisma.task.delete({
        where: {
          id: taskId,
          userId,
        },
      });

      // Publish task.deleted event
      await kafkaProducer.publishTaskEvent(
        'task.deleted',
        userId,
        taskId,
        {
          id: task.id,
          title: task.title,
          description: task.description || '',
          status: task.status,
          priority: task.priority,
          tags: task.tags,
          dueDate: task.dueDate?.toISOString(),
          isRecurring: task.isRecurring,
          createdAt: task.createdAt.toISOString(),
          updatedAt: task.updatedAt.toISOString(),
        },
        correlationId
      );

      // Publish to task-updates for real-time sync
      await kafkaProducer.publishTaskUpdate(
        userId,
        taskId,
        { action: 'deleted' },
        correlationId
      );

      logger.info('Task deleted:', { taskId, userId, correlationId });
    } catch (error) {
      logger.error('Failed to delete task:', error);
      throw error;
    }
  }
}

export const taskService = new TaskService();
