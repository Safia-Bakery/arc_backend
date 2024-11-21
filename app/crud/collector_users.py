from sqlalchemy.orm import Session
from app.models.users_model import Users
from app.schemas.collector_users import CreateUser, UpdateUser


def get_by_telegram_id(db: Session, telegram_id: int):
    query = db.query(Users).filter(Users.telegram_id == telegram_id).first()
    return query


def create_user(db: Session, data: CreateUser):
    query = Users(
        telegram_id=data.telegram_id,
        full_name=data.full_name,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_user(db: Session, data: UpdateUser):
    query = db.query(Users).filter(Users.telegram_id == data.telegram_id).first()
    if data.branch_id is not None:
        query.branch_id = data.branch_id
    if data.group_id is not None:
        query.group_id = data.group_id

    db.commit()
    db.refresh(query)
    return query

