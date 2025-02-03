from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from orders.schema import schema_router
from app.schemas.manager_branchs import getManagers


class GetParentFill(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GetFillialChild(BaseModel):
    id: UUID
    name: str
    origin: int
    parentfillial: Optional[GetParentFill] = None
    manager:Optional[getManagers]=None

    class Config:
        orm_mode = True