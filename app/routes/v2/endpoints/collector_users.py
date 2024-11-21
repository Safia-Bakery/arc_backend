import pytz
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.crud.collector_users import create_user, get_by_telegram_id, update_user
from app.routes.depth import get_db
from app.schemas.collector_users import CreateUser, UpdateUser
from app.schemas.collector_users import GetUser


collector_users_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@collector_users_router.post("/collector/user/", response_model=GetUser)
async def create_collector_user(
    data: CreateUser,
    db: Session = Depends(get_db)
):
    return create_user(db=db, data=data)


@collector_users_router.get("/collector/user/", response_model=GetUser)
async def get_collector_user(
    telegram_id: int,
    db: Session = Depends(get_db)
):
    return get_by_telegram_id(db=db, telegram_id=telegram_id)


@collector_users_router.put("/collector/user/", response_model=GetUser)
async def update_collector_user(
    data: UpdateUser,
    db: Session = Depends(get_db)
):
    return update_user(db=db, data=data)
