# ----------import packages
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
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
from app.utils.utils import get_current_user_for_docs
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
from app.routes.v2.endpoints.calendars import calendar_router

# from secondmain import router
from iikoview import urls
from hrcomments.routers.router import hrrouter
from users.routers.router import user_router
from users.schema import schema
from queries import it_query
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
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from routes.inv_routes import inv_router
from routes.it_routes import it_router
from routes.arc_routes import arc_routes
from app.routes.v2.endpoints.kru_users import kru_users_router
from app.routes.v2.endpoints.kru_categories import kru_categories
from app.routes.v2.endpoints.kru_tasks_finished import kru_tasks_finished
from app.routes.v2.endpoints.kru_tasks import kru_tasks_router
from app.routes.v2.endpoints.files import file_router
from app.routes.v2.endpoints.branchs import branchs_router
from app.routes.v2.endpoints.it_extra import it_extra_router
from app.routes.v2.endpoints.it_requests import it_requests_router
from app.routes.v2.endpoints.category import category_router
from app.routes.v2.endpoints.inventory_requests import inv_requests_router
from app.routes.v2.endpoints.tool_balance import tool_balance_router
from app.routes.v2.endpoints.arc_factory_requests import arc_factory_requests
from app.routes.v2.endpoints.arc_factory_managers import arc_factory_managers
from app.routes.v2.endpoints.arc_factory_divisions import arc_factory_divisions
from app.routes.v2.endpoints.collector_users import collector_users_router
from app.routes.v2.endpoints.groups import groups_router
from app.routes.v2.endpoints.collector_orders import collector_orders_router
from app.routes.v2.endpoints.toolparents import toolparents_router
from app.routes.v2.endpoints.uniform_category import uniform_category_router
from app.routes.v2.endpoints.uniform_requests import uniform_requests_router
from app.routes.v2.endpoints.appointments import appointments_router
from app.routes.v2.endpoints.positions import positions_router
from app.routes.v2.endpoints.inventory_tools import inv_requests_tools_router
from app.routes.v2.endpoints.schedules import schedules_router
from app.routes.v2.endpoints.kru_reports import kru_reports_router
from app.routes.v2.endpoints.branch_tools import branch_tools_router
from app.routes.v2.endpoints.manager_branchs import factory_branchs_router
from app.routes.v2.endpoints.video_control import video_requests_router
from app.routes.v2.endpoints.iikotransfers import iiko_transfer_router
from app.routes.v2.endpoints.coins import coins_router
# models.Base.metadata.create_all(bind=engine)
load_dotenv()


# --------token generation
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
BOT_TOKEN = os.environ.get("BOT_TOKEN")


origins = ["https://service.safiabakery.uz",'https://admin.service.safiabakery.uz',"http://localhost:5173"]

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")
# database connection
app = FastAPI(swagger_ui_parameters = {"docExpansion":"none"},docs_url=None, redoc_url=None, openapi_url=None,)
app.include_router(calendar_router, tags=["calendars"])
app.include_router(factory_branchs_router,tags=['Factory Managers'])
app.include_router(iiko_transfer_router, prefix="/api/v2", tags=["iiko"])
app.include_router(it_extra_router, prefix="/api/v2", tags=["IT"])
app.include_router(it_requests_router, prefix="/api/v2", tags=["IT"])
app.include_router(video_requests_router, prefix="/api/v2", tags=["VIDEO"])
app.include_router(category_router, prefix="/api/v2", tags=["Category"])
app.include_router(inv_requests_router, prefix="/api/v2", tags=["Inventory"])
# app.include_router(tool_balance_cron_router, prefix="/api/v2", tags=["Cron tool balances"])
app.include_router(tool_balance_router, prefix="/api/v2", tags=["Tool balances"])
app.include_router(arc_factory_requests, prefix="/api/v2", tags=["Arc factory"])
app.include_router(arc_factory_managers, prefix="/api/v2", tags=["Arc factory"])
app.include_router(arc_factory_divisions, prefix="/api/v2", tags=["Arc factory"])
app.include_router(collector_users_router, tags=["Collector project"])
app.include_router(collector_orders_router, tags=["Collector project"])
app.include_router(groups_router, tags=["Groups"])
app.include_router(toolparents_router, tags=["Tool Parents"])
app.include_router(coins_router,tags=['Coins'])
app.include_router(uniform_category_router, prefix="/api/v2", tags=['UNIFORM'])
app.include_router(uniform_requests_router, prefix="/api/v2", tags=['UNIFORM'])
app.include_router(schedules_router, prefix="/api/v2", tags=['SCHEDULES'])
app.include_router(appointments_router, prefix="/api/v2", tags=['APPOINTMENTS'])
app.include_router(positions_router, prefix="/api/v2", tags=['Positions'])
app.include_router(router)
app.include_router(urls)
app.include_router(hrrouter)
app.include_router(user_router)
app.include_router(inv_router)
app.include_router(it_router)
app.include_router(arc_routes)
app.include_router(kru_users_router, tags=["KRU"])
app.include_router(kru_categories, tags=["KRU"])
app.include_router(kru_tasks_finished, tags=["KRU"])
app.include_router(kru_tasks_router, tags=["KRU"])
app.include_router(kru_reports_router, tags=["KRU"])
app.include_router(branch_tools_router, tags=["KRU"])
app.include_router(file_router, tags=["Files"])
app.include_router(branchs_router, tags=["Branchs"])
app.include_router(inv_requests_tools_router,prefix="/api/v2", tags=["Inventory"])



app.mount("/files", StaticFiles(directory="files"), name="files")

timezonetash = pytz.timezone("Asia/Tashkent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(current_user: str = Depends(get_current_user_for_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI",swagger_ui_parameters={"docExpansion": "none"},)


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(current_user: str = Depends(get_current_user_for_docs)):
    return get_openapi(title="Custom OpenAPI", version="1.0.0", routes=app.routes)


def scheduled_function(db: Session):
    key = authiiko()
    groups = getgroups(key=key)
    group_list = crud.synchgroups(db, groups)
    del groups
    products = getproducts(key=key)

    product_list = crud.synchproducts(db, grouplist=group_list, products=products)
    del products

    prices_arc = get_prices(key=key,department_id='fe7dce09-c2d4-46b9-bab1-86be331ed641')
    crud.update_products_price(db=db,prices=prices_arc,store_id_checker='4aafb5af-66c3-4419-af2d-72897f652019')
    del prices_arc
    prices_inv = get_prices(key=key,department_id='c39aa435-8cdf-4441-8723-f532797fbeb9')
    crud.update_products_price(db=db,prices=prices_inv,store_id_checker="0bfe01f2-6864-48f5-a79e-c885dc76116a")
    del prices_inv

def meal_pushes(db:Session):
    branchs = get_fillials_unordered(db=db)
    
    text = "Филиалы не отправившие заявку на Стафф питание🥘\n\n"
    all_user = all_users(db=db)
    for i in branchs:
        text += f"{i.name}\n"
    text += "\n\nНеобходимо отправить заявку до 16:00 ❗️"
    limit = 0
    send_users = []
    for i in all_user:
        if i.id not in send_users:
            sendtotelegramchannel(bot_token=BOT_TOKEN,chat_id=i.telegram_id,message_text=text)
            if limit == 30:
                time.sleep(2)
                limit = 0
            else:
                limit += 1
            send_users.append(i.id)
    del all_user
    del branchs
    return True

def it_close_request(db:Session):
    queries = it_query.it_query_with_status(db=db,status=6)
    for i in queries:
        it_query.update_status_it(db=db,id=i.id,status=3)
    del queries
    queries = it_query.it_query_with_status(db=db,status=8)
    for i in queries:
        it_query.update_status_it(db=db,id=i.id,status=4)
    del queries
    return True


@app.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    trigger  = CronTrigger(hour=1, minute=20, second=00,timezone=timezonetash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(scheduled_function, trigger=trigger, args=[next(get_db())])
    scheduler.start()





# @app.on_event("startup")
# def it_query_checker():
#     scheduler = BackgroundScheduler()
#     trigger = CronTrigger(minute="*/30")  # Trigger every half hour
#     scheduler.add_job(it_close_request, trigger=trigger, args=[next(get_db())])
#     scheduler.start()


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


@app.get("/users/for/brigada/{id}", response_model=Page[schemas.UserGetlist])
async def user_for_brigada(
    id: int,
    name: Optional[str] = None,
    department: Optional[int] = None,
    sphere_status: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    brigrada = crud.get_user_for_brig(db, id,name=name,department=department,sphere_status=sphere_status)
    return paginate(brigrada)



@app.put("/brigadas")
async def update_brigada(
    form_data: schemas.UpdateBrigadaSch,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    brigada = crud.update_brigada_id(db, form_data=form_data)

    if form_data.users:
        crud.set_null_user_brigada(db, form_data.id)
        crud.attach_user_brigads(db, form_data.users, form_data.id)
    else:
        crud.set_null_user_brigada(db, form_data.id)
    return {"success": True, "message": "everthing is ok", "brigada": brigada}


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

    fillials = crud.update_fillial_cr(db, form_data)
    if form_data.department_id:
        crud.update_fillil_origin(db, form_data=form_data)
    return fillials


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


@app.get("/fillials/{id}", response_model=schemas.GetFillialSch)
async def get_fillials_id(
    id: UUID,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    
    return crud.get_fillial_id(db, id)


@app.post("/fillials",tags=["fillials"])
async def create_fillial(
    form_data: schemas.AddFillialSch,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query =crud.add_fillials(db=db,data=form_data)
    return query


@app.post("/store",tags=["fillials"])
async def create_store(
    form_data: schemas.AddStoreSh,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query =crud.add_store(db=db,form_data=form_data)
    return query



add_pagination(app)
add_pagination(router)
add_pagination(urls)



