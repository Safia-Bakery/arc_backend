from sqlalchemy.orm import Session
from app.models.groups import Groups


def get_groups(db: Session, ids):
    if ids:
        query = db.query(Groups).filter(Groups.id.in_(ids)).all()
    else:
        query = db.query(Groups).all()

    return query


def get_group(db: Session, name):
    query = db.query(Groups).filter(Groups.name == name).first()
    return query
