-- Library Management System Database Schema
-- This schema includes tables for members, books, borrowing records, and reservations

-- Drop existing tables if they exist
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS borrowing_records;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS staff;

-- Create staff table
CREATE TABLE staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    role VARCHAR(50) NOT NULL,
    hire_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create members table
CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    membership_date DATE NOT NULL,
    membership_status ENUM('Active', 'Inactive', 'Suspended') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create books table
CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(13) NOT NULL UNIQUE,
    publication_year INT NOT NULL,
    publisher VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    location VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (publication_year > 0),
    CHECK (total_copies >= 0),
    CHECK (available_copies >= 0),
    CHECK (available_copies <= total_copies)
);

-- Create borrowing_records table
CREATE TABLE borrowing_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount DECIMAL(10,2) DEFAULT 0.00,
    status ENUM('Borrowed', 'Returned', 'Overdue') NOT NULL DEFAULT 'Borrowed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE RESTRICT,
    CHECK (borrow_date <= due_date),
    CHECK (return_date IS NULL OR return_date >= borrow_date)
);

-- Create reservations table
CREATE TABLE reservations (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    status ENUM('Pending', 'Fulfilled', 'Cancelled') NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE RESTRICT
);

-- Insert sample data for staff
INSERT INTO staff (name, email, phone, role, hire_date) VALUES
('John Smith', 'john.smith@library.com', '555-0101', 'Librarian', '2020-01-15'),
('Mary Johnson', 'mary.johnson@library.com', '555-0102', 'Assistant Librarian', '2021-03-20'),
('Robert Brown', 'robert.brown@library.com', '555-0103', 'Library Technician', '2022-06-10');

-- Insert sample data for members
INSERT INTO members (name, email, phone, address, membership_date, membership_status) VALUES
('Alice Cooper', 'alice.cooper@email.com', '555-0201', '123 Main St, City', '2023-01-01', 'Active'),
('Bob Wilson', 'bob.wilson@email.com', '555-0202', '456 Oak Ave, Town', '2023-02-15', 'Active'),
('Carol Davis', 'carol.davis@email.com', '555-0203', '789 Pine Rd, Village', '2023-03-20', 'Active');

-- Insert sample data for books
INSERT INTO books (title, author, isbn, publication_year, publisher, category, total_copies, available_copies, location) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 1925, 'Scribner', 'Fiction', 3, 3, 'Fiction-A1'),
('To Kill a Mockingbird', 'Harper Lee', '9780446310789', 1960, 'Grand Central', 'Fiction', 2, 2, 'Fiction-B2'),
('1984', 'George Orwell', '9780451524935', 1949, 'Signet Classic', 'Fiction', 4, 4, 'Fiction-C3'),
('The Art of Programming', 'John Doe', '9781234567890', 2020, 'Tech Books', 'Computer Science', 2, 2, 'CS-A1'),
('Database Design', 'Jane Smith', '9780987654321', 2019, 'Data Press', 'Computer Science', 3, 3, 'CS-B2');

-- Insert sample borrowing records
INSERT INTO borrowing_records (book_id, member_id, borrow_date, due_date, return_date, status) VALUES
(1, 1, '2024-01-01', '2024-01-15', NULL, 'Borrowed'),
(2, 2, '2024-01-05', '2024-01-20', NULL, 'Borrowed'),
(3, 3, '2024-01-10', '2024-01-25', NULL, 'Borrowed');

-- Insert sample reservations
INSERT INTO reservations (book_id, member_id, reservation_date, status) VALUES
(4, 1, '2024-01-15', 'Pending'),
(5, 2, '2024-01-16', 'Pending'); 