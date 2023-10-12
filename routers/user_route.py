from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import database
from service import oauth2
from repository import user_repo
from schemas.user import User, TokenData, CreateUser

router = APIRouter(
    prefix='/user',
    tags=['User']
)

get_db = database.get_db

@router.get('/', response_model=list[User])
def get_all_user(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_admin)):
    return user_repo.get_all(db)


@router.post("/create", )
def create_user(request: CreateUser, db: Session = Depends(get_db)):
    user_repo.create(request, db)


@router.get('/me', response_model=User)
def get_user(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return user_repo.read(current_user.username, db)


@router.put("/update", response_model=User)
def update_user(request: User, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return user_repo.update(current_user.username, request, db)

