from datetime import date
from datetime import datetime
from typing import Optional
import pytz
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.crud import calendars as calendar_crud
from app.crud.arc_requests import create_arc_auto_reqeust
from app.routes.depth import get_db, get_current_user
from app.schemas import calendars as calendar_sch
from app.crud.departments import get_child_branch
from app.utils.utils import send_inlinekeyboard_text
from app.core.config import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

auto_request_user_id = 9
auto_request_category_id=21



calendar_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')




def arc_auto_request(db:Session):
    # Create a new session each time the job is triggered
    current_date = datetime.now(tz=timezone_tash).date()
    calendars_list = calendar_crud.current_date_calendars(db=db, current_date=current_date)

    current_datetime = datetime.now(tz=timezone_tash).strftime('%Y-%m-%d %H:%M:%S')
    print(calendars_list)
    for item in calendars_list:
        print(item)
        branch_id = get_child_branch(db=db, id=item.branch_id).id
        request_create = create_arc_auto_reqeust(
            db=db,
            branch_id=branch_id,
            category_id=auto_request_category_id,
            user_id=auto_request_user_id,
            description="Автоматическое создание заявки",
            update_time={'0': current_datetime}
        )

        calendar_crud.update_calendar_request_id(db=db, calendar_id=item.id, request_id=request_create.id)

        text = f"📑Заявка № {request_create.id}\n\n📍Филиал: {request_create.fillial.parentfillial.name}\n" \
               f"🕘Дата поступления заявки: {current_datetime}\n\n" \
               f"🔰Категория проблемы: {request_create.category.name}\n" \
               f"⚙️Название оборудования: {request_create.product}\n" \
               f"💬Комментарии: {request_create.description}"
        print(request_create.id)
        send_inlinekeyboard_text(bot_token=settings.BOT_TOKEN,
                                 chat_id=-1001920671327,
                                 message_text=text)


@calendar_router.on_event('startup')
def startup_event():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=18, minute=56, second=0,
                          timezone=timezone_tash)  # Set the desired time for the function to run (here, 12:10 PM)

    # Check if the job already exists
    scheduler.add_job(arc_auto_request, trigger=trigger, args=[next(get_db())])


    scheduler.start()




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
def get_calendar(current_date:date,
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

