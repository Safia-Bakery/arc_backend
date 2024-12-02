# ----------import packages
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, UploadFile, status
from typing import Annotated
from typing import Optional
from microservices import get_current_user, get_db, confirmation_request
from fastapi_pagination import paginate, Page, add_pagination
from fastapi import APIRouter, Form
from orders.crud import query
from app.utils import utils
from app.schemas.users import UserFullBack
from app.core.config import Settings
from app.crud.category import add_category, update_category, filter_category, get_category_id
from app.schemas.category import GetCategory, CreateCategory


category_router = APIRouter()

sizes = Settings().sizes


@category_router.post("/category",)
async def add_category_route(
        data: CreateCategory,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    if data.file is not None:
        # for file in image:
        file_name = f"files/{utils.generate_random_filename()+data.file}"

    add_category_cr = add_category(
        db=db,
        data=data
    )
    if data.department == 9:
        for i in sizes:
            query.createcat_product(db=db, category_id=add_category_cr.id, name=i, description=None, image=None, status=1)

    return {"id": add_category_cr.id, "name": add_category_cr.name, "status": add_category_cr.status}


@category_router.put("/category")
async def update_category_route(
    id: Annotated[int, Form()],
    name: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    status: Annotated[int, Form()] = None,
    urgent: Annotated[bool, Form()] = None,
    department: Annotated[int, Form()] = None,
    ftime: Annotated[float, Form()] = None,
    sphere_status: Annotated[int, Form()] = None,
    file: UploadFile = None,
    sub_id: Annotated[int, Form()] = None,
    parent_id: Annotated[int, Form()] = None,
    is_child: Annotated[bool, Form()] = None,
    telegram_id: Annotated[str, Form()] = None,
    price: Annotated[float, Form()] = None,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    if file is not None:
        # for file in image:
        folder_name = f"files/{utils.generate_random_filename()+file.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        file = folder_name
    response = update_category(
        db=db,
        id=id,
        file=file,
        name=name,
        description=description,
        status=status,
        urgent=urgent,
        department=department,
        sphere_status=sphere_status,
        sub_id=sub_id,
        ftime=ftime,
        parent_id=parent_id,
        is_child=is_child,
        telegram_id=telegram_id,
        price=price
    )
    if response.department == 9:
        query.deletecat_product(db=db,category_id=id)
        for i in sizes:
            query.createcat_product(db=db,category_id=id,name=i,description=None,image=None,status=1)
    if response:
        return GetCategory.from_orm(response)
    else:
        return {"message": "not found"}


@category_router.get("/category", response_model=Page[GetCategory])
async def filter_category_route(
    sphere_status: Optional[int] = None,
    sub_id: Optional[int] = None,
    department: Optional[int] = None,
    category_status: Optional[int] = None,
    name: Optional[str] = None,
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    response = filter_category(
        db,
        category_status=category_status,
        name=name,
        sub_id=sub_id,
        department=department,
        sphere_status=sphere_status,
        parent_id=parent_id
    )
    return paginate(response)


@category_router.get("/category/{id}", response_model=GetCategory)
async def get_category_id_route(
    id: int,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        response = get_category_id(db, id)
        return response
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="info with this id not found "
        )

