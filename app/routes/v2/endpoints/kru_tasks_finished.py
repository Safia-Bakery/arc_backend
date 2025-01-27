from typing import List

import pytz
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.files import create_file_tasks
from app.crud.kru_tasks_finished import create_kru_finished_task
from app.routes.depth import get_db, get_current_user
from app.schemas.kru_finished_tasks import KruFinishedTasksCreate
from app.schemas.users import GetUserFullData

kru_tasks_finished = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@kru_tasks_finished.post("/kru/finished-tasks/")
async def create_kru_finished_task_api(
    data: List[KruFinishedTasksCreate],
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)
):
    for task in data:
        kru_task = create_kru_finished_task(db=db, data=task, user_id=current_user.id, branch_id=current_user.branch_id)

        if task.file is not None:
            create_file_tasks(db=db, kru_finished_task_id=kru_task.id, url=task.file)

    return {"status":"success", "message":"Finished Tasks created successfully"}


