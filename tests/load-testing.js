import http from 'k6/http';
import { check, sleep } from 'k6';

// Configuration
export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up to 20 users
    { duration: '1m', target: 20 },  // Stay at 20 users
    { duration: '30s', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.01'],   // Error rate should be less than 1%
  },
};

// Base URL for the API
const BASE_URL = 'http://localhost:8000/api/v1';

// Test data
const testUser = {
  username: 'loadtestuser',
  email: 'loadtest@example.com',
  password: 'LoadTestPass123!',
  first_name: 'Load',
  last_name: 'Tester',
};

let authToken = '';

// Setup - Create a test user
export function setup() {
  const res = http.post(`${BASE_URL}/auth/register/`, JSON.stringify(testUser), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'user created successfully': (r) => r.status === 201,
  });

  // Login to get auth token
  const loginRes = http.post(`${BASE_URL}/auth/token/`, JSON.stringify({
    username: testUser.username,
    password: testUser.password,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  if (loginRes.status === 200) {
    const tokenData = JSON.parse(loginRes.body);
    authToken = tokenData.access;
  }

  return { authToken };
}

// Main test scenario
export default function (data) {
  const { authToken } = data;
  const headers = {
    'Authorization': `Bearer ${authToken}`,
    'Content-Type': 'application/json',
  };

  // Test user profile endpoint
  const profileRes = http.get(`${BASE_URL}/auth/profile/`, { headers });
  check(profileRes, {
    'profile retrieved successfully': (r) => r.status === 200,
  });

  // Test teams endpoint
  const teamsRes = http.get(`${BASE_URL}/teams/`, { headers });
  check(teamsRes, {
    'teams retrieved successfully': (r) => r.status === 200,
  });

  // Test notifications endpoint
  const notificationsRes = http.get(`${BASE_URL}/notifications/`, { headers });
  check(notificationsRes, {
    'notifications retrieved successfully': (r) => r.status === 200,
  });

  // Test calendar events endpoint
  const eventsRes = http.get(`${BASE_URL}/calendar/events/`, { headers });
  check(eventsRes, {
    'events retrieved successfully': (r) => r.status === 200,
  });

  // Test focus sessions endpoint
  const focusRes = http.get(`${BASE_URL}/focus/sessions/`, { headers });
  check(focusRes, {
    'focus sessions retrieved successfully': (r) => r.status === 200,
  });

  // Add some sleep to simulate real user behavior
  sleep(1);
}

// Teardown - Clean up test user
export function teardown(data) {
  // In a real scenario, you might want to delete the test user
  // This would require admin privileges or a special cleanup endpoint
  console.log('Load test completed');
}