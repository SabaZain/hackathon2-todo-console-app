import { TaskService } from '../../services/TaskService';
import { PrismaClient } from '@prisma/client';

// Mock Prisma
jest.mock('@prisma/client');

describe('TaskService - Unit Tests', () => {
  let taskService: TaskService;
  let mockPrisma: jest.Mocked<PrismaClient>;

  beforeEach(() => {
    mockPrisma = {
      task: {
        create: jest.fn(),
        findMany: jest.fn(),
        findUnique: jest.fn(),
        update: jest.fn(),
        delete: jest.fn(),
      },
    } as any;

    taskService = new TaskService(mockPrisma);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('createTask', () => {
    it('should create a task successfully', async () => {
      const taskData = {
        title: 'Test Task',
        description: 'Test Description',
        userId: 'user-123',
        priority: 'high',
        tags: ['work', 'urgent'],
      };

      const expectedTask = {
        id: 'task-123',
        ...taskData,
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      mockPrisma.task.create.mockResolvedValue(expectedTask as any);

      const result = await taskService.createTask(taskData);

      expect(result).toEqual(expectedTask);
      expect(mockPrisma.task.create).toHaveBeenCalledWith({
        data: taskData,
      });
    });

    it('should throw error when title is missing', async () => {
      const taskData = {
        description: 'Test Description',
        userId: 'user-123',
      } as any;

      await expect(taskService.createTask(taskData)).rejects.toThrow();
    });

    it('should create recurring task with pattern', async () => {
      const taskData = {
        title: 'Recurring Task',
        userId: 'user-123',
        isRecurring: true,
        recurrencePattern: 'daily',
      };

      const expectedTask = {
        id: 'task-123',
        ...taskData,
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      mockPrisma.task.create.mockResolvedValue(expectedTask as any);

      const result = await taskService.createTask(taskData);

      expect(result.isRecurring).toBe(true);
      expect(result.recurrencePattern).toBe('daily');
    });
  });

  describe('getTasks', () => {
    it('should return all tasks for a user', async () => {
      const userId = 'user-123';
      const expectedTasks = [
        { id: 'task-1', title: 'Task 1', userId },
        { id: 'task-2', title: 'Task 2', userId },
      ];

      mockPrisma.task.findMany.mockResolvedValue(expectedTasks as any);

      const result = await taskService.getTasks(userId);

      expect(result).toEqual(expectedTasks);
      expect(mockPrisma.task.findMany).toHaveBeenCalledWith({
        where: { userId },
        orderBy: { createdAt: 'desc' },
      });
    });

    it('should filter tasks by priority', async () => {
      const userId = 'user-123';
      const priority = 'high';

      mockPrisma.task.findMany.mockResolvedValue([]);

      await taskService.getTasks(userId, { priority });

      expect(mockPrisma.task.findMany).toHaveBeenCalledWith({
        where: { userId, priority },
        orderBy: { createdAt: 'desc' },
      });
    });

    it('should filter tasks by tags', async () => {
      const userId = 'user-123';
      const tags = ['work', 'urgent'];

      mockPrisma.task.findMany.mockResolvedValue([]);

      await taskService.getTasks(userId, { tags });

      expect(mockPrisma.task.findMany).toHaveBeenCalledWith({
        where: {
          userId,
          tags: { hasSome: tags },
        },
        orderBy: { createdAt: 'desc' },
      });
    });

    it('should search tasks by title', async () => {
      const userId = 'user-123';
      const search = 'important';

      mockPrisma.task.findMany.mockResolvedValue([]);

      await taskService.getTasks(userId, { search });

      expect(mockPrisma.task.findMany).toHaveBeenCalledWith({
        where: {
          userId,
          OR: [
            { title: { contains: search, mode: 'insensitive' } },
            { description: { contains: search, mode: 'insensitive' } },
          ],
        },
        orderBy: { createdAt: 'desc' },
      });
    });
  });

  describe('updateTask', () => {
    it('should update a task successfully', async () => {
      const taskId = 'task-123';
      const userId = 'user-123';
      const updates = {
        title: 'Updated Title',
        completed: true,
      };

      const existingTask = {
        id: taskId,
        userId,
        title: 'Original Title',
        completed: false,
      };

      const updatedTask = {
        ...existingTask,
        ...updates,
      };

      mockPrisma.task.findUnique.mockResolvedValue(existingTask as any);
      mockPrisma.task.update.mockResolvedValue(updatedTask as any);

      const result = await taskService.updateTask(taskId, userId, updates);

      expect(result).toEqual(updatedTask);
      expect(mockPrisma.task.update).toHaveBeenCalledWith({
        where: { id: taskId },
        data: updates,
      });
    });

    it('should throw error when task not found', async () => {
      const taskId = 'nonexistent';
      const userId = 'user-123';

      mockPrisma.task.findUnique.mockResolvedValue(null);

      await expect(
        taskService.updateTask(taskId, userId, { title: 'New Title' })
      ).rejects.toThrow('Task not found');
    });

    it('should throw error when user does not own task', async () => {
      const taskId = 'task-123';
      const userId = 'user-123';
      const wrongUserId = 'user-456';

      const existingTask = {
        id: taskId,
        userId: wrongUserId,
        title: 'Task',
      };

      mockPrisma.task.findUnique.mockResolvedValue(existingTask as any);

      await expect(
        taskService.updateTask(taskId, userId, { title: 'New Title' })
      ).rejects.toThrow('Unauthorized');
    });
  });

  describe('deleteTask', () => {
    it('should delete a task successfully', async () => {
      const taskId = 'task-123';
      const userId = 'user-123';

      const existingTask = {
        id: taskId,
        userId,
        title: 'Task to delete',
      };

      mockPrisma.task.findUnique.mockResolvedValue(existingTask as any);
      mockPrisma.task.delete.mockResolvedValue(existingTask as any);

      await taskService.deleteTask(taskId, userId);

      expect(mockPrisma.task.delete).toHaveBeenCalledWith({
        where: { id: taskId },
      });
    });

    it('should throw error when task not found', async () => {
      const taskId = 'nonexistent';
      const userId = 'user-123';

      mockPrisma.task.findUnique.mockResolvedValue(null);

      await expect(taskService.deleteTask(taskId, userId)).rejects.toThrow(
        'Task not found'
      );
    });
  });

  describe('completeTask', () => {
    it('should mark task as completed', async () => {
      const taskId = 'task-123';
      const userId = 'user-123';

      const existingTask = {
        id: taskId,
        userId,
        completed: false,
      };

      const completedTask = {
        ...existingTask,
        completed: true,
        completedAt: new Date(),
      };

      mockPrisma.task.findUnique.mockResolvedValue(existingTask as any);
      mockPrisma.task.update.mockResolvedValue(completedTask as any);

      const result = await taskService.completeTask(taskId, userId);

      expect(result.completed).toBe(true);
      expect(result.completedAt).toBeDefined();
    });

    it('should handle recurring task completion', async () => {
      const taskId = 'task-123';
      const userId = 'user-123';

      const existingTask = {
        id: taskId,
        userId,
        completed: false,
        isRecurring: true,
        recurrencePattern: 'daily',
      };

      mockPrisma.task.findUnique.mockResolvedValue(existingTask as any);
      mockPrisma.task.update.mockResolvedValue({
        ...existingTask,
        completed: true,
      } as any);

      const result = await taskService.completeTask(taskId, userId);

      expect(result.completed).toBe(true);
      // Verify that recurring task event would be published
    });
  });
});
