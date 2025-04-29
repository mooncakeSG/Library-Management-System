from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app
from database import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_member():
    response = client.post(
        "/members/",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "phone": "1234567890"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"

def test_create_duplicate_member():
    # Create first member
    client.post(
        "/members/",
        json={
            "email": "duplicate@example.com",
            "name": "Duplicate User",
            "phone": "1234567890"
        }
    )
    
    # Try to create duplicate member
    response = client.post(
        "/members/",
        json={
            "email": "duplicate@example.com",
            "name": "Another User",
            "phone": "9876543210"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_search_books():
    # Create a test book
    client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890",
            "publication_year": 2023
        }
    )
    
    # Search for the book
    response = client.get("/books/?search=Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Test Book"

def test_create_borrowing_record():
    # Create a test book
    book_response = client.post(
        "/books/",
        json={
            "title": "Borrowable Book",
            "author": "Test Author",
            "isbn": "9876543210",
            "publication_year": 2023
        }
    )
    book_id = book_response.json()["id"]
    
    # Create a test member
    member_response = client.post(
        "/members/",
        json={
            "email": "borrower@example.com",
            "name": "Borrower User",
            "phone": "1234567890"
        }
    )
    member_id = member_response.json()["id"]
    
    # Create borrowing record
    response = client.post(
        "/borrowing-records/",
        json={
            "book_id": book_id,
            "member_id": member_id,
            "borrow_date": "2024-01-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["member_id"] == member_id

def test_create_duplicate_borrowing():
    # Create a test book
    book_response = client.post(
        "/books/",
        json={
            "title": "Duplicate Borrow Book",
            "author": "Test Author",
            "isbn": "1111111111",
            "publication_year": 2023
        }
    )
    book_id = book_response.json()["id"]
    
    # Create a test member
    member_response = client.post(
        "/members/",
        json={
            "email": "duplicate_borrower@example.com",
            "name": "Duplicate Borrower",
            "phone": "1234567890"
        }
    )
    member_id = member_response.json()["id"]
    
    # Create first borrowing record
    client.post(
        "/borrowing-records/",
        json={
            "book_id": book_id,
            "member_id": member_id,
            "borrow_date": "2024-01-01"
        }
    )
    
    # Try to create duplicate borrowing record
    response = client.post(
        "/borrowing-records/",
        json={
            "book_id": book_id,
            "member_id": member_id,
            "borrow_date": "2024-01-02"
        }
    )
    assert response.status_code == 400
    assert "Book is already borrowed" in response.json()["detail"] 