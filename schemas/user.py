from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str

class CreateUser(UserBase):
    password: str


class User(UserBase):
    name: Union[str, None] = None
    gender: Union[int, None] = None
    id_role: Union[int, None] = None
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: int

    class Config:
        orm_mode = True