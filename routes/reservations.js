const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');
const Joi = require('joi');

// Validation schema
const reservationSchema = Joi.object({
  book_id: Joi.number().integer().required(),
  member_id: Joi.number().integer().required(),
  reservation_date: Joi.date().required(),
  status: Joi.string().valid('Pending', 'Fulfilled', 'Cancelled').default('Pending')
});

// Get all reservations
router.get('/', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM reservations');
    res.json(rows);
  } catch (error) {
    console.error('Error fetching reservations:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get reservation by ID
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM reservations WHERE reservation_id = ?', [req.params.id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: 'Reservation not found' });
    }
    res.json(rows[0]);
  } catch (error) {
    console.error('Error fetching reservation:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new reservation
router.post('/', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = reservationSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if book exists
    const [book] = await pool.query('SELECT * FROM books WHERE book_id = ?', [value.book_id]);
    if (book.length === 0) {
      return res.status(404).json({ error: 'Book not found' });
    }

    // Check if member exists
    const [member] = await pool.query('SELECT * FROM members WHERE member_id = ?', [value.member_id]);
    if (member.length === 0) {
      return res.status(404).json({ error: 'Member not found' });
    }

    // Check if reservation already exists
    const [existing] = await pool.query(
      'SELECT * FROM reservations WHERE book_id = ? AND member_id = ? AND status = "Pending"',
      [value.book_id, value.member_id]
    );
    if (existing.length > 0) {
      return res.status(400).json({ error: 'Reservation already exists' });
    }

    // Create reservation
    const [result] = await pool.query(
      'INSERT INTO reservations (book_id, member_id, reservation_date, status) VALUES (?, ?, ?, ?)',
      [value.book_id, value.member_id, value.reservation_date, value.status]
    );

    res.status(201).json({
      message: 'Reservation created successfully',
      reservation_id: result.insertId
    });
  } catch (error) {
    console.error('Error creating reservation:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update reservation
router.put('/:id', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = reservationSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if reservation exists
    const [existing] = await pool.query('SELECT * FROM reservations WHERE reservation_id = ?', [req.params.id]);
    if (existing.length === 0) {
      return res.status(404).json({ error: 'Reservation not found' });
    }

    // Update reservation
    await pool.query(
      'UPDATE reservations SET book_id = ?, member_id = ?, reservation_date = ?, status = ? WHERE reservation_id = ?',
      [value.book_id, value.member_id, value.reservation_date, value.status, req.params.id]
    );

    res.json({ message: 'Reservation updated successfully' });
  } catch (error) {
    console.error('Error updating reservation:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router; 