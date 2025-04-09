import re

from unicodedata import category

from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast,String,extract
from uuid import UUID


from app.models.category import Category
from app.schemas.arc_factory_requests import GetArcFactoryRequests, UpdateArcFactoryRequests, GenerateExcell

from app.models.requests import Requests
from app.models.users_model import Users
from crud import timezonetash

timezonetash = pytz.timezone('Asia/Tashkent')


def get_arc_factory_requests(
        db:Session,
        user_id,
        fillial_id,
        status,
        id,
        brigada_id,
        user_name,
        created_at,
        category_id,
        request_ids: Optional[list[int]] = None,
):
    query = db.query(Requests).join(Category).join(Users).filter(Category.department==1,Category.sphere_status==2)
    if user_id is not None:
        query = query.filter(Requests.user_id==user_id)
    if status is not None:
        query = query.filter(Requests.status==status)
    if fillial_id is not None:
        query = query.filter(Requests.fillial_id==fillial_id)
    if id is not None:
        query = query.filter(Requests.id==id)
    if brigada_id is not None:
        query = query.filter(Requests.brigada_id==brigada_id)
    if user_name is not None:
        query = query.filter(Users.full_name.ilike(f"%{user_name}%"))
    if created_at is not None:
        query = query.filter(cast(Requests.created_at, Date) == created_at)
    if category_id is not None:
        query = query.filter(Requests.category_id==category_id)

    if request_ids is not None:
        request_ids = [int(i) for i in re.findall(r"\d+", str(request_ids))]
        query = query.filter(Requests.id.in_(request_ids))

    return query.order_by(Requests.created_at.desc()).all()


def get_arc_factory_request(db:Session,request_id):
    return db.query(Requests).filter(Requests.id==request_id).first()


def update_arc_factory_request(db:Session,request_id,request:UpdateArcFactoryRequests):
    query = db.query(Requests).filter(Requests.id==request_id).first()
    query.status = request.status
    now = datetime.now(tz=timezonetash)
    if request.status == 1:
        query.started_at = now
    elif request.status == 6:
        query.finished_at = now
    query.brigada_id = request.brigada_id
    query.deny_reason = request.deny_reason
    query.category_id = request.category_id
    updated_data = query.update_time or {}
    updated_data[str(request.status)] = str(datetime.now(tz=timezonetash))
    query.update_time = updated_data
    db.commit()
    db.refresh(query)
    return query


def get_arc_excell(db:Session, form_data: GenerateExcell):
    finish_date = form_data.finish_date + timedelta(days=1)
    query = db.query(Requests).join(Category).filter(
        and_(Category.department == 1, Category.sphere_status==2)
    ).filter(Requests.created_at.between(form_data.start_date,finish_date))
    if form_data.status is not None:
        query = query.filter(Requests.status.in_(form_data.status))
    if form_data.category_id is not None:
        query = query.filter(Requests.category_id.in_(form_data.category_id))

    return query.order_by(Requests.id.desc()).all()


