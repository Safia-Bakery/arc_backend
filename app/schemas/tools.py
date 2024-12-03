from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from app.schemas.tool_balance import GetToolBalance


class ToolsSearch(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    mainunit: Optional[str] = None
    producttype: Optional[str] = None
    iikoid:Optional[UUID]=None
    price:Optional[float]=None
    parentid:Optional[UUID]=None
    total_price:Optional[float]=None
    amount_left:Optional[float]=None
    min_amount:Optional[float]=None
    max_amount:Optional[float]=None
    ftime:Optional[float]=None
    status:Optional[int]=None
    image:Optional[str]=None
    category_id:Optional[int]=None

    class Config:
        orm_mode = True


class GetTool(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    parentid: Optional[str] = None
    mainunit: Optional[str] = None
    producttype: Optional[str] = None
    iikoid: Optional[UUID] = None
    ftime: Optional[float] = None
    status: Optional[int] = None
    image: Optional[str] = None
    category_id: Optional[int] = None
    # tool_balance: Optional[GetToolBalance] = None

    class Config:
        orm_mode = True