from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models
from config.database import get_db
from schemas.cartbase import CartCreate, CartUpdate


def get_cart(cart_id: int, db: Session = Depends(get_db)):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()


def get_carts(db: Session = Depends(get_db)):
    return db.query(models.Cart).all()


def get_carts_by_username(username: str, db: Session = Depends(get_db)):
    return db.query(models.Cart).filter(models.Cart.username == username).all()


def get_carts_by_book_id(book_id: int, db: Session = Depends(get_db), ):
    return db.query(models.Cart).filter(models.Cart.id_book == book_id).all()


def get_cart_by_username_and_id(id: int, username: str, db: Session = Depends(get_db)):
    return db.query(models.Cart).filter(models.Cart.id == id, models.Cart.username == username).first()


def create_cart(cart: CartCreate, username: str, db: Session = Depends(get_db)):
    db_cart = db.query(models.Cart).filter(models.Cart.username == username,
                                           models.Cart.id_book == cart.id_book).first()
    if not db_cart:
        db_cart = models.Cart(username=username, id_book=cart.id_book, count=cart.count)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
    else:
        db_cart.count += cart.count
        db.commit()
        db.refresh(db_cart)
    return db_cart


def update_cart(id: int, cart: CartUpdate, username: str, db: Session = Depends(get_db)):
    db_cart = db.query(models.Cart).filter(models.Cart.username == username, models.Cart.id == id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db_cart.count = cart.count
    if db_cart.count == 0:
        delete_cart(id, username, db)
        return
    db.commit()
    db.refresh(db_cart)
    return db_cart


def delete_cart(id: int, username: str, db: Session = Depends(get_db)):
    db_cart = db.query(models.Cart).filter(username=username, id=id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="CartBase not found")
    db.delete(db_cart)
    db.commit()

def delete_cart_by_id(id: int, username: str, db: Session = Depends(get_db)):
    db_cart = db.query(models.Cart).filter(models.Cart.id==id and models.Cart.username == username).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="CartBase not found")
    db.delete(db_cart)
    db.commit()
