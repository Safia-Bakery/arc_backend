from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from fastapi_pagination import paginate,Page,add_pagination
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Optional
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions,get_db,get_current_user
from typing import Optional
import models
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import crud
from users.schema import schema
from database import engine,SessionLocal
import os

from dotenv import load_dotenv
import os 
load_dotenv()

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # should be kept secret
JWT_REFRESH_SECRET_KEY =  os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
user_router = APIRouter()



@user_router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),db:Session=Depends(get_db)):
    user = crud.get_user(db,form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }


@user_router.post('/register', summary="Create access and refresh tokens for user")
async def register(form_data: schema.UserCreate,db:Session=Depends(get_db)):
        try:
            user = crud.create_user(db,form_data)
        except:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exist"
            )
        
        return schema.User(id=user.id,username=user.username,full_name=user.full_name)



@user_router.get('/all/permissions',summary='from this api you can get list of roles',response_model=list[schema.ParentPage])
async def admin_pages(db:Session=Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user)):

    permission = checkpermissions(request_user=request_user ,db=db,page=14)
    if permission:
        #roles_list = crud.get_roles(db)
        return crud.get_roles(db)
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )
    

@user_router.get('/all/permissions',summary='from this api you can get list of roles',response_model=list[schema.ParentPage])
async def admin_pages(db:Session=Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user)):

    permission = checkpermissions(request_user=request_user ,db=db,page=14)
    if permission:
        #roles_list = crud.get_roles(db)
        return crud.get_roles(db)
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )
    


@user_router.post('/user/roles')
async def user_group(group_data:schema.CreateGroupSch, db:Session=Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=15)
    if permission:
    
        return crud.create_group(db,group_data)
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )
    

@user_router.put('/user/roles')
async def user_group_update(group_data:schema.UpdateGroupSch, db:Session=Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=2)
    if permission:
        updation = crud.update_group(db,group_data)
        if updation:
            return {'success':True,'message':'updated'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot update becouse role id doesnot match"
            )
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )


@user_router.get('/user/role')
async def user_group_get(db:Session=Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=14)
    if permission:
        return crud.get_group(db)
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )
    

@user_router.get('/user/group/permissions/{id}')
async def group_permissions(id:int,db:Session=Depends(get_db),request_user: schema.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=14)
    if permission:
        try:

            permission_list = crud.get_permissions(db,id=id)
            if permission_list:
                role_name = permission_list[0].group.name
                role_id = permission_list[0].group.id
                
            else:
                group = crud.get_group_by_id(db,id=id)
                role_name= group.name
                role_id = group.id
            permission_list = [ i.page_id for i in permission_list]


            return {'permissions':permission_list,'role_name':role_name,'role_id':role_id}
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="id there is no group like this"
            )
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )