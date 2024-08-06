from sqlalchemy.orm import Session
from users.schema import schema
import models
import schemas
from typing import Optional
import bcrypt
from microservices import find_hierarchy
from Variables import role_ids
import pytz
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import or_, and_, Date, cast
from datetime import datetime,timedelta
from allschemas import inv_schemas






def delete_tool(db:Session,id):
    query = db.query(models.Tools).filter(models.Tools.id == id).delete()
    db.commit()
    return query


def get_my_orders(db:Session,user_id:int,status,from_date,to_date):
    query = db.query(models.Requests).filter(models.Requests.user_id == user_id,models.Requests.category.has(models.Category.department == 2))

    if status is not None:
        if status:
            query = query.filter(models.Requests.status.in_([3,4,5,6,7,8,9]))
        elif not status:
            query = query.filter(models.Requests.status.in_([0,1,2]))
    if from_date is not None and to_date is not None:
        query = query.filter(and_(models.Requests.created_at >= from_date,models.Requests.created_at <= to_date+timedelta(days=1)))



    return query.order_by(models.Requests.created_at.desc()).all()


def add_category_tool(db:Session,form_data:inv_schemas.CreateCategoryTool):
    query = db.query(models.Tools).filter(models.Tools.id == form_data.tool_id).first()
    if query:
        query.category_id = form_data.category_id
        db.commit()
        db.refresh(query)

    return query


def delete_category_tool(db:Session,form_data:inv_schemas.DeleteCategoryTool):
    query = db.query(models.Tools).filter(models.Tools.id == form_data.tool_id).first()
    if query:
        query.category_id = None
        db.commit()
        db.refresh(query)
    return query

def get_category_tools(db:Session,category_id,id,name):
    query = db.query(models.Tools)
    if id is not None:
        query = query.filter(models.Tools.id == id)
    if category_id is not None:
        query = query.filter(models.Tools.category_id==category_id)
    if name is not None:
        query = query.filter(models.Tools.name.ilike(f"%{name}%"))
    return query.all()

