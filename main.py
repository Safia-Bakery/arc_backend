# ----------import packages
from jose import JWTError, jwt

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import warnings
import pytz
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
    BackgroundTasks,
    Security,
)
import time
from pydantic import ValidationError
import schemas
import bcrypt
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
from typing import Optional
import models
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import crud
from database import engine, SessionLocal
from fastapi_pagination import paginate, Page, add_pagination

# from secondmain import router
from iikoview import urls
from hrcomments.routers.router import hrrouter
from users.routers.router import user_router
from users.schema import schema
from orders.routers.router import router
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orders.crud.query import get_fillials_unordered

  # Set the desired time for the function to run (here, 12:00 PM)
from microservices import (
    create_refresh_token,
    verify_password,
    create_access_token,
    checkpermissions,
    get_db,
    get_current_user,
    authiiko,
    getgroups,
    getproducts,
    get_prices,
    sendtotelegramchannel

)
from users.crud.query import all_users
from dotenv import load_dotenv
import os

models.Base.metadata.create_all(bind=engine)
load_dotenv()


# --------token generation
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
from fastapi.staticfiles import StaticFiles


origins = ["*"]

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")
# database connection
app = FastAPI()
app.include_router(router)
app.include_router(urls)
app.include_router(hrrouter)
app.include_router(user_router)
app.mount("/files", StaticFiles(directory="files"), name="files")
timezonetash = pytz.timezone("Asia/Tashkent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def scheduled_function(db: Session):
    key = authiiko()
    groups = getgroups(key=key)
    group_list = crud.synchgroups(db, groups)
    del groups
    products = getproducts(key=key)
    
    product_list = crud.synchproducts(db, grouplist=group_list, products=products)
    del products
    prices_inv = get_prices(key=key,department_id='c39aa435-8cdf-4441-8723-f532797fbeb9')
    crud.update_products_price(db=db,prices=prices_inv)
    del prices_inv
    prices_arc = get_prices(key=key,department_id='fe7dce09-c2d4-46b9-bab1-86be331ed641')
    crud.update_products_price(db=db,prices=prices_arc)
    del prices_arc

def meal_pushes(db:Session):
    branchs = get_fillials_unordered(db=db)
    
    text = ""
    all_user = all_users(db=db)
    for i in branchs:
        text += f"{i.name}\n"
    text = 'test'
    limit = 0
    for i in all_user:
        if limit == 30:
            time.sleep(2)
            sendtotelegramchannel(bot_token=BOT_TOKEN,chat_id=i.telegram_id,message_text=text)
            limit = 0
        else:
            limit += 1


@app.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger  = CronTrigger(hour=1, minute=20, second=00,timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(scheduled_function, trigger=trigger, args=[next(get_db())])
    scheduler.start()

@app.on_event("startup")
def meal_messages():
    scheduler = BackgroundScheduler()
    trigger  = CronTrigger(hour=20, minute=55, second=00,timezone=timezonetash)
    scheduler.add_job(meal_pushes, trigger=trigger,args=[next(get_db())])
    scheduler.start()

@app.post("/user/group/permission")
async def group_permissions(
    id: int,
    per_list: list[int],
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    permission = checkpermissions(request_user=request_user, db=db, page=15)
    if permission:
        try:
            crud.delete_roles(db, id)
            permisison = [models.Roles(group_id=id, page_id=i) for i in per_list]
            bulk_create_per = crud.bulk_create_per(db, permisison)
            if not bulk_create_per:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="there is an error maybe foreignkey doesnot match",
                )
            return {"message": "everthing is good", "success": True}
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="foreign key values doesnot match each other",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you do not have permission like this",
        )


@app.get("/users/settings", response_model=Page[schema.UsersSettingsSch])
async def get_user_list(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    permission = checkpermissions(request_user=request_user, db=db, page=5)
    if permission:
        try:
            users_lsit = crud.get_user_list(db)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are seeing this error because of server error",
            )
        users = paginate(users_lsit)
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you do not have permission like this",
        )


@app.post("/user/attach/role")
async def user_role_attach(
    role: schemas.UserRoleAttachSch,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    permission = checkpermissions(request_user=request_user, db=db, page=2)
    if permission:
        try:
            user_update = crud.user_role_attach(db, role)
            if user_update:
                return {"success": True, "message": "User attached to some group"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="cannot find user you selected",
                )
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="You are seeing this error because of server error",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you do not have permission like this",
        )


@app.post("/brigadas")
async def create_brigada(
    form_data: schemas.UservsRoleCr,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    try:
        crud.create_brigada(db, form_data)
        return {"success": True, "message": "everything is fine"}
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="foreign key values doesnot match each other",
        )


@app.get("/brigadas", response_model=Page[schemas.GetBrigadaList])
async def get_list_brigada(
    sphere_status: Optional[int] = None,
    department: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    users = crud.get_brigada_list(
        db, sphere_status=sphere_status, department=department
    )
    return paginate(users)


@app.get("/brigadas/{id}", response_model=schemas.GetBrigadaIdSch)
async def get_brigada_id(
    id: int,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    brigrada = crud.get_brigada_id(db, id)
    if brigrada:
        return brigrada
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


@app.get("/users/for/brigada/{id}", response_model=list[schemas.UserGetlist])
async def user_for_brigada(
    id: int,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    brigrada = crud.get_user_for_brig(db, id)
    if brigrada:
        return brigrada
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


@app.put("/brigadas")
async def update_brigada(
    form_data: schemas.UpdateBrigadaSch,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    brigrada = crud.update_brigada_id(db, form_data=form_data)

    if form_data.users:
        crud.set_null_user_brigada(db, form_data.id)
        crud.attach_user_brigads(db, form_data.users, form_data.id)
    else:
        crud.set_null_user_brigada(db, form_data.id)
    return {"success": True, "message": "everthing is ok", "brigada": brigrada}


@app.post("/expanditure")
async def create_expanditure(
    form_data: schemas.ExpanditureSchema,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    permission = checkpermissions(request_user=request_user, db=db, page=28)
    if permission:
        try:
            crud.expanditure_create(
                db, form_data=form_data, brigada_id=request_user.brigada_id
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found exceptnion "
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not super user"
        )


@app.get("/me")
async def get_me(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    if request_user.status == 1:
        permissions = []
        for i in crud.get_roles_pages_super(db):
            permissions.append(i.id)
        role = "superadmin"
    elif request_user.group_id and request_user.status != 2:
        group_id = request_user.group_id

        permissions = []
        role = request_user.group.name
        for i in crud.get_roles_pages(db, group_id):
            permissions.append(i.page_id)
    else:
        role = None
        permissions = []
    return {
        "success": True,
        "username": request_user.username,
        "full_name": request_user.full_name,
        "role": role,
        "id": request_user.id,
        "permissions": permissions,
    }


@app.put("/fillials")
async def update_fillials(
    form_data: schemas.UpdateFillialSch,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    # permission = checkpermissions(request_user=request_user, db=db, page=23)
    # if permission:
    fillials = crud.update_fillial_cr(db, form_data)
    if form_data.department_id:
        crud.update_fillil_origin(db, form_data=form_data)
    return fillials
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="You are not super user"
    #     )


@app.get("/fillials", response_model=Page[schemas.GetFillialSch])
async def filter_fillials(
    origin: int,
    name: Optional[str] = None,
    country: Optional[str] = None,
    latitude: Optional[float] = None,
    longtitude: Optional[float] = None,
    fillial_status: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    return paginate(
        crud.filter_fillials(
            db,
            name=name,
            country=country,
            latitude=latitude,
            longtitude=longtitude,
            fillial_status=fillial_status,
            origin=origin,
        )
    )

    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN, detail="You are not super user"
    #    )


@app.get("/fillials/{id}", response_model=schemas.GetFillialSch)
async def get_fillials_id(
    id: UUID,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    
    return crud.get_fillial_id(db, id)

    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="You are not super user"
    #     )


add_pagination(app)
add_pagination(router)
add_pagination(urls)

