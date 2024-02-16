
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
    Excell_generate_it
)
from fastapi import APIRouter
from queries import it_query
from allschemas import it_schema



it_router = APIRouter()



@it_router.post("/it/excell", tags=["IT"], status_code=status.HTTP_200_OK)
def get_it_excell(form_data : it_schema.generate_excell,db: Session = Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user),):
    query = it_query.get_it_excell(db=db,form_data =form_data)
    file_name = Excell_generate_it(data=query)
    return {'file_name':file_name}

