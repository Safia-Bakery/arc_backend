from sqlalchemy.orm import Session

import models
import schemas
from typing import Optional
import bcrypt
import pytz
from datetime import datetime ,date
from sqlalchemy import or_,and_,Date,cast,func,Integer
timezonetash = pytz.timezone("Asia/Tashkent")



def calculate_bycat(db:Session,sphere_status,department,started_at,finished_at):
    query = db.query(
    models.Category.name.label('category_name'),
    func.count(models.Requests.id).label('count_1'),
    func.cast(func.avg(func.extract('epoch', models.Requests.started_at -models.Requests.created_at)) / 60, Integer).label('avg_1')
).filter(models.Category.sphere_status==sphere_status,models.Category.department==department).join(models.Requests,models.Category.id == models.Requests.category_id).group_by(models.Category.name)
    return query