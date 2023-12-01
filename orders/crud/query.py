from sqlalchemy.orm import Session
from users.schema import schema
import models
import schemas
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime 
from sqlalchemy import or_,and_,Date,cast,Integer


def marketing_table(db:Session,timer,created_at,finished_at):
    total = db.query(models.Category.name,func.count(models.Requests.id),func.cast(func.avg(func.extract('epoch', models.Requests.finished_at -models.Requests.started_at)) /timer, Integer)).join(models.Requests).filter(models.Requests.status==3,models.Category.department==3,models.Requests.created_at.between(created_at,finished_at)).group_by(models.Category.name).all()
    dict_data = {}
    for i in total:
        dict_data[i[0]] = [i[1],i[2]]
    return dict_data


def marketing_pie(db:Session,created_at,finished_at):
    percentages = (
    db.query(
        func.count(models.Requests.id).label('total_count'),
        func.jsonb_build_object(
            'category_name', models.Category.name,
            'percent', func.cast(func.count(models.Requests.id) * 100.0 / func.nullif(func.sum(func.count(models.Requests.id)).over(), 0), Integer)
        ).label('category_percent')
    )
    .join(models.Requests)
    .filter(models.Requests.status == 3, models.Category.department == 3,models.Requests.created_at.between(created_at,finished_at))
    .group_by(models.Category.name)
    #.group_by(models.Requests.status)
    .all()
    )
    dict_data = {}
    for i in percentages:
        dict_data[i[1]['category_name']] = [i[0],i[1]['percent']]
    return dict_data