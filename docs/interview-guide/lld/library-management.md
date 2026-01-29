---
sidebar_position: 7
title: "Design Library Management System"
description: >-
  Complete LLD for library management system. Book catalog, member management,
  borrowing, and reservation system.
keywords:
  - library design
  - LLD library
  - book management
  - reservation system
difficulty: Intermediate
estimated_time: 30 minutes
prerequisites:
  - SOLID Principles
companies: [Amazon, Microsoft, Flipkart]
---

# Design a Library Management System

Library system tests modeling real-world entities, relationships, and business rules.

---

## Requirements

- Add/remove/search books
- Member registration
- Book checkout/return
- Reservation system
- Fine calculation for overdue
- Track book copies

---

## Class Diagram

```
┌─────────────────┐       ┌─────────────────┐
│     Library     │       │      Book       │
├─────────────────┤       ├─────────────────┤
│ - books         │──────▶│ - isbn          │
│ - members       │       │ - title         │
│ - loans         │       │ - author        │
├─────────────────┤       │ - copies[]      │
│ + searchBook()  │       └─────────────────┘
│ + checkout()    │                │
│ + return()      │                ▼
└─────────────────┘       ┌─────────────────┐
         │                │    BookCopy     │
         ▼                ├─────────────────┤
┌─────────────────┐       │ - barcode       │
│     Member      │       │ - status        │
├─────────────────┤       │ - rack          │
│ - memberId      │       └─────────────────┘
│ - name          │
│ - loans[]       │       ┌─────────────────┐
│ - reservations[]│       │      Loan       │
├─────────────────┤       ├─────────────────┤
│ + borrow()      │──────▶│ - bookCopy      │
│ + return()      │       │ - member        │
│ + reserve()     │       │ - dueDate       │
└─────────────────┘       │ - returnDate    │
                          └─────────────────┘
```

---

## Implementation

### Enums

```python
from enum import Enum
from datetime import datetime, timedelta
import uuid

class BookStatus(Enum):
    AVAILABLE = "available"
    LOANED = "loaned"
    RESERVED = "reserved"
    LOST = "lost"

class MemberStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"

class ReservationStatus(Enum):
    PENDING = "pending"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
```

### Book and BookCopy

```python
class Book:
    def __init__(self, isbn: str, title: str, author: str, 
                 publisher: str, category: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.category = category
        self.copies = []
    
    def add_copy(self, rack_location: str) -> 'BookCopy':
        copy = BookCopy(self, rack_location)
        self.copies.append(copy)
        return copy
    
    def get_available_copy(self) -> 'BookCopy':
        for copy in self.copies:
            if copy.status == BookStatus.AVAILABLE:
                return copy
        return None
    
    def available_count(self) -> int:
        return sum(1 for c in self.copies if c.status == BookStatus.AVAILABLE)

class BookCopy:
    def __init__(self, book: Book, rack_location: str):
        self.barcode = str(uuid.uuid4())[:8]
        self.book = book
        self.rack_location = rack_location
        self.status = BookStatus.AVAILABLE
```

### Member

```python
class Member:
    MAX_BOOKS = 5
    LOAN_DAYS = 14
    FINE_PER_DAY = 0.50
    
    def __init__(self, name: str, email: str, phone: str):
        self.member_id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.phone = phone
        self.status = MemberStatus.ACTIVE
        self.loans = []
        self.reservations = []
        self.total_fines = 0.0
    
    def can_borrow(self) -> bool:
        if self.status != MemberStatus.ACTIVE:
            return False
        if len(self.loans) >= self.MAX_BOOKS:
            return False
        if self.total_fines > 10.0:  # Max unpaid fines
            return False
        return True
    
    def borrow(self, book_copy: 'BookCopy') -> 'Loan':
        if not self.can_borrow():
            raise Exception("Cannot borrow: check status or limits")
        
        loan = Loan(self, book_copy)
        self.loans.append(loan)
        book_copy.status = BookStatus.LOANED
        return loan
    
    def return_book(self, barcode: str) -> float:
        loan = next((l for l in self.loans if l.book_copy.barcode == barcode), None)
        if not loan:
            raise Exception("No active loan found for this book")
        
        fine = loan.close()
        self.loans.remove(loan)
        self.total_fines += fine
        
        return fine
    
    def pay_fine(self, amount: float):
        self.total_fines = max(0, self.total_fines - amount)
```

### Loan and Reservation

```python
class Loan:
    def __init__(self, member: Member, book_copy: BookCopy):
        self.loan_id = str(uuid.uuid4())[:8]
        self.member = member
        self.book_copy = book_copy
        self.issue_date = datetime.now()
        self.due_date = self.issue_date + timedelta(days=Member.LOAN_DAYS)
        self.return_date = None
    
    def is_overdue(self) -> bool:
        return datetime.now() > self.due_date
    
    def calculate_fine(self) -> float:
        if not self.is_overdue():
            return 0.0
        
        end_date = self.return_date or datetime.now()
        overdue_days = (end_date - self.due_date).days
        return overdue_days * Member.FINE_PER_DAY
    
    def close(self) -> float:
        self.return_date = datetime.now()
        self.book_copy.status = BookStatus.AVAILABLE
        return self.calculate_fine()
    
    def renew(self) -> bool:
        if self.is_overdue():
            return False
        self.due_date += timedelta(days=Member.LOAN_DAYS)
        return True

class Reservation:
    def __init__(self, member: Member, book: Book):
        self.reservation_id = str(uuid.uuid4())[:8]
        self.member = member
        self.book = book
        self.created_at = datetime.now()
        self.status = ReservationStatus.PENDING
    
    def fulfill(self, book_copy: BookCopy):
        self.status = ReservationStatus.FULFILLED
        return self.member.borrow(book_copy)
    
    def cancel(self):
        self.status = ReservationStatus.CANCELLED
```

### Library

```python
class Library:
    def __init__(self, name: str):
        self.name = name
        self.books = {}  # isbn -> Book
        self.members = {}  # member_id -> Member
        self.reservations = []
    
    def add_book(self, isbn: str, title: str, author: str,
                 publisher: str, category: str, copies: int = 1) -> Book:
        if isbn in self.books:
            book = self.books[isbn]
        else:
            book = Book(isbn, title, author, publisher, category)
            self.books[isbn] = book
        
        for _ in range(copies):
            book.add_copy(f"Rack-{len(book.copies)}")
        
        return book
    
    def register_member(self, name: str, email: str, phone: str) -> Member:
        member = Member(name, email, phone)
        self.members[member.member_id] = member
        return member
    
    def search_by_title(self, title: str) -> list:
        return [b for b in self.books.values() 
                if title.lower() in b.title.lower()]
    
    def search_by_author(self, author: str) -> list:
        return [b for b in self.books.values() 
                if author.lower() in b.author.lower()]
    
    def checkout(self, member_id: str, isbn: str) -> Loan:
        member = self.members.get(member_id)
        book = self.books.get(isbn)
        
        if not member or not book:
            raise Exception("Invalid member or book")
        
        copy = book.get_available_copy()
        if not copy:
            raise Exception("No available copies")
        
        return member.borrow(copy)
    
    def return_book(self, member_id: str, barcode: str) -> float:
        member = self.members.get(member_id)
        if not member:
            raise Exception("Invalid member")
        
        fine = member.return_book(barcode)
        self._process_reservations(barcode)
        return fine
    
    def reserve(self, member_id: str, isbn: str) -> Reservation:
        member = self.members.get(member_id)
        book = self.books.get(isbn)
        
        if not member or not book:
            raise Exception("Invalid member or book")
        
        if book.available_count() > 0:
            raise Exception("Book is available, no need to reserve")
        
        reservation = Reservation(member, book)
        self.reservations.append(reservation)
        member.reservations.append(reservation)
        return reservation
    
    def _process_reservations(self, barcode: str):
        # Find the book and check for pending reservations
        for book in self.books.values():
            for copy in book.copies:
                if copy.barcode == barcode:
                    pending = [r for r in self.reservations 
                              if r.book.isbn == book.isbn 
                              and r.status == ReservationStatus.PENDING]
                    if pending:
                        # Notify first reservation
                        # In real system, send email/notification
                        pass
                    return
```

---

## Usage Example

```python
# Create library
library = Library("City Library")

# Add books
book1 = library.add_book("978-0-13-468599-1", "Clean Code", 
                         "Robert Martin", "Pearson", "Programming", 3)

# Register member
member = library.register_member("Alice", "alice@email.com", "555-0100")

# Checkout
loan = library.checkout(member.member_id, "978-0-13-468599-1")
print(f"Due date: {loan.due_date}")

# Return
fine = library.return_book(member.member_id, loan.book_copy.barcode)
print(f"Fine: ${fine}")
```

---

## Key Takeaways

1. **Book vs BookCopy:** Separate identity (ISBN) from physical copies.
2. **Business rules in Member:** Borrowing limits, fine thresholds.
3. **Reservation queue:** Process when books returned.
4. **Fine calculation:** Based on overdue days.
