from sqlalchemy.orm import Session
from app.models.communication import Communication


def message_create(db: Session, message, request_id, status, photo, user_id):
    query = Communication(request_id=request_id,
                          message=message,
                          status=status,
                          user_id=user_id,
                          photo=photo
                          )
    db.add(query)
    db.commit()
    return query
