
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
    get_db,get_current_user
)
from fastapi import APIRouter
from queries import arc_query



arc_routes = APIRouter()



@arc_routes.get('/v1/arc/stats', tags=["ARC"], status_code=status.HTTP_200_OK)
def get_stats(started_at:Optional[date]=None,finished_at:Optional[date]=None,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = arc_query.stats_query(db=db,started_at=started_at,finished_at=finished_at)
    return query