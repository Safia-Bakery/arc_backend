from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.arc_factory_managers import GetArcFactoryManagers


class CreateArcFactoryDivision(BaseModel):
    name : str
    manager_id : int
    status : Optional[int]=0
    class Config:
        orm_mode = True

class UpdateArcFactoryDivision(BaseModel):
    name : Optional[str]=  None
    manager_id : Optional[int]= None
    status : Optional[int]= None
    class Config:
        orm_mode = True

class GetArcFactoryDivisions(BaseModel):
    name : Optional[str]=  None
    manager_id : Optional[int]= None
    status : Optional[int]= None
    class Config:
        orm_mode = True


class GetArcFactoryDivision(BaseModel):
    id : UUID
    name : Optional[str]=0
    manager_id : Optional[int]=0
    status : Optional[int]=0
    manager : Optional[GetArcFactoryManagers]=None
    class Config:
        orm_mode = True




