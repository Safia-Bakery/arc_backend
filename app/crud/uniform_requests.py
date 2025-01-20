import re
from datetime import datetime
from typing import Optional
import pytz
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.parentfillials import ParentFillials
from app.models.category import Category
from app.models.requests import Requests
from app.models.fillials import Fillials
from app.models.orderproducts import OrderProducts
from app.schemas.uniform_requests import UpdateRequest, CreateRequest

timezonetash = pytz.timezone("Asia/Tashkent")


def get_request(db: Session, id):
    return db.query(Requests).filter(Requests.id == id).first()


def filtered_requests(
        db: Session,
        id,
        fillial_id,
        created_at,
        request_status
):
    query = db.query(Requests).join(Category).filter(Category.department == 9)

    if id is not None:
        query = query.filter(Requests.id == id)
    if fillial_id is not None:
        query = query.join(Fillials).filter(Fillials.parentfillial_id == fillial_id)
    if created_at is not None:
        query = query.filter(Requests.created_at == created_at)
    if request_status is not None:
        request_status = [int(i) for i in re.findall(r"\d+", str(request_status))]
        query = query.filter(Requests.status.in_(request_status))
    # if created_at is not None and finished_at is not None:
    #     query = query.filter(Requests.created_at.between(created_at, finished_at))

    return query.order_by(Requests.id.desc()).all()


def edit_request(db: Session, user_manager, data: Optional[UpdateRequest] = None):
    request_obj = db.query(Requests).filter(Requests.id == data.id).first()
    request_obj.user_manager = user_manager
    if data.status is not None:
        now = datetime.now(tz=timezonetash)
        request_obj.status = data.status
        updated_data = request_obj.update_time or {}
        updated_data[str(data.status)] = str(now)
        if data.status == 1:
            request_obj.started_at = now
        elif data.status in [3, 4, 6]:
            request_obj.finished_at = now

        db.query(Requests).filter(Requests.id == request_obj.id).update({"update_time": updated_data})

    if data.deny_reason is not None:
        request_obj.deny_reason = data.deny_reason
    total_price =0

    if data.request_products is not None:
        request_products_obj = db.query(OrderProducts).filter(OrderProducts.request_id == request_obj.id).all()
        for i in range(len(request_products_obj)):
            if  data.request_products[i].confirmed:
                total_price = total_price + (request_products_obj[i].amount * request_products_obj[i].orpr_product.prod_cat.price)
            request_products_obj[i].confirmed = data.request_products[i].confirmed
            request_products_obj[i].deny_reason = data.request_products[i].deny_reason

    request_obj.price= total_price

    db.commit()
    db.refresh(request_obj)
    return request_obj


def getparentfillial(db: Session, id):
    query = db.query(ParentFillials).filter(ParentFillials.id == id).first()
    return query


def filterbranchchildid(db: Session, parent_id, origin: Optional[int] = None):
    query = db.query(Fillials).filter(
        Fillials.status == 1, Fillials.parentfillial_id == parent_id
    )
    if origin:
        query = query.filter(Fillials.origin == origin)

    return query.first()


def add_uniform_product(db: Session, product_id, amount, request_id):
    query = OrderProducts(product_id=product_id, amount=amount, request_id=request_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def add_request(
        db: Session,
        user,
        data: Optional[CreateRequest] = None
):
    parent_fillial = getparentfillial(db, data.fillial_id)
    if parent_fillial:
        if parent_fillial.is_fabrica == 1:
            fillial_id = parent_fillial.id
            sklad_id = fillial_id
        else:
            filliald_id = filterbranchchildid(db, data.fillial_id, origin=None)
            sklad_id = filliald_id.id
    else:
        sklad_id = data.fillial_id

    now = datetime.now(tz=timezonetash)
    update_time = {"0": str(now)}
    try:
        request = Requests(
            fillial_id=sklad_id,
            category_id=data.request_products[0].category_id,
            update_time=update_time,
            user_id=user.id
        )
        db.add(request)
        db.flush()

        for item in data.request_products:
            request_product = OrderProducts(
                product_id=item.product_id,
                amount=item.amount,
                request_id=request.id
            )
            db.add(request_product)
            db.flush()

        db.commit()

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None

    db.refresh(request)
    return request
