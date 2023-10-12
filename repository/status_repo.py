from fastapi import Depends
from sqlalchemy.orm import Session

import models
from config.database import get_db


def get_all(db: Session = Depends(get_db)):
    status_list = db.query(models.Status).all()
    return status_list


def get(id: int, db: Session = Depends(get_db)):
    status = db.query(models.Status).filter(id=id).first
    return status

