
# ----------import packages
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
)
import schemas
from typing import Annotated
import models
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from database import engine, SessionLocal
from fastapi_pagination import paginate, Page
from users.schema import schema
from microservices import (
    checkpermissions,
    getgroups,
    getproducts,
    list_stores,
    get_suppliers,
    send_document_iiko,
    howmuchleft,
    find_hierarchy,
    get_prices,
    file_generator,
    get_db,
    get_current_user,
    Excell_generate_it,
uniform_excell_generate
)
from fastapi import APIRouter
from queries import it_query
from allschemas import it_schema
import subprocess



it_router = APIRouter()



@it_router.post("/it/excell", tags=["IT"], status_code=status.HTTP_200_OK)
def get_it_excell(form_data : it_schema.generate_excell,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = it_query.get_it_excell(db=db,form_data =form_data)
    file_name = Excell_generate_it(data=query)
    return {'file_name':file_name}




@it_router.get("/it/stats", tags=["IT"], status_code=status.HTTP_200_OK)
def IT_stats_v2(started_at: Optional[date] = None, finished_at: Optional[date] = None, department: Optional[int] = None,  db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    data = it_query.IT_stats_v2(db=db,started_at=started_at, finished_at=finished_at,department=department,timer=60)
    return data




@it_router.post("/restart-arcbot/")
async def restart_arcbot(request_user: schema.UserFullBack = Depends(get_current_user)):
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



@it_router.post("/v1/telegrams", tags=["IT"],response_model=it_schema.GetTelegram)
async def send_telegram_message(
        form_data : it_schema.CreateTelegram,
        request_user: schema.UserFullBack = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return it_query.create_telegram(db=db,form_data=form_data)


@it_router.put("/v1/telegrams", tags=["IT"],response_model=it_schema.GetTelegram)
async def update_telegram_message(
        form_data : it_schema.UpdateTelegram,

        db: Session = Depends(get_db),
        request_user: schema.UserFullBack = Depends(get_current_user),
):
    return it_query.update_telegram(db=db,form_data=form_data)


@it_router.get("/v1/telegrams", tags=["IT"],response_model=Page[it_schema.GetTelegram])
async def get_telegram_messages(
        id:Optional[int]=None,
        db: Session = Depends(get_db),
        request_user: schema.UserFullBack = Depends(get_current_user),
):
    return paginate(it_query.get_telegram(db=db,id=id))


@it_router.get('/v1/excell/uniforms', tags=["Uniforms"])
async def get_uniforms(
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        status: Optional[list[int]] = None,
        db: Session = Depends(get_db),
                       request_user: schema.UserFullBack = Depends(get_current_user)):
    data = it_query.get_uniform_requests(db=db,from_date=from_date,to_date=to_date,status=status)
    return uniform_excell_generate(data=data)





