from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import review_repo
from schemas.reviewbase import ReviewBase, ReviewCreate
from schemas.user import TokenData
from service import oauth2

router = APIRouter(
    tags=['Review']
)

@router.get('/reviews/{id}', response_model=list[ReviewBase])
def get_reviews_by_book(id: int, db: Session = Depends(get_db)):
    return review_repo.get_reviews_by_book(id, db)

@router.post('/create_review/{id}')
def create_review_book(id: int, request: ReviewCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return review_repo.create_review(id, current_user.username, request, db)
