from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    price: Optional[float] = None
    description: Optional[str] = None
    status: Optional[int] = 1
    urgent: Optional[bool] = True
    universal_size: Optional[bool] = False

    class Config:
        orm_mode = True


class UpdateCategory(BaseModel):
    id: int
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    status: Optional[int] = None
    urgent: Optional[bool] = None
    universal_size: Optional[bool] = None

    class Config:
        orm_mode = True


class GetCategory(BaseModel):
    id: int
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    status: Optional[int] = None
    urgent: Optional[bool] = None
    universal_size: Optional[bool] = None

    class Config:
        orm_mode = True