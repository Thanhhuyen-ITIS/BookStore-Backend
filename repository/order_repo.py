from datetime import date

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from config.database import get_db
from models import Order, Cart
from repository import cart_repo, status_repo, book_repo
from schemas.order import OrderBase, OrderUpdate, OrderCreate


def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


def get_orders_by_username(username: str, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.username == username).all()


def get_order_by_username_id(id: int, username: str, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == id, Order.username == username).first()

    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
        return
    return db_order


def create_order(order: OrderCreate, username: str, db: Session = Depends(get_db)):
    db_book = book_repo.get_book(order.id_book, db)
    total_price = db_book.cost * order.quantity
    db_order = Order(username=username, id_book=order.id_book, quantity=order.quantity, order_date=date.today(),
                     total_price=total_price)
    db_book.quatity_sold += db_order.quantity
    db_book.stock -= db_order.quantity
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def create_order_from_cart(id: int, username: str, db: Session = Depends(get_db)):
    db_cart = cart_repo.get_cart_by_username_and_id(id, username, db)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db_book = book_repo.get_book(db_cart.id_book)
    total_price = db_book.cost * db_cart.quantity
    db_order = Order(username=username, id_book=db_cart.id_book, quantity=db_cart.quantity, cost=date.today(),
                     total_price=total_price)

    db.add(db_order)
    db.commit()
    db.refresh(db_order)



def create_orders(orders: list[OrderCreate], username: str, db: Session = Depends(get_db)):
    for order in orders:
        db_book = book_repo.get_book(order.id_book, db)
        total_price = db_book.cost * order.quantity
        db_order = Order(username=username, id_book=order.id_book, quantity=order.quantity, order_date=date.today(),
                         total_price=total_price, name=order.name, address=order.address)
        db_book.quatity_sold += db_order.quantity
        db_book.stock -= db_order.quantity
        db.add(db_order)
        db.commit()


def update_order_by_user(order_id: int, username: str, order: OrderUpdate, db: Session = Depends(get_db), ):
    db_order = db.query(Order).filter(Order.id == order_id, Order.username == username).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.id_status == 7 and order.id_status == 3:  # đang giao -> nhan
        db_order.id_status = 3
        db_book = book_repo.get_book(db_order.id_book, db)
        db_book.quatity_sold += 1

    elif db_order.id_status == 1 and order.id_status == 5:  # huy don khi chua duyet
        db_order.id_status = 5
        db_book = book_repo.get_book(db_order.id_book, db)
        db_book.quatity_sold -= db_order.quantity
        db_book.stock += db_order.quantity
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order_by_admin(order_id: int, order: OrderUpdate, db: Session = Depends(get_db), ):
    db_order = get_order(order_id, db)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.id_status == 1 and order.id_status == 2:  # chua duyet -> duyet
        db_order.id_status = 2
    elif db_order.id_status == 2 and order.id_status == 7:  # duyet->ddnag giao
        db_order.id_status = 7
    elif db_order.id_status == 7 and order.id_status == 6:  # giao hang -> tra hang
        db_order.id_status = 6
        db_book = book_repo.get_book(db_order.id_book, db)
        db_book.quatity_sold -= db_order.quantity
        db_book.stock += db_order.quantity
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = get_order(order_id, db)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    if db_order.id_status == 3 and order.id_status == 4:  # ddax nhaajn -> da danh gia
        db_order.id_status = 4
    db.commit()
    db.refresh(db_order)
    return db_order
