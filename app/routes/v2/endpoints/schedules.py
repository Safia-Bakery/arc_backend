from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.schedules import get_all_actual_schedules, add_schedule, edit_schedule, delete_schedule, get_one_schedule
from app.routes.depth import get_db
from app.schemas.schedules import GetSchedule, CreateSchedule, UpdateSchedule



schedules_router = APIRouter()



@schedules_router.get('/schedules', response_model=List[GetSchedule])
async def get_schedules(
        db: Session = Depends(get_db)
):
    schedules = get_all_actual_schedules(db=db)
    return schedules


@schedules_router.get('/schedules/{id}', response_model=GetSchedule)
async def get_schedule(
        id: int,
        db: Session = Depends(get_db)
):
    schedule = get_one_schedule(db=db, id=id)
    return schedule


@schedules_router.post('/schedules', response_model=GetSchedule)
async def create_schedules(
        body: CreateSchedule,
        db: Session = Depends(get_db)
):
    created_schedule = add_schedule(db=db, data=body)
    if created_schedule is None:
        raise HTTPException(status_code=400, detail='На данной дате назначена встреча !')

    return created_schedule


@schedules_router.put('/schedules', response_model=GetSchedule)
async def update_schedules(
        body: UpdateSchedule,
        db: Session = Depends(get_db)
):
    edited_schedule = edit_schedule(db=db, data=body)
    return edited_schedule


@schedules_router.delete('/schedules/{id}')
async def delete_schedules(
        id: int,
        db: Session = Depends(get_db)
):
    deleted_schedule = delete_schedule(db=db, id=id)
    return deleted_schedule
