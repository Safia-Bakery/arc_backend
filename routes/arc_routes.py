
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
from fastapi import APIRouter
from queries import arc_query
from allschemas import arc_schema


arc_routes = APIRouter()



@arc_routes.get('/v1/arc/stats', tags=["ARC"], status_code=status.HTTP_200_OK)
def get_stats(started_at:Optional[date]=None,finished_at:Optional[date]=None,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = arc_query.stats_query(db=db,started_at=started_at,finished_at=finished_at)
    return query


@arc_routes.post('/v1/expense/type', tags=["ARC"], status_code=status.HTTP_200_OK)
def create_expense_type(form_data:arc_schema.CreateExpensetype,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = arc_query.create_expense_type(db=db,form_data=form_data)
    return query

@arc_routes.get('/v1/expense/type', tags=["ARC"], status_code=status.HTTP_200_OK)
def get_expense_type(name:Optional[str]=None,status:Optional[int]=None,id:Optional[int]=None,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = arc_query.get_expense_type(db=db,name=name,status=status,id=id)
    return query


@arc_routes.post('/v1/expense', tags=["ARC"], status_code=status.HTTP_200_OK)
def create_expense(form_data:arc_schema.CreateExpense,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = arc_query.create_expense(db=db,form_data=form_data,user_id=request_user.id)
    return query

@arc_routes.get('/v1/expense',response_model=Page[arc_schema.GetExpenses], tags=["ARC"], status_code=status.HTTP_200_OK)
def get_expense(amount:Optional[float]=None,description:Optional[str]=None,expensetype_id:Optional[int]=None,status:Optional[int]=None,id:Optional[int]=None,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = arc_query.get_expense(db=db,amount=amount,description=description,expensetype_id=expensetype_id,status=status,id=id)
    return paginate(query)

@arc_routes.put('/v1/expense', tags=["ARC"], status_code=status.HTTP_200_OK)
def update_expense(form_data:arc_schema.UpdateExpense,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = arc_query.update_expense(db=db,form_data=form_data)
    return query






