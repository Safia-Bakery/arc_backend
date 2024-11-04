from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID
from .users import GetBrigada, UserGetJustNames
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
    user: Optional[UserGetJustNames] = None
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
    category_id: Optional[int] = None
    parentfillial_id: Optional[UUID] = None
    finishing_time: Optional[datetime] = None
    brigada_id: Optional[int] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True


class CreateRequest(BaseModel):
    parentfillial_id: UUID
    category_id: Optional[int] = None
    description: Optional[str] = None
    files: Optional[list[UploadFile]] = None

    class Config:
        orm_mode = True


class MessageRequestCreate(BaseModel):
    request_id: int
    message: str
    status: Optional[int] = 0
