from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from app.schemas.users import GetBrigadaList, UserGetlist
from app.schemas.category import GetCategory
from app.schemas.fillials import GetFillialChild
from app.schemas.files import FileSch


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
    brigada: Optional[GetBrigadaList] = None
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