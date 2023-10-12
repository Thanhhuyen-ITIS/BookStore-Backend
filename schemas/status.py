from pydantic import BaseModel

class StatusBase(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode = True