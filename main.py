#----------import packages 
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from pydantic import ValidationError
import schemas
import bcrypt
import models
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import crud
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page,add_pagination
from secondmain import router
from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions,get_db,get_current_user
models.Base.metadata.create_all(bind=engine)
#--------token generation
JWT_SECRET_KEY = 'thisistokenforusersecretauth'   # should be kept secret
JWT_REFRESH_SECRET_KEY =  'thisistokenforusersecretrefresh'
ALGORITHM = "HS256"
from fastapi.staticfiles import StaticFiles

origins = ["*"]

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
#database connection
app = FastAPI()
app.include_router(router)
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
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
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
    



@app.get('/all/permissions',summary='from this api you can get list of roles')
async def admin_pages(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):

    if request_user.status!=1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    roles_list = crud.get_roles(db)
    
    return roles_list





@app.post('/user/roles')
async def user_group(group_data:schemas.CreateGroupSch, db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    
    return crud.create_group(db,group_data)

@app.put('/user/roles')
async def user_group_update(group_data:schemas.UpdateGroupSch, db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    updation = crud.update_group(db,group_data)
    if updation:
        return {'success':True,'message':'updated'}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cannot update becouse role id doesnot match"
        )

@app.get('/user/role')
async def user_group_get(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    return crud.get_group(db)


@app.get('/user/group/permissions/{id}')
async def group_permissions(id:int,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
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



@app.post('/user/group/permission')
async def group_permissions(id:int,per_list:list[int],db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
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
    
    

@app.get('/users/settings',response_model=Page[schemas.UsersSettingsSch])
async def get_user_list(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    try: 
        users_lsit = crud.get_user_list(db)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="You are seeing this error because of server error"
        )
    users = paginate(users_lsit)
    return users



@app.post('/user/attach/role')
async def user_role_attach(role:schemas.UserRoleAttachSch,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
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
    

@app.post('/brigadas')
async def create_brigada(form_data:schemas.UservsRoleCr,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='brigada')
    if permission:
        try:
            crud.create_brigada(db,form_data)
            return  {'success':True,'message':"everything is fine"}
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



@app.get('/brigadas',response_model=Page[schemas.GetBrigadaList])
async def get_list_brigada(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='brigada')
    if permission:
        
        users = crud.get_brigada_list(db)
        return paginate(users)
       

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    

@app.get('/brigadas/{id}',response_model=schemas.GetBrigadaIdSch)
async def get_brigada_id(id:int,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='brigada')
    if permission:
            
        brigrada = crud.get_brigada_id(db,id)
        if brigrada:
            return brigrada
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
       

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )


@app.put('/brigadas')
async def update_brigada(form_data:schemas.UpdateBrigadaSch,db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='brigada')
    if permission:
        try:
            brigrada = crud.update_brigada_id(db,form_data=form_data)
            if form_data.users:
                users = crud.attach_user_brigads(db,form_data.users,form_data.id)
            return {'success':True,'message':'everthing is ok','brigada':brigrada}
        except:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
       

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )


@app.get('/me')
async def get_me(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status ==1:
        permissions = '*'
        role='superadmin'
    elif request_user.group_id and request_user.status !=2:
        group_id = request_user.group_id
        
        permissions = {}
        role = request_user.group.name
        for i in crud.get_roles_pages(db,group_id):
            permissions[i.page.page_name]=True
    else:
        role = None
        permissions={}
    return {'success':True,'username':request_user.username,'full_name':request_user.full_name,'role':role,'id':request_user.id,'permissions':permissions}

@app.post('/fillials')
async def add_fillials(form_data:schemas.AddFillialSch,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='fillials')
    if permission:
        return crud.add_fillials(db,data=form_data)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )



@app.put('/fillials')
async def update_fillials(form_data:schemas.UpdateFillialSch,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='fillials')
    if permission:
        return crud.update_fillial_cr(db,form_data)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    


@app.get('/fillials',response_model=Page[schemas.GetFillialSch])
async def get_fillials(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='fillials')
    if permission:
        return paginate(crud.get_fillial_list(db))

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    

@app.get('/fillials/{id}',response_model=schemas.GetFillialSch)
async def get_fillials_id(id:int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='fillials')
    if permission:
        return crud.get_fillial_id(db,id)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )




add_pagination(app)
add_pagination(router)