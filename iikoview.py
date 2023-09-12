#----------import packages 
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
import schemas
from typing import Annotated
import models
from typing import Optional
from datetime import datetime,date
import statisquery
from microservices import sendtotelegramchannel
import crud
from microservices import get_current_user,get_db,list_departments,authiiko
from database import engine,SessionLocal
from fastapi_pagination import paginate,Page

from microservices import checkpermissions,getgroups,getproducts,list_stores,get_suppliers,send_document_iiko
#from main import get_db,get_current_user
from fastapi import APIRouter
urls = APIRouter()



@urls.get('/synch/department',response_model=Page[schemas.GetFillialSch])
async def insert_departments(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)): 
    permission = checkpermissions(request_user=request_user,db=db,page=9)
    if permission:
        data = crud.insert_fillials(db,items=list_departments(key=authiiko()))
        stores = crud.insert_otdels(db,items=list_stores(key=authiiko()))
        suppliers = crud.synch_suppliers(db,suppliers=get_suppliers(key=authiiko()))
        branches = crud.get_branch_list(db)
        return paginate(branches)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )


@urls.put('/deparment/update')
async def update_otdel(form_data:schemas.DepartmenUdpate,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=23)
    if permission:
        query = crud.udpatedepartment(db,form_data=form_data)
        return query
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )



@urls.get('/synch/groups')
async def insert_groups(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=30)
    if permission:
        groups = getgroups(key = authiiko())
        products = getproducts(key=authiiko())
        group_list = crud.synchtools(db,groups)
        product_list = crud.synchproducts(db,grouplist=group_list,products=products)
        return {'success':True}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )


@urls.get('/tool/iarch',response_model=list[schemas.ToolParentsch])
async def toolgroups(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    return crud.getarchtools(db)


@urls.get('/tools/',response_model=Page[schemas.ToolsSearch])
async def toolgroups(query:str,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    data = crud.gettools(db,query)
    return paginate(data)



@urls.post('/v1/expenditure')
async def insert_expenditure(amount:Annotated[int,Form()],request_id:Annotated[int,Form()],tool_id:Annotated[int,Form()],comment:Annotated[str,Form()]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=28)
    #if permission:

        query_expenditure = crud.addexpenditure(db,request_id=request_id,amount=amount,tool_id=tool_id,user_id=request_user.id,comment=comment)
        
        return {'success':True}
    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )


@urls.post('/v1/upload/file')
async def upload_file(request_id:Annotated[int,Form()],files:list[UploadFile]= None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    if files:
        file_obj_list = []
        for file in files:
            file_path = f"files/{file.filename}"
            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            file_obj_list.append(models.Files(request_id=request_id,url=file_path,status=1))
        data = crud.bulk_create_files(db,file_obj_list)
    return data


@urls.put('/v1/expanditure/iiko')
async def synch_expanditure_iiko(form_data:schemas.SynchExanditureiiko,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=26)
    #if permission:
        data = crud.check_expanditure_iiko(db,form_data=form_data)
        for i in data:
            if i.status==0:

                query = crud.synch_expanditure_crud(db,id=i.id)
                send_document_iiko(key=authiiko(),data=query)
        return True
    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )

@urls.delete('/v1/expanditure')
async def delete_expanditure(id=int,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    #permission = checkpermissions(request_user=request_user,db=db,page=28)
    #if permission:
        data = crud.delete_expanditure(db,id)
        if data:
            return {'success':True}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="not id not found"
            )
    #else:
    #    raise HTTPException(
    #        status_code=status.HTTP_403_FORBIDDEN,
    #        detail="You are not super user"
    #    )

@urls.post('/v1/comments',response_model=schemas.GetComments)
async def add_comments(form_data:schemas.AddComments,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=1)
    if permission:
        data = crud.add_comment(db=db,form_data=form_data,user_id = request_user.id)
        return data
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )

@urls.get('/v1/comments',response_model=Page[schemas.GetComments])
async def get_comments(db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    permission = checkpermissions(request_user=request_user,db=db,page=13)
    if permission:
        data = crud.get_comment(db=db)
        return paginate(data)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not super user"
        )
    


#---------------------statistics-----------------------------------




@urls.get('/v1/stats/category')
async def get_statistics(timer:int,department:Optional[int]=None,sphere_status:Optional[int]=None,started_at:Optional[date]=None,finished_at:Optional[date]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    query = statisquery.calculate_bycat(db=db,department=department,sphere_status=sphere_status,started_at=started_at,finished_at=finished_at,timer=timer)
    category_percent= statisquery.calculate_percentage(db=db,sphere_status=sphere_status,department=department,started_at=started_at,finished_at=finished_at)
    data = [{'category':i[0],'amount':i[1],'time':i[2]} for i in query]
    return {'success':True,'piechart':category_percent,'table':data}


@urls.get('/v1/stats/department')
async def getstatis(sphere_status:int,department:int,db:Session=Depends(get_db),started_at:Optional[date]=None,finished_at:Optional[date]=None,request_user:schemas.UserFullBack=Depends(get_current_user)):
    query = statisquery.countfillialrequest(db=db,sphere_status=sphere_status,department=department,started_at=started_at,finished_at=finished_at)
    data  = [{'name':i[1],'amount':i[2]} for i in query]
    return data



@urls.get('/v1/stats/brigada')
async def getstatsbrigada(sphere_status:int,department:int,started_at:Optional[date]=None,finished_at:Optional[date]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    query  = statisquery.countbbrigadarequest(db=db,sphere_status=sphere_status,department=department,started_at=started_at,finished_at=finished_at)
    data = [{'name':i[0],'amount':i[1],'time':i[2]} for i in query]
    return data



@urls.get('/v1/stats/brigada/category')
async def getbrigadavscategoryst(timer:int,started_at:Optional[date]=None,finished_at:Optional[date]=None,db:Session=Depends(get_db),request_user:schemas.UserFullBack=Depends(get_current_user)):
    query = statisquery.countbrigadavscategory(db=db,timer=timer,started_at=started_at,finished_at=finished_at)
    is_in = {}
    for i in query:
        if i[0] not in is_in.keys():
            is_in[i[0]]=[list(i)]
        else:
            is_in[i[0]].append(list(i))
    
    #data = [{'brigada':i[0],'category':i[1],'amount':i[2],'time':i[3]} for i in query]
    return is_in



