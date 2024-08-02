
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
    name_generator,
    file_generator,
    get_db,get_current_user
)
from allschemas import inv_schemas
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



@inv_router.post('/v1/image/upload', tags=["ARC"], status_code=status.HTTP_200_OK)
async def upload_image(file: UploadFile = File(...),db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    folder_name = f"files/{name_generator() + file.filename}"
    with open(folder_name, "wb") as buffer:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            buffer.write(chunk)
    file = folder_name

    return {"file_path":file}



@inv_router.get('/v1/my/orders', tags=["INV"], status_code=status.HTTP_200_OK, response_model=Page[schemas.GetRequestid])
def my_orders(status:Optional[bool]=None,
              db: Session = Depends(get_db),
              request_user: schema.UserFullBack = Depends(get_current_user)):
    return paginate(inv_query.get_my_orders(db=db,user_id=request_user.id,status=status))


@inv_router.post('/v1/category/tools', tags=["INV"], status_code=status.HTTP_200_OK)
def add_category_tools(form_data: inv_schemas.CreateCategoryTool, db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    return inv_query.add_category_tool(db=db,form_data=form_data)

@inv_router.delete('/v1/category/tools', tags=["INV"], status_code=status.HTTP_200_OK)
def delete_category_tools(form_data:inv_schemas.DeleteCategoryTool, db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = inv_query.delete_category_tool(db=db,form_data=form_data)
    return  {'success': True}


@inv_router.get('/v1/category/tools', tags=["INV"], status_code=status.HTTP_200_OK,response_model=Page[schemas.ToolsSearch])
def get_category_tools(id: Optional[int] = None,category_id:Optional[int]=None, db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    return paginate(inv_query.get_category_tools(db=db,id=id,category_id=category_id))


