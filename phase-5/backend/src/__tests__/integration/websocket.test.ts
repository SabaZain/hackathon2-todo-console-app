import { io as ioClient, Socket } from 'socket.io-client';
import { Server } from 'socket.io';
import { createServer } from 'http';
import express from 'express';

describe('WebSocket Real-Time Sync - Integration Tests', () => {
  let httpServer: any;
  let io: Server;
  let clientSocket: Socket;
  let serverPort: number;

  beforeAll((done) => {
    const app = express();
    httpServer = createServer(app);
    io = new Server(httpServer, {
      cors: {
        origin: '*',
      },
    });

    httpServer.listen(() => {
      serverPort = httpServer.address().port;
      done();
    });
  });

  afterAll((done) => {
    io.close();
    httpServer.close(done);
  });

  beforeEach((done) => {
    clientSocket = ioClient(`http://localhost:${serverPort}`, {
      auth: {
        userId: 'test-user-123',
      },
    });

    clientSocket.on('connect', done);
  });

  afterEach(() => {
    if (clientSocket.connected) {
      clientSocket.disconnect();
    }
  });

  describe('Connection Management', () => {
    it('should connect successfully with auth', (done) => {
      expect(clientSocket.connected).toBe(true);
      done();
    });

    it('should track connected clients', (done) => {
      io.on('connection', (socket) => {
        expect(socket.handshake.auth.userId).toBe('test-user-123');
        done();
      });
    });

    it('should handle disconnection', (done) => {
      io.on('connection', (socket) => {
        socket.on('disconnect', () => {
          done();
        });
      });

      clientSocket.disconnect();
    });
  });

  describe('Task Update Broadcasting', () => {
    it('should receive task-update event', (done) => {
      const taskUpdate = {
        type: 'task.updated',
        taskId: 'task-123',
        userId: 'test-user-123',
        data: {
          title: 'Updated Task',
        },
      };

      clientSocket.on('task-update', (data) => {
        expect(data).toMatchObject(taskUpdate);
        done();
      });

      // Simulate server broadcasting
      io.emit('task-update', taskUpdate);
    });

    it('should broadcast to specific user only', (done) => {
      const userId = 'test-user-123';
      const otherUserId = 'other-user-456';

      // Create second client for other user
      const otherClient = ioClient(`http://localhost:${serverPort}`, {
        auth: { userId: otherUserId },
      });

      let receivedByTarget = false;
      let receivedByOther = false;

      clientSocket.on('task-update', () => {
        receivedByTarget = true;
      });

      otherClient.on('task-update', () => {
        receivedByOther = true;
      });

      // Broadcast to specific user
      io.on('connection', (socket) => {
        if (socket.handshake.auth.userId === userId) {
          socket.emit('task-update', {
            type: 'task.updated',
            taskId: 'task-123',
          });
        }
      });

      setTimeout(() => {
        expect(receivedByTarget).toBe(true);
        expect(receivedByOther).toBe(false);
        otherClient.disconnect();
        done();
      }, 500);
    });
  });

  describe('Multiple Connections', () => {
    it('should handle multiple connections from same user', (done) => {
      const secondClient = ioClient(`http://localhost:${serverPort}`, {
        auth: { userId: 'test-user-123' },
      });

      secondClient.on('connect', () => {
        expect(clientSocket.connected).toBe(true);
        expect(secondClient.connected).toBe(true);
        secondClient.disconnect();
        done();
      });
    });

    it('should broadcast to all user connections', (done) => {
      const secondClient = ioClient(`http://localhost:${serverPort}`, {
        auth: { userId: 'test-user-123' },
      });

      let firstReceived = false;
      let secondReceived = false;

      clientSocket.on('task-update', () => {
        firstReceived = true;
      });

      secondClient.on('task-update', () => {
        secondReceived = true;
      });

      secondClient.on('connect', () => {
        io.emit('task-update', {
          type: 'task.created',
          taskId: 'new-task',
        });

        setTimeout(() => {
          expect(firstReceived).toBe(true);
          expect(secondReceived).toBe(true);
          secondClient.disconnect();
          done();
        }, 500);
      });
    });
  });

  describe('Message Types', () => {
    it('should handle task.created event', (done) => {
      clientSocket.on('task-update', (data) => {
        expect(data.type).toBe('task.created');
        expect(data.taskId).toBeDefined();
        done();
      });

      io.emit('task-update', {
        type: 'task.created',
        taskId: 'new-task-123',
        data: { title: 'New Task' },
      });
    });

    it('should handle task.updated event', (done) => {
      clientSocket.on('task-update', (data) => {
        expect(data.type).toBe('task.updated');
        expect(data.changes).toBeDefined();
        done();
      });

      io.emit('task-update', {
        type: 'task.updated',
        taskId: 'task-123',
        changes: { title: 'Updated' },
      });
    });

    it('should handle task.deleted event', (done) => {
      clientSocket.on('task-update', (data) => {
        expect(data.type).toBe('task.deleted');
        done();
      });

      io.emit('task-update', {
        type: 'task.deleted',
        taskId: 'task-123',
      });
    });

    it('should handle task.completed event', (done) => {
      clientSocket.on('task-update', (data) => {
        expect(data.type).toBe('task.completed');
        expect(data.data.completed).toBe(true);
        done();
      });

      io.emit('task-update', {
        type: 'task.completed',
        taskId: 'task-123',
        data: { completed: true },
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle connection errors gracefully', (done) => {
      const badClient = ioClient('http://localhost:9999');

      badClient.on('connect_error', (error) => {
        expect(error).toBeDefined();
        badClient.disconnect();
        done();
      });
    });

    it('should handle malformed messages', (done) => {
      clientSocket.on('task-update', (data) => {
        // Should still receive the message
        expect(data).toBeDefined();
        done();
      });

      io.emit('task-update', null);
    });
  });

  describe('Performance', () => {
    it('should handle rapid message broadcasting', (done) => {
      let receivedCount = 0;
      const messageCount = 100;

      clientSocket.on('task-update', () => {
        receivedCount++;
        if (receivedCount === messageCount) {
          done();
        }
      });

      for (let i = 0; i < messageCount; i++) {
        io.emit('task-update', {
          type: 'task.updated',
          taskId: `task-${i}`,
        });
      }
    });
  });
});
