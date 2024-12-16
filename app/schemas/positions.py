from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CreatePosition(BaseModel):
    name: str
    department: Optional[int] = None

    class Config:
        orm_mode = True


class GetPosition(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[int] = None
    department: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UpdatePosition(BaseModel):
    id: int
    name: Optional[str] = None
    status: Optional[int] = None
    department: Optional[int] = None

    class Config:
        orm_mode = True