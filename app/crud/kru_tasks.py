from datetime import datetime
from typing import Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased

from app.models.tool_branch_relations import ToolBranchCategoryRelation
from app.models.kru_finished_tasks import KruFinishedTasks
from app.models.kru_tasks import KruTasks
from app.schemas.kru_tasks import KruTasksCreate, KruTasksUpdate
from app.models.tools import Tools


def create_kru_task(db:Session, data: KruTasksCreate):
    query = KruTasks(
        name=data.name,
        kru_category_id=data.kru_category_id,
        description=data.description,
        answers=data.answers
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_kru_tasks(db:Session, category_id, name: Optional[str] = None):
    query = db.query(KruTasks).filter(
        and_(
            KruTasks.status == 1,
            KruTasks.kru_category_id == category_id
        )
    )
    if name is not None:
        query = query.filter(KruTasks.name.ilike(f'%{name}%'))
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
    if data.answers is not None:
        query.answers = data.answers

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

def get_today_products(db: Session, branch_id, category_id):
    today = datetime.now().date()

    finished_today_products = db.query(
        KruFinishedTasks.tool_id
    ).join(
        KruTasks
    ).filter(
        and_(
            KruFinishedTasks.branch_id == branch_id,
            func.date(KruFinishedTasks.created_at) == today,
            KruTasks.kru_category_id == category_id
        )
    )

    remaining_products = db.query(
        Tools
    ).join(
        ToolBranchCategoryRelation, Tools.id == ToolBranchCategoryRelation.tool_id
    ).filter(
        and_(
            ToolBranchCategoryRelation.branch_id == branch_id,
            ToolBranchCategoryRelation.kru_category_id == category_id,
            Tools.id.notin_(finished_today_products)
        )
    )

    tasks = db.query(
        KruTasks
    ).filter(
        and_(
            KruTasks.status == 1,
            KruTasks.kru_category_id == category_id
        )
    )

    remaining_products = remaining_products.all()
    tasks = tasks.all()
    data_dict = {
        "products": remaining_products,
        "tasks": tasks
    }
    return data_dict



def get_today_tasks(db: Session, branch_id, category_id):
    today = datetime.now().date()
    # Subquery to get task_ids that were finished today
    finished_today_tasks = db.query(
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
        finished_today_tasks = finished_today_tasks.filter(KruTasks.kru_category_id == category_id)

    # Main query: get tasks that are not finished today
    available_tasks = db.query(
        KruTasks
    ).filter(
        and_(
            KruTasks.status == 1,
            KruTasks.id.notin_(finished_today_tasks)
        )
    )
    if category_id is not None:
        available_tasks = available_tasks.filter(KruTasks.kru_category_id == category_id)

    data_dict = {
        "products": [],
        "tasks": available_tasks.all()
    }
    return data_dict