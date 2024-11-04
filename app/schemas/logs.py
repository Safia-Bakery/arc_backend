from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from .fillials import GetFillialChild, GetParentFill
from .tools import GetTool
from .users import UserFullBack,UserGetJustNames


class CreateLogs(BaseModel):
    user: UserFullBack
    created_at: Optional[datetime]
    status: Optional[int] = None

    class Config:
        orm_mode = True


class GetLogs(BaseModel):
    id: int
    user: UserGetJustNames
    created_at: Optional[datetime]
    status: Optional[int] = None

    class Config:
        orm_mode = True

