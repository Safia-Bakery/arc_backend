from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from fastapi_pagination import paginate, Page
from typing import Optional
from app.schemas.it_extra import *
from app.routes.depth import get_db, get_current_user
from app.schemas.users import UserFullBack
from app.schemas.inventory_requests import (GetRequest,
                                            CreateInventoryRequest,
                                            UpdateRequest,
                                            UpdateInventoryExpenditure
                                            )
from app.schemas.requests import GetOneRequest
from app.crud import inv_requests
from datetime import datetime, date
from app.crud.expanditure import create_expanditure

inv_requests_router = APIRouter()


@inv_requests_router.get("/requests/inv/factory", response_model=Page[GetRequest])
async def filter_factory_requests(
        id: Optional[int] = None,
        user: Optional[str] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user),
):


    request_list = inv_requests.filter_requests_all(
        db,
        id=id,
        user=user,
        fillial_id=fillial_id,
        created_at=created_at,
        request_status=request_status,
        department=9
    )

    return paginate(request_list)


@inv_requests_router.get("/requests/inv/retail", response_model=Page[GetRequest])
async def filter_retail_requests(
        id: Optional[int] = None,
        user: Optional[str] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user),
):
    request_list = inv_requests.filter_requests_all(
        db,
        id=id,
        user=user,
        fillial_id=fillial_id,
        created_at=created_at,
        request_status=request_status,
        department=2
    )

    return paginate(request_list)


@inv_requests_router.get("/requests/inv/{id}", response_model=GetOneRequest)
async def get_request(
    id: int,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.get_request_id(db, id)
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")



@inv_requests_router.post("/requests/inv", response_model=GetOneRequest)
async def create_request(
    request: CreateInventoryRequest,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.create_request(db, request,user_id=request_user.id)
        for  item in request.expenditure:
            create_expanditure(db, amount=item.amount,tool_id=item.tool_id,request_id=request_list.id)
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")



