from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookRead, BookUpdate

# The APIRouter acts like a mini-FastAPI app for organizing routes
router = APIRouter (
    prefix="/books",
    tags=["Books"]
)

# Hardcoded for Phase D. We will replace this with real Auth next session.
FAKE_USER_ID = 2

# 1. CREATE a Book (POST) ------------------------------------------------
@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    # Convert the Pydantic model to a dictionary and unpack it (**).
    # Force the user_id to be our logged-in user so they can't forge ownership.
    new_book = Book(**book_in.model_dump(), user_id=FAKE_USER_ID)
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book) # Grab the generated ID and created_at timestamp
    return new_book

# 2. READ ALL Books for User (GET) ---------------------------------------
@router.get("/", response_model=List[BookRead])
def list_books(db: Session = Depends(get_db)):
    # CRITICAL: Always filter by owner!
    stmt = select(Book).where(Book.user_id == FAKE_USER_ID)
    # scalars().all() extracts the actual Book objects from the SQLAlchemy result rows
    books = db.execute(stmt).scalars().all()
    
    return books

# 3. READ ONE book (GET) -------------------------------------------------
@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    # We must require BOTH the book_id and the user_id.
    # Without user_id, someone could guess book_id=5 and read another user's book.
    stmt = select(Book).where(Book.id == book_id, Book.user_id == FAKE_USER_ID)
    book = db.execute(stmt).scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found or access denied")
    return book

# 4. UPDATE a Book (PUT) -------------------------------------------------
@router.put("/{book_id}", response_model=BookRead)
def update_book(book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)):
    # First, fetch the book to ensure it exists and belongs to the user
    stmt = select(Book).where(Book.id == book_id, Book.user_id == FAKE_USER_ID)
    book = db.execute(stmt).scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # exclude_unset=True is the magic here.
    # If the user only sends {"title": "New Title"}, it ignores the missing "rating".
    # Without this, missing fields would overwrite existing DB data with NULLs.
    update_data = book_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(book, key, value) # Python's way of doing book.title = value
        
    db.commit()
    db.refresh(book)
    return book

# 5. DELETE a Book (DELETE) ----------------------------------------------
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    stmt = select(Book).where(Book.id == book_id, Book.user_id == FAKE_USER_ID)
    book = db.execute(stmt).scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    # 204 No Content requires that we return absolutely nothing, not even a dictionary.
    return None