from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from models import Book
from schemas.bookbase import BookBase, BookCreate


def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


def get_books_by_title(title: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()


def get_books_by_author(author: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()


def get_books_by_category(category_id: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.id_category == category_id).all()
def get_book_by_title_author_id(id: int, title: str, author: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.title == title and Book.author == author and Book.id != id)
def create_book(book: BookCreate, db: Session = Depends(get_db)):

    db_book = Book(**book.dict())

    db.add(db_book)
    db.commit()

    return db_book


def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    # db_book = get_book_by_title_author_id(book_id, book.title, book.author, db)
    # if db_book:
    #     raise HTTPException(status_code=422, detail=f'Cuốn sách {book.title} của {book.author} đã tồn tại')
    db_book = get_book(book_id, db)

    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db_book.release_date = book.release_date
        db_book.about = book.about
        db_book.page = book.page
        db_book.id_category = book.id_category
        db_book.picture = book.picture
        db_book.stock = book.stock

        db.commit()
    return db_book

def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book(book_id, db)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book