from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.branchs import GetBranchs


class CreateUser(BaseModel):
    full_name: Optional[str]=None
    telegram_id: int
    branch_id: Optional[int]=None
    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    full_name: Optional[str]=None
    branch_id: Optional[UUID]=None
    id : int
    class Config:
        orm_mode = True



class GetUser(BaseModel):
    id : int
    full_name : Optional[str]=None
    telegram_id : Optional[int]=None
    branch_id : Optional[int]=None
    branch : Optional[GetBranchs]=None
    class Config:
        orm_mode = True


