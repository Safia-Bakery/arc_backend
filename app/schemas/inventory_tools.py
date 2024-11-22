from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class InventoryFactoryTool(BaseModel):
    id: int
    name: Optional[str] = None
    status: Optional[int] = None
    factory_image:Optional[str]=None
    class Config:
        orm_mode = True

class GroupsFactoryTool(BaseModel):
    id : UUID
    name : Optional[str] =None
    parent_id :Optional[UUID]=None
    class Config:
        orm_mode = True


class ProductsVsGroups(BaseModel):
    groups : Optional[list[GroupsFactoryTool]]=None
    products :Optional[list[InventoryFactoryTool]]
    class Config:
        orm_mode = True


