from pydantic import BaseModel
from typing import Optional
from .users import UserFullBack
from datetime import datetime


class MessageRequest(BaseModel):
    id: int
    message: Optional[str] = None
    status: int
    user: Optional[UserFullBack] = None
    photo: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True