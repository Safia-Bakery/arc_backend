from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.branchs import GetBranchs


class CreateCalendars(BaseModel):
    branch_id: UUID
    date: date
    is_active: Optional[int]=None
    class Config:
        orm_mode = True



class UpdateCalendars(BaseModel):
    branch_id: Optional[UUID]=None
    date: Optional[date]=None
    is_active: Optional[int]=None
    id: UUID
    class Config:
        orm_mode = True


class GetCalendars(BaseModel):
    id: int
    branch_id: UUID
    date: date
    branch: Optional[GetBranchs]=None
    is_active: Optional[int]=None
    class Config:
        orm_mode = True


class GetOneCalendar(BaseModel):
    id: UUID
    branch_id: UUID
    date: date
    is_active: Optional[int]=None
    branch: Optional[GetBranchs]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True



class FilterCalendar(BaseModel):
    months :Optional[list[int]]=None
    years :Optional[list[int]]=None
    class Config:
        orm_mode = True






