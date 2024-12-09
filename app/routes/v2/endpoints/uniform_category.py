from typing import Optional, List

import pytz
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud import uniform_category
from app.schemas.uniform_category import CreateCategory, UpdateCategory, GetCategory
from app.schemas.users import UserFullBack
from microservices import get_current_user, get_db
from users.schema import schema

timezonetash = pytz.timezone("Asia/Tashkent")

load_dotenv()


uniform_category_router = APIRouter()


sizes = [
    'XS (42 - 44)',
    'S (46 - 48)',
    'M (50 - 52)',
    'L (54 - 56)',
    'XL (58 - 60)',
    'XXL (62 - 64)',
    'XXXL (66 - 68)'
         ]


@uniform_category_router.post("/category/uniform/", response_model=CreateCategory)
async def add_category(
        data: CreateCategory,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    category_obj = uniform_category.add_category(data=data, db=db)
    if category_obj.universal_size is True:
        uniform_category.add_category_products(
            db=db,
            category_id=category_obj.id,
            name="universal",
            description=None,
            image=None,
            status=1
        )
    else:
        for i in sizes:
            uniform_category.add_category_products(
                db=db,
                category_id=category_obj.id,
                name=i,
                description=None,
                image=None,
                status=1
            )

    # return {"id": category_obj.id, "name": category_obj.name, "status": category_obj.status}
    return category_obj


@uniform_category_router.put("/category/uniform/", response_model=UpdateCategory)
async def update_category(
        data: UpdateCategory,
        db: Session = Depends(get_db),
        request_user: schema.UserFullBack = Depends(get_current_user)
):
    category_obj = uniform_category.update_category(data=data, db=db)
    if category_obj.universal_size is True:
        category_products = uniform_category.get_category_products(db=db, name="universal", category_id=category_obj.id)
        if not category_products:
            uniform_category.add_category_products(
                db=db,
                category_id=category_obj.id,
                name="universal",
                description=None,
                image=None,
                status=1
            )
    return category_obj


@uniform_category_router.get("/category/uniform/", response_model=List[GetCategory])
async def get_categories(
        name: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    uniform_categories = uniform_category.get_categories(db=db, name=name)
    return uniform_categories


@uniform_category_router.get("/category/uniform/{id}/", response_model=GetCategory)
async def get_category(
        id: int,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    category = uniform_category.get_category_id(db=db, id=id)
    return category