from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import logging

import crud
import models
import schemas
from database import engine, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System API",
    description="A simple library management system API for educational purposes",
    version="1.0.0"
)

# Member endpoints
@app.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating new member: {member.email}")
        return crud.create_member(db=db, member=member)
    except Exception as e:
        logger.error(f"Error creating member: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/members/", response_model=List[schemas.Member])
def read_members(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Fetching members with skip={skip} and limit={limit}")
        members = crud.get_members(db, skip=skip, limit=limit)
        return members
    except Exception as e:
        logger.error(f"Error fetching members: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/members/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@app.put("/members/{member_id}", response_model=schemas.Member)
def update_member(member_id: int, member: schemas.MemberBase, db: Session = Depends(get_db)):
    db_member = crud.update_member(db, member_id=member_id, member=member)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    success = crud.delete_member(db, member_id=member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}

# Book endpoints
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating new book: {book.title}")
        return crud.create_book(db=db, book=book)
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for book title or author"),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Fetching books with skip={skip}, limit={limit}, search={search}")
        books = crud.get_books(db, skip=skip, limit=limit, search=search)
        return books
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookBase, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    success = crud.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# Borrowing Record endpoints
@app.post("/borrowing-records/", response_model=schemas.BorrowingRecord)
def create_borrowing_record(borrowing: schemas.BorrowingRecordCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating new borrowing record for book_id={borrowing.book_id}")
        return crud.create_borrowing_record(db=db, borrowing=borrowing)
    except Exception as e:
        logger.error(f"Error creating borrowing record: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/borrowing-records/", response_model=List[schemas.BorrowingRecord])
def read_borrowing_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = crud.get_borrowing_records(db, skip=skip, limit=limit)
    return records

@app.get("/borrowing-records/{record_id}", response_model=schemas.BorrowingRecord)
def read_borrowing_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_borrowing_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    return db_record

@app.put("/borrowing-records/{record_id}", response_model=schemas.BorrowingRecord)
def update_borrowing_record(record_id: int, borrowing: schemas.BorrowingRecordBase, db: Session = Depends(get_db)):
    db_record = crud.update_borrowing_record(db, record_id=record_id, borrowing=borrowing)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    return db_record

# Reservation endpoints
@app.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return crud.create_reservation(db=db, reservation=reservation)

@app.get("/reservations/", response_model=List[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db, skip=skip, limit=limit)
    return reservations

@app.get("/reservations/{reservation_id}", response_model=schemas.Reservation)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crud.get_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@app.put("/reservations/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: int, reservation: schemas.ReservationBase, db: Session = Depends(get_db)):
    db_reservation = crud.update_reservation(db, reservation_id=reservation_id, reservation=reservation)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    ) 