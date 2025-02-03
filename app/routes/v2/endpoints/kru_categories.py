from typing import Optional

import pytz
from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import Page, paginate, Params
from sqlalchemy.orm import Session

from app.crud.kru_category import create_kru_category, get_kru_categories, get_one_kru_category, update_kru_category, \
    delete_kru_category, get_category_products_number
from app.crud.kru_tasks import get_today_products, get_today_tasks
from app.crud.users import get_user_by_tg_id
from app.routes.depth import get_db, get_current_user
from app.schemas.kru_categories import KruCategoriesCreate, KruCategoriesUpdate, KruCategoriesGet
from app.schemas.users import GetUserFullData

kru_categories = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')



class CustomParams(Params):
    size: int = 1  # Set default page size


@kru_categories.post("/kru/categories/",response_model=KruCategoriesGet)
async def create_kru_category_api(
    form_data: KruCategoriesCreate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)
):
    return create_kru_category(db=db, data=form_data)


@kru_categories.get("/kru/categories/",response_model=Page[KruCategoriesGet])
async def get_kru_categories_api(
        tg_id: Optional[int] = None,
        name: Optional[str] = None,
        parent: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: GetUserFullData = Depends(get_current_user)
):
    if tg_id is None:
        query_data = get_kru_categories(db=db, name=name, parent=parent)
    else:
        user = get_user_by_tg_id(db=db, tg_id=tg_id)
        # query_data = get_kru_categories(db=db, name=name, branch_id=user.branch_id)
        query_data = get_kru_categories(db=db, name=name, parent=parent)
        for index, item in enumerate(query_data):
            if item.id == 26:
                products = get_today_products(db=db, category_id=item.id, branch_id=user.branch_id)["products"]
                products_count = len(products)
                query_data[index].products_count = products_count
            elif item.id == 27:
                tasks = get_today_tasks(db=db, category_id=item.id, branch_id=user.branch_id)["tasks"]
                tasks_count = len(tasks)
                query_data[index].tasks_count = tasks_count

    return paginate(query_data)



@kru_categories.get("/kru/categories/{id}",response_model=KruCategoriesGet)
async def get_one_kru_category_api(
    id: int,
    tg_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    query = get_one_kru_category(db=db, id=id)
    if tg_id is not None:
        user = get_user_by_tg_id(db=db, tg_id=tg_id)
        if id == 26:
            products = get_today_products(db=db, category_id=id, branch_id=user.branch_id)["products"]
            products_count = len(products)
            query.products_count = products_count
        elif id == 27:
            tasks = get_today_tasks(db=db, category_id=id, branch_id=user.branch_id)["tasks"]
            tasks_count = len(tasks)
            query.tasks_count = tasks_count

    return query


@kru_categories.put("/kru/categories/",response_model=KruCategoriesGet)
async def update_kru_category_api(
    form_data: KruCategoriesUpdate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    return update_kru_category(db=db, data=form_data)


@kru_categories.delete("/kru/categories/{id}",response_model=KruCategoriesGet)
async def delete_kru_category_api(
    id: int,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    return delete_kru_category(db=db,id=id)




