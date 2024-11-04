import datetime
import re
from typing import Optional
import pytz
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.comments import Comments
from app.models.fillials import Fillials
from app.models.requests import Requests
from app.models.users_model import Users
from app.models.files import Files
from app.schemas.it_requests import PutRequest, CreateRequest



timezonetash = pytz.timezone("Asia/Tashkent")


def filter_request_brigada(
        db: Session,
        id,
        category_id,
        brigada_id,
        fillial_id,
        created_at,
        request_status,
        user,
        arrival_date,
        rate,
        urgent,
        started_at,
        finished_at
):
    query = db.query(Requests).join(Category).filter(Category.department == 4)


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
    if arrival_date is not None:
        query = query.filter(cast(Requests.arrival_date, Date) == arrival_date)
    if rate == True:
        query = query.filter(Requests.id == Comments.request_id)
    if urgent is not None:
        query = query.filter(Category.urgent == urgent)
    if started_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(started_at, finished_at))
    if created_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(created_at, finished_at))
    # if reopened is not None:
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
    # categories = db.query(Category).with_entities(Category.id).filter(Category.department == 4).all()
    query = db.query(Requests).join(Category).filter(Category.department == 4)

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
    if rate == True:
        query = query.filter(Requests.id == Comments.request_id)
    if brigada_id is not None:
        query = query.filter(Requests.brigada_id == brigada_id)
    if urgent is not None:
        query = query.filter(Category.urgent == urgent)
    if started_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(started_at, finished_at))
    if created_at is not None and finished_at is not None:
        query = query.filter(Requests.created_at.between(created_at, finished_at))

    results = query.order_by(Requests.id.desc()).all()
    return results


def get_request_id(db: Session, id):
    return db.query(Requests).filter(Requests.id == id).first()


def filterbranchchildid(db: Session, parent_id, origin: Optional[int] = None):
    query = db.query(Fillials).filter(
        Fillials.status == 1, Fillials.parentfillial_id == parent_id
    )
    if origin:
        query = query.filter(Fillials.origin == origin)

    return query.first()


def edit_request(db: Session,
                 id: int,
                 user: Optional[object] = None,
                 data: Optional[PutRequest] = None,
                 tg_message_id: Optional[int] = None
                 ):
    query = db.query(Requests).filter(Requests.id == id).first()
    now = datetime.datetime.now(tz=timezonetash)
    if data is not None:
        if not user.brigada_id:
            if data.finishing_time is not None:
                query.finishing_time = data.finishing_time
            if data.category_id is not None:
                query.category_id = data.category_id

        if data.status is not None:
            query.status = data.status
            updated_data = query.update_time or {}
            updated_data[str(data.status)] = str(now)
            # query.update_time = updated_data
            if data.status == 1:
                query.started_at = now
            elif data.status == 6:
                query.finished_at = now

            db.query(Requests).filter(Requests.id == id).update({"update_time": updated_data})

        if data.fillial_id is not None:
            filliald_od = filterbranchchildid(db, data.fillial_id)
            query.fillial_id = filliald_od.id
        if data.brigada_id is not None:
            query.brigada_id = data.brigada_id

    if tg_message_id is not None:
        query.tg_message_id = tg_message_id

    db.commit()
    db.refresh(query)
    return query

def add_request(
        db: Session,
        data: Optional[CreateRequest] = None,
        tg_message_id: Optional[int] = None
):
    fillial_id = filterbranchchildid(db, data.parentfillial_id).id
    now = datetime.datetime.now(tz=timezonetash)
    update_time = {"0": str(now)}
    sla = 0
    finishing_time = now + datetime.timedelta(hours=sla)
    query = Requests(
        fillial_id=fillial_id,
        category_id=data.category_id,
        description=data.description,
        update_time=update_time,
        tg_message_id=tg_message_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)

    file_obj_list = []
    if data.files:
        for file in data.files:
            file_path = f"files/{file.filename}"
            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            file_obj_list.append(
                Files(
                    request_id=query.id,
                    url=file_path
                )
            )

    db.bulk_save_objects(file_obj_list)
    db.commit()

    return query