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
from app.crud.inventory_factory_tools import get_tools,get_groups
from app.routes.depth import get_db, get_current_user
from app.schemas.users import UserFullBack
from app.schemas.inventory_tools import ProductsVsGroups

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
    else:
        tools = []
    return {"groups":groups,'products':tools}


