from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from app.schemas.branchs import GetBranchs
from app.schemas.users import UserGetlist
from app.schemas.tools import GetTool


class OrderItem(BaseModel):
    product : Optional[GetTool] =None
    amount: Optional[int]=None
    class Config:
        orm_mode = True



class CreateOrderItem(BaseModel):
    product_id: int
    amount : int






class CreateOrder(BaseModel):
    products: List[CreateOrderItem]

    class Config:
        orm_mode = True


class UpdateOrder(BaseModel):
    status: int

    class Config:
        orm_mode = True


class GetOrder(BaseModel):
    id: int
    branch_id: Optional[UUID]
    branch: Optional[GetBranchs] = None
    status: Optional[int]
    created_by: Optional[int] = None
    accepted_by: Optional[int] = None
    created_user: Optional[UserGetlist] = None
    accepted_user: Optional[UserGetlist] = None
    order_item: Optional[list[OrderItem]] = None
    created_at: Optional[datetime] =None

    class Config:
        orm_mode = True


class OrdersHistory(BaseModel):
    active: Optional[List[GetOrder]]
    closed: Optional[List[GetOrder]]
