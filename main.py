#----------import packages 
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

import warnings
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status,BackgroundTasks,Security
from pydantic import ValidationError
import schemas
import bcrypt
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
from typing import Optional
import models
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import crud
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page,add_pagination
from secondmain import router
from iikoview import urls

from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions,get_db,get_current_user
from dotenv import load_dotenv
import os 
models.Base.metadata.create_all(bind=engine)
load_dotenv()



#--------token generation
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # should be kept secret
JWT_REFRESH_SECRET_KEY =  os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
from fastapi.staticfiles import StaticFiles


origins = ["*"]

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
#database connection
app = FastAPI()
app.include_router(router)
app.include_router(urls)
app.mount("/files", StaticFiles(directory="files"), name="files")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------get user from token



#------------AUTHENTICATION

@app.post('/login', summary="Create access and refresh tokens for user")
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


@app.post('/tg/login')
async def telegram_login(form_data:schemas.TGlogin,db:Session=Depends(get_db)):
    user = crud.getusertelegramid(db,form_data.telegram_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    return {
        'sphere_status':user.sphere_status,
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }


@app.post('/register', summary="Create access and refresh tokens for user")
async def register(form_data: schemas.UserCreate,db:Session=Depends(get_db)):
        try:
            user = crud.create_user(db,form_data)
        except:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exist"
            )
        
        return schemas.User(id=user.id,username=user.username,full_name=user.full_name)
    



@app.get('/all/permissions',summary='from this api you can get list of roles',response_model=list[schemas.ParentPage])
async def admin_pages(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):

    permission = checkpermissions(request_user=request_user ,db=db,page=14)
    if permission:
        #roles_list = crud.get_roles(db)
        return crud.get_roles(db)
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )




@app.post('/user/roles')
async def user_group(group_data:schemas.CreateGroupSch, db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=15)
    if permission:
    
        return crud.create_group(db,group_data)
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )

@app.put('/user/roles')
async def user_group_update(group_data:schemas.UpdateGroupSch, db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
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

@app.get('/user/role')
async def user_group_get(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=14)
    if permission:
        return crud.get_group(db)
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )



@app.get('/user/group/permissions/{id}')
async def group_permissions(id:int,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
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



@app.post('/user/group/permission')
async def group_permissions(id:int,per_list:list[int],db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=15)
    if permission:
        try:
            crud.delete_roles(db,id)
            permisison = [models.Roles(group_id=id,page_id=i) for i in per_list]
            bulk_create_per = crud.bulk_create_per(db,permisison)
            if not bulk_create_per:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="there is an error maybe foreignkey doesnot match"
            )
            return {'message':'everthing is good','success':True}
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="foreign key values doesnot match each other"
        )
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )
    
    

@app.get('/users/settings',response_model=Page[schemas.UsersSettingsSch])
async def get_user_list(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=5)
    if permission:
        try: 
            users_lsit = crud.get_user_list(db)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are seeing this error because of server error"
            )
        users = paginate(users_lsit)
        return users
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )



@app.post('/user/attach/role')
async def user_role_attach(role:schemas.UserRoleAttachSch,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=2)
    if permission:
        try:
            user_update = crud.user_role_attach(db,role)
            if user_update:
                return {'success':True,'message':'User attached to some group'}
            else:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="cannot find user you selected"
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are seeing this error because of server error"
            )
    else:
        raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="you do not have permission like this"
            )


@app.post('/brigadas')
async def create_brigada(form_data:schemas.UservsRoleCr,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=16)
    #if permission:
        try:
            crud.create_brigada(db,form_data)
            return  {'success':True,'message':"everything is fine"}
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="foreign key values doesnot match each other"
            )
    #else:
    #    raise HTTPException(
    #                    status_code=status.HTTP_403_FORBIDDEN,
    #                    detail="you do not have permission like this"
    #        )



@app.get('/brigadas',response_model=Page[schemas.GetBrigadaList])
async def get_list_brigada(sphere_status:Optional[int]=None,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=3)
    #if permission:
        
        users = crud.get_brigada_list(db,sphere_status=sphere_status)
        return paginate(users)
       

    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )
    

@app.get('/brigadas/{id}',response_model=schemas.GetBrigadaIdSch)
async def get_brigada_id(id:int,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=17)
    #if permission:
            
        brigrada = crud.get_brigada_id(db,id)
        if brigrada:
            return brigrada
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
       


    

@app.get('/users/for/brigada/{id}',response_model=list[schemas.UserGetlist])
async def user_for_brigada(id:int,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=17)
    #if permission:
            
        brigrada = crud.get_user_for_brig(db,id)
        if brigrada:
            return brigrada
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
        
       




@app.put('/brigadas')
async def update_brigada(form_data:schemas.UpdateBrigadaSch,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=17)
    #if permission:
        #try:
            brigrada = crud.update_brigada_id(db,form_data=form_data)

            if form_data.users:
                crud.set_null_user_brigada(db,form_data.id)
                crud.attach_user_brigads(db,form_data.users,form_data.id)
            else:
                crud.set_null_user_brigada(db,form_data.id)
            return {'success':True,'message':'everthing is ok','brigada':brigrada}



@app.post('/expanditure')
async def create_expanditure(form_data:schemas.ExpanditureSchema,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=28)
    if permission:
        try:
            crud.expanditure_create(db,form_data=form_data,brigada_id=request_user.brigada_id)
        except:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found exceptnion "
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )





@app.get('/me')
async def get_me(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status ==1:
        permissions = []
        for i in crud.get_roles_pages_super(db):
            permissions.append(i.id)
        role='superadmin'
    elif request_user.group_id and request_user.status !=2:
        group_id = request_user.group_id
        
        permissions = []
        role = request_user.group.name
        for i in crud.get_roles_pages(db,group_id):
            permissions.append(i.page_id)
    else:
        role = None
        permissions=[]
    return {'success':True,'username':request_user.username,'full_name':request_user.full_name,'role':role,'id':request_user.id,'permissions':permissions}



@app.put('/fillials')
async def update_fillials(form_data:schemas.UpdateFillialSch,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=23)
    if permission:
        fillials = crud.update_fillial_cr(db,form_data)
        if form_data.department_id:
            crud.update_fillil_origin(db,form_data=form_data)

        return fillials

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    



    

    
@app.get('/fillials',response_model=Page[schemas.GetFillialSch])
async def filter_fillials(origin:int,name:Optional[str]=None,country:Optional[str]=None,latitude:Optional[float]=None,longtitude:Optional[float]=None,fillial_status:Optional[int]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=29)
    if permission:
        return paginate(crud.filter_fillials(db,name=name,country=country,latitude=latitude,longtitude=longtitude,fillial_status=fillial_status,origin=origin))

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    

@app.get('/fillials/{id}',response_model=schemas.GetFillialSch)
async def get_fillials_id(id:UUID,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=23)
    if permission:
        return crud.get_fillial_id(db,id)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )




add_pagination(app)
add_pagination(router)
add_pagination(urls)

