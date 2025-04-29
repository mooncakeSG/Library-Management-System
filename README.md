# Library Management System

A comprehensive library management system built with Node.js, Express, and MySQL. This system allows you to manage books, members, borrowing records, and reservations through a RESTful API.

## Features

- Member management (CRUD operations)
- Book inventory management
- Borrowing records tracking
- Reservation system
- RESTful API with Express
- MySQL database integration
- Input validation with Joi
- Error handling and logging
- Search functionality
- Pagination support

## Database Schema

The system uses the following main tables:

### Staff Table
- `staff_id` (PK): Unique identifier for staff members
- `name`: Staff member's full name
- `email`: Unique email address
- `phone`: Contact number
- `role`: Staff role (Librarian, Assistant Librarian, etc.)
- `hire_date`: Date of employment

### Members Table
- `member_id` (PK): Unique identifier for members
- `name`: Member's full name
- `email`: Unique email address
- `phone`: Contact number
- `address`: Member's address
- `membership_date`: Date of membership
- `membership_status`: Current status (Active, Inactive, Suspended)

### Books Table
- `book_id` (PK): Unique identifier for books
- `title`: Book title
- `author`: Book author
- `isbn`: Unique ISBN number
- `publication_year`: Year of publication
- `publisher`: Publishing company
- `category`: Book category
- `total_copies`: Total number of copies
- `available_copies`: Number of available copies
- `location`: Physical location in library

### Borrowing Records Table
- `record_id` (PK): Unique identifier for borrowing records
- `book_id` (FK): Reference to books table
- `member_id` (FK): Reference to members table
- `borrow_date`: Date of borrowing
- `due_date`: Expected return date
- `return_date`: Actual return date
- `fine_amount`: Any fines incurred
- `status`: Current status (Borrowed, Returned, Overdue)

### Reservations Table
- `reservation_id` (PK): Unique identifier for reservations
- `book_id` (FK): Reference to books table
- `member_id` (FK): Reference to members table
- `reservation_date`: Date of reservation
- `status`: Current status (Pending, Fulfilled, Cancelled)

## API Endpoints

### Members
- `GET /api/members` - List all members
- `GET /api/members/:id` - Get member details
- `POST /api/members` - Create a new member
- `PUT /api/members/:id` - Update member information
- `DELETE /api/members/:id` - Delete a member

### Books
- `GET /api/books` - List all books
- `GET /api/books/:id` - Get book details
- `POST /api/books` - Add a new book
- `PUT /api/books/:id` - Update book information
- `DELETE /api/books/:id` - Delete a book

### Borrowing Records
- `GET /api/borrowing` - List all borrowing records
- `GET /api/borrowing/:id` - Get borrowing record details
- `POST /api/borrowing` - Create a borrowing record
- `PUT /api/borrowing/:id` - Update borrowing record

### Reservations
- `GET /api/reservations` - List all reservations
- `GET /api/reservations/:id` - Get reservation details
- `POST /api/reservations` - Create a reservation
- `PUT /api/reservations/:id` - Update reservation status

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management-system
```

2. Install dependencies:
```bash
npm install
```

3. Set up the database:
   - Create a MySQL database
   - Update the `.env` file with your database credentials
   - Run the SQL script to create tables and sample data:
   ```bash
   mysql -u your_username -p your_database < library_schema.sql
   ```

4. Start the server:
```bash
# Development mode
npm run dev

# Production mode
npm start
```

5. Access the API:
   - The API will be available at http://localhost:3000
   - You can use tools like Postman or curl to test the endpoints

## Testing

Run the test suite:
```bash
npm test
```

## Project Structure

```
library-management-system/
├── app.js              # Express application
├── config/             # Configuration files
│   └── database.js     # Database connection
├── routes/             # Route handlers
│   ├── members.js      # Member routes
│   ├── books.js        # Book routes
│   ├── borrowing.js    # Borrowing routes
│   └── reservations.js # Reservation routes
├── library_schema.sql  # Database schema and sample data
├── package.json        # Project dependencies
└── README.md           # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is for educational use only.
