from datetime import datetime
from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel
from app.schemas.fillials import GetFillialChild
from app.schemas.logs import GetLogs
from app.schemas.orders import OrderProductsGet, CreateOrderProducts
from app.schemas.users import UserGetJustNames
from app.schemas.uniform_category import GetCategory


class GetRequest(BaseModel):
    id: int
    user: Optional[UserGetJustNames] = None
    fillial: Optional[GetFillialChild] = None
    user_manager: Optional[str] = None
    created_at: datetime
    deny_reason: Optional[str] = None
    description: Optional[str] = None
    pause_reason: Optional[str] = None
    status: int
    category: Optional[GetCategory] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    is_bot: Optional[bool] = None
    update_time: Optional[Dict[str, str]] = None
    request_orpr: Optional[list[OrderProductsGet]] = None
    price: Optional[float] = None
    phone_number: Optional[str] = None
    log: Optional[list[GetLogs]] = None

    class Config:
        orm_mode = True


class GetRequestList(BaseModel):
    id: int
    fillial: Optional[GetFillialChild] = None
    created_at: datetime
    request_orpr: Optional[list[OrderProductsGet]] = None
    price: Optional[float] = None
    description: Optional[str] = None
    status: int

    class Config:
        orm_mode = True


class UpdateRequest(BaseModel):
    id: int
    status: Optional[int] = None
    deny_reason: Optional[str] = None
    request_products: list[OrderProductsGet]

    class Config:
        orm_mode = True


class CreateRequest(BaseModel):
    fillial_id: UUID
    request_products: list[CreateOrderProducts]

    class Config:
        orm_mode = True
