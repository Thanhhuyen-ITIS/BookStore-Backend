from datetime import date

from pydantic import BaseModel


class OrderCreate(BaseModel):
    id_book: int
    quantity: int
    name: str
    address: str

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    id_status: int

    class Config:
        orm_mode = True


class OrderBase(OrderUpdate, OrderCreate):
    id: int
    username: str
    total_price: int
    order_date: date

    class Config:
        orm_mode = True
