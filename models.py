from sqlalchemy import Column, Integer, String, Date, Enum, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    membership_date = Column(Date, nullable=False)
    membership_status = Column(Enum('Active', 'Inactive', 'Suspended'), nullable=False, default='Active')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    borrowing_records = relationship("BorrowingRecord", back_populates="member")
    reservations = relationship("Reservation", back_populates="member")

class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    publisher = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    location = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    borrowing_records = relationship("BorrowingRecord", back_populates="book")
    reservations = relationship("Reservation", back_populates="book")

class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    role = Column(String(50), nullable=False)
    hire_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    borrowing_records = relationship("BorrowingRecord", back_populates="staff")

class BorrowingRecord(Base):
    __tablename__ = "borrowing_records"

    record_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.book_id', ondelete='RESTRICT'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.member_id', ondelete='RESTRICT'), nullable=False)
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    fine_amount = Column(DECIMAL(10, 2), default=0.00)
    status = Column(Enum('Borrowed', 'Returned', 'Overdue'), nullable=False, default='Borrowed')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    book = relationship("Book", back_populates="borrowing_records")
    member = relationship("Member", back_populates="borrowing_records")

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.book_id', ondelete='RESTRICT'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.member_id', ondelete='RESTRICT'), nullable=False)
    reservation_date = Column(Date, nullable=False)
    status = Column(Enum('Pending', 'Fulfilled', 'Cancelled'), nullable=False, default='Pending')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    book = relationship("Book", back_populates="reservations")
    member = relationship("Member", back_populates="reservations") 