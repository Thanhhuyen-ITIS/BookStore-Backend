from fastapi import Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models import Comment
from schemas.commentbase import CommentCreate


def get_idbook(idBook: int, db:Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.id_book==idBook).all()

def create(request: CommentCreate,id_book:int, username:str, db:Session = Depends(get_db)):
    comment = Comment(comment=request.comment, id_book=id_book, username=username);
    db.add(comment)
    db.commit()

