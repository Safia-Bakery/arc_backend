from sqlalchemy.orm import Session
from app.models.toolparents import ToolParents


def get_toolparents(db: Session, parent_id, status, name):
    query = db.query(ToolParents)
    if status is not None:
        query = query.filter(ToolParents.status == status)
    if name is not None:
        query = query.filter(ToolParents.name.ilike(f"%{name}%"))
    if parent_id is not None:
        query = query.filter(ToolParents.parent_id == parent_id)

    result = query.order_by(ToolParents.name.asc()).all()
    return result


def update_toolparent(db: Session, id, status):
    query = db.query(ToolParents).filter(ToolParents.id == id).first()
    if status is not None:
        query.status = status
    db.commit()
    db.refresh(query)
    return query
