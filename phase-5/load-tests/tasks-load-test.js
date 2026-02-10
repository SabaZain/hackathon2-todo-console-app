import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.01'],   // Error rate should be less than 1%
    errors: ['rate<0.1'],             // Custom error rate should be less than 10%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3001';
let authToken = '';

// Setup function - runs once per VU
export function setup() {
  // Register a test user
  const registerRes = http.post(`${BASE_URL}/api/auth/register`, JSON.stringify({
    email: `loadtest-${Date.now()}@example.com`,
    password: 'LoadTest123!@#',
    name: 'Load Test User',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(registerRes, {
    'registration successful': (r) => r.status === 201,
  });

  return { token: registerRes.json('token') };
}

// Main test function
export default function (data) {
  const token = data.token;
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  // Test 1: Create Task
  const createTaskRes = http.post(
    `${BASE_URL}/api/tasks`,
    JSON.stringify({
      title: `Load Test Task ${Date.now()}`,
      description: 'This is a load test task',
      priority: 'high',
      tags: ['loadtest', 'performance'],
    }),
    { headers }
  );

  const createSuccess = check(createTaskRes, {
    'task created': (r) => r.status === 201,
    'task has id': (r) => r.json('id') !== undefined,
  });

  errorRate.add(!createSuccess);

  if (!createSuccess) {
    console.error(`Failed to create task: ${createTaskRes.status}`);
    return;
  }

  const taskId = createTaskRes.json('id');

  sleep(1);

  // Test 2: Get All Tasks
  const getTasksRes = http.get(`${BASE_URL}/api/tasks`, { headers });

  const getSuccess = check(getTasksRes, {
    'tasks retrieved': (r) => r.status === 200,
    'tasks is array': (r) => Array.isArray(r.json()),
  });

  errorRate.add(!getSuccess);

  sleep(1);

  // Test 3: Get Single Task
  const getTaskRes = http.get(`${BASE_URL}/api/tasks/${taskId}`, { headers });

  check(getTaskRes, {
    'task retrieved': (r) => r.status === 200,
    'task id matches': (r) => r.json('id') === taskId,
  });

  sleep(1);

  // Test 4: Update Task
  const updateTaskRes = http.put(
    `${BASE_URL}/api/tasks/${taskId}`,
    JSON.stringify({
      title: `Updated Task ${Date.now()}`,
      priority: 'urgent',
    }),
    { headers }
  );

  check(updateTaskRes, {
    'task updated': (r) => r.status === 200,
    'title updated': (r) => r.json('title').includes('Updated'),
  });

  sleep(1);

  // Test 5: Complete Task
  const completeTaskRes = http.post(
    `${BASE_URL}/api/tasks/${taskId}/complete`,
    null,
    { headers }
  );

  check(completeTaskRes, {
    'task completed': (r) => r.status === 200,
    'task marked complete': (r) => r.json('completed') === true,
  });

  sleep(1);

  // Test 6: Filter Tasks
  const filterRes = http.get(
    `${BASE_URL}/api/tasks?priority=high&tags=loadtest`,
    { headers }
  );

  check(filterRes, {
    'filtered tasks retrieved': (r) => r.status === 200,
  });

  sleep(1);

  // Test 7: Search Tasks
  const searchRes = http.get(
    `${BASE_URL}/api/tasks?search=Load Test`,
    { headers }
  );

  check(searchRes, {
    'search results retrieved': (r) => r.status === 200,
  });

  sleep(1);

  // Test 8: Delete Task
  const deleteTaskRes = http.del(`${BASE_URL}/api/tasks/${taskId}`, null, { headers });

  check(deleteTaskRes, {
    'task deleted': (r) => r.status === 204,
  });

  sleep(2);
}

// Teardown function - runs once per VU
export function teardown(data) {
  // Cleanup if needed
}
