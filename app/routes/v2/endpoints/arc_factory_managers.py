from typing import Optional

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string
from app.schemas.branchs import GetBranchs
from fastapi_pagination import Page,paginate
from app.crud.branchs import get_branchs
from app.schemas.arc_factory_managers import CreateArcFactoryManagers,GetArcFactoryManagers,UpdateArcFactoryManagers
from app.crud.arc_factory_managers import create_arc_factory_manager,get_arc_factory_managers,get_arc_factory_manager,update_arc_factory_manager


arc_factory_managers = APIRouter()


@arc_factory_managers.post("/arc/factory/managers",response_model=GetArcFactoryManagers)
async def create_manager(manager:CreateArcFactoryManagers,
                         db:Session=Depends(get_db),
                         current_user: GetUserFullData = Depends(get_current_user)):
    return create_arc_factory_manager(db=db,manager=manager)


@arc_factory_managers.get("/arc/factory/managers",response_model=Page[GetArcFactoryManagers])
async def get_managers(
        name:Optional[str]=None,
        description:Optional[str]=None,
        status:Optional[int]=None,
        current_user: GetUserFullData = Depends(get_current_user),
        db:Session=Depends(get_db)):
    return paginate(get_arc_factory_managers(db=db,name=name,description=description,status=status))


@arc_factory_managers.get("/arc/factory/managers/{manager_id}",response_model=GetArcFactoryManagers)
async def get_manager(
        manager_id:int,
        current_user: GetUserFullData = Depends(get_current_user),
        db:Session=Depends(get_db)):
    return get_arc_factory_manager(db=db,manager_id=manager_id)


@arc_factory_managers.put("/arc/factory/managers/{manager_id}",response_model=GetArcFactoryManagers)
async def update_manager(
        manager_id:int,
        manager:UpdateArcFactoryManagers,
        db:Session=Depends(get_db),
        current_user: GetUserFullData = Depends(get_current_user)):
    return update_arc_factory_manager(db=db,manager_id=manager_id,manager=manager)
