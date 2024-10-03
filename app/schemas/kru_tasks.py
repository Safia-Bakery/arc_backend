from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from .kru_categories import KruCategoriesGet


class KruTasksCreate(BaseModel):
    name: str
    category_id: int
    class Config:
        orm_mode = True

class KruTasksUpdate(BaseModel):
    name: Optional[str]=None
    category_id: Optional[int]=None
    id : int
    class Config:
        orm_mode = True

class KruTasksGet(BaseModel):
    id : int
    name : Optional[str]=None
    category_id : Optional[int]=None
    class Config:
        orm_mode = True




