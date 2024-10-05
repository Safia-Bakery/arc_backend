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
from app.schemas.kru_users import CreateUser,UpdateUser



def get_by_telegram_id(db:Session,telegram_id:int):
    query = db.query(Users).filter(Users.telegram_id==telegram_id).first()
    return query


def create_user(db:Session,form_data:CreateUser):
    query = Users(
        telegram_id=form_data.telegram_id,
        username=form_data.username,
        full_name=form_data.full_name,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_user(db:Session,form_data:UpdateUser):
    query = db.query(Users).filter(Users.telegram_id==form_data.telegram_id).first()
    if form_data.branch_id is not None:
        query.branch_id = form_data.branch_id
    if form_data.full_name is not None:
        query.full_name = form_data.full_name




    db.commit()
    db.refresh(query)
    return query

