from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.utils.utils import generate_random_string
from app.models.users_model import Users
from app.models.kru_categories import KruCategories
from app.schemas.kru_categories import KruCategoriesCreate,KruCategoriesUpdate,KruCategoriesGet


def create_kru_category(db:Session,form_data:KruCategoriesCreate):
    query = KruCategories(
        name=form_data.name,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_kru_categories(db:Session,id:Optional[int]=None,name:Optional[str]=None):
    query = db.query(KruCategories).filter(KruCategories.status==1)
    if id is not None:
        query = query.filter(KruCategories.id == id)
    if name is not None:
        query = query.filter(KruCategories.name.ilike(f'%{name}%'))
    return query.all()


def get_one_kru_category(db:Session,id):
    query = db.query(KruCategories).filter(KruCategories.id==id).first()
    return query


def update_kru_category(db:Session,form_data:KruCategoriesUpdate):
    query = db.query(KruCategories).filter(KruCategories.id==form_data.id).first()
    if form_data.name is not None:
        query.name = form_data.name
    db.commit()
    db.refresh(query)
    return query

def delete_kru_category(db:Session,id:int):
    query = db.query(KruCategories).filter(KruCategories.id==id).first()
    if query is not None:
        query.status = 0
        db.commit()
    return query







