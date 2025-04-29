const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');
const Joi = require('joi');

// Validation schema
const borrowingSchema = Joi.object({
  book_id: Joi.number().integer().required(),
  member_id: Joi.number().integer().required(),
  borrow_date: Joi.date().required(),
  due_date: Joi.date().required().min(Joi.ref('borrow_date')),
  return_date: Joi.date().allow(null),
  fine_amount: Joi.number().precision(2).min(0).default(0),
  status: Joi.string().valid('Borrowed', 'Returned', 'Overdue').default('Borrowed')
});

// Get all borrowing records
router.get('/', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM borrowing_records');
    res.json(rows);
  } catch (error) {
    console.error('Error fetching borrowing records:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get borrowing record by ID
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM borrowing_records WHERE record_id = ?', [req.params.id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: 'Borrowing record not found' });
    }
    res.json(rows[0]);
  } catch (error) {
    console.error('Error fetching borrowing record:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new borrowing record
router.post('/', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = borrowingSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if book exists and is available
    const [book] = await pool.query('SELECT * FROM books WHERE book_id = ?', [value.book_id]);
    if (book.length === 0) {
      return res.status(404).json({ error: 'Book not found' });
    }
    if (book[0].available_copies <= 0) {
      return res.status(400).json({ error: 'Book is not available for borrowing' });
    }

    // Check if member exists
    const [member] = await pool.query('SELECT * FROM members WHERE member_id = ?', [value.member_id]);
    if (member.length === 0) {
      return res.status(404).json({ error: 'Member not found' });
    }

    // Check if book is already borrowed
    const [existing] = await pool.query(
      'SELECT * FROM borrowing_records WHERE book_id = ? AND status = "Borrowed"',
      [value.book_id]
    );
    if (existing.length > 0) {
      return res.status(400).json({ error: 'Book is already borrowed' });
    }

    // Start transaction
    const connection = await pool.getConnection();
    await connection.beginTransaction();

    try {
      // Create borrowing record
      const [result] = await connection.query(
        'INSERT INTO borrowing_records (book_id, member_id, borrow_date, due_date, return_date, fine_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [value.book_id, value.member_id, value.borrow_date, value.due_date, value.return_date, value.fine_amount, value.status]
      );

      // Update book available copies
      await connection.query(
        'UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?',
        [value.book_id]
      );

      await connection.commit();
      res.status(201).json({
        message: 'Borrowing record created successfully',
        record_id: result.insertId
      });
    } catch (error) {
      await connection.rollback();
      throw error;
    } finally {
      connection.release();
    }
  } catch (error) {
    console.error('Error creating borrowing record:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update borrowing record
router.put('/:id', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = borrowingSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if borrowing record exists
    const [existing] = await pool.query('SELECT * FROM borrowing_records WHERE record_id = ?', [req.params.id]);
    if (existing.length === 0) {
      return res.status(404).json({ error: 'Borrowing record not found' });
    }

    // Start transaction
    const connection = await pool.getConnection();
    await connection.beginTransaction();

    try {
      // Update borrowing record
      await connection.query(
        'UPDATE borrowing_records SET book_id = ?, member_id = ?, borrow_date = ?, due_date = ?, return_date = ?, fine_amount = ?, status = ? WHERE record_id = ?',
        [value.book_id, value.member_id, value.borrow_date, value.due_date, value.return_date, value.fine_amount, value.status, req.params.id]
      );

      // If status changed to Returned, update book available copies
      if (value.status === 'Returned' && existing[0].status !== 'Returned') {
        await connection.query(
          'UPDATE books SET available_copies = available_copies + 1 WHERE book_id = ?',
          [value.book_id]
        );
      }

      await connection.commit();
      res.json({ message: 'Borrowing record updated successfully' });
    } catch (error) {
      await connection.rollback();
      throw error;
    } finally {
      connection.release();
    }
  } catch (error) {
    console.error('Error updating borrowing record:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router; 