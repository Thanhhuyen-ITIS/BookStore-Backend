from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config.database import get_db
from models import Review
from repository import order_repo
from schemas.order import OrderUpdate
from schemas.reviewbase import ReviewBase, ReviewCreate


def get_review(review_id: int, db: Session = Depends(get_db),):
    return db.query(Review).filter(Review.id == review_id).first()


def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


def get_reviews_by_book(id_book: int, db: Session = Depends(get_db), ):
    return db.query(Review).filter(Review.id_book == id_book).all()


def create_review(id: int, username: str, review: ReviewCreate, db: Session = Depends(get_db), ):
    db_order = order_repo.get_order_by_username_id(id, username, db)

    if (not db_order) or db_order.id_status != 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Bạn không thể đưa ra đánh giá khi chưa mua sản phầm')
    db_review = Review(username=username, id_book=db_order.id_book, star=review.star, comment=review.comment)
    db.add(db_review)

    status_order = OrderUpdate(id_status=4)
    order_repo.update_order(id, status_order, db)
    db.commit()
    db.refresh(db_review)
    return db_review
