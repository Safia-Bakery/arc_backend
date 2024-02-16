from sqlalchemy.orm import Session
from users.schema import schema
import models
import schemas
from typing import Optional
import bcrypt
from microservices import find_hierarchy
from Variables import role_ids
import pytz
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import or_, and_, Date, cast
from datetime import datetime,timedelta
from allschemas import it_schema



timezonetash = pytz.timezone("Asia/Tashkent")


def it_query_with_status(db:Session,status):
    three_days_timedelta = timedelta(days=3)
    current_time = datetime.now(timezonetash)
    query = db.query(models.Requests).join(models.Category).filter(models.Requests.status == status).filter(
        models.Category.department == 2).filter(models.Requests.finished_at- current_time < three_days_timedelta).all()
    return query



def update_status_it(db:Session,id):
    query = db.query(models.Requests).filter(models.Requests.id == id).update({models.Requests.status: 3})
    db.commit()
    return query


def get_it_excell(db:Session,form_data:it_schema.generate_excell):
    query = db.query(models.Requests).join(models.Category).filter(models.Category.department == 4).filter(models.Requests.created_at.between(form_data.start_date,form_data.finish_date))
    if form_data.status:
        query = query.filter(models.Requests.status == form_data.status)

    return query.all()