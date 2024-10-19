from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from .fillials import GetFillialChild, GetParentFill
from .tools import GetTool


class GetBalances(BaseModel):
    department_id: Optional[GetParentFill] = None
    store_id: GetFillialChild
    tool_id: GetTool
    amount: Optional[float] = None
    sum: Optional[float] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True
