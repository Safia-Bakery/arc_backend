from sqlalchemy.orm import Session
from users.schema import schema
from orders.schema import schema_router

import models
import schemas
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import or_, and_, Date, cast, Integer

timezonetash = pytz.timezone("Asia/Tashkent")


def marketing_table(db: Session, timer, created_at, finished_at):
    total = (
        db.query(
            models.Category.sub_id,
            func.count(models.Requests.id).filter(models.Requests.status == 3),
            func.cast(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Requests.finished_at - models.Requests.started_at,
                    )
                ).filter(models.Requests.status == 3)
                / timer,
                Integer,
            ),
            func.count(models.Requests.id).filter(models.Requests.status.in_([0, 1,2])),

        )
        .join(models.Requests)
        .filter(
            models.Category.department == 3,
            models.Requests.created_at.between(created_at, finished_at),
        )
        .group_by(models.Category.sub_id)
        .all()
    )
    dict_data = {}
    for i in total:
        dict_data[i[0]] = [i[1], i[2],i[3]]
    return dict_data


def marketing_pie(db: Session, created_at, finished_at):
    percentages = (
        db.query(
            func.count(models.Requests.id).label("total_count"),
            func.jsonb_build_object(
                "category_sub_id",
                models.Category.sub_id,
                "percent",
                func.cast(
                    func.count(models.Requests.id)
                    * 100.0
                    / func.nullif(func.sum(func.count(models.Requests.id)).over(), 0),
                    Integer,
                ),
            ).label("category_percent"),
        )
        .join(models.Requests)
        .filter(
            models.Requests.status == 3,
            models.Category.department == 3,
            models.Requests.created_at.between(created_at, finished_at),
        )
        .group_by(models.Category.sub_id)
        # .group_by(models.Requests.status)
        .all()
    )

    dict_data = {}
    for i in percentages:
        dict_data[i[1]["category_sub_id"]] = [i[0], i[1]["percent"]]
    return dict_data


def category_percent(db: Session, created_at, finished_at):
    dict_data = {}
    data = (
        db.query(
            models.Category.name,
            func.count(models.Requests.id).label("total_count"),
            func.count(models.Requests.id)
            .filter(models.Requests.status == 3)
            .label("status_3_count"),
            func.cast(
                func.count(models.Requests.id).filter(models.Requests.status == 3)
                * 100.0
                / func.count(models.Requests.id),
                Integer,
            ).label("percent"),
        )
        .join(models.Requests)
        .filter(
            models.Category.department == 3,
            models.Requests.created_at.between(created_at, finished_at),
        )
        .group_by(models.Category.name)
        .all()
    )
    for i in data:
        dict_data[i[0]] = [i[1], i[2], i[3]]
    return dict_data


def category_pie(db: Session, created_at, finished_at):
    total = (
        db.query(
            models.Category.name,
            func.count(models.Requests.id),
            func.cast(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Requests.finished_at - models.Requests.started_at,
                    )
                )
                / 60,
                Integer,
            ),
        )
        .join(models.Requests)
        .filter(
            models.Requests.status == 3,
            models.Category.department == 3,
            models.Requests.created_at.between(created_at, finished_at),
        )
        .group_by(models.Category.name)
        .all()
    )
    dict_data = {}
    for i in total:
        dict_data[i[0]] = [i[1], i[2]]
    return dict_data


def redirect_request(db: Session, form_data: schema_router.RedirectRequest):
    query = db.query(models.Requests).filter(models.Requests.id == form_data.id).first()
    if query:
        query.old_cat_id = query.category_id
        query.category_id = form_data.category_id
        query.is_redirected = True
        db.commit()
        db.refresh(query)
        # update time
        updated_data = query.update_time or {}
        updated_data["redirect_time"] = str(datetime.now(tz=timezonetash))
        query.update_time = updated_data
        db.query(models.Requests).filter(models.Requests.id == form_data.id).update(
            {"update_time": updated_data}
        )
        db.commit()
        return query
    return query


def department_counter(db: Session):
    query = (
        db.query(
            models.Category.department,
            models.Category.sphere_status,
            func.count(models.Requests.id).label("request_count"),
        )
        .filter(models.Requests.status == 0)
        .join(models.Requests, models.Category.id == models.Requests.category_id)
        .group_by(models.Category.department, models.Category.sphere_status)
        .all()
    )
    arrays = []
    for i in query:
        arrays.append(list(i))
    return arrays


def createcat_product(db: Session, name, category_id, status, image, description):
    query = models.Products(
        name=name,
        category_id=category_id,
        status=status,
        image=image,
        description=description,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def updatecat_product(db: Session, id, name, category_id, status, image, description):
    query = db.query(models.Products).filter(models.Products.id == id).first()
    if query:
        if name is not None:
            query.name = name
        if category_id is not None:
            query.category_id = category_id
        if status is not None:
            query.status = status
        if image is not None:
            query.image = image
        if description is not None:
            query.description = description

        db.commit()
        db.refresh(query)
    return query


def querycat_product(db: Session, id, name, category_id):
    query = db.query(models.Products)
    if id is not None:
        query = query.filter(models.Products.id == id)
    if name is not None:
        query = query.filter(models.Products.name.ilike(f"%{name}%"))
    if category_id is not None:
        query = query.filter(models.Products.category_id == category_id)
    return query.all()


def add_product_request(db: Session, request_id, product_id, amount):
    query = models.OrderProducts(
        request_id=request_id, product_id=product_id, amount=amount
    )
    db.add(query)
    db.commit()
    return True


def cars_add(db: Session, name, status, number):
    query = models.Cars(name=name, status=status, number=number)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def cars_update(db: Session, id, name, status, number):
    query = db.query(models.Cars).filter(models.Cars.id == id).first()
    if query:
        if name is not None:
            query.name = name
        if status is not None:
            query.status = status
        if number is not None:
            query.number = number
        db.commit()
        db.refresh(query)
    return query

def cars_query(db: Session, id, name, status, number):
    query = db.query(models.Cars)
    if id is not None:
        query = query.filter(models.Cars.id == id)
    if name is not None:
        query = query.filter(models.Cars.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(models.Cars.status == status)
    if number is not None:
        query = query.filter(models.Cars.number.ilike(f"%{number}%"))
    return query.all()


def add_expenditure(db: Session, request_id, amount, comment, tool_id,status):
    query = models.Expanditure(request_id=request_id, amount=amount, comment=comment, tool_id=tool_id,status=status)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_expenditure(db:Session,form_data:schema_router.UpdateExpenditure):
    query = db.query(models.Expanditure).filter(models.Expanditure.id == form_data.id).first()
    if query:
        if form_data.amount is not None:
            query.amount = form_data.amount
        if form_data.comment is not None:
            query.comment = form_data.comment
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
    return query


def message_create(db:Session,message,request_id,status,photo,user_id):
    query= models.Communication(request_id=request_id,message=message,status=status,user_id=user_id,photo=photo)
    db.add(query)
    db.commit()
    return query


def get_fillials_unordered(db:Session):
    current_time = datetime.now(tz=timezonetash).date()
    query = db.query(models.Fillials).join(models.Requests).join(models.Category).filter(cast(models.Requests.created_at, Date) == current_time).filter(models.Category.department==6).all()
    data = [ i.parentfillial_id for i in query]
    query = (db.query(models.ParentFillials).
             join(models.Fillials).
             filter(models.ParentFillials.id.notin_(data)).
             filter(or_(models.Fillials.origin==1,models.Fillials.origin==2))
             .all())
    return query



def update_finishing_time(db:Session,request_id,finishing_time):
    query = db.query(models.Requests).filter(models.Requests.id==request_id).update({models.Requests.finishing_time:finishing_time})
    db.commit()
    return True
