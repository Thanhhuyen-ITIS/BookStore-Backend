from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from config.database import get_db
from repository import cart_repo
from schemas.cartbase import CartBase, CartCreate, CartUpdate
from schemas.user import TokenData
from service import oauth2

router = APIRouter(
    tags=['Cart']
)

@router.get('/carts', response_model=list[CartBase])
def get_carts(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_admin)):
    return cart_repo.get_carts(db)

@router.get('/my_cart', response_model=list[CartBase])
def get_carts(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return cart_repo.get_carts_by_username(current_user.username, db)

@router.get('/my_cart/{id}', response_model=CartBase)
def get_cart(id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return cart_repo.get_cart_by_username_and_id(id, current_user.username, db)

@router.post('/add_cart')
def add_cart(cart: CartCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    cart_repo.create_cart(cart, current_user.username, db)

@router.delete('/delete_cart/{id}')
def delete_cart(id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    cart_repo.delete_cart_by_id(id, current_user.username, db )

@router.put('/update_cart/{id}', response_model=CartBase)
def update_cart(id: int,cart: CartUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return cart_repo.update_cart(id,cart, current_user.username, db)