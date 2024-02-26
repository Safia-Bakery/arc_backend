
# ----------import packages
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
import pytz
import schemas
from typing import Annotated
import models
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from database import engine, SessionLocal
from fastapi_pagination import paginate, Page
from users.schema import schema
from microservices import (
    checkpermissions,
    getgroups,
    getproducts,
    list_stores,
    get_suppliers,
    send_document_iiko,
    howmuchleft,
    find_hierarchy,
    get_prices,
    file_generator,
    get_db,get_current_user
)
from fastapi import APIRouter
from queries import inv_query
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

timezonetash = pytz.timezone("Asia/Tashkent")

inv_router = APIRouter()

#def 
#
#@inv_query.on_event("startup")
#def startup_event():
#    scheduler = BackgroundScheduler()
#    trigger  = CronTrigger(hour=1, minute=20, second=00,timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
#    scheduler.add_job(scheduled_function, trigger=trigger, args=[next(get_db())])
#    scheduler.start()


@inv_router.delete("/tools", tags=["Tools"], status_code=status.HTTP_200_OK)
def delete_tool(id: int, db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = inv_query.delete_tool(db=db, id=id)
    return  {'success': True}
