from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
from config.database import SessionLocal
from schemas.user import CreateUser, User
from security.hashing import Hash

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return  users
def create(request: CreateUser, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == request.username).first()
    if db_user:
        raise HTTPException(status_code=500, detail=f'Người dùng  {request.username} đã tồn tại')
    new_user = models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def read(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {username} is not available')
    return user

def update(username: str, request: User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if user:
        user.username = request.username
        user.email = request.email
        user.name = request.name
        user.dob = request.dob
        user.gender = request.gender

        db.commit()
    return user
