# Phase 5 Testing Guide

Complete testing documentation for the Phase 5 event-driven task management system.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Test Types](#test-types)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Writing Tests](#writing-tests)
6. [CI/CD Integration](#cicd-integration)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Phase 5 includes comprehensive testing across multiple layers:

- **Unit Tests**: Test individual functions and services
- **Integration Tests**: Test API endpoints and service interactions
- **E2E Tests**: Test complete user workflows
- **Load Tests**: Test system performance under load
- **WebSocket Tests**: Test real-time synchronization
- **Kafka Tests**: Test event-driven flows

### Test Stack

- **Jest**: Unit and integration testing
- **Supertest**: HTTP API testing
- **Playwright**: E2E browser testing
- **k6**: Load and performance testing

---

## Test Types

### 1. Unit Tests

**Location**: `backend/src/**/__tests__/unit/*.test.ts`

**Purpose**: Test individual functions, services, and utilities in isolation.

**Example**:
```typescript
describe('TaskService', () => {
  it('should create a task', async () => {
    const task = await taskService.createTask({
      title: 'Test Task',
      userId: 'user-123',
    });
    expect(task.id).toBeDefined();
  });
});
```

**Run**:
```bash
npm run test:unit
```

### 2. Integration Tests

**Location**: `backend/src/**/__tests__/integration/*.test.ts`

**Purpose**: Test API endpoints, database interactions, and service integrations.

**Example**:
```typescript
describe('POST /api/tasks', () => {
  it('should create a new task', async () => {
    const response = await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'Integration Test' })
      .expect(201);

    expect(response.body.title).toBe('Integration Test');
  });
});
```

**Run**:
```bash
npm run test:integration
```

### 3. E2E Tests

**Location**: `frontend/e2e/*.spec.ts`

**Purpose**: Test complete user workflows in a real browser.

**Example**:
```typescript
test('should create and complete a task', async ({ page }) => {
  await page.goto('/tasks');
  await page.click('button:has-text("New Task")');
  await page.fill('input[name="title"]', 'E2E Task');
  await page.click('button:has-text("Create")');
  await page.click('[data-testid="complete-checkbox"]');
  await expect(page.locator('text=E2E Task')).toHaveClass(/completed/);
});
```

**Run**:
```bash
cd frontend
npm run test:e2e
```

### 4. Load Tests

**Location**: `load-tests/*.js`

**Purpose**: Test system performance under load.

**Example**:
```javascript
export default function() {
  const res = http.post(`${BASE_URL}/api/tasks`, payload, { headers });
  check(res, {
    'status is 201': (r) => r.status === 201,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

**Run**:
```bash
k6 run load-tests/tasks-load-test.js
```

### 5. WebSocket Tests

**Location**: `backend/src/__tests__/integration/websocket.test.ts`

**Purpose**: Test real-time synchronization.

**Example**:
```typescript
test('should broadcast task updates', (done) => {
  clientSocket.on('task-update', (data) => {
    expect(data.type).toBe('task.updated');
    done();
  });
  io.emit('task-update', { type: 'task.updated' });
});
```

### 6. Kafka Event Tests

**Location**: `backend/src/__tests__/integration/kafka-events.test.ts`

**Purpose**: Test event-driven flows.

**Example**:
```typescript
test('should process task.completed event', async () => {
  await producer.send({
    topic: 'task-events',
    messages: [{ value: JSON.stringify(event) }],
  });

  await waitFor(() => receivedEvents.length > 0);
  expect(receivedEvents[0].type).toBe('task.completed');
});
```

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run unit tests only
npm run test:unit

# Run integration tests only
npm run test:integration

# Watch mode
npm run test:watch

# Run specific test file
npm test -- tasks.test.ts
```

### Frontend E2E Tests

```bash
cd frontend

# Install Playwright browsers (first time only)
npx playwright install

# Run all E2E tests
npm run test:e2e

# Run in headed mode (see browser)
npm run test:e2e -- --headed

# Run specific browser
npm run test:e2e -- --project=chromium

# Debug mode
npm run test:e2e -- --debug

# Generate report
npm run test:e2e -- --reporter=html
```

### Load Tests

```bash
cd load-tests

# Install k6 (if not installed)
# macOS: brew install k6
# Linux: sudo apt-get install k6
# Windows: choco install k6

# Run tasks load test
k6 run tasks-load-test.js

# Run with custom VUs and duration
k6 run --vus 100 --duration 5m tasks-load-test.js

# Run WebSocket load test
k6 run websocket-load-test.js

# Run with environment variables
k6 run -e BASE_URL=http://production.example.com tasks-load-test.js
```

---

## Test Coverage

### Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| Backend Services | 80% | TBD |
| API Routes | 90% | TBD |
| Frontend Components | 70% | TBD |
| E2E Critical Paths | 100% | TBD |

### Generate Coverage Report

```bash
# Backend
cd backend
npm run test:coverage

# View HTML report
open coverage/lcov-report/index.html
```

### Coverage Thresholds

Configured in `jest.config.js`:
```javascript
coverageThreshold: {
  global: {
    branches: 70,
    functions: 70,
    lines: 70,
    statements: 70,
  },
}
```

---

## Writing Tests

### Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **One Assertion Per Test**: Keep tests focused
3. **Use Descriptive Names**: Test names should explain what they test
4. **Clean Up After Tests**: Use `afterEach` and `afterAll`
5. **Mock External Dependencies**: Don't rely on external services
6. **Test Edge Cases**: Not just happy paths

### Unit Test Template

```typescript
import { ServiceToTest } from '../ServiceToTest';

describe('ServiceToTest', () => {
  let service: ServiceToTest;

  beforeEach(() => {
    service = new ServiceToTest();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('methodName', () => {
    it('should do something when condition', () => {
      // Arrange
      const input = { /* test data */ };

      // Act
      const result = service.methodName(input);

      // Assert
      expect(result).toEqual(expectedOutput);
    });

    it('should throw error when invalid input', () => {
      expect(() => service.methodName(null)).toThrow();
    });
  });
});
```

### Integration Test Template

```typescript
import request from 'supertest';
import { app } from '../../index';

describe('API Endpoint', () => {
  let authToken: string;

  beforeAll(async () => {
    // Setup: Get auth token
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'test' });
    authToken = res.body.token;
  });

  afterAll(async () => {
    // Cleanup
  });

  it('should return expected response', async () => {
    const response = await request(app)
      .get('/api/endpoint')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    expect(response.body).toMatchObject({
      // expected structure
    });
  });
});
```

### E2E Test Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Login or setup
  });

  test('should complete user workflow', async ({ page }) => {
    // Navigate
    await page.click('button:has-text("Action")');

    // Interact
    await page.fill('input[name="field"]', 'value');

    // Submit
    await page.click('button[type="submit"]');

    // Verify
    await expect(page.locator('text=Success')).toBeVisible();
  });
});
```

---

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Every push to any branch
- Every pull request
- Before deployment

**Workflow**: `.github/workflows/ci.yaml`

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          npm install
          npm run test:coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Pre-commit Hooks

Run tests before committing:

```bash
# Install husky
npm install --save-dev husky

# Setup pre-commit hook
npx husky add .husky/pre-commit "npm test"
```

---

## Troubleshooting

### Common Issues

#### 1. Tests Timeout

**Problem**: Tests hang or timeout

**Solutions**:
- Increase timeout: `jest.setTimeout(30000)`
- Check for unresolved promises
- Ensure cleanup in `afterEach`/`afterAll`
- Close database connections

#### 2. Database Connection Errors

**Problem**: Cannot connect to test database

**Solutions**:
- Ensure test database is running
- Check `DATABASE_URL` environment variable
- Use separate test database
- Run migrations: `npm run prisma:migrate`

#### 3. Port Already in Use

**Problem**: Test server can't start

**Solutions**:
- Kill process using port: `lsof -ti:3001 | xargs kill`
- Use random port for tests
- Ensure previous tests cleaned up

#### 4. Flaky Tests

**Problem**: Tests pass/fail inconsistently

**Solutions**:
- Add proper waits in E2E tests
- Use `waitFor` utilities
- Avoid hardcoded timeouts
- Check for race conditions
- Ensure proper test isolation

#### 5. Mock Issues

**Problem**: Mocks not working correctly

**Solutions**:
- Clear mocks between tests: `jest.clearAllMocks()`
- Reset modules: `jest.resetModules()`
- Check mock implementation
- Verify mock is called: `expect(mock).toHaveBeenCalled()`

### Debug Mode

**Jest**:
```bash
node --inspect-brk node_modules/.bin/jest --runInBand
```

**Playwright**:
```bash
npm run test:e2e -- --debug
```

**k6**:
```bash
k6 run --http-debug tasks-load-test.js
```

---

## Test Data Management

### Test Database

Use separate database for tests:

```bash
# .env.test
DATABASE_URL="postgresql://test:test@localhost:5432/phase5_test"
```

### Fixtures

Create reusable test data:

```typescript
// fixtures/tasks.ts
export const testTasks = {
  basic: {
    title: 'Test Task',
    userId: 'user-123',
  },
  recurring: {
    title: 'Daily Task',
    isRecurring: true,
    recurrencePattern: 'daily',
  },
};
```

### Factories

Generate test data dynamically:

```typescript
// factories/taskFactory.ts
export const createTask = (overrides = {}) => ({
  id: `task-${Date.now()}`,
  title: 'Test Task',
  userId: 'user-123',
  completed: false,
  createdAt: new Date(),
  ...overrides,
});
```

---

## Performance Testing

### Load Test Scenarios

1. **Baseline**: Normal load (50 users)
2. **Peak**: High load (200 users)
3. **Stress**: Breaking point (500+ users)
4. **Spike**: Sudden traffic increase
5. **Soak**: Extended duration (1+ hours)

### Metrics to Monitor

- **Response Time**: p50, p95, p99
- **Throughput**: Requests per second
- **Error Rate**: Failed requests percentage
- **Resource Usage**: CPU, memory, connections

### Performance Thresholds

```javascript
thresholds: {
  http_req_duration: ['p(95)<500'],  // 95% under 500ms
  http_req_failed: ['rate<0.01'],    // <1% errors
  http_reqs: ['rate>100'],           // >100 req/s
}
```

---

## Continuous Improvement

### Test Metrics

Track over time:
- Test count
- Coverage percentage
- Test execution time
- Flaky test rate

### Regular Reviews

- Review test failures weekly
- Update tests when features change
- Remove obsolete tests
- Add tests for bugs found

### Test Automation

- Run tests on every commit
- Block merges if tests fail
- Generate coverage reports
- Alert on coverage drops

---

## Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Playwright Documentation](https://playwright.dev/)
- [k6 Documentation](https://k6.io/docs/)
- [Testing Best Practices](https://testingjavascript.com/)

---

## Quick Reference

```bash
# Backend
npm test                    # Run all tests
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests only
npm run test:coverage      # With coverage report
npm run test:watch         # Watch mode

# Frontend
npm run test:e2e           # E2E tests
npm run test:e2e -- --headed  # With browser visible
npm run test:e2e -- --debug   # Debug mode

# Load Tests
k6 run tasks-load-test.js              # Basic load test
k6 run --vus 100 tasks-load-test.js    # 100 virtual users
k6 run websocket-load-test.js          # WebSocket test
```

---

**Status**: Testing infrastructure complete and ready for use!
