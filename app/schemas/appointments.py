from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.schemas.branchs import GetBranchs
from app.schemas.positions import GetPosition
from app.schemas.users import GetUserFullData


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
    position: Optional[GetPosition] = None
    user: Optional[GetUserFullData] = None
    branch: Optional[GetBranchs] = None

    class Config:
        orm_mode = True


class UpdateAppointment(BaseModel):
    id: int
    employee_name: Optional[str] = None
    status: Optional[int] = None
    description: Optional[str] = None
    deny_reason: Optional[str] = None

    class Config:
        orm_mode = True
