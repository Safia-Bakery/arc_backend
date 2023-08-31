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
from microservices import sendtotelegramchannel
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
            requestdata= crud.filter_request_brigada(db,id=id,category_id=category_id,fillial_id=fillial_id,request_status=request_status,created_at=created_at,user=user,brigada_id=request_user.brigada_id,sphere_status=sphere_status)
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
async def get_request_id(form_data:schemas.AcceptRejectRequest,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):

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
                try:
                    sendtotelegramchannel(bot_token=bot_token,chat_id=request_list.user.telegram_id,message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки №{request_list.id} по Маркетингу завершена.")
                except:
                    pass
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
        try:
            if not factory:
                filliald_od = crud.filterbranchchildid(db,fillial_id)
                sklad_id = filliald_od.id
            if factory:
                sklad_id = fillial_id
            responserq = crud.add_request(db,category_id=category_id,description=description,fillial_id=sklad_id,product=product,user_id=request_user.id)
            file_obj_list = []

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
            return {'success':True,'message':'everything is saved'}
        except:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="not id not found"
        )









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

@router.get('/fillials/list/tg')
async def get_fillial_list_tg(db:Session=Depends(get_db)):
    return crud.get_branch_list(db)

@router.get('/get/fillial/fabrica/tg')
async def get_fillials_fabrica_tg(db:Session=Depends(get_db)):
    return crud.getfillialchildfabrica(db)

@router.get('/fillials/list/tg/location')
async def get_fillial_list_tg(db:Session=Depends(get_db)):
    return crud.get_branch_list_location(db)
    
@router.get('/tools/{query}')
async def get_user_with_id(query:str,db:Session=Depends(get_db)):
    tools = crud.search_tools(db,query)[:5]
    if tools:
        return tools
    else: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )



@router.get('/get/category/tg')
async def get_category_list_tg(sphere_status:int,sub_id:Optional[int]=None,db:Session=Depends(get_db)):
    return crud.get_category_list(db,sub_id=sub_id,sphere_status=sphere_status)


@router.post('/tg/create/user')
async def tg_create_userview(user:schemas.BotRegister,db:Session=Depends(get_db)):
    try:
        user = crud.tg_create_user(db,user)
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="Already exist"
        )



@router.get('/tg/user/exist')
async def tg_get_user(user:schemas.BotCheckUser,db:Session=Depends(get_db)):
    userinfo = crud.tg_get_user(db,user)
    if userinfo:
        return {'success':True}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )


@router.post('/tg/request')
async def tg_post_request(files:UploadFile,file_name:Annotated[str,Form()],telegram_id:Annotated[int,Form()],description:Annotated[str, Form()],product:Annotated[str, Form()],fillial:Annotated[str, Form()],category:Annotated[str, Form()],type:Annotated[int,Form()],factory:Annotated[int,Form()],db:Session=Depends(get_db)):
    categoryquery = crud.getcategoryname(db,category)
    telegram_idquery = crud.getusertelegramid(db,telegram_id)
    childfillial = crud.getchildbranch(db,fillial,type=type,factory=factory)
    if categoryquery is None or telegram_idquery is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
            )
    
    response_query = crud.add_request(db,category_id=categoryquery.id,fillial_id=childfillial.id,description=description,product=product,user_id=telegram_idquery.id)
    file_obj_list = []
    file_path = f"files/{file_name}"
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await files.read(1024)
            if not chunk:
                break
            buffer.write(chunk)
        file_obj_list.append(models.Files(request_id=response_query.id,url=file_path))
        crud.bulk_create_files(db,file_obj_list)
    return {'Message':'hello','id':response_query.id}




@router.get('/tg/check/user')
async def tg_check_user_request(telegram_id:int,db:Session=Depends(get_db)):
    user = crud.getusertelegramid(db,telegram_id)
    if user:
        if user.brigada_id:
            return {'success':True,'brigada_name':user.brigader.name}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="not found"
                )
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="not found"
                )
    

    
@router.post('/tg/get/branch')
async def tg_get_branch_location(branch_name:Annotated[str,Form()],db:Session=Depends(get_db)):
    branch = crud.getfillialname(db,branch_name)
    if branch:
        return branch
    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="not found"
                )
    
@router.get('/tg/branch/get/request',response_model=list[schemas.GetRequestList])
async def tg_get_branch_request(telegram_id:int,db:Session=Depends(get_db)):
    user = crud.getusertelegramid(db,telegram_id)
    query = crud.tg_get_request_list(db,brigada_id=user.brigada_id)
    return query



@router.get('/tg/get/request',response_model=schemas.GetRequestList)
async def tg_get_request_id(id:int,db:Session=Depends(get_db)):
    query = crud.get_request_id(db,id)
    return query

@router.put('/tg/request')
async def tg_update_request(form_data:schemas.TgUpdateStatusRequest,db:Session=Depends(get_db)):
    query = crud.tg_update_requst_st(db,form_data=form_data)
    return query


    

    



