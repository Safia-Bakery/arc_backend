from unicodedata import category
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from fastapi_pagination import paginate, Page
from typing import Optional
from app.core.config import settings
from app.crud.inventory_factory_tools import get_tools, get_groups, get_one_tool, update_one_tool,CreateOrUpdateToolCategory,get_inventory_factory_tools,get_inventory_categories
from app.routes.depth import get_db, get_current_user
from app.schemas.users import UserFullBack
from app.schemas.category import GetCategory
from app.schemas.inventory_tools import ProductsVsGroups,InventoryFactoryTool,UpdateInventoryFactoryTool,InventoryFactoryToolOne,ProductsVsGroupsRetail


inv_requests_tools_router = APIRouter()

@inv_requests_tools_router.get('/inventory/factory/tools',response_model=ProductsVsGroups)
async  def get_tools_router(
        name:Optional[str]=None,
        parent_id : Optional[UUID]=None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    groups = get_groups(db=db,name=name,parent_id=parent_id)
    if parent_id is not None:
        tools = get_tools(db=db,name=name,parent_id=parent_id)
    elif name is not None:
        tools = get_tools(db=db, name=name, parent_id=parent_id)
    else:
        tools = []
    return {"groups":groups,'products':tools}



@inv_requests_tools_router.get('/inventory/retail/tools',response_model=ProductsVsGroupsRetail)
async  def get_tools_router(
        name:Optional[str]=None,
        parent_id : Optional[UUID]=None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    groups = get_groups(db=db,name=name,parent_id=parent_id)
    if parent_id is not None:
        tools = get_tools(db=db,name=name,parent_id=parent_id)
    elif name is not None:
        tools = get_tools(db=db,name=name,parent_id=parent_id)
    else:
        tools = []
    return {"folders":groups,'tools':tools}



@inv_requests_tools_router.get('/inventory/factory/tools/{id}',response_model=InventoryFactoryToolOne)
def get_one_tool_api(
        id:int,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    query = get_one_tool(db=db,id=id)
    if query.category_tools:
        query.category_id=query.category_tools[0].category_id
        query.category = query.category_tools[0].categories
    return query



@inv_requests_tools_router.put('/inventory/factory/tools/{id}',response_model=InventoryFactoryToolOne)
async def update_one_tool_api(
        id :int,
        data :UpdateInventoryFactoryTool,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
        ):
    query = update_one_tool(db=db,id=id,data=data)
    if data.category_id is not None:
        category = CreateOrUpdateToolCategory(db=db,category_id=data.category_id,tool_id=id)
        if category.category_id and category.categories:
            query.category_id=category.category_id
            query.category = category.categories
        else:

            query.category_id =None
            query.category = None

    return query

@inv_requests_tools_router.get('/inventory/factory/categories/',response_model=Page[GetCategory])
async  def get_inventory_factory_categories(
        status:Optional[int]=None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    return paginate(get_inventory_categories(db=db,department=10,status=status))



@inv_requests_tools_router.get('/inventory/factory/categories/tools',response_model=Page[InventoryFactoryTool])
async  def get_inventory_factory_categories_tool(
        category_id:Optional[int]=None,
        name : Optional[str]=None,
        status: Optional[int]=None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    return paginate(get_inventory_factory_tools(db=db,category_id=category_id,name=name,status=status))
















