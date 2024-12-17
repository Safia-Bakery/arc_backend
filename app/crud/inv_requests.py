import re
from datetime import datetime
import pytz
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.fillials import Fillials
from app.models.requests import Requests
from app.models.users_model import Users
from app.schemas.inventory_requests import CreateInventoryRequest, UpdateRequest

timezonetash = pytz.timezone("Asia/Tashkent")


def filter_requests_all(
        db: Session,
        id,
        user,
        fillial_id,
        created_at,
        request_status,
        department
):
    query = db.query(Requests).join(Category).filter(Category.department == department)


    if id is not None:
        query = query.filter(Requests.id == id)
    if fillial_id is not None:
        query = query.outerjoin(Fillials).filter(Fillials.parentfillial_id == fillial_id)
    if created_at is not None:
        query = query.filter(cast(Requests.created_at, Date) == created_at)
    if request_status is not None:
        request_status = [int(i) for i in re.findall(r"\d+", str(request_status))]
        query = query.filter(Requests.status.in_(request_status))
    if user is not None:
        query = query.filter(Users.full_name.ilike(f"%{user}%"))

    results = query.order_by(Requests.id.desc()).all()
    return results


def get_request_id(db: Session, id):
    return db.query(Requests).filter(Requests.id == id).first()



def create_request(db: Session, request: CreateInventoryRequest,user_id):
    query = Requests(
        user_id=user_id,
        fillial_id=request.fillial_id,
        status=0,
        description=request.description,
        product=request.product,
        category_id=request.category_id,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_auto_request(db:Session,user_id,fillial_id,description,product,category_id):
    query = Requests(
        user_id=user_id,
        fillial_id=fillial_id,
        status=0,
        description=description,
        product=product,
        category_id=category_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def update_request(db: Session, request: UpdateRequest):
    query = db.query(Requests).filter(Requests.id == request.id).first()
    now = datetime.now(tz=timezonetash)
    if request.status is not None:
        query.status = request.status
    if request.deny_reason is not None:
        query.deny_reason = request.deny_reason
    if request.status == 1:
        query.started_at = now
    elif request.status in [3, 4, 6, 8]:
        query.finished_at = now

    db.commit()
    return query
