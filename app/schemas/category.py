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