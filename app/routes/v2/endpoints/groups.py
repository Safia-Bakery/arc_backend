import pytz
from fastapi import APIRouter, Query
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.crud.groups import get_groups, get_group
from app.routes.depth import get_db, get_current_user
from app.schemas.groups import GetGroup
from app.schemas.users import GetUserFullData

groups_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@groups_router.get("/groups/", response_model=List[GetGroup])
async def get_user_groups(
        ids: Optional[List[int]] = Query(None),
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    return get_groups(db=db, ids=ids)


@groups_router.get("/group/", response_model=GetGroup)
async def get_user_group(
        name: str,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    return get_group(db=db, name=name)

