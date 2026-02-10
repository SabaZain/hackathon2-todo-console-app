import request from 'supertest';
import { app } from '../../index';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

describe('Task API - Integration Tests', () => {
  let authToken: string;
  let userId: string;
  let createdTaskId: string;

  beforeAll(async () => {
    // Setup: Create test user and get auth token
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'Test123!@#',
        name: 'Test User',
      });

    authToken = response.body.token;
    userId = response.body.user.id;
  });

  afterAll(async () => {
    // Cleanup: Delete test data
    await prisma.task.deleteMany({ where: { userId } });
    await prisma.user.delete({ where: { id: userId } });
    await prisma.$disconnect();
  });

  afterEach(async () => {
    // Clean up tasks after each test
    await prisma.task.deleteMany({ where: { userId } });
  });

  describe('POST /api/tasks', () => {
    it('should create a new task', async () => {
      const taskData = {
        title: 'Integration Test Task',
        description: 'This is a test task',
        priority: 'high',
        tags: ['test', 'integration'],
      };

      const response = await request(app)
        .post('/api/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .send(taskData)
        .expect(201);

      expect(response.body).toMatchObject({
        title: taskData.title,
        description: taskData.description,
        priority: taskData.priority,
        tags: taskData.tags,
        completed: false,
      });

      expect(response.body.id).toBeDefined();
      expect(response.body.userId).toBe(userId);

      createdTaskId = response.body.id;
    });

    it('should return 400 for invalid task data', async () => {
      const invalidData = {
        description: 'Missing title',
      };

      await request(app)
        .post('/api/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .send(invalidData)
        .expect(400);
    });

    it('should return 401 without auth token', async () => {
      const taskData = {
        title: 'Unauthorized Task',
      };

      await request(app)
        .post('/api/tasks')
        .send(taskData)
        .expect(401);
    });

    it('should create recurring task', async () => {
      const recurringTask = {
        title: 'Daily Standup',
        isRecurring: true,
        recurrencePattern: 'daily',
        dueDate: new Date(Date.now() + 86400000).toISOString(),
      };

      const response = await request(app)
        .post('/api/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .send(recurringTask)
        .expect(201);

      expect(response.body.isRecurring).toBe(true);
      expect(response.body.recurrencePattern).toBe('daily');
    });
  });

  describe('GET /api/tasks', () => {
    beforeEach(async () => {
      // Create test tasks
      await prisma.task.createMany({
        data: [
          {
            title: 'Task 1',
            userId,
            priority: 'high',
            tags: ['work'],
          },
          {
            title: 'Task 2',
            userId,
            priority: 'low',
            tags: ['personal'],
          },
          {
            title: 'Task 3',
            userId,
            priority: 'high',
            tags: ['work', 'urgent'],
            completed: true,
          },
        ],
      });
    });

    it('should return all tasks for authenticated user', async () => {
      const response = await request(app)
        .get('/api/tasks')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body).toHaveLength(3);
      expect(response.body[0]).toHaveProperty('id');
      expect(response.body[0]).toHaveProperty('title');
    });

    it('should filter tasks by priority', async () => {
      const response = await request(app)
        .get('/api/tasks?priority=high')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body).toHaveLength(2);
      expect(response.body.every((task: any) => task.priority === 'high')).toBe(true);
    });

    it('should filter tasks by tags', async () => {
      const response = await request(app)
        .get('/api/tasks?tags=work')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.length).toBeGreaterThan(0);
      expect(
        response.body.every((task: any) => task.tags.includes('work'))
      ).toBe(true);
    });

    it('should filter completed tasks', async () => {
      const response = await request(app)
        .get('/api/tasks?completed=true')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body).toHaveLength(1);
      expect(response.body[0].completed).toBe(true);
    });

    it('should search tasks by title', async () => {
      const response = await request(app)
        .get('/api/tasks?search=Task 1')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body).toHaveLength(1);
      expect(response.body[0].title).toBe('Task 1');
    });

    it('should sort tasks by priority', async () => {
      const response = await request(app)
        .get('/api/tasks?sortBy=priority&sortOrder=desc')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      // High priority should come first
      expect(response.body[0].priority).toBe('high');
    });
  });

  describe('GET /api/tasks/:id', () => {
    let taskId: string;

    beforeEach(async () => {
      const task = await prisma.task.create({
        data: {
          title: 'Specific Task',
          userId,
        },
      });
      taskId = task.id;
    });

    it('should return a specific task', async () => {
      const response = await request(app)
        .get(`/api/tasks/${taskId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.id).toBe(taskId);
      expect(response.body.title).toBe('Specific Task');
    });

    it('should return 404 for nonexistent task', async () => {
      await request(app)
        .get('/api/tasks/nonexistent-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);
    });

    it('should return 403 for task owned by another user', async () => {
      // Create another user's task
      const otherUser = await prisma.user.create({
        data: {
          email: 'other@example.com',
          password: 'hashed',
          name: 'Other User',
        },
      });

      const otherTask = await prisma.task.create({
        data: {
          title: 'Other User Task',
          userId: otherUser.id,
        },
      });

      await request(app)
        .get(`/api/tasks/${otherTask.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(403);

      // Cleanup
      await prisma.task.delete({ where: { id: otherTask.id } });
      await prisma.user.delete({ where: { id: otherUser.id } });
    });
  });

  describe('PUT /api/tasks/:id', () => {
    let taskId: string;

    beforeEach(async () => {
      const task = await prisma.task.create({
        data: {
          title: 'Task to Update',
          userId,
          priority: 'low',
        },
      });
      taskId = task.id;
    });

    it('should update a task', async () => {
      const updates = {
        title: 'Updated Task',
        priority: 'high',
        tags: ['updated'],
      };

      const response = await request(app)
        .put(`/api/tasks/${taskId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send(updates)
        .expect(200);

      expect(response.body.title).toBe(updates.title);
      expect(response.body.priority).toBe(updates.priority);
      expect(response.body.tags).toEqual(updates.tags);
    });

    it('should return 404 for nonexistent task', async () => {
      await request(app)
        .put('/api/tasks/nonexistent-id')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ title: 'Updated' })
        .expect(404);
    });
  });

  describe('DELETE /api/tasks/:id', () => {
    let taskId: string;

    beforeEach(async () => {
      const task = await prisma.task.create({
        data: {
          title: 'Task to Delete',
          userId,
        },
      });
      taskId = task.id;
    });

    it('should delete a task', async () => {
      await request(app)
        .delete(`/api/tasks/${taskId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(204);

      // Verify task is deleted
      const deletedTask = await prisma.task.findUnique({
        where: { id: taskId },
      });
      expect(deletedTask).toBeNull();
    });

    it('should return 404 for nonexistent task', async () => {
      await request(app)
        .delete('/api/tasks/nonexistent-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);
    });
  });

  describe('POST /api/tasks/:id/complete', () => {
    let taskId: string;

    beforeEach(async () => {
      const task = await prisma.task.create({
        data: {
          title: 'Task to Complete',
          userId,
          completed: false,
        },
      });
      taskId = task.id;
    });

    it('should mark task as completed', async () => {
      const response = await request(app)
        .post(`/api/tasks/${taskId}/complete`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.completed).toBe(true);
      expect(response.body.completedAt).toBeDefined();
    });

    it('should handle completing already completed task', async () => {
      // Complete once
      await request(app)
        .post(`/api/tasks/${taskId}/complete`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      // Complete again
      const response = await request(app)
        .post(`/api/tasks/${taskId}/complete`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.completed).toBe(true);
    });
  });
});
