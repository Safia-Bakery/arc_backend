from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.calendars import Calendars
from app.schemas.calendars import GetCalendars,CreateCalendars,UpdateCalendars


def create_calendar(db:Session,form_data:CreateCalendars):
    query = Calendars(is_active=form_data.is_active,
                      date=form_data.date,
                      branch_id=form_data.branch_id,
                      )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_calendar(db:Session,form_data:UpdateCalendars):
    query = db.query(Calendars).filter(Calendars.id == form_data.id).first()
    if query:
        if form_data.is_active is not None:
            query.is_active = form_data.is_active
        if form_data.date is not None:
            query.date = form_data.date
        if form_data.branch_id is not None:
            query.branch_id = form_data.branch_id
    db.commit()
    db.refresh(query)
    return query

def get_calendars(db:Session,id:Optional[int]=None,current_date:Optional[datetime]=None):
    query = db.query(Calendars).filter(Calendars.is_active == 1)
    if id is not None:
        query = query.filter(Calendars.id == id)
    if current_date is not None:
        query = query.filter(Calendars.date == current_date)
    return query.order_by(Calendars.created_at.desc()).all()

def get_one_calendar(db:Session,id:int):
    query = db.query(Calendars).filter(Calendars.id==id).first()
    return query

def delete_calendar(db:Session,id:int):
    query = db.query(Calendars).filter(Calendars.id==id).first()
    if query:
        query.is_active = 0
    db.commit()
    return query