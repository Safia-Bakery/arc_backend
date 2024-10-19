from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast,String,extract
from uuid import UUID

from app.models.fillials import Fillials
from app.models.parentfillials import ParentFillials


def get_child_branch(db:Session,id:int):
    query = db.query(Fillials).filter(Fillials.parentfillial_id==id).first()
    return query


def get_all_departments(db: Session):
    query = db.query(ParentFillials).all()
    return query