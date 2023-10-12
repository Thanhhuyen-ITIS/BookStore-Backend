from fastapi import Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models import Category


def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()