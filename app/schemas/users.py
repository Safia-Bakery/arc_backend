from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.branchs import GetBranchs


class UserFullBack(BaseModel):
    id: int
    username: str
    success: Optional[bool] = True
    full_name: Optional[str] = None
    status: Optional[int] = None
    sphere_status: Optional[int] = None
    brigader: Optional[object] = None
    brigada_id: Optional[object] = None
    group_id: Optional[int] = None
    group: Optional[object] = None
    telegram_id: Optional[int] = None

    class Config:
        orm_mode = True


class GetUserFullData(BaseModel):
    id:int
    username:str
    full_name:Optional[str]=None
    telegram_id:Optional[int]=None
    branch_id:Optional[UUID]=None
    branch:Optional[GetBranchs]=None


    class Config:
        orm_mode = True


class UpdateGroupSch(BaseModel):
    name: str
    id: int

    class Config:
        orm_mode = True


class UserGetlist(BaseModel):
    id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    group: Optional[UpdateGroupSch] = None
    status: int

    class Config:
        orm_mode = True


class GetBrigada(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: int
    user: list[UserGetlist]
    sphere_status: int
    department: int
    is_outsource: Optional[bool] = None
    chat_id: Optional[int] = None
    topic_id: Optional[int] = None

    class Config:
        orm_mode = True