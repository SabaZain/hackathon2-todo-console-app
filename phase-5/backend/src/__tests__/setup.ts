// Test setup file
import { PrismaClient } from '@prisma/client';

// Global test timeout
jest.setTimeout(30000);

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.DATABASE_URL = process.env.TEST_DATABASE_URL || 'postgresql://test:test@localhost:5432/phase5_test';
process.env.REDIS_URL = process.env.TEST_REDIS_URL || 'redis://localhost:6379';
process.env.KAFKA_BROKER = process.env.TEST_KAFKA_BROKER || 'localhost:9092';
process.env.JWT_SECRET = 'test-secret-key';

// Global test database client
let prisma: PrismaClient;

beforeAll(async () => {
  prisma = new PrismaClient();

  // Run migrations
  // await prisma.$executeRaw`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`;
});

afterAll(async () => {
  // Clean up test database
  await prisma.$disconnect();
});

// Export for use in tests
export { prisma };
