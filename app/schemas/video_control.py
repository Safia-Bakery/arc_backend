from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.category import GetCategory
from app.schemas.users import GetBrigada, UserGetJustNames
from schemas import GetFillialChild


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )



class GetRequests(BaseConfig):
    id: int
    user: Optional[UserGetJustNames] = None
    brigada: Optional[GetBrigada] = None
    fillial: Optional[GetFillialChild] = None
    category: Optional[GetCategory] = None
    status: int
    created_at: datetime



class GenerateExcell(BaseConfig):
    start_date: date
    finish_date: date

