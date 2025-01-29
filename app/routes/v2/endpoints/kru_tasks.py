from typing import Optional, List

import pytz
from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import Page, paginate
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.kru_tasks import create_kru_task, get_kru_tasks, get_one_kru_task, update_kru_task,delete_kru_task,get_today_tasks
from app.routes.depth import get_db, get_current_user
from app.schemas.kru_tasks import KruTasksCreate, KruTasksUpdate, KruTasksGet, Tasks
from app.schemas.users import GetUserFullData

kru_tasks_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@kru_tasks_router.post("/kru/tasks/",response_model=Tasks)
async def create_kru_task_api(
    form_data: KruTasksCreate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Create new task
    """
    return create_kru_task(db=db, data=form_data)


@kru_tasks_router.get("/kru/tasks/",response_model=Page[Tasks])
async def get_kru_tasks_api(
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)
):

    return paginate(get_kru_tasks(db=db, name=name, category_id=category_id))



@kru_tasks_router.get("/kru/tasks/{id}",response_model=Tasks)
async def get_one_kru_task_api(
    id: int,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):

    return get_one_kru_task(db=db,id=id)


@kru_tasks_router.put("/kru/tasks/",response_model=Tasks)
async def update_kru_task_api(
    data: KruTasksUpdate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):

    return update_kru_task(db=db, data=data)


@kru_tasks_router.delete("/kru/tasks/{id}", response_model=Tasks)
async def delete_kru_task_api(
    id: int,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):

    return delete_kru_task(db=db,id=id)


@kru_tasks_router.get("/kru/tasks/available/",response_model=KruTasksGet)
async def get_available_tasks_api(
    category_id: Optional[int],
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)
):

    today_tasks = get_today_tasks(db=db, branch_id=current_user.branch_id, category_id=category_id)
    return today_tasks

