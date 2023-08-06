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
from uuid import UUID
from microservices import sendtotelegramchannel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import crud
from microservices import get_current_user,get_db,list_departments,authiiko
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page,add_pagination

from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions,getgroups,getproducts,list_stores
#from main import get_db,get_current_user
from fastapi import APIRouter
from uuid import UUID
urls = APIRouter()



@urls.get('/synch/department',response_model=Page[schemas.GetFillialSch])
async def insert_departments(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)): 
    data = crud.insert_fillials(db,items=list_departments(key=authiiko()))
    stores = crud.insert_otdels(db,items=list_stores(key=authiiko()))
    branches = crud.get_branch_list(db)
    return paginate(branches)


@urls.get('/synch/groups')
async def insert_groups(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    groups = getgroups(key = authiiko())
    products = getproducts(key=authiiko())
    group_list = crud.synchtools(db,groups)
    product_list = crud.synchproducts(db,grouplist=group_list,products=products)
    return {'success':True}


@urls.get('/tool/iarch',response_model=list[schemas.ToolParentsch])
async def toolgroups(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    return crud.getarchtools(db)


@urls.get('/v1/tool',response_model=Page[schemas.ToolsSearch])
async def toolgroups(query:str,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    data = crud.gettools(db,query)
    return paginate(data)




@urls.post('/v1/expenditure')
async def insert_expenditure(amount:Annotated[int,Form()],request_id:Annotated[int,Form()],tool_id:Annotated[int,Form()],comment:Annotated[str,Form()]=None,files:list[UploadFile]= None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    crud.addexpenditure(db,request_id=request_id,amount=amount,tool_id=tool_id)
    if comment:
        addcomment = crud.addcomment(db,request_id=request_id,comment=comment)
    if files:
        file_obj_list = []
        for file in files:
            file_path = f"files/{file.filename}"
            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            file_obj_list.append(models.Files(request_id=request_id,url=file_path,status=1))
        crud.bulk_create_files(db,file_obj_list)
    return {'success':True}




    





