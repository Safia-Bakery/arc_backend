from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from fastapi_pagination import paginate, Page
from typing import Optional
from app.schemas.it_extra import *
from app.routes.depth import get_db, get_current_user
from app.schemas.users import UserFullBack
from app.schemas.inventory_requests import (GetRequest,
                                            GetRequestFactoryInv,
                                            CreateInventoryRequest,
                                            UpdateRequest,
                                            UpdateInventoryExpenditure
                                            )

from app.schemas.requests import GetOneRequest,GetOneRequestInventoryFactory
from app.crud import inv_requests, logs, files
from app.crud.manager_branchs import get_managers,get_one_manager,get_manager_divisions
from app.schemas.manager_branchs import getManagers,getDivisions
from app.schemas.users import UserGetJustNames

factory_branchs_router = APIRouter()


@factory_branchs_router.get("/factory/managers", response_model=list[getManagers])
async  def get_factory_managers(
        name:Optional[str]=None,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    query =get_managers(db=db,name=name)
    return query


@factory_branchs_router.get("/factory/managers/divisions",response_model=list[getDivisions])
async  def get_factory_divisions(
        manager_id:int,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    query = get_manager_divisions(db=db,manager_id=manager_id)
    return query