from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.utils.utils import generate_random_string
from app.models.users_model import Users
from app.models.kru_finished_tasks import KruFinishedTasks
from app.schemas.kru_finished_tasks import KruFinishedTasksCreate



def create_kru_finished_task(db:Session,form_data:KruFinishedTasksCreate):
    query = KruFinishedTasks(
        task_id=form_data.task_id,
        user_id=form_data.user_id,
        comment=form_data.comment,
        branch_id=form_data.branch_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


