from typing import Optional

import pytz
from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.crud.kru_category import create_kru_category, get_kru_categories, get_one_kru_category, update_kru_category, \
    delete_kru_category
from app.routes.depth import get_db, get_current_user
from app.schemas.kru_categories import KruCategoriesCreate, KruCategoriesUpdate, KruCategoriesGet
from app.schemas.users import GetUserFullData

kru_categories = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@kru_categories.post("/kru_categories/",response_model=KruCategoriesGet)
async def create_kru_category_api(
    form_data: KruCategoriesCreate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Create new category
    """
    return create_kru_category(db=db,form_data=form_data)


@kru_categories.get("/kru_categories/",response_model=Page[KruCategoriesGet])
async def get_kru_categories_api(
    id:Optional[int]=None,
    name:Optional[str]=None,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Get categories
    """
    return paginate(get_kru_categories(db=db,id=id,name=name))



@kru_categories.get("/kru_categories/{id}",response_model=KruCategoriesGet)
async def get_one_kru_category_api(
    id:int,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Get one category
    """
    return get_one_kru_category(db=db,id=id)


@kru_categories.put("/kru_categories/",response_model=KruCategoriesGet)
async def update_kru_category_api(
    id:int,
    form_data: KruCategoriesUpdate,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Update category
    """
    return update_kru_category(db=db,form_data=form_data)


@kru_categories.delete("/kru_categories/{id}",response_model=KruCategoriesGet)
async def delete_kru_category_api(
    id:int,
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Delete category
    """
    return delete_kru_category(db=db,id=id)




