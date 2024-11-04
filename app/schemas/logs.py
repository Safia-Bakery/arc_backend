from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .users import UserGetJustNames


# class CreateLogs(BaseModel):
#     request: GetOneRequest
#     user: UserFullBack
#     created_at: Optional[datetime]
#     status: Optional[int] = None
#
#     class Config:
#         orm_mode = True


class GetLogs(BaseModel):
    id: int
    user: UserGetJustNames
    created_at: Optional[datetime]
    status: Optional[int] = None

    class Config:
        orm_mode = True

