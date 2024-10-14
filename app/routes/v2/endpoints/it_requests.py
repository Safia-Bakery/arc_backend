from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Header,
    Request,
    status,
    APIRouter
)
from fastapi_pagination import paginate, Page
from typing import Optional
from app.schemas.it_extra import *
from app.routes.depth import get_db, get_current_user
from app.schemas.users import UserFullBack
from app.schemas.it_requests import GetRequest, GetOneRequest
from app.crud import it_requests
from app.models.category import Category
from datetime import datetime, date


it_requests_router = APIRouter()


def get_children(category_id, db: Session):
    children = db.query(Category).filter_by(parent_id=category_id).filter(Category.status == 1)
    children = children.all()
    for child in children:
        yield child
        yield from get_children(child.id, db=db)


@it_requests_router.get("/it/requests", response_model=Page[GetRequest])
async def filter_requests(
        id: Optional[int] = None,
        category_id: Optional[int] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        user: Optional[str] = None,
        brigada_id: Optional[int] = None,
        arrival_date: Optional[date] = None,
        rate: Optional[bool] = False,
        urgent: Optional[bool] = None,
        started_at: Optional[date] = None,
        finished_at: Optional[date] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    # if user input data it filter all child categories
    # so in this case get child function gets all child categories
    cat_list = []
    cat_list.append(category_id)

    for i in get_children(category_id=category_id, db=db):
        cat_list.append(i.id)

    request_list = it_requests.filter_requests_all(
        db,
        id=id,
        category_id=cat_list,
        fillial_id=fillial_id,
        request_status=request_status,
        created_at=created_at,
        user=user,
        arrival_date=arrival_date,
        rate=rate,
        brigada_id=request_user.brigada_id or brigada_id,
        urgent=urgent,
        started_at=started_at,
        finished_at=finished_at
    )

    return paginate(request_list)


@it_requests_router.get("/it/requests/{id}", response_model=GetOneRequest)
async def get_request(
    id: int,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = it_requests.get_request_id(db, id)
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")
