
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict,Field
from app.schemas.category import GetCategory


class InventoryFactoryTool(BaseModel):
    id: int
    name: Optional[str] = None
    status: Optional[int] = None
    factory_image: Optional[str] = Field(None, alias='file')
    parentid:Optional[UUID]=None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class InventoryFactoryToolOne(BaseModel):
    id: int
    name: Optional[str] = None
    status: Optional[int] = None
    factory_image: Optional[str] = Field(None, alias='file')
    category_id:Optional[int]=None
    category :Optional[GetCategory]=None
    model_config = ConfigDict(
        populate_by_name=True,
    )

class GroupsFactoryTool(BaseModel):
    id : UUID
    name : Optional[str] =None
    parent_id :Optional[UUID]=None
    class Config:
        orm_mode=True



class ProductsVsGroups(BaseModel):
    groups : Optional[list[GroupsFactoryTool]]=None
    products :Optional[list[InventoryFactoryTool]]= None
    class Config:
        orm_mode = True




class UpdateInventoryFactoryTool(BaseModel):
    name : str
    status: Optional[int]=None
    category_id:Optional[int]=None
    file : Optional[str]=None

