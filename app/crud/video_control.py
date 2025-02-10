import re
from datetime import timedelta, datetime

import pytz
from sqlalchemy import and_, or_, cast, Date
from sqlalchemy.orm import Session

from app.models.users_model import Users
from app.models.fillials import Fillials
from app.models.category import Category
from app.models.requests import Requests
from app.schemas.video_control import GenerateExcell



timezonetash = pytz.timezone("Asia/Tashkent")


def filtered_requests(
        id,
        user,
        brigada_id,
        fillial_id,
        urgent,
        is_expired,
        request_status,
        created_at,
        db: Session
):
    # categories = db.query(Category).with_entities(Category.id).filter(Category.department == 4).all()
    query = db.query(Requests).join(Category).filter(
        and_(
            Category.department == 4,
            or_(
                Category.id == 48,
                Category.parent_id == 48
            )
        )
    )

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
    if brigada_id is not None:
        query = query.filter(Requests.brigada_id == brigada_id)
    if urgent is not None:
        query = query.filter(Category.urgent == urgent)
    # if is_expired is not None:
    #     now = datetime.now(tz=timezonetash)
    #     if is_expired:
    #         if [int(status) for status in request_status if int(status) in [3, 4, 6]]:
    #             query = query.filter(Requests.finished_at > Requests.finishing_time)
    #         elif [int(status) for status in request_status if int(status) in [0, 1]]:
    #             query = query.filter(now > Requests.finishing_time)
    #     if not is_expired:
    #         if [int(status) for status in request_status if int(status) in [3, 4, 6]]:
    #             query = query.filter(Requests.finished_at <= Requests.finishing_time)
    #         elif [int(status) for status in request_status if int(status) in [0, 1]]:
    #             query = query.filter(now <= Requests.finishing_time)

    # if created_at is not None and finished_at is not None:
    #     query = query.filter(Requests.created_at.between(created_at, finished_at))

    results = query.order_by(Requests.id.desc()).all()
    return results



def get_video_excell(db:Session, form_data: GenerateExcell):
    finish_date = form_data.finish_date + timedelta(days=1)
    query = db.query(Requests).join(Category).filter(
        and_(
            Category.department == 4,
            cast(Requests.created_at, Date).between(form_data.start_date, finish_date),
            or_(
                Category.id == 48,
                Category.parent_id == 48
            )
        )
    )
    # if form_data.status is not None:
    #     query = query.filter(Requests.status == form_data.status)
    # if form_data.category_id is not None:
    #     query = query.filter(Requests.category_id == form_data.category_id)
    return query.order_by(Requests.id.desc()).all()