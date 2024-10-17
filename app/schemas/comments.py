from pydantic import BaseModel
from .users import UserGetlist
from typing import Optional


class GetComments(BaseModel):
    id: int
    user: UserGetlist
    comment: Optional[str] = None
    rating: Optional[int] = None
    class Config:
        orm_mode = True
