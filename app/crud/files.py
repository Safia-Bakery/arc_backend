from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.requests import Requests
from app.models.files import Files

timezone_tash = pytz.timezone('Asia/Tashkent')


def create_file_tasks(db:Session,url:str,kru_finished_task_id:int):
    query = Files(url=url,kru_finished_task_id=kru_finished_task_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_files_report(db:Session, url: str, request_id: Optional[int]):
    query = Files(url=url,request_id=request_id)
    db.add(query)
    db.commit()
    return query


def create_appointment_files(db:Session, file_url, appointment_id):
    query = Files(url=file_url, appointment_id=appointment_id)
    db.add(query)
    db.commit()
    return query

