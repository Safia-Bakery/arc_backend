from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID


class KruCategoriesCreate(BaseModel):
    name: str
    class Config:
        orm_mode = True


class KruCategoriesUpdate(BaseModel):
    name: Optional[str]=None
    id : int
    class Config:
        orm_mode = True


class KruCategoriesGet(BaseModel):
    id : int
    name : Optional[str]=None
    class Config:
        orm_mode = True