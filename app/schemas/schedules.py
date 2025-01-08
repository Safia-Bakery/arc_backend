from datetime import datetime, time, date
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.schemas.appointments import GetAppointment



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class GetSchedule(BaseConfig):
    id: int
    date: date
    time: Optional[time]
    is_available: Optional[bool]
    description: Optional[str]
    department: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    appointments: Optional[List[GetAppointment]]



class CreateSchedule(BaseConfig):
    date: date
    time: Optional[str] = None
    is_available: Optional[bool] = False
    description: Optional[str] = None


class UpdateSchedule(BaseConfig):
    id: int
    time: Optional[str] = None
    is_available: Optional[bool] = False
    description: Optional[str] = None