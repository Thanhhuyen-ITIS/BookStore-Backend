from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import order_repo
from routers import review_route
from schemas.order import OrderBase, OrderUpdate, OrderCreate
from schemas.user import TokenData
from service import oauth2

router = APIRouter(
    tags=['Order']
)
@router.get('/orders', response_model=list[OrderBase])
def get_orders(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_admin)):
    return order_repo.get_orders(db)


@router.get('/order/{id}', response_model=OrderBase)
def get_order_by_id(id: int, db: Session = Depends(get_db),
                    current_user: TokenData = Depends(oauth2.get_current_admin)):
    return order_repo.get_order(id, db)


@router.get('/my_orders', response_model=list[OrderBase])
def get_my_order(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return order_repo.get_orders_by_username(current_user.username, db)


@router.get('/my_order/{id}', response_model=OrderBase)
def get_my_order_by_id(id: int, db: Session = Depends(get_db),
                       current_user: TokenData = Depends(oauth2.get_current_user)):
    return order_repo.get_order_by_username_id(id, current_user.username, db)


@router.post('/create_order')
def create_order(order: OrderCreate, db: Session = Depends(get_db),
                 current_user: TokenData = Depends(oauth2.get_current_user)):
    order_repo.create_order(order, current_user.username, db)

@router.post('/create_orders')
def create_orders(orders: list[OrderCreate], db: Session = Depends(get_db),
                 current_user: TokenData = Depends(oauth2.get_current_user)):
    order_repo.create_orders(orders, current_user.username, db)


@router.post('/add_to_order/{id}')
def create_order_from_cart(id: int, db: Session = Depends(get_db),
                 current_user: TokenData = Depends(oauth2.get_current_user)):
    order_repo.create_order_from_cart(id, current_user.username, db)


@router.put('/update_order/{id}', response_model=OrderBase)
def update_order_by_admin(id: int, order_update: OrderUpdate, db: Session = Depends(get_db),
                          current_user: TokenData = Depends(oauth2.get_current_admin)):
    return order_repo.update_order_by_admin(id, order_update, db)


@router.put('/update_my_order/{id}', response_model=OrderBase)
def update_order_by_user(id: int, order_update: OrderUpdate, db: Session = Depends(get_db),
                         current_user: TokenData = Depends(oauth2.get_current_user)):
    return order_repo.update_order_by_user(id, current_user.username, order_update, db)
