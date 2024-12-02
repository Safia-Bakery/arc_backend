from pydantic import BaseModel, validator, Field,ConfigDict
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.logs import GetLogs
from .files import FilesGet

from .users import GetBrigada, UserGetJustNames
from .comments import GetComments
from .category import GetCategory
from .files import FileSch
from .arc_factory_divisions import GetArcFactoryDivision



class GetCoinsRequests(BaseModel):
    id: int
    user_id: Optional[int] = None
    description: Optional[str]=None
    fillial_id: Optional[UUID] = None
    status: Optional[int] = None
    user: Optional[UserGetJustNames] = None
    fillial: Optional[GetArcFactoryDivision] =None
    deny_reason:Optional[str]=None
    is_bot: Optional[int] = 1
    created_at: Optional[datetime] = None
    user_manager: Optional[str] = None
    started_at: Optional[datetime] = None
    price: Optional[float] = Field(None, alias="amount")  # Maps 'division_id' to 'fillial_id
    finished_at: Optional[datetime] = None
    model_config = ConfigDict(
        populate_by_name=True,
    )


class UpdateCoinRequest(BaseModel):
    status :Optional[int]=None
    deny_reason:Optional[str]=None

