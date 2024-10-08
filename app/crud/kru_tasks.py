from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from sqlalchemy.orm import aliased
from uuid import UUID
from app.utils.utils import generate_random_string
from app.models.users_model import Users
from app.models.kru_tasks import KruTasks
from app.models.kru_finished_tasks import KruFinishedTasks
from app.models.kru_categories import KruCategories
from app.schemas.kru_tasks import KruTasksCreate,KruTasksUpdate,KruTasksGet


def create_kru_task(db:Session,form_data:KruTasksCreate):
    query = KruTasks(
        name=form_data.name,
        kru_category_id=form_data.kru_category_id,
        description=form_data.description,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_kru_tasks(db:Session,id:Optional[int]=None,name:Optional[str]=None,category_name:Optional[str]=None,category_id:Optional[int]=None):
    query = db.query(KruTasks).join(KruCategories).filter(KruTasks.status==1)
    if id is not None:
        query = query.filter(KruTasks.id == id)
    if name is not None:
        query = query.filter(KruTasks.name.ilike(f'%{name}%'))
    if category_name is not None:
        query = query.filter(KruCategories.name.ilike(f'%{category_name}%'))
    if category_id is not None:
        query = query.filter(KruTasks.kru_category_id == category_id)
    return query.all()

def get_one_kru_task(db:Session,id):
    query = db.query(KruTasks).filter(KruTasks.id==id).first()
    return query

def update_kru_task(db:Session,form_data:KruTasksUpdate):
    query = db.query(KruTasks).filter(KruTasks.id==form_data.id).first()
    if form_data.name is not None:
        query.name = form_data.name
    if form_data.description is not None:
        query.description = form_data.description

    db.commit()
    db.refresh(query)
    return query


def delete_kru_task(db:Session,id:int):
    query = db.query(KruTasks).filter(KruTasks.id==id).first()
    if query is not None:
        query.status = 0
        db.commit()
    return query


# get todays tasks which are not in finished tasks list i mean which are not in KruFinishedTasks table

def get_todays_tasks(db: Session,branch_id,category_id,category_name):
    today = datetime.now().date()

    # Alias for finished tasks to filter out tasks finished today
    finished_task_alias = aliased(KruFinishedTasks)

    # Subquery to get task_ids that were finished today
    finished_today_subquery = db.query(finished_task_alias.task_id).filter(
        finished_task_alias.created_at >= today,
        finished_task_alias.branch_id ==branch_id
    )
    if category_id is not None:
        finished_today_subquery = finished_today_subquery.filter(finished_task_alias.kru_category_id == category_id)

    if category_name is not None:
        finished_today_subquery = finished_today_subquery.filter(KruCategories.name.ilike(f'%{category_name}%'))

    # Main query: get tasks that are not finished today
    query = db.query(KruTasks).join(KruCategories).filter(
        KruTasks.status == 1,  # Only tasks with status 1 (active)
        ~KruTasks.id.in_(finished_today_subquery),  # Exclude tasks finished today

    )
    if category_id is not None:
        query = query.filter(KruTasks.kru_category_id == category_id)
    if category_name is not None:
        query = query.filter(KruCategories.name.ilike(f'%{category_name}%'))

    return query.all()
