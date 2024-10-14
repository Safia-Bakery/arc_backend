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


def filter_request_brigada(
    db: Session,
    id,
    category_id,
    brigada_id,
    fillial_id,
    created_at,
    request_status,
    user,
    sphere_status,
    arrival_date,
    rate,
    urgent,
    started_at,
    finished_at
):
    query = db.query(Requests).join(Category)
    query.options(
        joinedload(Requests.request_orpr)
        .joinedload(OrderProducts.orpr_product)
        .joinedload(Products.prod_cat)
    )

    if id is not None:
        query = query.filter(Requests.id == id)
    if fillial_id is not None:
        query = query.filter(Fillials.parentfillial_id == fillial_id)
    if category_id is not None:
        query = query.filter(Requests.category_id.in_(category_id))
    if created_at is not None:
        query = query.filter(Requests.created_at == created_at)
    if request_status is not None:
        request_status = [int(i) for i in re.findall(r"\d+", str(request_status))]
        query = query.filter(Requests.status.in_(request_status))
    if user is not None:
        query = query.filter(Users.full_name.ilike(f"%{user}/%"))
    if sphere_status is not None:
        query = query.filter(Category.sphere_status == sphere_status)
    if arrival_date is not None:
        query = query.filter(cast(Requests.arrival_date, Date) == arrival_date)
    if rate ==True:
        query = query.filter(Requests.id==Comments.request_id)
    if urgent is not None:
        query = query.filter(Category.urgent == urgent)
    if started_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(started_at,finished_at))
    if created_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(created_at,finished_at))
    #if reopened is not None:
    #    query = query.filter(func.jsonb_object_keys(models.Requests.update_time) == '7')
    query = query.filter(Requests.brigada_id == brigada_id)
    return query.order_by(Requests.id.desc()).all()


def filter_requests_all(
    db: Session,
    id,
    category_id,
    fillial_id,
    created_at,
    request_status,
    user,
    arrival_date,
    rate,
    brigada_id,
    urgent,
    started_at,
    finished_at
):
    categories = db.query(Category).with_entities(Category.id).filter(Category.department == 4).all()
    query = db.query(Requests).filter(Requests.category_id.in_(categories))

    query.options(
        joinedload(Requests.request_orpr)
        .joinedload(OrderProducts.orpr_product)
        .joinedload(Products.prod_cat)
    )

    if id is not None:
        query = query.filter(Requests.id == id)
    if fillial_id is not None:
        query = query.outerjoin(Fillials).filter(Fillials.parentfillial_id == fillial_id)
    if category_id is not None:
        query = query.filter(Requests.category_id.in_(category_id))
    if created_at is not None and finished_at is None:
        query = query.filter(cast(Requests.created_at, Date) == created_at)
    if request_status is not None:
        request_status = [int(i) for i in re.findall(r"\d+", str(request_status))]
        query = query.filter(Requests.status.in_(request_status))
    if user is not None:
        query = query.filter(Users.full_name.ilike(f"%{user}%"))
    if arrival_date is not None:
        query = query.filter(cast(Requests.arrival_date, Date) == arrival_date)
    if rate ==True:
        query = query.filter(Requests.id==Comments.request_id)
    if brigada_id is not None:
        query = query.filter(Requests.brigada_id == brigada_id)
    if urgent is not None:
        query = query.filter(Category.urgent == urgent)
    if started_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(started_at,finished_at))
    if created_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(created_at,finished_at))

    results = query.order_by(Requests.id.desc()).all()
    return results


def get_request_id(db: Session, id):
    return db.query(models.Requests).filter(Requests.id == id).first()
