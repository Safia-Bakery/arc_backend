from sqlalchemy.orm import Session

from app.models.fillials import Fillials
from app.models.parentfillials import ParentFillials


def get_child_branch(db:Session,id:int):
    query = db.query(Fillials).filter(Fillials.parentfillial_id==id).first()
    return query


def get_all_departments(db: Session):
    query = db.query(ParentFillials).distinct().all()
    return query