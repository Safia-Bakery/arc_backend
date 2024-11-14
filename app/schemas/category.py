from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from orders.schema import schema_router
from app.schemas.telegrams import TelegramsGet


class GetCategory(BaseModel):
    name: str
    description: Optional[str] = None
    status: int
    id: int
    urgent: bool
    sub_id: Optional[int] = None
    department: int
    sphere_status: Optional[int] = None
    file: Optional[str] = None
    ftime: Optional[float] = None
    parent_id:Optional[int] = None
    is_child:Optional[bool]=None
    telegram_id:Optional[int]=None
    telegram:Optional[TelegramsGet]=None
    price:Optional[float]=None

    class Config:
        orm_mode = True
        from_attributes = True


class CreateCategory(BaseModel):
    name: str
    department: int
    ftime: Optional[float] = None
    description: Optional[str] = None
    status: Optional[int] = 1
    urgent: Optional[bool] = True
    sphere_status: Optional[int] = None
    file: Optional[str] = None
    sub_id: Optional[int] = None
    parent_id: Optional[int] = None
    is_child: Optional[bool] = None
    telegram_id: Optional[int] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True
        from_attributes = True

class UpdateCategory(BaseModel):
    id : int
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    urgent: Optional[bool] = None
    sub_id: Optional[int] = None
    file: Optional[str] = None
    ftime: Optional[float] = None
    parent_id:Optional[int] = None
    is_child:Optional[bool]=None
    telegram_id:Optional[int]=None
    price:Optional[float]=None
