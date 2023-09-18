#----------import packages 
from jose import JWTError, jwt
from datetime import datetime, timedelta,date
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from pydantic import ValidationError
import schemas
import bcrypt
from typing import Annotated
from uuid import UUID
import models
from microservices import sendtotelegramchannel,sendtotelegram,sendtotelegramaddcomment
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import crud
from microservices import get_current_user,get_db
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page,add_pagination
from dotenv import load_dotenv
from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions
#from main import get_db,get_current_user
from fastapi import APIRouter
import os
load_dotenv()
router = APIRouter()
bot_token = os.environ.get('BOT_TOKEN')

BASE_URL = 'https://backend.service.safiabakery.uz/'

@router.post('/category')
async def add_category(form_data:schemas.AddCategorySch,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=20)
    #if permission:
        return crud.add_category_cr(db,form_data)

    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )




@router.put('/category')
async def update_category(form_data:schemas.UpdateCategorySch,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=21)
    #if permission:
        response = crud.update_category_cr(db,form_data)
        if response:
            return response
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )
    

#@router.get('/category',response_model=Page[schemas.GetCategorySch])
#async def get_category(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
#    permission = checkpermissions(request_user=request_user,db=db,page='category')
#    if permission:
#        response = crud.get_category_list(db)
#        return paginate(response)
#
#    else:
#        raise HTTPException(
#            status_code=status.HTTP_403_FORBIDDEN,
#            detail="You are not super user"
#        )
    


@router.get('/category',response_model=Page[schemas.GetCategorySch])
async def filter_category(sphere_status:Optional[int]=None,sub_id:Optional[int]=None,department:Optional[int]=None,category_status:Optional[int]=None,name:Optional[str]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=6)
    #if permission:
        response = crud.filter_category(db,category_status=category_status,name=name,sub_id=sub_id,department=department,sphere_status=sphere_status)
        return paginate(response)

    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )


@router.get('/category/{id}',response_model=schemas.GetCategorySch)
async def get_category_id(id:int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=21)
    try:
        #if permission:
            response = crud.get_category_id(db,id)
            return response
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="info with this id not found "
        )

    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )
    


    

#@router.get('/request',response_model=Page[schemas.GetRequestList])
#async def get_request(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
#    permission = checkpermissions(request_user=request_user,db=db,page='requests')
#    if permission:
#        try:
#            if request_user.brigada_id:
#                requestdata= crud.get_request_list_for_brigada(db,request_user.brigada_id)
#                return paginate(requestdata)
#            request_list = crud.get_request_list(db)
#            return paginate(request_list)
#        except:
#            raise HTTPException(
#            status_code=status.HTTP_409_CONFLICT,
#            detail="not fund"
#        )
#    else:
#        raise HTTPException(
#            status_code=status.HTTP_403_FORBIDDEN,
#            detail="You are not super user"
#        )
@router.get('/request',response_model=Page[schemas.GetRequestList])
async def filter_request(department:int,sub_id:Optional[int]=None,id:Optional[int]=None,category_id:Optional[int]=None,fillial_id:Optional[UUID]=None,created_at:Optional[date]=None,request_status:Optional[int]=None,user:Optional[str]=None,sphere_status:Optional[int]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):

        
        if request_user.brigada_id:
            requestdata= crud.filter_request_brigada(db,id=id,sub_id=sub_id,category_id=category_id,fillial_id=fillial_id,request_status=request_status,created_at=created_at,user=user,brigada_id=request_user.brigada_id,sphere_status=sphere_status,department=department)
            return paginate(requestdata)
        request_list = crud.filter_requests_all(db,sub_id=sub_id,department=department,id=id,category_id=category_id,fillial_id=fillial_id,request_status=request_status,created_at=created_at,user=user,sphere_status=sphere_status)
        return paginate(request_list)
    





@router.get('/request/{id}',response_model=schemas.GetRequestid)
async def get_request_id(id:int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):

        try:
            request_list = crud.get_request_id(db,id)

            return request_list
        except:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="not fund"
        )



    

@router.put('/request/attach/brigada')
async def put_request_id(form_data:schemas.AcceptRejectRequest,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):

        #try:
            request_list = crud.acceptreject(db,form_data=form_data,user=request_user.full_name)
            if form_data.status == 1:
                try:
                    brigada_id = request_list.brigada.id
                    brigader_telid = crud.get_user_brig_id(db,brigada_id).telegram_id
                    sendtotelegramchannel(bot_token=bot_token,chat_id=brigader_telid,message_text=f"{request_list.brigada.name} вам назначена заявка, №{request_list.id} {request_list.fillial.name}")
                except:
                    pass
                if request_list.category.department==1:
                    try:
                        sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, на вашу заявку №{request_list.id} назначена команда🚙: {request_list.brigada.name}")
                    except:
                        pass
                else:
                    try:
                        sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки №{request_list.id} по Маркетингу: В процессе.")
                    except:
                        pass
            if form_data.status ==3:
                if request_list.category.department==3:
                     
                    try:
                        sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки №{request_list.id} по Маркетингу: Завершен.")
                    except:
                        pass
                else:
                    try:
                        sendtotelegramaddcomment(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки №{request_list.id} по APC: Завершен.")
                    except:
                        pass
            if form_data.status==4:
                sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Ваша заявка {request_list.id} была отменена.")
            if request_list:
                return request_list
            else:
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not fund"
        )
        #except:
        #    raise HTTPException(
        #    status_code=status.HTTP_409_CONFLICT,
        #    detail="not fund"
        #)









@router.post('/request')
async def get_category(files:list[UploadFile],category_id:int,fillial_id:UUID,description:str,factory:Optional[bool]=False,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user),product:Optional[str]=None):
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
            
            responserq = crud.add_request(db,category_id=category_id,description=description,fillial_id=sklad_id,product=product,user_id=request_user.id,is_bot=0)
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
        #except:
        #    raise HTTPException(
        #    status_code=status.HTTP_409_CONFLICT,
        #    detail="not id not found"
        #)









@router.get('/categories/fillials',summary='you can get list of fillials and categories when you are creating request')
async def get_category_and_fillials(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
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
    

#@router.get('/users',response_model=Page[schemas.UserGetlist])
#async def get_user_lisrt(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
#    permission = checkpermissions(request_user=request_user,db=db,page='users')
#    if permission:
#        
#            users = crud.get_user_list(db)
#            return paginate(users)
#       
#
#    else:
#        raise HTTPException(
#            status_code=status.HTTP_403_FORBIDDEN,
#            detail="You are not super user"
#        )


@router.get('/users',response_model=Page[schemas.UserGetlist])
async def filter_user(full_name:Optional[str]=None,username:Optional[str]=None,role_id:Optional[int]=None,phone_number:Optional[str]=None,user_status:Optional[int]=None,position:Optional[bool]=True,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=5)
    #if permission:

            users = crud.filter_user(db,user_status=user_status,username=username,phone_number=phone_number,role_id=role_id,full_name=full_name,position=position)
            return paginate(users)


    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )

@router.put('/users',response_model=schemas.UserGetlist)
async def filter_user(form_data:schemas.UserUpdateAll,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=19)
    #if permission:
        
        updateuser = crud.update_user(db,form_data=form_data)
        return updateuser
    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )




@router.get('/users/{id}',response_model=schemas.GetUserIdSch)
async def get_user_with_id(id:int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=19)
    #if permission:
        
            users = crud.get_user_id(db,id)
            if users:
                return users
            else: 
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )

    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )

@router.post('/tools',response_model=schemas.CreateTool)
async def get_user_with_id(form_data:schemas.CreateTool,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
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
async def get_tool_list(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    try:
        query_from = crud.get_list_tools(db)
        return paginate(query_from)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="database not found"
        )




@router.get('/get/fillial/fabrica',response_model=Page[schemas.GetFillialChild])
async def get_fillials_fabrica(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    return paginate(crud.getfillialchildfabrica(db))


#----------------TELEGRAM BOT --------------------





