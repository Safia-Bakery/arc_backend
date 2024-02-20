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
from sqlalchemy import or_, and_, Date, cast,Integer
from datetime import datetime,timedelta



def get_category_list(db:Session,parent_id,department,sphere_status):
    query = db.query(models.Category).filter(models.Category.status==1)
    if parent_id is not None:
        query = query.filter(models.Category.parent_id==parent_id)
    else:
        query = query.filter(models.Category.parent_id.is_(None))
    if department is not None:
        query= query.filter(models.Category.department==department)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    
    return query.all()


def create_data_dict(db:Session,category,started_at,finished_at,timer=60):
    
   


        #---------time delta create------------
        ftime_timedelta = timedelta(seconds=category.ftime*3600)

        #---------number of total requests-----------
        total_requests = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status.in_([0,1,2,3]))
        if started_at is not None and finished_at is not None:
            total_requests = total_requests.filter(models.Requests.created_at.between(started_at,finished_at))
        total_requests = total_requests.count()


        #---------number of finished on time requests-----------
        finished_on_time = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status==3).filter(
            models.Requests.finished_at - models.Requests.started_at <= ftime_timedelta
        )
        if started_at is not None and finished_at is not None:
            finished_on_time = finished_on_time.filter(models.Requests.created_at.between(started_at,finished_at))
        finished_on_time = finished_on_time.count()


        #---------number of not finished on time requests-----------
        not_finished_on_time = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status==3).filter(
            models.Requests.finished_at - models.Requests.started_at > ftime_timedelta)
        if started_at is not None and finished_at is not None:
            not_finished_on_time = not_finished_on_time.filter(models.Requests.created_at.between(started_at,finished_at))
        not_finished_on_time = not_finished_on_time.count()
        

        #---------number of status zero requests-----------
        status_zero = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status.in_([0,1,2]))
        if started_at is not None and finished_at is not None:
            status_zero = status_zero.filter(models.Requests.created_at.between(started_at,finished_at))
        status_zero = status_zero.count()

        #---------calculating percentages-----------
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


        #------------average finishing time------------
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
                / timer,
                Integer,
            ),
        )
        .join(models.Requests)
        .filter(
            models.Requests.status.in_([0,1,2,3]),
            models.Category.id == category.id,
        )
        .group_by(models.Category.name)
        
        )
        if started_at is not None and finished_at is not None:
            total = total.filter(models.Requests.created_at.between(started_at,finished_at))
        total = total.all()


        if total:
            total = total[0][2]
        else: 
            total = 0
        
        dict_data = {
            "total_requests":total_requests,
            "finished_on_time":finished_on_time,
            "not_finished_on_time":not_finished_on_time,
            "status_zero":status_zero,
            "percentage_finished_on_time":percentage_finished_on_time,
            "percentage_not_finished_on_time":percentage_not_finished_on_time,
            "percentage_status_zero":percentage_status_zero,
            "avg_finishing":total,
            'category':category.name
        }

        return dict_data




def stats_query(db:Session,started_at,finished_at,timer=60):

    data = {
    }


    def get_children(category_id):
        children = db.query(models.Category).filter_by(parent_id=category_id).filter(models.Category.status==1)
        if started_at is not None and finished_at is not None:
            children = children.filter(models.Requests.created_at.between(started_at,finished_at))
        children = children.all()
        for child in children:
            yield child
            yield from get_children(child.id)

    categories = db.query(models.Category).join(models.Requests).filter(models.Category.parent_id==None,models.Category.department==1,models.Category.sphere_status==1)
    if started_at is not None and finished_at is not None:
        categories = categories.filter(models.Requests.created_at.between(started_at,finished_at))
    categories = categories.filter(models.Category.status==1).all()

    for category in categories:
        data[category.name] = []
        all_data = create_data_dict(db=db,category=category,started_at=started_at,finished_at=finished_at,timer=timer)
        data[category.name].append(all_data)
        for child in get_children(category.id):
            all_data = create_data_dict(db=db,category=child,started_at=started_at,finished_at=finished_at,timer=timer)
            data[category.name].append(all_data)

  
    return data


        

