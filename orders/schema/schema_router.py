from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form


class RedirectRequest(BaseModel):
    id: int
    category_id: int


class CatproductAdd(BaseModel):
    category_id: int
    name: str
    status: Optional[int] = 1


class UpdateGetCatProduct(BaseModel):
    id: int
    category_id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True
