from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from orders.schema import schema_router
from app.schemas.users import GetBrigadaList, UserGetlist
from app.schemas.category import GetCategorySch
from app.schemas.fillials import GetFillialChild
from app.schemas.files import FileSch
from app.schemas.expanditure import GetExpanditure
from app.schemas.orders import OrderProductsGet


class RatingNumber(BaseModel):
    id: int
    rating: Optional[int] = None

    class Config:
        orm_mode = True


class GetRequest(BaseModel):
    product: Optional[str] = None
    id: int
    rating: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime
    status: int
    brigada: Optional[GetBrigadaList] = None
    file: list[FileSch]
    category: Optional[GetCategorySch] = None
    fillial: Optional[GetFillialChild] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    user: Optional[UserGetlist] = None
    user_manager: Optional[str] = None
    is_bot: Optional[bool] = None
    arrival_date: Optional[datetime] = None
    bread_size: Optional[str] = None
    size: Optional[str] = None
    expanditure: list[GetExpanditure]
    request_orpr:Optional[list[OrderProductsGet]] = None
    id: int
    location: Optional[Dict[str, str]] = None
    update_time: Optional[Dict[str, str]] = None
    comments: Optional[list[RatingNumber]]=None
    pause_reason: Optional[str] = None
    price:Optional[float]=None
    phone_number:Optional[str]=None
    class Config:
        orm_mode = True