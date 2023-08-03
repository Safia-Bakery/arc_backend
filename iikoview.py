#----------import packages 
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from pydantic import ValidationError
import schemas
import bcrypt
from typing import Annotated
import models
from microservices import sendtotelegramchannel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import crud
from microservices import get_current_user,get_db,list_departments,authiiko
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page,add_pagination

from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions,getgroups,getproducts
#from main import get_db,get_current_user
from fastapi import APIRouter

urls = APIRouter()



@urls.get('/synch/department',response_model=Page[schemas.GetFillialSch])
async def insert_departments(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)): 
    data = crud.insert_fillials(db,items=list_departments(key=authiiko()))
    branches = crud.get_branch_list(db)
    return paginate(branches)


@urls.get('/synch/groups')
async def insert_departments(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    groups = getgroups(key = authiiko())
    products = getproducts(key=authiiko())
    data = crud.synchtools(db,groups)

    





