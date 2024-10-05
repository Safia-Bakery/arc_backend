from typing import Optional

import pytz
from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import Page, paginate
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.kru_tasks import create_kru_task, get_kru_tasks, get_one_kru_task, update_kru_task,delete_kru_task,get_todays_tasks
from app.routes.depth import get_db, get_current_user
from app.schemas.kru_tasks import KruTasksCreate, KruTasksUpdate, KruTasksGet
from app.schemas.users import GetUserFullData

kru_tasks_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@kru_tasks_router.post("/kru_tasks/",response_model=KruTasksGet)
async def create_kru_task_api(
    form_data: KruTasksCreate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Create new task
    """
    return create_kru_task(db=db,form_data=form_data)


@kru_tasks_router.get("/kru_tasks/",response_model=Page[KruTasksGet])
async def get_kru_tasks_api(
    id:Optional[int]=None,
    name:Optional[str]=None,
    category_name:Optional[str]=None,
    kru_category_id:Optional[int]=None,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Get tasks
    """
    return paginate(get_kru_tasks(db=db,id=id,name=name,category_name=category_name,category_id=kru_category_id))



@kru_tasks_router.get("/kru_tasks/{id}",response_model=KruTasksGet)
async def get_one_kru_task_api(
    id:int,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Get one task
    """
    return get_one_kru_task(db=db,id=id)


@kru_tasks_router.put("/kru_tasks/",response_model=KruTasksGet)
async def update_kru_task_api(
    form_data: KruTasksUpdate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Update task
    """
    return update_kru_task(db=db,form_data=form_data)


@kru_tasks_router.delete("/kru_tasks/{id}",response_model=KruTasksGet)
async def delete_kru_task_api(
    id:int,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Delete task
    """
    return delete_kru_task(db=db,id=id)


@kru_tasks_router.get("/kru_tasks/todays/",response_model=list[KruTasksGet])
async def get_todays_tasks_api(
    branch_id:UUID,
    category_id: Optional[int] = None,
    category_name:Optional[str]=None,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Get todays tasks
    """
    return get_todays_tasks(db=db,branch_id=branch_id,category_id=category_id,category_name=category_name)


