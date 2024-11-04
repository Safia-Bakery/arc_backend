from pydantic import BaseModel


class GetGroup(BaseModel):
    id: int
    name: str
    status: int

    class Config:
        orm_mode = True