const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');
const Joi = require('joi');

// Validation schema
const memberSchema = Joi.object({
  name: Joi.string().required().min(2).max(100),
  email: Joi.string().email().required(),
  phone: Joi.string().required().pattern(/^[0-9-+() ]{10,20}$/),
  address: Joi.string().required()
});

// Get all members
router.get('/', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM members');
    res.json(rows);
  } catch (error) {
    console.error('Error fetching members:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get member by ID
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM members WHERE member_id = ?', [req.params.id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: 'Member not found' });
    }
    res.json(rows[0]);
  } catch (error) {
    console.error('Error fetching member:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new member
router.post('/', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = memberSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if email already exists
    const [existing] = await pool.query('SELECT * FROM members WHERE email = ?', [value.email]);
    if (existing.length > 0) {
      return res.status(400).json({ error: 'Email already registered' });
    }

    // Insert new member
    const [result] = await pool.query(
      'INSERT INTO members (name, email, phone, address, membership_date, membership_status) VALUES (?, ?, ?, ?, CURDATE(), "Active")',
      [value.name, value.email, value.phone, value.address]
    );

    res.status(201).json({
      message: 'Member created successfully',
      member_id: result.insertId
    });
  } catch (error) {
    console.error('Error creating member:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update member
router.put('/:id', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = memberSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if member exists
    const [existing] = await pool.query('SELECT * FROM members WHERE member_id = ?', [req.params.id]);
    if (existing.length === 0) {
      return res.status(404).json({ error: 'Member not found' });
    }

    // Update member
    await pool.query(
      'UPDATE members SET name = ?, email = ?, phone = ?, address = ? WHERE member_id = ?',
      [value.name, value.email, value.phone, value.address, req.params.id]
    );

    res.json({ message: 'Member updated successfully' });
  } catch (error) {
    console.error('Error updating member:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Delete member
router.delete('/:id', async (req, res) => {
  try {
    // Check if member exists
    const [existing] = await pool.query('SELECT * FROM members WHERE member_id = ?', [req.params.id]);
    if (existing.length === 0) {
      return res.status(404).json({ error: 'Member not found' });
    }

    // Delete member
    await pool.query('DELETE FROM members WHERE member_id = ?', [req.params.id]);

    res.json({ message: 'Member deleted successfully' });
  } catch (error) {
    console.error('Error deleting member:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router; 