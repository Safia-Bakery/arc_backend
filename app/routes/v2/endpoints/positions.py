from typing import List
import pytz
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.positions import get_positions, add_position, edit_position
from app.routes.depth import get_db, get_current_user
from app.schemas.positions import GetPosition, CreatePosition, UpdatePosition
from app.schemas.users import UserGetJustNames

positions_router = APIRouter()
timezonetash = pytz.timezone("Asia/Tashkent")
BASE_URL = 'https://api.service.safiabakery.uz/'


@positions_router.post("/positions", response_model=GetPosition)
async def create_appointment(
        data: CreatePosition,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    position = add_position(data=data, db=db)
    return position


@positions_router.get("/positions", response_model=List[GetPosition])
async def get_position_list(
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    positions = get_positions(db=db)
    return positions


@positions_router.get("/positions/{id}", response_model=GetPosition)
async def get_position(
        id: int,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    position = get_positions(db=db, id=id)
    return position


@positions_router.put("/positions", response_model=GetPosition)
async def put_position(
        data: UpdatePosition,
        db: Session = Depends(get_db),
        request_user: UserGetJustNames = Depends(get_current_user)
):
    position = edit_position(db=db, data=data)
    return position
