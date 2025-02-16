from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.requests import Requests
from app.models.parentfillials import ParentFillials
from app.models.fillials import Fillials
from app.models.files import Files

timezone_tash = pytz.timezone('Asia/Tashkent')


def get_branchs(db:Session,id:Optional[int]=None,branch_name:Optional[str]=None):
    query = db.query(ParentFillials)
    if id is not None:
        query = query.filter(ParentFillials.id == id)
    if branch_name is not None:
        query = query.filter(ParentFillials.name.ilike(f'%{branch_name}%'))
    return query.all()


def get_child_branchs(db:Session,parent_fillial):
    query = db.query(Fillials).filter(Fillials.parentfillial_id==parent_fillial)
    return query.first()



