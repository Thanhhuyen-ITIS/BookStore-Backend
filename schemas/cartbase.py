from pydantic import BaseModel


class CartUpdate(BaseModel):
    count: int
class CartCreate(CartUpdate):
    id_book: int

class CartBase(CartCreate):
    id: int
    username: str

    class Config:
        orm_mode = True
