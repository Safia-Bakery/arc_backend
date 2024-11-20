from pydantic import BaseModel, validator, Field,ConfigDict
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.logs import GetLogs

from .users import GetBrigada, UserGetJustNames
from .comments import GetComments
from .category import GetCategory
from .files import FileSch
from .arc_factory_divisions import GetArcFactoryDivision








class GetArcFactoryRequests(BaseModel):
    id :int
    user_id : Optional[int]=None
    fillial_id: Optional[UUID] = Field(None, alias="division_id")  # Maps 'division_id' to 'fillial_id'
    status: Optional[int] = None
    user: Optional[UserGetJustNames] = None
    fillial: Optional[GetArcFactoryDivision] = Field(None, alias="division")  # Maps 'fillial' to 'division'
    brigada: Optional[GetBrigada] = None
    category : Optional[GetCategory] = None
    is_bot : Optional[int] = 1
    created_at : Optional[datetime] = None
    user_manager : Optional[str] = None
    comments : Optional[list[GetComments]] = None
    model_config = ConfigDict(
        populate_by_name=True,
    )


class UpdateArcFactoryRequests(BaseModel):
    status : int
    brigada_id : Optional[int]
    deny_reason : Optional[str]
    category_id : Optional[int]

    class Config:
        orm_mode = True



class GetArcFactoryRequest(BaseModel):
    id: int
    user_id: Optional[int] = None
    fillial_id: Optional[UUID] = Field(None, alias="division_id")  # Maps 'division_id' to 'fillial_id'
    status: Optional[int] = None
    user: Optional[UserGetJustNames] = None
    fillial: Optional[GetArcFactoryDivision] = Field(None, alias="division")  # Maps 'fillial' to 'division'
    brigada: Optional[GetBrigada] = None
    category: Optional[GetCategory] = None
    is_bot: Optional[int] = 1
    created_at: Optional[datetime] = None
    user_manager: Optional[str] = None
    comments: Optional[list[GetComments]] = None
    files: Optional[list[FileSch]] = None
    logs: Optional[list[GetLogs]] = None
    phone_number: Optional[str] = None
    update_time: Optional[Dict[str, str]] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    model_config = ConfigDict(
        populate_by_name=True,
    )






