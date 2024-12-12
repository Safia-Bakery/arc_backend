from typing import Optional

from sqlalchemy.orm import Session

from app.models.positions import Positions
from app.schemas.positions import CreatePosition, UpdatePosition


def get_positions(db: Session, id: Optional[int] = None):
    obj = db.query(Positions)
    if id is not None:
        obj = obj.get(ident=id)
        return obj

    return obj.all()


def add_position(data: CreatePosition, db: Session):
    obj = Positions(
        name=data.name,
        department=data.department,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def edit_position(db: Session, data: UpdatePosition):
    obj = db.query(Positions).get(ident=data.id)
    if data.name is not None:
        obj.name = data.name
    if data.department is not None:
        obj.department = data.department

    db.commit()
    db.refresh(obj)
    return obj
