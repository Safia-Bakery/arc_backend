from sqlalchemy.orm import Session
from app.models.logs import Logs



def create_log(db: Session, data, user):
    query = Logs(
        request_id=data.id,
        user_id=user.id,
        status=data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query
