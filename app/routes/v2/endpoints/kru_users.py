from typing import Optional

import pytz
from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.crud.kru_users import create_user, get_by_telegram_id
from app.models.users_model import Users
from app.routes.depth import get_db, get_current_user
from app.schemas.kru_users import CreateUser
from app.schemas.users import GetUserFullData

kru_users_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@kru_users_router.post("/kru_users/",response_model= GetUserFullData)
async def create_kru_user(
    form_data: CreateUser,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Create new user
    """
    return  create_user(db=db,form_data=form_data)



@kru_users_router.get("/kru_users/",response_model=GetUserFullData)
async def get_kru_users_api(
    telegram_id:Optional[int]=None,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Get users
    """
    return get_by_telegram_id(db=db,telegram_id=telegram_id)