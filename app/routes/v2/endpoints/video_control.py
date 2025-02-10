from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from app.crud.video_control import filtered_requests, get_video_excell
from app.routes.depth import get_db, get_current_user
from app.schemas.users import UserFullBack
from app.schemas.video_control import GetRequests, GenerateExcell
from microservices import Excell_generate_it


video_requests_router = APIRouter()



@video_requests_router.get("/requests/video", response_model=Page[GetRequests])
async def filter_requests(
        id: Optional[int] = None,
        # category_id: Optional[int] = None,
        user: Optional[str] = None,
        brigada_id: Optional[int] = None,
        fillial_id: Optional[UUID] = None,
        request_status: Optional[str] = None,
        created_at: Optional[date] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    request_list = filtered_requests(
        id=id,
        user=user,
        brigada_id=request_user.brigada_id if request_user.brigada_id else brigada_id,
        fillial_id=fillial_id,
        request_status=request_status,
        created_at=created_at,
        db=db
    )

    return paginate(request_list)



@video_requests_router.post("/video/excell")
def get_it_excell(
        form_data: GenerateExcell,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    query = get_video_excell(db=db, form_data=form_data)
    file_name = Excell_generate_it(data=query)
    return {'file_name':file_name}

