from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.kru_categories import KruCategories
from app.schemas.kru_categories import KruCategoriesCreate, KruCategoriesUpdate


def create_kru_category(db:Session, data: KruCategoriesCreate):
    query = KruCategories(
        name=data.name,
        parent=data.parent,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        tool_id=data.tool_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_kru_categories(db:Session, name: Optional[str] = None, parent: Optional[int] = None):
    query = db.query(KruCategories).filter(KruCategories.status==1)
    # if id is not None:
    #     query = query.filter(KruCategories.id == id)
    if parent is not None:
        query = query.filter(KruCategories.parent == parent)
    if parent is None:
        query = query.filter(KruCategories.parent.is_(None))
    if name is not None:
        query = query.filter(KruCategories.name.ilike(f'%{name}%'))
    return query.all()


def get_one_kru_category(db:Session,id):
    query = db.query(KruCategories).filter(KruCategories.id==id).first()
    return query


def update_kru_category(db:Session, data: KruCategoriesUpdate):
    query = db.query(KruCategories).filter(KruCategories.id == data.id).first()
    if data.name is not None:
        query.name = data.name
    if data.parent is not None:
        query.parent = data.parent
    if data.description is not None:
        query.description = data.description
    if data.start_time is not None:
        query.start_time = data.start_time
    if data.end_time is not None:
        query.end_time = data.end_time
    if data.tool_id is not None:
        query.tool_id = data.tool_id

    db.commit()
    db.refresh(query)
    return query


def delete_kru_category(db:Session,id:int):
    query = db.query(KruCategories).filter(KruCategories.id==id).first()
    if query is not None:
        query.status = 0
        db.commit()
    return query


def get_sub_categories(db: Session, id):
    query = db.query(func.count(KruCategories.id)).filter(KruCategories.parent == id).scalar()
    return query




