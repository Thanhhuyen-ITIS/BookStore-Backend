from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
from config.database import get_db


def get(id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == id).first()
    return role
