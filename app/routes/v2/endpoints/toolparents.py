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
from app.schemas.toolparents import GetToolParent
from app.crud import toolparents
from datetime import datetime, date


toolparents_router = APIRouter()


@toolparents_router.get("/tools/parents", response_model=Page[GetToolParent])
async def get_toolparents(
        parent_id: Optional[str] = None,
        status: Optional[int] = None,
        name: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    tool_parents = toolparents.get_toolparents(db=db, parent_id=parent_id, status=status, name=name)
    return paginate(tool_parents)


@toolparents_router.put("/tools/parents", response_model=GetToolParent)
async def put_toolparent(
        id: str,
        status: Optional[int] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    tool_parent = toolparents.update_toolparent(db=db, id=id, status=status)
    return tool_parent

