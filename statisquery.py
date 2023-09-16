from sqlalchemy.orm import Session

import models
from uuid import UUID
import schemas
from typing import Optional
import bcrypt
import pytz
from datetime import datetime ,date
from sqlalchemy import or_,and_,Date,cast,func,Integer
timezonetash = pytz.timezone("Asia/Tashkent")



def calculate_bycat(timer,db:Session,sphere_status:Optional[int]=None,department:Optional[int]=None,started_at:Optional[date]=None,finished_at:Optional[date]=None):
    query = db.query(
    models.Category.name.label('category_name'),
    func.count(models.Requests.id).label('count_1'),
    func.cast(func.avg(func.extract('epoch', models.Requests.finished_at -models.Requests.started_at)) / timer, Integer).label('avg_1'))  
    if sphere_status:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if department:
        query = query.filter(models.Category.department ==department)
    if started_at and finished_at:
        query = query.filter(models.Requests.created_at.between(started_at,finished_at))

    return query.join(models.Requests,models.Category.id == models.Requests.category_id).filter(models.Requests.status==3).group_by(models.Category.name).all()



def calculate_percentage(db:Session,sphere_status,department,started_at:Optional[date]=None,finished_at:Optional[date]=None):
    total_requests = db.query(models.Requests).join(models.Category).filter(models.Category.sphere_status==sphere_status,models.Requests.status==3,models.Category.department==department,models.Requests.created_at.between(started_at,finished_at)).count()
    categories = db.query(models.Category).filter(models.Category.status==1,models.Category.sphere_status==sphere_status,models.Category.department==department).all()
    category_percentages = []
    for category in categories:
        category_name = category.name
        category_request_count = db.query(models.Requests).join(models.Category).filter(models.Requests.category_id == category.id,models.Requests.status==3,models.Category.department==department,models.Category.sphere_status==sphere_status,models.Requests.created_at.between(started_at,finished_at)).count()
        
        category_percentage = {
            'category_name': category_name,
            'request_count': category_request_count,
            'percentage': (category_request_count / total_requests) * 100 if total_requests > 0 else 0
        }
        category_percentages.append(category_percentage)
    return category_percentages

def countfillialrequest(db:Session,sphere_status,department,started_at,finished_at):
    total = db.query(models.Fillials.name.label('fillial_name'),models.ParentFillials.name.label('parent_fillai'),
                     func.count(models.Requests.id).label('count_1')).join(models.ParentFillials).join(
                         models.Requests).join(models.Category).filter(models.Requests.status==3,models.Category.sphere_status==sphere_status,models.Category.department==department,models.Requests.created_at.between(started_at,finished_at)).group_by(models.Fillials.name,models.ParentFillials.name).all()
    return total



def countbbrigadarequest(db:Session,sphere_status,department,started_at,finished_at,timer=60):
    total = db.query(models.Brigada.name,func.count(models.Requests.id),func.cast(func.avg(func.extract('epoch', models.Requests.finished_at -models.Requests.started_at)) / timer, Integer)).join(models.Requests).join(models.Category).filter(models.Requests.status==3,models.Category.department==department,models.Category.sphere_status==sphere_status,models.Requests.created_at.between(started_at,finished_at)).group_by(models.Brigada.name).all()
    return total


def countbrigadavscategory(timer,started_at,finished_at,db:Session):
    total = db.query(models.Brigada.name.label('brigada_name'),models.Category.name.label('category_name'),
                     func.count(models.Requests.id),
                     func.cast(func.avg(func.extract('epoch', models.Requests.finished_at -models.Requests.started_at)) / timer, Integer).label('avg_1')).join(models.Category).join(
                         models.Brigada).filter(models.Requests.status==3,models.Requests.created_at.between(started_at,finished_at)).group_by(models.Brigada.name,models.Category.name).all()
    return total


def howmuchleftcrud(db:Session,lst,store_id):  
    for i in lst:
        total = db.query(models.Tools).filter(models.Tools.iikoid==i['product']).first()
        if total:
            total.total_price = float(i['sum'])
            total.amount_left=float(i['amount'])
            total.last_update = datetime.now(timezonetash)

            if total.sklad_id:
                if UUID(i['store']) not in total.sklad_id:
                    total.sklad_id = total.sklad_id.append(UUID(i['store']))
            else:
                total.sklad_id = [store_id]
            db.commit()
            db.refresh(total)
                #total.otdel_sphere.
        else:
            pass
    return True



def howmuchleftgetlist(db:Session,id):
    query = db.query(models.Tools).filter(models.Tools.sklad_id.contains([id])).all()
    return query
            