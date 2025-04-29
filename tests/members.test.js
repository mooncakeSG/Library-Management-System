const request = require('supertest');
const app = require('../app');
const { pool } = require('../config/database');

// Test data
const testMember = {
  name: 'Test User',
  email: 'test@example.com',
  phone: '1234567890',
  address: '123 Test St'
};

let memberId;

// Setup and teardown
beforeAll(async () => {
  // Clear members table before tests
  await pool.query('DELETE FROM members WHERE email = ?', [testMember.email]);
});

afterAll(async () => {
  // Clean up after tests
  await pool.query('DELETE FROM members WHERE email = ?', [testMember.email]);
  await pool.end();
});

describe('Members API', () => {
  // Test creating a new member
  test('POST /api/members - Create new member', async () => {
    const response = await request(app)
      .post('/api/members')
      .send(testMember);

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('member_id');
    memberId = response.body.member_id;
  });

  // Test getting all members
  test('GET /api/members - Get all members', async () => {
    const response = await request(app)
      .get('/api/members');

    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);
    expect(response.body.length).toBeGreaterThan(0);
  });

  // Test getting a specific member
  test('GET /api/members/:id - Get member by ID', async () => {
    const response = await request(app)
      .get(`/api/members/${memberId}`);

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('name', testMember.name);
    expect(response.body).toHaveProperty('email', testMember.email);
  });

  // Test updating a member
  test('PUT /api/members/:id - Update member', async () => {
    const updatedMember = {
      ...testMember,
      name: 'Updated Test User'
    };

    const response = await request(app)
      .put(`/api/members/${memberId}`)
      .send(updatedMember);

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('message', 'Member updated successfully');
  });

  // Test deleting a member
  test('DELETE /api/members/:id - Delete member', async () => {
    const response = await request(app)
      .delete(`/api/members/${memberId}`);

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('message', 'Member deleted successfully');
  });
}); 