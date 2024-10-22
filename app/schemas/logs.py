from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from .fillials import GetFillialChild, GetParentFill
from .tools import GetTool
from .requests import GetOneRequest
from .users import UserFullBack


class CreateLogs(BaseModel):
    request: GetOneRequest
    user: UserFullBack
    created_at: Optional[datetime]
    status: Optional[int] = None

    class Config:
        orm_mode = True
