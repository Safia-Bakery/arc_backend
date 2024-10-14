from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID


class GenerateExcel(BaseModel):
    start_date: date
    finish_date: date
    category_id: Optional[int] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True



class GetTelegram(BaseModel):
    id: int
    chat_id: str
    name: str
    class Config:
        orm_mode = True

class CreateTelegram(BaseModel):
    chat_id: str
    name: str
    class Config:
        orm_mode = True

class UpdateTelegram(BaseModel):
    id: int
    chat_id: str
    name: str
    class Config:
        orm_mode = True


class Uniformexcellgeneration(BaseModel):
    start_date:Optional[date]=None
    finish_date:Optional[date]=None
    status: Optional[list[int]]=None