from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.requests import Requests

timezone_tash = pytz.timezone('Asia/Tashkent')


def get_request_by_id(db:Session,request_id):
    query = db.query(Requests).filter(Requests.id==request_id).first()
    return query




def update_status_request(db:Session,id,status):
    query = db.query(Requests).filter(Requests.id == id).first()
    query.status = status
    update_time = dict(query.update_time)
    update_time[str(status)] = datetime.now(timezone_tash).isoformat()
    query.update_time = update_time
    db.commit()
    return query


def get_requests_by_status(db: Session, status):
    one_day_before = datetime.now(timezone_tash) - timedelta(days=1)
    query = db.query(Requests).filter(Requests.status == status).filter(Requests.finished_at <= one_day_before).all()
    return query






