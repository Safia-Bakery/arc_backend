
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
    get_db
)
from fastapi import APIRouter
from queries import inv_query



inv_router = APIRouter()



@inv_router.delete("/tools", tags=["Tools"], status_code=status.HTTP_200_OK)
def delete_tool(id: int, db: Session = Depends(get_db)):
    query = inv_query.delete_tool(db=db, id=id)
    return  {'success': True}
