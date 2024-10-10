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
from app.crud import it_extra
from app.utils.it_utils import excell_generate_it, uniform_excell_generate
from datetime import datetime, date
import subprocess


it_extra_router = APIRouter()


@it_extra_router.post("/it/excell", tags=["IT"], status_code=status.HTTP_200_OK)
def get_it_excell(form_data: GenerateExcel, db: Session = Depends(get_db),
                  request_user: UserFullBack = Depends(get_current_user)):
    query = it_extra.get_it_excell(db=db, form_data=form_data)
    file_name = excell_generate_it(data=query)
    return {'file_name': file_name}


@it_extra_router.get("/it/stats", tags=["IT"], status_code=status.HTTP_200_OK)
def IT_stats_v2(started_at: Optional[date] = None,
                finished_at: Optional[date] = None,
                department: Optional[int] = None,
                db: Session = Depends(get_db),
                request_user: UserFullBack = Depends(get_current_user)):
    data = it_extra.IT_stats_v2(db=db, started_at=started_at, finished_at=finished_at, department=department, timer=60)
    return data


@it_extra_router.post("/restart-arcbot/")
async def restart_arcbot(request_user: UserFullBack = Depends(get_current_user)):
    try:
        completed_process = subprocess.run(
            ["sudo", "systemctl", "restart", "Arcbot.service"],
            check=True,
            text=True,
            capture_output=True
        )
        return {"message": "Arcbot service restarted successfully", "stdout": completed_process.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart Arcbot service: {e.stderr}")


@it_extra_router.post("/v1/telegrams", tags=["IT"], response_model=GetTelegram)
async def send_telegram_message(
        form_data: CreateTelegram,
        request_user: UserFullBack = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return it_extra.create_telegram(db=db,form_data=form_data)


@it_extra_router.put("/v1/telegrams", tags=["IT"], response_model=GetTelegram)
async def update_telegram_message(
        form_data: UpdateTelegram,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)):
    return it_extra.update_telegram(db=db, form_data=form_data)


@it_extra_router.get("/v1/telegrams", tags=["IT"], response_model=Page[GetTelegram])
async def get_telegram_messages(
        id:Optional[int]=None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user),
):
    return paginate(it_extra.get_telegram(db=db, id=id))


@it_extra_router.post('/v1/excell/uniforms', tags=["Uniforms"])
async def get_uniforms(
        form_data: Uniformexcellgeneration,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)):

    data = it_extra.get_uniform_requests(db=db,from_date=form_data.start_date,to_date=form_data.finish_date,status=form_data.status)
    return uniform_excell_generate(data=data)
