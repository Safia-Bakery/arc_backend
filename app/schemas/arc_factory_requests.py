from pydantic import BaseModel, validator, Field,ConfigDict
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.logs import GetLogs

from .users import GetBrigada, UserGetJustNames
from .category import GetCategory
from .files import FileSch
from .arc_factory_divisions import GetArcFactoryDivision








class GetArcFactoryRequests(BaseModel):
    user_id : Optional[int]=None
    fillial_id: Optional[UUID] = Field(None, alias="division_id")  # Maps 'division_id' to 'fillial_id'
    status: Optional[int] = None
    user: Optional["UserGetJustNames"] = None
    fillial: Optional["GetArcFactoryDivision"] = Field(None, alias="division")  # Maps 'fillial' to 'division'

    model_config = ConfigDict(
        populate_by_name=True,
    )


class UpdateArcFactoryRequests(BaseModel):
    status : int
    brigada_id : Optional[int]
    deny_reason : Optional[str]

    class Config:
        orm_mode = True



class GetArcFactoryRequest(BaseModel):
    user_id : Optional[int]=None
    fillial_id: Optional[UUID] = Field(None, alias="division_id")  # Maps 'division_id' to 'fillial_id'
    status: Optional[int] = None
    user: Optional["UserGetJustNames"] = None
    fillial: Optional["GetArcFactoryDivision"] = Field(None, alias="division")  # Maps 'fillial' to 'division'
    logs : Optional[list[GetLogs]] = None


    model_config = ConfigDict(
        populate_by_name=True,
    )






