from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    category: str

    class Config:
        orm_mode = True