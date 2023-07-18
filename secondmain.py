#----------import packages 
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from pydantic import ValidationError
import schemas
import bcrypt
import models
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import crud
from microservices import get_current_user,get_db
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page,add_pagination

from microservices import create_refresh_token,verify_password,create_access_token,checkpermissions
#from main import get_db,get_current_user
from fastapi import APIRouter

router = APIRouter()

@router.post('/category')
async def add_category(form_data:schemas.AddCategorySch,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='category')
    if permission:
        return crud.add_category_cr(db,form_data)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    



@router.put('/category')
async def update_category(form_data:schemas.UpdateCategorySch,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='category')
    if permission:
        response = crud.update_category_cr(db,form_data)
        if response:
            return response
        else:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    

@router.get('/category',response_model=Page[schemas.GetCategorySch])
async def get_category(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='category')
    if permission:
        response = crud.get_category_list(db)
        return paginate(response)

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    

@router.get('/category/{id}',response_model=schemas.GetCategorySch)
async def get_category_id(id:int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='category')
    try:
        if permission:
            response = crud.get_category_id(db,id)
            return response
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="info with this id not found "
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    


    

@router.get('/request',response_model=Page[schemas.GetRequestList])
async def get_request(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='requests')
    if permission:
        try:
            if request_user.brigada_id:
                requestdata= crud.get_request_list_for_brigada(db,request_user.brigada_id)
                return paginate(requestdata)
            request_list = crud.get_request_list(db)
            return paginate(request_list)
        except:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="not fund"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
@router.get('/request/',response_model=Page[schemas.GetRequestList])
async def filter_request(fillial_id:Optional[int]=None,urgent:Optional[bool]=None,started_at:Optional[datetime]=None,finished_at:Optional[datetime]=None,request_status:Optional[int]=None,department:Optional[str]=None,user_id:Optional[int]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='requests')
    if permission:
        try:
            if request_user.brigada_id:
                requestdata= crud.filter_request_brigada(db,fillial_id=fillial_id,request_status=request_status,urgent=urgent,started_at=started_at,finished_at=finished_at,user_id=user_id,brigda_id=request_user.brigada_id)
                return paginate(requestdata)
            request_list = crud.filter_requests_all(db,fillial_id=fillial_id,request_status=request_status,urgent=urgent,started_at=started_at,finished_at=finished_at,user_id=user_id)
            return paginate(request_list)
        except:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="not fund"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )


    


@router.get('/request/{id}',response_model=schemas.GetRequestList)
async def get_request_id(id:int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='requests')
    if permission:
        try:
            request_list = crud.get_request_id(db,id)

            return request_list
        except:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="not fund"
        )


    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    

@router.put('/request/attach/brigada')
async def get_request_id(form_data:schemas.AcceptRejectRequest,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='requests')
    if permission:  
        try:
            request_list = crud.acceptreject(db,form_data=form_data)
            if request_list:
                return request_list
            else:
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not fund"
        )
        except:
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="not fund"
        )


    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )


@router.post('/request')
async def get_category(files:list[UploadFile],urgent:bool,product:str,category_id:int,fillial_id:int,description:str,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='requests')
    if permission:
        try:
            responserq = crud.add_request(db,urgent=urgent,category_id=category_id,description=description,fillial_id=fillial_id,product=product,user_id=request_user.id)
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


    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )



@router.get('/categories/fillials',summary='you can get list of fillials and categories when you are creating request')
async def get_category_and_fillials(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='requests')
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
async def get_user_lisrt(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='users')
    if permission:
        
            users = crud.get_user_list(db)
            return paginate(users)
       

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    

@router.get('/users/{id}',response_model=schemas.GetUserIdSch)
async def get_user_with_id(id:int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='users')
    if permission:
        
            users = crud.get_user_id(db,id)
            if users:
                return users
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

@router.post('/tools',response_model=schemas.CreateTool)
async def get_user_with_id(form_data:schemas.CreateTool,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page='tools')
    if permission:
        
        tools = crud.create_tool(db,form_data)
        return tools

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )




#----------------TELEGRAM BOT --------------------

@router.get('/fillials/list/tg')
async def get_fillial_list_tg(db:Session=Depends(get_db)):
    return crud.get_branch_list(db)
    
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
    

    



