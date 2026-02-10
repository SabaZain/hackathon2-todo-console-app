import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';
import ws from 'k6/ws';

const errorRate = new Rate('websocket_errors');

export const options = {
  stages: [
    { duration: '1m', target: 20 },   // Ramp up to 20 concurrent connections
    { duration: '3m', target: 20 },   // Maintain 20 connections
    { duration: '1m', target: 50 },   // Ramp up to 50 connections
    { duration: '3m', target: 50 },   // Maintain 50 connections
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    websocket_errors: ['rate<0.05'],  // Less than 5% error rate
    ws_connecting: ['p(95)<1000'],    // 95% of connections under 1s
    ws_msgs_received: ['count>100'],  // Receive at least 100 messages
  },
};

const BASE_URL = __ENV.WS_URL || 'ws://localhost:3001';

export default function () {
  const url = `${BASE_URL}/socket.io/?EIO=4&transport=websocket`;

  const params = {
    headers: {
      'Authorization': `Bearer ${__ENV.AUTH_TOKEN}`,
    },
  };

  const res = ws.connect(url, params, function (socket) {
    socket.on('open', () => {
      console.log('WebSocket connection established');

      // Send authentication
      socket.send(JSON.stringify({
        type: 'auth',
        userId: `loadtest-user-${__VU}`,
      }));
    });

    socket.on('message', (data) => {
      const message = JSON.parse(data);

      const success = check(message, {
        'message received': (m) => m !== null,
        'message has type': (m) => m.type !== undefined,
      });

      errorRate.add(!success);
    });

    socket.on('error', (e) => {
      console.error(`WebSocket error: ${e}`);
      errorRate.add(true);
    });

    socket.on('close', () => {
      console.log('WebSocket connection closed');
    });

    // Keep connection alive for test duration
    socket.setTimeout(() => {
      socket.close();
    }, 30000); // 30 seconds

    // Simulate user activity
    socket.setInterval(() => {
      socket.send(JSON.stringify({
        type: 'ping',
        timestamp: Date.now(),
      }));
    }, 5000); // Every 5 seconds
  });

  check(res, {
    'WebSocket connection successful': (r) => r && r.status === 101,
  });

  sleep(1);
}
