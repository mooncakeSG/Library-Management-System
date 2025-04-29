from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

# Member schemas
class MemberBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    member_id: int
    membership_date: date
    membership_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Book schemas
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    publisher: str
    category: str
    total_copies: int = 1
    available_copies: int = 1
    location: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    book_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Staff schemas
class StaffBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: str
    hire_date: date

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    staff_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Borrowing Record schemas
class BorrowingRecordBase(BaseModel):
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    fine_amount: Optional[Decimal] = Decimal('0.00')
    status: str = 'Borrowed'

class BorrowingRecordCreate(BorrowingRecordBase):
    pass

class BorrowingRecord(BorrowingRecordBase):
    record_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Reservation schemas
class ReservationBase(BaseModel):
    book_id: int
    member_id: int
    reservation_date: date
    status: str = 'Pending'

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    reservation_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 