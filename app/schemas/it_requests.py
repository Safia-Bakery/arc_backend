from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from .users import GetBrigada, UserGetlist, GetUserFullData
from .category import GetCategory
from .fillials import GetFillialChild
from .files import FileSch


class RatingNumber(BaseModel):
    id: int
    rating: Optional[int] = None

    class Config:
        orm_mode = True


class GetRequest(BaseModel):
    id: int
    rating: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime
    status: int
    brigada: Optional[GetBrigada] = None
    file: list[FileSch]
    category: Optional[GetCategory] = None
    fillial: Optional[GetFillialChild] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    user: Optional[UserGetlist] = None
    is_bot: Optional[bool] = None
    location: Optional[Dict[str, str]] = None
    update_time: Optional[Dict[str, str]] = None
    comments: Optional[list[RatingNumber]] = None
    pause_reason: Optional[str] = None
    price: Optional[float] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class PutRequest(BaseModel):
    id: int
    user: Optional[GetUserFullData] = None
    fillial: Optional[GetFillialChild] = None
    brigada: Optional[GetBrigada] = None
    status: Optional[int] = None
    category: Optional[GetCategory] = None
    finishing_time: Optional[datetime] = None
    deny_reason: Optional[str] = None
    update_time: Optional[dict] = None
    tg_message_id: Optional[int] = None

    class Config:
        orm_mode = True


class MessageRequestCreate(BaseModel):
    request_id: int
    message: str
    status: Optional[int] = 0
