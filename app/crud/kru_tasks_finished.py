from sqlalchemy.orm import Session

from app.models.kru_finished_tasks import KruFinishedTasks
from app.schemas.kru_finished_tasks import KruFinishedTasksCreate


def create_kru_finished_task(db:Session, data: KruFinishedTasksCreate, user_id, branch_id):
    query = KruFinishedTasks(
        task_id=data.task_id,
        user_id=user_id,
        branch_id=branch_id,
        comment=data.comment
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


