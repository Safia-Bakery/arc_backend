from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID

from .users import GetBrigada, UserGetJustNames
from .category import GetCategory
from .files import FileSch
from .arc_factory_divisions import GetArcFactoryDivision






class CreateArcFactoryRequests(BaseModel):
    user_id : int
    division_id : int
    branch_id : int
    status : Optional[int]=0
    class Config:
        orm_mode = True


class GetArcFactoryRequests(BaseModel):
    user_id : int
    division_id : int
    branch_id : int
    status : int
    user : UserGetJustNames
    division : GetArcFactoryDivision

    class Config:
        orm_mode = True







