from pydantic import BaseModel


class RoleBase(BaseModel):
    id: int
    role: str

    class Config:
        orm_mode = True

