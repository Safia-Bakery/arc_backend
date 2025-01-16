from uuid import UUID

from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from .users import GetBrigada, UserGetlist
from .category import GetCategory
from .fillials import GetFillialChild
from .files import FileSch
from .comments import GetComments
from .communication import MessageRequest
from .expanditure import GetExpanditure,GetExpanditureFactoryInv
from .orders import OrderProductsGet, CarsGet


class GetRequest(BaseModel):
    id: int
    user: Optional[UserGetlist] = None
    fillial: Optional[GetFillialChild] = None
    expanditure: list[GetExpanditure]
    created_at: datetime
    status: int
    user_manager: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True

class GetRequestFactoryInv(BaseModel):
    id: int
    user: Optional[UserGetlist] = None
    fillial: Optional[GetFillialChild] = None
    expanditure: list[GetExpanditureFactoryInv]
    created_at: datetime
    status: int
    user_manager: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class GetOneRequest(BaseModel):
    id: int
    user: Optional[UserGetlist] = None
    product: Optional[str] = None
    description: Optional[str] = None
    deny_reason: Optional[str] = None
    # pause_reason: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime
    status: int
    # brigada: Optional[GetBrigadaList] = None
    file: list[FileSch]
    category: Optional[GetCategory] = None
    fillial: Optional[GetFillialChild] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    user_manager: Optional[str] = None
    expanditure: list[GetExpanditure]
    # comments: list[GetComments]
    is_bot: Optional[bool] = None
    # size: Optional[str] = None
    # arrival_date: Optional[datetime] = None
    # bread_size: Optional[str] = None
    # location: Optional[Dict[str, str]] = None
    update_time: Optional[Dict[str, str]] = None
    finishing_time: Optional[datetime] = None
    # is_redirected: Optional[bool] = None
    # old_cat_id: Optional[int] = None
    # request_orpr: Optional[list[OrderProductsGet]] = None
    # cars: Optional[CarsGet] = None
    # communication: Optional[list[MessageRequest]] = None
    # price: Optional[float] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class RequestExpenditureCreate(BaseModel):
    amount: int
    tool_id: int


class CreateInventoryRequest(BaseModel):
    fillial_id:  UUID
    category_id: int
    description: Optional[str] = None
    product: Optional[str] = None
    expenditure: list[RequestExpenditureCreate] = None
    files: Optional[list[str]] = None
    phone_number:Optional[str]=None



class UpdateInventoryExpenditure(BaseModel):
    id: int
    status: Optional[int] = None
    amount: Optional[int] = None
    comment: Optional[str] = None
    class Config:
        orm_mode = True



class UpdateRequest(BaseModel):
    id : int
    deny_reason: Optional[str] = None
    pause_reason: Optional[str] = None
    status: Optional[int] = None






