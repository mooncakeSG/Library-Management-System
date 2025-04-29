const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');
const Joi = require('joi');

// Validation schema
const bookSchema = Joi.object({
  title: Joi.string().required().min(1).max(200),
  author: Joi.string().required().min(2).max(100),
  isbn: Joi.string().required().pattern(/^[0-9-]{10,13}$/),
  publication_year: Joi.number().integer().min(1000).max(new Date().getFullYear()).required(),
  publisher: Joi.string().required().min(2).max(100),
  category: Joi.string().required().min(2).max(50),
  total_copies: Joi.number().integer().min(1).default(1),
  available_copies: Joi.number().integer().min(0).default(1),
  location: Joi.string().required().min(2).max(50)
});

// Get all books
router.get('/', async (req, res) => {
  try {
    const { search } = req.query;
    let query = 'SELECT * FROM books';
    let params = [];

    if (search) {
      query += ' WHERE title LIKE ? OR author LIKE ?';
      params = [`%${search}%`, `%${search}%`];
    }

    const [rows] = await pool.query(query, params);
    res.json(rows);
  } catch (error) {
    console.error('Error fetching books:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get book by ID
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM books WHERE book_id = ?', [req.params.id]);
    if (rows.length === 0) {
      return res.status(404).json({ error: 'Book not found' });
    }
    res.json(rows[0]);
  } catch (error) {
    console.error('Error fetching book:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new book
router.post('/', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = bookSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if ISBN already exists
    const [existing] = await pool.query('SELECT * FROM books WHERE isbn = ?', [value.isbn]);
    if (existing.length > 0) {
      return res.status(400).json({ error: 'Book with this ISBN already exists' });
    }

    // Insert new book
    const [result] = await pool.query(
      'INSERT INTO books (title, author, isbn, publication_year, publisher, category, total_copies, available_copies, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [value.title, value.author, value.isbn, value.publication_year, value.publisher, value.category, value.total_copies, value.available_copies, value.location]
    );

    res.status(201).json({
      message: 'Book created successfully',
      book_id: result.insertId
    });
  } catch (error) {
    console.error('Error creating book:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update book
router.put('/:id', async (req, res) => {
  try {
    // Validate request body
    const { error, value } = bookSchema.validate(req.body);
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    // Check if book exists
    const [existing] = await pool.query('SELECT * FROM books WHERE book_id = ?', [req.params.id]);
    if (existing.length === 0) {
      return res.status(404).json({ error: 'Book not found' });
    }

    // Update book
    await pool.query(
      'UPDATE books SET title = ?, author = ?, isbn = ?, publication_year = ?, publisher = ?, category = ?, total_copies = ?, available_copies = ?, location = ? WHERE book_id = ?',
      [value.title, value.author, value.isbn, value.publication_year, value.publisher, value.category, value.total_copies, value.available_copies, value.location, req.params.id]
    );

    res.json({ message: 'Book updated successfully' });
  } catch (error) {
    console.error('Error updating book:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Delete book
router.delete('/:id', async (req, res) => {
  try {
    // Check if book exists
    const [existing] = await pool.query('SELECT * FROM books WHERE book_id = ?', [req.params.id]);
    if (existing.length === 0) {
      return res.status(404).json({ error: 'Book not found' });
    }

    // Delete book
    await pool.query('DELETE FROM books WHERE book_id = ?', [req.params.id]);

    res.json({ message: 'Book deleted successfully' });
  } catch (error) {
    console.error('Error deleting book:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router; 