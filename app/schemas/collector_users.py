from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.schemas.branchs import GetBranchs
from app.schemas.groups import GetGroup


class CreateUser(BaseModel):
    telegram_id: int
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    telegram_id: int
    group_id: Optional[int] = None
    branch_id: Optional[UUID] = None

    class Config:
        orm_mode = True


class GetUser(BaseModel):
    id: int
    full_name: Optional[str] = None
    telegram_id: Optional[int] = None
    branch_id: Optional[UUID] = None
    branch: Optional[GetBranchs] = None
    group_id: Optional[int] = None
    group: Optional[GetGroup] = None

    class Config:
        orm_mode = True
