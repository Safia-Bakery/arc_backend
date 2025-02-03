from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.requests import Requests
from app.models.managers import Managers
from app.models.fillials import Fillials

timezone_tash = pytz.timezone('Asia/Tashkent')




def get_managers(db:Session,name):
    query = db.query(Managers)
    if name is not None:
        query.filter(Managers.name.ilike(f"%{name}%"))
    return query.all()


def get_one_manager(db:Session,id):
    query = db.query(Managers).filter(Managers.id==id).first()
    return query


def get_manager_divisions(db:Session,manager_id):
    query = db.query(Fillials).filter(Fillials.manager_id==manager_id).all()
    return query

