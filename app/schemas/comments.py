from pydantic import BaseModel
from .it_requests import GetRequest
from .users import UserGetlist
from typing import Optional


class GetComments(BaseModel):
    id: int
    request: GetRequest
    user: UserGetlist
    comment: Optional[str] = None
    rating: Optional[int] = None

    class Config:
        orm_mode = True
