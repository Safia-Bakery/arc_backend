from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .tools import ToolsSearch
from .users import UserGetlist


class GetExpanditure(BaseModel):
    id: int
    amount: int
    tool: Optional[ToolsSearch] = None
    comment: Optional[str] = None
    user: Optional[UserGetlist] = None
    created_at: datetime
    status:Optional[int] = None

    class Config:
        orm_mode = True