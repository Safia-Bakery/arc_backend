from datetime import datetime
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased

from app.models.kru_categories import KruCategories
from app.models.kru_finished_tasks import KruFinishedTasks
from app.models.kru_tasks import KruTasks
from app.schemas.kru_tasks import KruTasksCreate, KruTasksUpdate


def create_kru_task(db:Session, data: KruTasksCreate):
    query = KruTasks(
        name=data.name,
        kru_category_id=data.kru_category_id,
        description=data.description
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_kru_tasks(db:Session, name:Optional[str]=None):
    # query = db.query(KruTasks).join(KruCategories).filter(KruTasks.status==1)
    query = db.query(KruTasks).filter(KruTasks.status==1)
    # if id is not None:
    #     query = query.filter(KruTasks.id == id)
    if name is not None:
        query = query.filter(KruTasks.name.ilike(f'%{name}%'))
    # if category_name is not None:
    #     query = query.filter(KruCategories.name.ilike(f'%{category_name}%'))
    # if category_id is not None:
    #     query = query.filter(KruTasks.kru_category_id == category_id)
    return query.all()

def get_one_kru_task(db:Session,id):
    query = db.query(KruTasks).filter(KruTasks.id==id).first()
    return query

def update_kru_task(db:Session, data: KruTasksUpdate):
    query = db.query(KruTasks).filter(KruTasks.id == data.id).first()
    if data.name is not None:
        query.name = data.name
    if data.description is not None:
        query.description = data.description
    if data.kru_category_id is not None:
        query.kru_category_id = data.kru_category_id
    if data.status is not None:
        query.status = data.status

    db.commit()
    db.refresh(query)
    return query


def delete_kru_task(db:Session, id:int):
    query = db.query(KruTasks).filter(KruTasks.id==id).first()
    if query is not None:
        query.status = 0
        db.commit()
    return query


# get todays tasks which are not in finished tasks list i mean which are not in KruFinishedTasks table

def get_today_tasks(db: Session, branch_id, category_id, category_name):
    today = datetime.now().date()

    # Alias for finished tasks to filter out tasks finished today
    # finished_task_alias = aliased(KruFinishedTasks)

    # Subquery to get task_ids that were finished today
    finished_today_subquery = db.query(
        KruFinishedTasks.task_id
    ).join(
        KruTasks
    ).filter(
        and_(
            KruFinishedTasks.created_at >= today,
            KruFinishedTasks.branch_id == branch_id
        )
    )
    if category_id is not None:
        finished_today_subquery = finished_today_subquery.filter(KruTasks.kru_category_id == category_id)

    # if category_name is not None:
    #     finished_today_subquery = finished_today_subquery.filter(KruCategories.name.ilike(f'%{category_name}%'))

    # Main query: get tasks that are not finished today
    query = db.query(
        KruTasks
    ).filter(
        KruTasks.status == 1,  # Only tasks with status 1 (active)
        ~KruTasks.id.in_(finished_today_subquery)  # Exclude tasks finished today
    )
    if category_id is not None:
        query = query.filter(KruTasks.kru_category_id == category_id)

    # if category_name is not None:
    #     query = query.filter(KruCategories.name.ilike(f'%{category_name}%'))

    return query.all()
