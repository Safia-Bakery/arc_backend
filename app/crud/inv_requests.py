from sqlalchemy.orm import Session,joinedload
from sqlalchemy import or_, and_, Date, cast
import re
from uuid import UUID
from sqlalchemy.sql import func

import models
from app.models.requests import Requests
from app.models.category import Category
from app.models.users_model import Users
from app.models.products import Products
from app.models.orderproducts import OrderProducts
from app.models.comments import Comments
from app.models.fillials import Fillials
from app.schemas.inventory_requests import CreateInventoryRequest,UpdateRequest



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




def update_request(db: Session, request: UpdateRequest):
    query = db.query(Requests).filter(Requests.id == request.id).first()
    if request.status is not None:
        query.status = request.status

    if request.deny_reason is not None:
        query.deny_reason = request.deny_reason

    db.commit()
    return query
