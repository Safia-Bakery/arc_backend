from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.branchs import GetBranchs
from app.schemas.files import FilesGet
from app.schemas.positions import GetPosition
from app.schemas.users import UserGetJustNames


class CreateAppointment(BaseModel):
    employee_name: str
    time_slot: datetime
    description: Optional[str] = None
    position_id: int
    branch_id: UUID

    class Config:
        orm_mode = True


class GetAppointment(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    time_slot: Optional[datetime] = None
    status: Optional[int] = None
    description: Optional[str] = None
    department: Optional[int] = None
    deny_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    position: Optional[GetPosition] = None
    user: Optional[UserGetJustNames] = None
    branch: Optional[GetBranchs] = None
    file: Optional[list[FilesGet]] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class GetCalendarAppointment(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = Field(None, alias="title")
    time_slot: Optional[datetime] = Field(None, alias="date")
    status: Optional[int] = None
    description: Optional[str] = None
    department: Optional[int] = None
    deny_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    position: Optional[GetPosition] = None
    user: Optional[UserGetJustNames] = None
    branch: Optional[GetBranchs] = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class UpdateAppointment(BaseModel):
    id: int
    employee_name: Optional[str] = None
    status: Optional[int] = None
    description: Optional[str] = None
    deny_reason: Optional[str] = None
    files: Optional[list[str]] = None

    class Config:
        orm_mode = True



class MyAppointments(BaseModel):
    new: Optional[List[GetAppointment]] = None
    archive: Optional[List[GetAppointment]] = None

    class Config:
        orm_mode = True
