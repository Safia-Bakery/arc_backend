from typing import Optional
from uuid import UUID
from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string
from app.schemas.branchs import GetBranchs
from fastapi_pagination import Page, paginate
from app.crud.arc_factory_divisions import create_arc_factory_division, get_arc_factory_divisions, \
    get_arc_factory_division, update_arc_factory_division
from app.schemas.arc_factory_divisions import CreateArcFactoryDivision, UpdateArcFactoryDivision, GetArcFactoryDivision

arc_factory_divisions = APIRouter()


@arc_factory_divisions.post("/arc/factory/divisions", response_model=GetArcFactoryDivision)
async def create_division(division: CreateArcFactoryDivision,
                          db: Session = Depends(get_db),
                          current_user: GetUserFullData = Depends(get_current_user)):
    return create_arc_factory_division(db=db, division=division)


@arc_factory_divisions.get("/arc/factory/divisions", response_model=Page[GetArcFactoryDivision])
async def get_divisions(parent_id: Optional[UUID] = None,
                        name: Optional[str] = None,
                        manager_id: Optional[int] = None,
                        status: Optional[int] = None,
                        current_user: GetUserFullData = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return paginate(
        get_arc_factory_divisions(db=db, parent_id=parent_id, name=name, manager_id=manager_id, status=status))


@arc_factory_divisions.get("/arc/factory/divisions/{division_id}", response_model=GetArcFactoryDivision)
async def get_division(
        division_id: UUID,
        current_user: GetUserFullData = Depends(get_current_user),
        db: Session = Depends(get_db)):
    return get_arc_factory_division(db=db, division_id=division_id)


@arc_factory_divisions.put("/arc/factory/divisions/{division_id}", response_model=GetArcFactoryDivision)
async def update_division(division_id: UUID,
                          division: UpdateArcFactoryDivision,
                          db: Session = Depends(get_db),
                          current_user: GetUserFullData = Depends(get_current_user)):
    return update_arc_factory_division(db=db, division_id=division_id, division=division)
