from pydantic import BaseModel

class CommentCreate(BaseModel):
    comment: str

    class Config:
        orm_mode = True


class CommentBase(CommentCreate):
    id:int
    id_book: int
    username: str

    class Config:
        orm_mode = True
