from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import category_repo
from schemas.categorybase import CategoryBase

router = APIRouter(
    tags=['Category']
)

@router.get('/categories', response_model=list[CategoryBase])
def get_categories(db: Session = Depends(get_db)):
    return category_repo.get_categories(db)