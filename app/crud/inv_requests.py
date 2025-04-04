import re
from datetime import datetime
from typing import Optional

import pytz
from sqlalchemy import Date, cast, and_, or_
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.fillials import Fillials
from app.models.requests import Requests
from app.models.users_model import Users
from app.schemas.inventory_requests import CreateInventoryRequest, UpdateRequest
from app.models.expanditure import Expanditure
from app.models.tools import Tools
from app.models.fillials import Fillials

timezonetash = pytz.timezone("Asia/Tashkent")


def filter_requests_all(
        db: Session,
        id,
        user,
        fillial_id,
        created_at,
        request_status,
        department,
        product_name
):
    # Start with the base query for the Requests table
    query = db.query(Requests).join(Requests.category).join(Requests.user).join(Requests.fillial)
    query = query.filter(Requests.status.isnot(None))
    # Apply the department filter if provided
    if department is not None:
        query = query.filter(Category.department == department)

    # Apply the other filters if provided
    if id is not None:
        query = query.filter(Requests.id == id)
    if fillial_id is not None:
        query = query.filter(Fillials.parentfillial_id == fillial_id)  # Directly filter based on `fillial_id`
    if created_at is not None:
        query = query.filter(cast(Requests.created_at, Date) == created_at)
    if request_status is not None:
        request_status = [int(i) for i in re.findall(r"\d+", str(request_status))]
        query = query.filter(
            Requests.status.in_(request_status)
        )
    if user is not None:
        query = query.filter(Users.full_name.ilike(f"%{user}%"))
    if product_name is not None:
        query = query.join(Requests.expanditure).join(Expanditure.tool)
        query = query.filter(Tools.name.ilike(f"%{product_name}%"))

    # Order by request ID and execute the query
    results = query.order_by(Requests.id.desc()).all()

    # Debug: Log the number of results

    return results


def get_request_id(db: Session, id):
    return db.query(Requests).filter(Requests.id == id).first()



def create_request(db: Session, request: CreateInventoryRequest, user_id, status):
    query = Requests(
        user_id=user_id,
        fillial_id=request.fillial_id,
        status=status,
        description=request.description,
        product=request.product,
        category_id=request.category_id,
        phone_number=request.phone_number
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


def update_request_status(db: Session, request_id, status):
    query = db.query(Requests).filter(Requests.id == request_id).first()
    now = datetime.now(tz=timezonetash)
    query.status = status
    if status == 1:
        query.started_at = now
    elif status in [3, 4, 6, 8]:
        query.finished_at = now

    db.commit()
    return query