from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from .users import GetBrigada, UserGetlist, GetUserFullData
from .category import GetCategory
from .fillials import GetFillialChild
from .files import FileSch
from .comments import GetComments
from .communication import MessageRequest
from .expanditure import GetExpanditure
from .orders import OrderProductsGet, CarsGet
from .logs import GetLogs


class GetOneRequest(BaseModel):
    id: int
    product: Optional[str] = None
    description: Optional[str] = None
    deny_reason: Optional[str] = None
    pause_reason: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime
    status: int
    brigada: Optional[GetBrigada] = None
    file: list[FileSch]
    category: Optional[GetCategory] = None
    fillial: Optional[GetFillialChild] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    user: Optional[UserGetlist] = None
    user_manager: Optional[str] = None
    expanditure: list[GetExpanditure]
    comments: list[GetComments]
    is_bot: Optional[bool] = None
    size: Optional[str] = None
    arrival_date: Optional[datetime] = None
    bread_size: Optional[str] = None
    location: Optional[Dict[str, str]] = None
    update_time: Optional[Dict[str, str]] = None
    finishing_time: Optional[datetime] = None
    is_redirected: Optional[bool] = None
    old_cat_id: Optional[int] = None
    request_orpr: Optional[list[OrderProductsGet]] = None
    cars: Optional[CarsGet] = None
    communication: Optional[list[MessageRequest]] = None
    price: Optional[float] = None
    phone_number: Optional[str] = None
    tg_message_id: Optional[int] = None
    log: Optional[list[GetLogs]] = None

    class Config:
        orm_mode = True
