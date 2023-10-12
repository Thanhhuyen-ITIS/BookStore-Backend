from datetime import date
from typing import Union

from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: Union[str, None] = None
    about: Union[str, None] = None
    id_category: int
    release_date: Union[date, None] = None
    picture: str
    page: Union[int, None] = None
    stock: Union[int, None] = None
    cost: int

    class Config:
        orm_mode = True
class BookBase(BookCreate):
    id: int
    quatity_sold: int

    class Config:
        orm_mode = True




