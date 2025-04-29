from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, date
import logging
import models
import schemas

logger = logging.getLogger(__name__)

# Member CRUD operations
def create_member(db: Session, member: schemas.MemberCreate):
    # Check if email already exists
    if db.query(models.Member).filter(models.Member.email == member.email).first():
        raise ValueError("Email already registered")
    
    db_member = models.Member(
        **member.dict(),
        membership_date=date.today(),
        membership_status='Active'
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.member_id == member_id).first()

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()

def update_member(db: Session, member_id: int, member: schemas.MemberBase):
    db_member = db.query(models.Member).filter(models.Member.member_id == member_id).first()
    if db_member:
        for key, value in member.dict(exclude_unset=True).items():
            setattr(db_member, key, value)
        db.commit()
        db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = db.query(models.Member).filter(models.Member.member_id == member_id).first()
    if db_member:
        db.delete(db_member)
        db.commit()
        return True
    return False

# Book CRUD operations
def create_book(db: Session, book: schemas.BookCreate):
    # Check if book with same ISBN already exists
    if db.query(models.Book).filter(models.Book.isbn == book.isbn).first():
        raise ValueError("Book with this ISBN already exists")
    
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Book)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Book.title.ilike(search_term),
                models.Book.author.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book: schemas.BookBase):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if db_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

# Borrowing Record CRUD operations
def create_borrowing_record(db: Session, borrowing: schemas.BorrowingRecordCreate):
    # Check if book is available
    book = get_book(db, borrowing.book_id)
    if not book:
        raise ValueError("Book not found")
    
    # Check if book is already borrowed
    active_borrowing = db.query(models.BorrowingRecord).filter(
        models.BorrowingRecord.book_id == borrowing.book_id,
        models.BorrowingRecord.return_date == None
    ).first()
    
    if active_borrowing:
        raise ValueError("Book is already borrowed")
    
    db_borrowing = models.BorrowingRecord(**borrowing.dict())
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing

def get_borrowing_record(db: Session, record_id: int):
    return db.query(models.BorrowingRecord).filter(models.BorrowingRecord.record_id == record_id).first()

def get_borrowing_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BorrowingRecord).offset(skip).limit(limit).all()

def update_borrowing_record(db: Session, record_id: int, borrowing: schemas.BorrowingRecordBase):
    db_borrowing = db.query(models.BorrowingRecord).filter(models.BorrowingRecord.record_id == record_id).first()
    if db_borrowing:
        for key, value in borrowing.dict(exclude_unset=True).items():
            setattr(db_borrowing, key, value)
        db.commit()
        db.refresh(db_borrowing)
    return db_borrowing

# Reservation CRUD operations
def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    # Check if book exists
    book = get_book(db, reservation.book_id)
    if not book:
        raise ValueError("Book not found")
    
    # Check if member exists
    member = get_member(db, reservation.member_id)
    if not member:
        raise ValueError("Member not found")
    
    # Check if reservation already exists
    existing_reservation = db.query(models.Reservation).filter(
        models.Reservation.book_id == reservation.book_id,
        models.Reservation.member_id == reservation.member_id,
        models.Reservation.status == "pending"
    ).first()
    
    if existing_reservation:
        raise ValueError("Reservation already exists")
    
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservation(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()

def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reservation).offset(skip).limit(limit).all()

def update_reservation(db: Session, reservation_id: int, reservation: schemas.ReservationBase):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id).first()
    if db_reservation:
        for key, value in reservation.dict(exclude_unset=True).items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation 