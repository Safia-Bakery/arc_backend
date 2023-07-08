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
from microservices import create_refresh_token,verify_password,create_access_token
models.Base.metadata.create_all(bind=engine)

#--------token generation
JWT_SECRET_KEY = 'thisistokenforusersecretauth'   # should be kept secret
JWT_REFRESH_SECRET_KEY =  'thisistokenforusersecretrefresh'
ALGORITHM = "HS256"

origins = ["*"]

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
#database connection
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------get user from token
async def get_current_user(token: str = Depends(reuseable_oauth),db:Session=Depends(get_db)) -> schemas.User:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        expire_date = payload.get('exp')
        sub = payload.get('sub')
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = crud.get_user(db,   sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user

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

@app.post('/register', summary="Create access and refresh tokens for user",response_model=schemas.User)
async def register(form_data: schemas.UserCreate,db:Session=Depends(get_db)):
    try:
        user = crud.create_user(db,form_data)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist"
        )
    return schemas.User(id=user.id,username=user.username,full_name=user.full_name)



@app.get('/all/roles',summary='from this api you can get list of roles')
async def admin_pages(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):

    if request_user.status!=1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    roles_list = crud.get_roles(db)
    
    return roles_list





@app.post('/user/group')
async def user_group(form_data:schemas.CreateGroupSch, db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
    if request_user.status !=1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    
    return crud.create_group(db,form_data)
@app.get('/user/group')
async def user_group(db:Session=Depends(get_db),request_user: schemas.UserFullBack = Depends(get_current_user)):
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
    role_list = crud.get_roles(db)

    permission_list = crud.get_permissions(db,id=id)
    permission_list = [ i.page_id for i in permission_list]
    return {'permissions':permission_list,'roles':role_list}



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
            detail="You are not super user"
        )
        return {'message':'hello'}
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not super user"
        )
    
    


add_pagination(app)