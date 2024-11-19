from typing import Optional

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string
from app.schemas.branchs import GetBranchs
from fastapi_pagination import Page,paginate
from app.crud.branchs import get_branchs
from app.schemas.arc_factory_requests import GetArcFactoryRequests,UpdateArcFactoryRequests
from app.crud.arc_factory_requests import get_arc_factory_requests,get_arc_factory_request,update_arc_factory_request

from app.models.requests import Requests




arc_factory_requests = APIRouter()


@arc_factory_requests.get("/arc/factory/requests",response_model=Page[GetArcFactoryRequests])
async def get_requests(
        user_id:Optional[int]=None,
        fillial_id:Optional[int]=None,
        status:Optional[int]=None,
        id:Optional[int]=None,
        current_user: GetUserFullData = Depends(get_current_user),
        db:Session=Depends(get_db)):
    return paginate(get_arc_factory_requests(db=db,user_id=user_id,fillial_id=fillial_id,status=status,id=id))


@arc_factory_requests.get("/arc/factory/requests/{request_id}",response_model=GetArcFactoryRequests)
async def get_request(
        request_id:int,
        current_user: GetUserFullData = Depends(get_current_user),
        db:Session=Depends(get_db)):
    return get_arc_factory_request(db=db,request_id=request_id)


@arc_factory_requests.put("/arc/factory/requests/{request_id}",response_model=GetArcFactoryRequests)
async def update_request(
        request_id:int,
        request:UpdateArcFactoryRequests,
        db:Session = Depends(get_db),
        current_user: GetUserFullData = Depends(get_current_user)):
    return update_arc_factory_request(db=db,request_id=request_id,request=request)
