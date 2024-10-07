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


@kru_tasks_finished.post("/kru_finished_tasks/")
async def create_kru_finished_task_api(
    form_data: KruFinishedTasksCreate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Create new finished task
    """
    kru_task = create_kru_finished_task(db=db,form_data=form_data)

    if form_data.file is not None:
        create_file_tasks(db=db,kru_finished_task_id=kru_task.id,url=form_data.file)
    return {"status":"success","message":"Task created successfully"}


