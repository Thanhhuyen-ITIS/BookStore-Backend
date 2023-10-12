from typing import Union

from pydantic import BaseModel


class ReviewCreate(BaseModel):
    star: int
    comment: Union[str, None] = None


class ReviewBase(ReviewCreate):
    id: int
    id_book: int
    username: Union[str, None] = None

    class Config:
        orm_mode = True
