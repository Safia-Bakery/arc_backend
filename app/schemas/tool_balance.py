from typing import Optional
from pydantic import BaseModel
from .fillials import GetParentFill
from .toolparents import GetToolParent


class GetToolBalance(BaseModel):
    branch: Optional[GetParentFill] = None
    amount: Optional[float] = None

    class Config:
        orm_mode = True


class GetTool(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    parentid: Optional[str] = None
    status: Optional[int] = None
    image: Optional[str] = None
    category_id: Optional[int] = None
    tool_balances: Optional[GetToolBalance] = None

    class Config:
        orm_mode = True


class UpdateToolBalance(BaseModel):
    tool_id: int
    amount: float

    class Config:
        orm_mode = True


class GetGroupToolBalances(BaseModel):
    groups: Optional[list[GetToolParent]] = None
    products: Optional[list[GetTool]] = None

    class Config:
        orm_mode = True
