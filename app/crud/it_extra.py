from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
from microservices import find_hierarchy
from Variables import role_ids
import pytz
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import or_, and_, Date, cast,between,Integer
from datetime import datetime, timedelta
from app.schemas import it_extra
from app.models.requests import Requests
from app.models.category import Category
from app.models.telegrams import Telegrams


def get_it_excell(db: Session, form_data: it_extra.GenerateExcel):
    finish_date = form_data.finish_date + timedelta(days=1)
    query = db.query(Requests).join(Category).filter(Category.department == 4).filter(
        Requests.created_at.between(form_data.start_date,finish_date)
    )
    if form_data.status:
        query = query.filter(Requests.status == form_data.status)
    if form_data.category_id is not None:
        query = query.filter(Requests.category_id == form_data.category_id)

    return query.order_by(Requests.id.desc()).all()


def IT_stats_v2(db:Session,started_at, finished_at,department,timer=60):
    categories = db.query(Category).join(Requests).filter(Category.status == 1)
    if department is not None:
        categories = categories.filter(Category.department == department)
    if finished_at is not None and started_at is not None:
        categories = categories.filter(Requests.created_at.between(started_at,finished_at))
    categories = categories.filter(Requests.status.in_([0,1,2,3,5,6,]))
    categories = categories.all()

    data = {}
    for category in categories:

        # ---------time delta create------------
        ftime_timedelta = timedelta(seconds=category.ftime * 3600)

        # ---------number of total requests-----------
        total_requests = db.query(Requests).filter(Requests.category_id == category.id).filter(
            Requests.status.in_([0, 1, 2, 3, 5, 6])
        )
        if started_at is not None and finished_at is not None:
            total_requests = total_requests.filter(Requests.created_at.between(started_at, finished_at))
        total_requests = total_requests.count()

        # ---------number of finished on time requests-----------
        finished_on_time = db.query(Requests).filter(Requests.category_id == category.id).filter(
            Requests.status.in_([3, 6])).filter(
            Requests.finished_at - Requests.started_at <= ftime_timedelta
        )
        if started_at is not None and finished_at is not None:
            finished_on_time = finished_on_time.filter(Requests.created_at.between(started_at, finished_at))
        finished_on_time = finished_on_time.count()

        # ---------number of not finished on time requests-----------
        not_finished_on_time = db.query(Requests).filter(Requests.category_id == category.id).filter(
            Requests.status.in_([3, 6])).filter(
            Requests.finished_at - Requests.started_at > ftime_timedelta)
        if started_at is not None and finished_at is not None:
            not_finished_on_time = not_finished_on_time.filter(
                Requests.created_at.between(started_at, finished_at))
        not_finished_on_time = not_finished_on_time.count()

        # ---------number of status zero requests-----------
        status_zero = db.query(Requests).filter(Requests.category_id == category.id).filter(
            Requests.status.in_([0, 1, 2, 5]))
        if started_at is not None and finished_at is not None:
            status_zero = status_zero.filter(Requests.created_at.between(started_at, finished_at))
        status_zero = status_zero.count()

        # ---------calculating percentages-----------
        try:
            percentage_finished_on_time = (finished_on_time / total_requests) * 100
        except:
            percentage_finished_on_time = 0
        try:
            percentage_not_finished_on_time = (not_finished_on_time / total_requests) * 100
        except:
            percentage_not_finished_on_time = 0
        try:
            percentage_status_zero = (status_zero / total_requests) * 100

        except:
            percentage_status_zero = 0

        # ------------average finishing time------------
        total = (
            db.query(
                Category.name,
                func.count(Requests.id),
                func.cast(
                    func.avg(
                        func.extract(
                            "epoch",
                            Requests.finished_at - Requests.started_at,
                        )
                    )
                    / timer,
                    Integer,
                ),
            )
            .join(Requests)
            .filter(
                Requests.status.in_([0, 1, 2, 3]),
                Category.id == category.id,
            )
            .group_by(Category.name)

        )
        if started_at is not None and finished_at is not None:
            total = total.filter(Requests.created_at.between(started_at, finished_at))
        total = total.all()

        # ------------end avg finishing time------------

        # ------------create response data------------

        if total:
            total = total[0][2]
        else:
            total = 0

        dict_data = {
            "total_requests": total_requests,
            "finished_on_time": finished_on_time,
            "not_finished_on_time": not_finished_on_time,
            "status_zero": status_zero,
            "percentage_finished_on_time": percentage_finished_on_time,
            "percentage_not_finished_on_time": percentage_not_finished_on_time,
            "percentage_status_zero": percentage_status_zero,
            "avg_finishing": total,
            'category': category.name
        }

        data[category.id] = dict_data

    return data


def create_telegram(db:Session, form_data: it_extra.CreateTelegram):
    query = Telegrams(
        chat_id=form_data.chat_id,
        name=form_data.name
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_telegram(db: Session, form_data: it_extra.UpdateTelegram):
    query = db.query(Telegrams).filter(Telegrams.id == form_data.id).first()
    if query:
        if query.chat_id is not None:
            query.chat_id = form_data.chat_id
        if query.name is not None:
            query.name = form_data.name
        db.commit()
        db.refresh(query)
    return query


def get_telegram(db:Session,id):
    query = db.query(Telegrams)
    if id is not None:
        query = query.filter(Telegrams.id==id)
    return query.all()


def get_uniform_requests(db:Session,from_date,to_date,status):
    query = db.query(Requests).join(Category).filter(Category.department==9)
    if from_date is not None:
        query = query.filter(Requests.created_at >= from_date)
    if to_date is not None:
        query = query.filter(Requests.created_at <= to_date)
    if status is not None:
        query = query.filter(Requests.status.in_(status))
    return query.all()