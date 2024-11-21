from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID


class CreateArcFactoryManagers(BaseModel):
    name: str
    description: Optional[str]=None
    class Config:
        orm_mode = True


class GetArcFactoryManagers(BaseModel):
    id :int
    name: Optional[str]=None
    description: Optional[str]=None
    status: Optional[int]=None

    class Config:
        orm_mode = True

class UpdateArcFactoryManagers(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    status: Optional[int]=None
    class Config:
        orm_mode = True
