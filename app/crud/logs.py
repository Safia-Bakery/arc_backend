from sqlalchemy.orm import Session
from app.models.logs import Logs


def create_log(db: Session, request_id, status, user_id):
    query = Logs(
        request_id=request_id,
        user_id=user_id,
        status=status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query
