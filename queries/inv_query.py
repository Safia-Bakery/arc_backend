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


def get_my_orders(db:Session,user_id:int,status):
    query = db.query(models.Requests).filter(models.Requests.user_id == user_id)
    query = query.filter(models.Category.department==2)
    if status is not None:
        if status:
            query = query.filter(models.Requests.status != 0)
        elif not status:
            query = query.filter(models.Requests.status == 0)

    return query.all()


def add_category_tool(db:Session,form_data:inv_schemas.CreateCategoryTool):
    query = models.CategoryTools(category_id=form_data.category_id,tool_id=form_data.tool_id,)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def delete_category_tool(db:Session,form_data:inv_schemas.DeleteCategoryTool):
    query = db.query(models.CategoryTools).filter(models.CategoryTools.category_id == form_data.category_id,models.CategoryTools.tool_id ==form_data.tool_id).delete()
    db.commit()
    return query

def get_category_tools(db:Session,category_id,id):
    query = db.query(models.Tools)
    if id is not None:
        query = query.filter(models.Tools.id == id)
    if category_id is not None:
        query = query.filter(models.Tools.CategoryTools.any(category_id=category_id))
    return query.all()

