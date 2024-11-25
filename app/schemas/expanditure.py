from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .tools import ToolsSearch
from .users import UserGetlist,UserGetJustNames
from .inventory_tools import InventoryFactoryToolOne



class GetExpanditure(BaseModel):
    id: int
    amount: int
    tool: Optional[ToolsSearch] = None
    comment: Optional[str] = None
    user: Optional[UserGetJustNames] = None
    created_at: datetime
    status:Optional[int] = None

    class Config:
        orm_mode = True



class GetExpanditureFactoryInv(BaseModel):
    id: int
    amount: int
    tool: Optional[InventoryFactoryToolOne] = None
    comment: Optional[str] = None
    user: Optional[UserGetJustNames] = None
    created_at: datetime
    status:Optional[int] = None

    class Config:
        orm_mode = True