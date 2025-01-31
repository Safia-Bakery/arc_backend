from typing import List

import pytz
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.files import create_file_tasks
from app.crud.kru_tasks_finished import create_kru_finished_task
from app.crud.users import get_user_by_tg_id
from app.routes.depth import get_db, token_checker
from app.schemas.kru_finished_tasks import KruFinishedTasksCreate
from app.schemas.users import GetUserFullData


kru_tasks_finished = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@kru_tasks_finished.post("/kru/finished-tasks/")
async def create_kru_finished_task_api(
    data: KruFinishedTasksCreate,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(token_checker)
):
    user = get_user_by_tg_id(db=db, tg_id=data.tg_id)
    for task_answer in data.answers:
        kru_task = create_kru_finished_task(
            db=db,
            data=task_answer,
            user_id=user.id,
            branch_id=user.branch_id,
            tool_id=data.tool_id
        )

        if task_answer.file is not None:
            create_file_tasks(db=db, kru_finished_task_id=kru_task.id, url=task_answer.file)

    return {"status":"success", "message":"Finished Tasks created successfully"}


