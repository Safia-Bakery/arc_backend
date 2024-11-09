import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.crud.tool_balance import create_update_tool_balance
from app.routes.depth import get_db
from app.utils.iiko_microservice import ApiRoutes
from datetime import datetime
from app.crud.departments import get_all_departments


tool_balance_cron_router = APIRouter()

timezonetash = pytz.timezone('Asia/Tashkent')


def product_balance_job(db: Session):
    api_route = ApiRoutes()
    department_list = get_all_departments(db=db)
    for department in department_list:
        product_balance_list = api_route.get_tool_balance(department.id)
        create_update_tool_balance(db, product_balance_list, department.id)
    del product_balance_list
    del department_list

    return True


@tool_balance_cron_router.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=16, minute=00, second=00, timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(product_balance_job, trigger=trigger, args=[next(get_db())])
    scheduler.start()

