from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from .fillials import GetFillialChild, GetParentFill
from .tools import GetTool


class GetBalances(BaseModel):
    store_id: GetFillialChild
    tool_id: GetTool
    department_id: Optional[GetParentFill] = None
    amount: Optional[float] = None
    sum: Optional[float] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True


class GetToolBalance(BaseModel):
    branch: Optional[GetParentFill] = None
    tool: Optional[GetTool] = None
    amount: Optional[float] = None

    class Config:
        orm_mode = True


class UpdateToolBalance(BaseModel):
    tool_id: int
    amount: float

    class Config:
        orm_mode = True
