#----------import packages 
from datetime import datetime, timedelta,date,time
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException,UploadFile,status,BackgroundTasks
from pydantic import ValidationError
import statisquery
import schemas
import bcrypt
from typing import Annotated,Dict
from uuid import UUID
import models
from microservices import sendtotelegramchannel,sendtotelegram,sendtotelegramaddcomment,inlinewebapp
from typing import Optional
import crud
from microservices import get_current_user,get_db
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page,add_pagination
from dotenv import load_dotenv
from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions
#from main import get_db,get_current_user
from fastapi import APIRouter,Form
from users.schema import schema
import os
from orders.crud import query
from orders.utils import util
from orders.schema import schema_router
load_dotenv()
router = APIRouter()
bot_token = os.environ.get('BOT_TOKEN')

BASE_URL = 'https://api.service.safiabakery.uz/'
FRONT_URL = 'https://admin.service.safiabakery.uz/'



@router.post('/category')
async def add_category(name:Annotated[str,Form()],department:Annotated[int,Form()],finish_time:Annotated[time,Form()]=None,description:Annotated[str,Form()]=None,status:Annotated[int,Form()]=1,urgent:Annotated[bool,Form()]=True,sphere_status:Annotated[int,Form()]=None,file:UploadFile=None,sub_id:Annotated[int,Form()]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    if file is not None:
        #for file in image:
        folder_name = f"files/{util.generate_random_filename()+file.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        file = folder_name
    return crud.add_category_cr(db=db,finish_time=finish_time,name=name,description=description,status=status,urgent=urgent,department=department,sphere_status=sphere_status,sub_id=sub_id,file=file)

@router.put('/category')
async def update_category(id:Annotated[int,Form()],name:Annotated[str,Form()]=None,description:Annotated[str,Form()]=None,status:Annotated[int,Form()]=None,urgent:Annotated[bool,Form()]=None,department:Annotated[int,Form()]=None,sphere_status:Annotated[int,Form()]=None,file:UploadFile=None,sub_id:Annotated[int,Form()]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    if file is not None:
        #for file in image:
        folder_name = f"files/{util.generate_random_filename()+file.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        file = folder_name
    response = crud.update_category_cr(db=db,id=id,file=file,name=name,description=description,status=status,urgent=urgent,department=department,sphere_status=sphere_status,sub_id=sub_id)
    if response:
        return response
    else:
        
        return {'message':'not found'}

@router.get('/category',response_model=Page[schemas.GetCategorySch])
async def filter_category(sphere_status:Optional[int]=None,sub_id:Optional[int]=None,department:Optional[int]=None,category_status:Optional[int]=None,name:Optional[str]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):

        response = crud.filter_category(db,category_status=category_status,name=name,sub_id=sub_id,department=department,sphere_status=sphere_status)
        return paginate(response)


@router.get('/category/{id}',response_model=schemas.GetCategorySch)
async def get_category_id(id:int,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    try:
            response = crud.get_category_id(db,id)
            return response
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="info with this id not found "
        )

@router.get('/request',response_model=Page[schemas.GetRequestList])
async def filter_request(department:Optional[int]=None,sub_id:Optional[int]=None,id:Optional[int]=None,category_id:Optional[int]=None,fillial_id:Optional[UUID]=None,created_at:Optional[date]=None,request_status:Optional[int]=None,user:Optional[str]=None,sphere_status:Optional[int]=None,arrival_date:Optional[date]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
        if request_user.brigada_id:
            requestdata= crud.filter_request_brigada(db,id=id,sub_id=sub_id,category_id=category_id,fillial_id=fillial_id,request_status=request_status,created_at=created_at,user=user,brigada_id=request_user.brigada_id,sphere_status=sphere_status,department=department,arrival_date=arrival_date)
            return paginate(requestdata)
        request_list = crud.filter_requests_all(db,sub_id=sub_id,department=department,id=id,category_id=category_id,fillial_id=fillial_id,request_status=request_status,created_at=created_at,user=user,sphere_status=sphere_status,arrival_date=arrival_date)
        return paginate(request_list)
    

@router.get('/request/{id}',response_model=schemas.GetRequestid)
async def get_request_id(id:int,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):

        try:
            request_list = crud.get_request_id(db,id) 
            return request_list
        except:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="not fund"
        )



@router.put('/request/attach/brigada')
async def put_request_id(form_data:schemas.AcceptRejectRequest,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
            request_list = crud.acceptreject(db,form_data=form_data,user=request_user.full_name)
            if form_data.status == 1:
                try:
                    brigada_id = request_list.brigada.id
                    brigader_telid = crud.get_user_brig_id(db,brigada_id).telegram_id
                    sendtotelegramchannel(bot_token=bot_token,chat_id=brigader_telid,message_text=f"{request_list.brigada.name} вам назначена заявка, #{request_list.id}s {request_list.fillial.name}")
                except:
                    pass
                if request_list.category.department==1:
                    try:
                        sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, на вашу заявку #{request_list.id}s назначена команда🚙: {request_list.brigada.name}")
                    except:
                        pass
                if request_list.category.department==5:
                    try:
                        sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, на вашу заявку #{request_list.id}s по Запросу машины🚛: В процессе.")
                    except:
                        pass
                if request_list.category.department==3:
                    try:
                        finishing_time = request_list.finishing_time
                        sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Маркетингу: В процессе.\n\n⏳Примерный срок завершения: {finishing_time}")
                    except:
                        pass
            if form_data.status == 2:
                if request_list.category.department==5:
                    try:
                        sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, мы отправили транспорт по вашему запросу #{request_list.id}s Ожидайте его прибытия.")
                    except:
                        pass  
                     
            if form_data.status ==3:
                url=f"{FRONT_URL}tg/order-rating/{request_list.id}?user_id={request_list.user.id}&department={request_list.category.department}&sub_id={request_list.category.sub_id}"
                if request_list.category.department==3:
                    try:
                        inlinewebapp(bot_token=bot_token,
                                     chat_id=request_list.user.telegram_id,
                                     message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Маркетингу: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                                     url=url)
                    except:
                        pass
                if request_list.category.department==5:
                     
                    try:
                        inlinewebapp(bot_token=bot_token,
                                     chat_id=request_list.user.telegram_id,
                                     message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Запросу машины🚛: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                                     url=url)
                    except:
                        pass
                if request_list.category.department==1:
                    try:
                        inlinewebapp(bot_token=bot_token,
                                     chat_id=request_list.user.telegram_id,
                                     message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по APC: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                                     url=url)
                    except:
                        pass
                if request_list.category.department==6:
                    try:
                        inlinewebapp(bot_token=bot_token,
                                     chat_id=request_list.user.telegram_id,
                                     message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                                     url=url)
                    except:
                        pass

            if form_data.status==4:
                sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Ваша заявка #{request_list.id}s была отменена по причине: {request_list.deny_reason}")
            if request_list:
                return request_list
            else:
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not fund")

@router.post('/request')
async def get_category(category_id:int,fillial_id:UUID,description:str,files:list[UploadFile]=None,cat_prod:list[int]=None,factory:Optional[bool]=False,location:Optional[Dict[str,str]]=None,size:Optional[str]=None,bread_size:Optional[str]=None,arrival_date:Optional[datetime]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user),product:Optional[str]=None):
        #try:
            category_query = crud.get_category_id(db=db,id=category_id)

            if category_query.sub_id:
                origin = None
            else:
                origin=1
            if not factory:
                filliald_od = crud.filterbranchchildid(db,fillial_id,origin=origin)
                sklad_id = filliald_od.id
            if factory:
                sklad_id = fillial_id
            
            responserq = crud.add_request(db,category_id=category_id,description=description,fillial_id=sklad_id,product=product,user_id=request_user.id,is_bot=0,size=size,arrival_date=arrival_date,bread_size=bread_size,location=location)
            if cat_prod is not None:
                for i in cat_prod:
                    query.add_product_request(db=db,request_id=responserq.id,product_id=i)
            
            file_obj_list = []
            #parsed_datetime = datetime.strptime(responserq.created_at,"%Y-%m-%dT%H:%M:%S.%f")
            formatted_datetime_str = responserq.created_at.strftime("%Y-%m-%d %H:%M")
            text  = f"📑Заявка № {responserq.id}\n\n📍Филиал: {responserq.fillial.parentfillial.name}\n"\
                                    f"🕘Дата поступления заявки: {formatted_datetime_str}\n\n"\
                                    f"🔰Категория проблемы: {responserq.category.name}\n"\
                                    f"⚙️ Название оборудования: {responserq.product}\n"\
                                    f"💬Комментарии: {responserq.description}"
            
            
            if files:
                for file in files:
                    file_path = f"files/{file.filename}"
                    with open(file_path, "wb") as buffer:
                        while True:
                            chunk = await file.read(1024)
                            if not chunk:
                                break
                            buffer.write(chunk)
                    file_obj_list.append(models.Files(request_id=responserq.id,url=file_path))
            crud.bulk_create_files(db,file_obj_list)
            keyboard = [
            ]
            if responserq.file:
                for i in responserq.file:
                    keyboard.append({'text':'Посмотреть фото/видео',"url":f"{BASE_URL}{i.url}"})
            if responserq.category.sphere_status==1 and responserq.category.department==1:
                sendtotelegram(bot_token=bot_token,chat_id='-1001920671327',message_text=text,keyboard=keyboard)
            if responserq.category.sphere_status==2 and responserq.category.department==1:
                sendtotelegram(bot_token=bot_token,chat_id='-1001831677963',message_text=text,keyboard=keyboard)
            
            return {'success':True,'message':'everything is saved'}


@router.get('/categories/fillials',summary='you can get list of fillials and categories when you are creating request')
async def get_category_and_fillials(db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=25)
    if permission:
        try:
            categories = crud.get_category_list(db)
            fillials = crud.get_fillial_list(db)
            return {'categories':categories,'fillials':fillials}
        except:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="this is server error "
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    




@router.get('/users',response_model=Page[schemas.UserGetlist])
async def filter_user(full_name:Optional[str]=None,username:Optional[str]=None,role_id:Optional[int]=None,phone_number:Optional[str]=None,user_status:Optional[int]=None,position:Optional[bool]=True,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
            users = crud.filter_user(db,user_status=user_status,username=username,phone_number=phone_number,role_id=role_id,full_name=full_name,position=position)
            return paginate(users)


@router.put('/users',response_model=schemas.UserGetlist)
async def filter_user(form_data:schemas.UserUpdateAll,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
        updateuser = crud.update_user(db,form_data=form_data)
        return updateuser

@router.get('/users/{id}',response_model=schemas.GetUserIdSch)
async def get_user_with_id(id:int,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
            users = crud.get_user_id(db,id)
            if users:
                return users
            else: 
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )

@router.post('/tools',response_model=schemas.CreateTool)
async def get_user_with_id(form_data:schemas.CreateTool,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='onlysuperadmin')
    if permission:
        
        tools = crud.create_tool(db,form_data)
        return tools

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )



@router.get('/tools',response_model=Page[schemas.GetToolList])
async def get_tool_list(db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    try:
        query_from = crud.get_list_tools(db)
        return paginate(query_from)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="database not found"
        )

@router.get('/get/fillial/fabrica',response_model=Page[schemas.GetFillialChild])
async def get_fillials_fabrica(db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    return paginate(crud.getfillialchildfabrica(db))


@router.get('/get/files')
async def get_files_another_service(background_task:BackgroundTasks,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    background_task.add_task(statisquery.get_files(db))

    return {'success':True}


@router.post('/send/message')
async def send_message_to_users(message:str,background_task:BackgroundTasks,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    background_task.add_task(statisquery.send_to_user_message(db=db,message=message))
    return {'success':True}

@router.get('/v1/stats/marketing/pie')
async def marketing_pie_stats(timer:int,created_at:date,finished_at:date,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    table = query.marketing_table(db=db,created_at=created_at,finished_at=finished_at,timer=timer)
    pie = query.marketing_pie(db=db,created_at=created_at,finished_at=finished_at)
    order = {'pie':pie,'table':table}
    return order

@router.get('/v1/stats/marketing/cat')
async def marketing_cat_stats(created_at:date,finished_at:date,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    table = query.category_percent(db=db,created_at=created_at,finished_at=finished_at)
    pie = query.category_pie(db=db,created_at=created_at,finished_at=finished_at)
    return {'tables':table,'pie':pie}

@router.put('/v1/request/redirect',response_model=schemas.GetRequestid)
async def redirect_request(form_data:schema_router.RedirectRequest,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    db_query = query.redirect_request(db=db,form_data=form_data)
    return db_query


@router.get('/v1/department/count')
async def counter_department(db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    db_query = query.department_counter(db=db)
    return {'counter':db_query,'comment':'first data inside list is department id ||| second data is sphere_status ||| third data is number of new requests'}


@router.post('/v1/cat/product',response_model=schema_router.UpdateGetCatProduct)
async def create_cat_product(category_id:Annotated[int,Form()],name:Annotated[str,Form()],status:Annotated[int,Form()]=1,image:Annotated[UploadFile,Form()]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    if image:
        file_path = f"files/{util.generate_random_filename()}{image.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path=None
    db_query = query.createcat_product(category_id=category_id,name=name,image=file_path,status=status,db=db)
    return db_query


@router.put('/v1/cat/product',response_model=schema_router.UpdateGetCatProduct)
async def update_cat_product(id:Annotated[int,Form()],status:Annotated[int,Form()]=None,category_id:Annotated[int,Form()]=None,name:Annotated[str,Form()]=None,image:Annotated[UploadFile,Form()]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    if image:
        file_path = f"files/{util.generate_random_filename()}{image.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path=None
    db_query = query.createcat_product(id=id,name=name,category_id=category_id,status=status,image=file_path,db=db)
    return db_query


@router.get('/v1/cat/product',response_model=list[schema_router.UpdateGetCatProduct])
async def query_cat_product(id:Optional[int]=None,category_id:Optional[int]=None,name:Optional[str]=None,db:Session=Depends(get_db),request_user:schema.UserFullBack=Depends(get_current_user)):
    db_query = query.querycat_product(db=db,id=id,name=name,category_id=category_id)
    return db_query


