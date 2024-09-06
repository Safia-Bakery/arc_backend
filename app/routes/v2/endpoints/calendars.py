from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Header,
    Request,
    status,
)

from app.schemas import calendars as calendar_sch
from app.crud import calendars as calendar_crud
from app.routes.depth import get_db, get_current_user



calendar_router = APIRouter()



@calendar_router.post('/calendar',response_model=calendar_sch.GetCalendars)
def create_calendar(form_data:calendar_sch.CreateCalendars,
                   db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    return calendar_crud.create_calendar(db,form_data)


@calendar_router.put('/calendar',response_model=calendar_sch.GetCalendars)
def update_calendar(form_data:calendar_sch.UpdateCalendars,
                   db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    return calendar_crud.update_calendar(db,form_data)


@calendar_router.get('/calendar',response_model=list[calendar_sch.GetCalendars])
def get_calendar(current_date:datetime,
        id:Optional[int]=None,
                db: Session = Depends(get_db),
                current_user = Depends(get_current_user)):

    return calendar_crud.get_calendars(db=db,id=id,current_date=current_date)



@calendar_router.get("/calendar/{id}",response_model=calendar_sch.GetCalendars)
def get_one_calendar(id:int,
                    db:Session = Depends(get_db),
                    current_user = Depends(get_current_user)):
    return  calendar_crud.get_one_calendar(db=db,id=id)



@calendar_router.delete("/calendar/{id}",response_model=calendar_sch.GetCalendars)
def delete_calendar(id:int,
                    db:Session = Depends(get_db),
                    current_user = Depends(get_current_user)):
    return  calendar_crud.delete_calendar(db=db,id=id)

