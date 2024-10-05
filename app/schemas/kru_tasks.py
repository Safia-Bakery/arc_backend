from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from .kru_categories import KruCategoriesGet


class KruTasksCreate(BaseModel):
    name: str
    kru_category_id: int
    description : Optional[str]=None

    class Config:
        orm_mode = True

class KruTasksUpdate(BaseModel):
    name: Optional[str]=None
    description : Optional[str]=None

    kru_category_id: Optional[int]=None
    id : int
    class Config:
        orm_mode = True

class KruTasksGet(BaseModel):
    id : int
    name : Optional[str]=None
    description : Optional[str]=None
    kru_category_id : Optional[int]=None
    status : Optional[int]=None
    class Config:
        orm_mode = True




