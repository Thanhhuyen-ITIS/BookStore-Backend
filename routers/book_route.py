from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import book_repo
from routers import review_route
from schemas.bookbase import BookBase, BookCreate
from schemas.user import User, TokenData
from service import oauth2

router = APIRouter(
    prefix='/book',
    tags=['Book']
)


@router.get('/', response_model=list[BookBase])
def get_books(db: Session = Depends(get_db)):
    return book_repo.get_books(db)

@router.get('/category/{id}', response_model=list[BookBase])
def get_books_by_category(id: int, db: Session = Depends(get_db)):
    return book_repo.get_books_by_category(id, db)

@router.get('/{id}', response_model=BookBase)
def get_book(id: int, db: Session = Depends(get_db)):
    return book_repo.get_book(id, db)


@router.post('/create')
def creat_book(request: BookCreate, db: Session = Depends(get_db),
               tokendata: TokenData = Depends(oauth2.get_current_admin)):
    book_repo.create_book(request, db)


@router.put("/update/{id}", response_model=BookBase)
def update(id: int, request: BookCreate, db: Session = Depends(get_db),
           tokendata: TokenData = Depends(oauth2.get_current_admin)):
    return book_repo.update_book(id, request, db)


@router.delete('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(oauth2.get_current_admin)):
    book_repo.delete_book(id, db)
