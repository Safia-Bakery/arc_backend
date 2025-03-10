# ----------import packages
from sqlalchemy.orm import Session
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
)
import schemas
from typing import Annotated
import models
from typing import Optional
from uuid import UUID
from datetime import datetime, date
import statisquery
from microservices import sendtotelegramchannel, invenory_factory_report
import crud
from microservices import get_current_user, get_db, list_departments, authiiko
from database import engine, SessionLocal
from fastapi_pagination import paginate, Page
from users.schema import schema
from microservices import (
    checkpermissions,
    getgroups,
    getproducts,
    list_stores,
    get_suppliers,
    send_document_iiko,
    howmuchleft,
    find_hierarchy,
    get_prices,
    file_generator
)

# from main import get_db,get_current_user
from fastapi import APIRouter

urls = APIRouter()


# ---------------------departments synchronizing with iiko-----------------------------------

@urls.get("/synch/department", response_model=Page[schemas.GetFillialSch])
async def insert_departments(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):

    data = crud.insert_fillials(db, items=list_departments(key=authiiko()))
    stores = crud.insert_otdels(db, items=list_stores(key=authiiko()))
    suppliers = crud.synch_suppliers(db, suppliers=get_suppliers(key=authiiko()))
    branches = crud.get_branch_list(db)
    return paginate(branches)


# ---------------------departments update departments -----------------------------------


@urls.put("/deparment/update")
async def update_otdel(
    form_data: schemas.DepartmenUdpate,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    
    query = crud.udpatedepartment(db, form_data=form_data)
    return query



# ---------------------synch groups and products with iiko-----------------------------------
# ---------------------it gets certain group of dat-----------------------------------

@urls.get("/synch/groups")
async def insert_groups(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)
):
    return {"success": True}


@urls.get("/v2/synch/groups")
async def insert_list_groups(
            db: Session = Depends(get_db),
            request_user: schema.UserFullBack = Depends(get_current_user)
    ):


    key =authiiko()
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
    return {"success": True}


# ---------------------get and filter products and groups -----------------------------------
# --------------------- if user insersts parent_id it usually gets products and groups childs of parent groups-----------------------------------
# ---------------------one group can be parent of products and also groups-----------------------------------
# ---------------------groups are like folders products are like files-----------------------------------

@urls.get("/tool/iarch")
async def toolgroups(
        parent_id: Optional[UUID] = None,
        name: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: schema.UserFullBack = Depends(get_current_user),
):
    data = {
        'folders': crud.getarchtools(db, parent_id),
        'tools': statisquery.tools_query_iarch(db, parent_id, name)
    }
    return data
    
# ---------------------Get all products -----------------------------------

@urls.get("/tools/", response_model=Page[schemas.ToolsSearch])
async def toolgroups(
    name: Optional[str] = None,
    id: Optional[int] = None,
    department: Optional[int] = None,
    few_amounts: Optional[bool] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    data = crud.gettools(db, name=name, id=id, department=department,few_amounts=few_amounts)
    return paginate(data)


# ---------------------update products  -----------------------------------

@urls.put("/tools/", response_model=schemas.ToolsSearch)
async def tools_update(
    form_data: schemas.ToolsUpdate,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    data = statisquery.tools_update(db=db,form_data=form_data)
    return data

# ---------------------after finishing product -----------------------------------

@urls.post("/v1/expenditure")
async def insert_expenditure(
    amount: Annotated[int, Form()],
    request_id: Annotated[int, Form()],
    tool_id: Annotated[int, Form()],
    comment: Annotated[str, Form()] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):

    query_expenditure = crud.addexpenditure(
        db,
        request_id=request_id,
        amount=amount,
        tool_id=tool_id,
        user_id=request_user.id,
        comment=comment,
    )

    return {"success": True}



@urls.post("/v1/upload/file")
async def upload_file(
    request_id: Annotated[int, Form()],
    files: list[UploadFile] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
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
            file_obj_list.append(
                models.Files(request_id=request_id, url=file_path, status=1)
            )
        data = crud.bulk_create_files(db, file_obj_list)
    return data


@urls.put("/v1/expanditure/iiko")
async def synch_expanditure_iiko(
    form_data: schemas.SynchExanditureiiko,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    # permission = checkpermissions(request_user=request_user,db=db,page=26)
    # if permission:
    key=authiiko()
    
    data = crud.check_expanditure_iiko(db, form_data=form_data)
    for i in data:
        if i.status == 0:
            query = crud.synch_expanditure_crud(db, id=i.id)
            send_document_iiko(key=key, data=query)
    return True


# else:
#    raise HTTPException(
#        status_code=status.HTTP_403_FORBIDDEN,
#        detail="You are not super user"
#    )


@urls.delete("/v1/expanditure")
async def delete_expanditure(
    id: int,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    # permission = checkpermissions(request_user=request_user,db=db,page=28)
    # if permission:
    data = crud.delete_expanditure(db, id)
    if data:
        return {"success": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="not id not found"
        )


# else:
#    raise HTTPException(
#        status_code=status.HTTP_403_FORBIDDEN,
#        detail="You are not super user"
#    )


@urls.post("/v1/comments", response_model=schemas.GetComments)
async def add_comments(form_data: schemas.AddComments, db: Session = Depends(get_db)):
    data = crud.add_comment(db=db, form_data=form_data)
    return data


@urls.get("/v1/comments", response_model=Page[schemas.GetComments])
async def get_comments(
    request_id: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    data = crud.get_comment(db=db, request_id=request_id)
    return paginate(data)


# ---------------------statistics-----------------------------------


@urls.get("/v1/stats/category")
async def get_statistics(
    timer: int,
    department: Optional[int] = None,
    sphere_status: Optional[int] = None,
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.calculate_bycat(
        db=db,
        department=department,
        sphere_status=sphere_status,
        started_at=started_at,
        finished_at=finished_at,
        timer=timer,
    )
    category_percent = statisquery.calculate_percentage(
        db=db,
        sphere_status=sphere_status,
        department=department,
        started_at=started_at,
        finished_at=finished_at,
    )
    data = [{"category": i[0], "amount": i[1], "time": i[2]} for i in query]
    return {"success": True, "piechart": category_percent, "table": data}


@urls.get("/v1/stats/department")
async def getstatis(
    sphere_status: int,
    department: int,
    db: Session = Depends(get_db),
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.countfillialrequest(
        db=db,
        sphere_status=sphere_status,
        department=department,
        started_at=started_at,
        finished_at=finished_at,
    )
    data = [{"name": i[1], "amount": i[2]} for i in query]
    return data


@urls.get("/v1/stats/brigada")
async def getstatsbrigada(
    sphere_status: int,
    department: int,
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.countbbrigadarequest(
        db=db,
        sphere_status=sphere_status,
        department=department,
        started_at=started_at,
        finished_at=finished_at,
    )
    data = [{"name": i[0], "amount": i[1], "time": i[2]} for i in query]
    return data


@urls.get("/v1/stats/brigada/category")
async def getbrigadavscategoryst(
    timer: int,
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,
    sphere_status: Optional[int] = None,
    department: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.countbrigadavscategory(
        db=db, timer=timer, started_at=started_at, finished_at=finished_at,department=department,sphere_status=sphere_status
    )
    is_in = {}
    for i in query:
        if i[0] not in is_in.keys():
            is_in[i[0]] = [list(i)]
        else:
            is_in[i[0]].append(list(i))

    # data = [{'brigada':i[0],'category':i[1],'amount':i[2],'time':i[3]} for i in query]
    return is_in


## how much left sklad


@urls.get("/v1/synch/left")
async def synchhowmuchleft(
    store_id: UUID,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    key = authiiko()
    query_iiko = howmuchleft(key=key, store_id=store_id)
    statisquery.howmuchleftcrud(db=db, store_id=store_id, lst=query_iiko)
    return {"success": True}


@urls.get("/v1/tools/left/stores")
async def gethowmuchleft(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    store_dict = [
        {"name": "АРС Фабрика Склад", "id": "f09c2c8d-00bb-4fa4-81b5-4f4e31995b86"},
        {"name": "АРС Розница Склад", "id": "4aafb5af-66c3-4419-af2d-72897f652019"},
        ]
    return {"stores": store_dict}


@urls.get("/v1/tools/left", response_model=Page[schemas.ToolsLeft])
async def gethowmuchleft(
    store_id: UUID = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.howmuchleftgetlist(db=db, id=store_id,name=name)
    return paginate(query)


@urls.get("/v1/expanditure/distinct")
async def getlistofdisinctexpand(
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,
    department: Optional[int] = None,
    sphere_status: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.getlistofdistinctexp(
        db=db, started_at=started_at, finished_at=finished_at,department=department,sphere_status=sphere_status
    )
    data = [{"amount": i[0], "name": i[1], "id": i[2],'price':i[3]} for i in query]
    return {"tests": data}


@urls.get("/v1/expanditure", response_model=Page[schemas.Expanditurelist])
async def getexpanditurefull(
    id: int,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.getexpanditureid(db=db, id=id)
    return paginate(query)


@urls.put("/working")
async def update_working_time(
    form_data: schemas.WorkTimeUpdate,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = crud.workingtimeupdate(db=db, form_data=form_data)
    return query


@urls.get("/working")
async def get_working_time(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = crud.working_time(db=db)
    return query


@urls.post("/toolsorder",tags=['ToolOrder'])
async def generate_tools(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    query = statisquery.order_tool_create(db=db,user_id=request_user.id)
    return {"success":True}



@urls.get("/toolsorder",response_model=Page[schemas.ToolsOrderget],tags=['ToolOrder'])
async def get_tools(
    status:Optional[int]=None,
    id:Optional[int]=None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),):
    query = statisquery.tools_order_query(db=db,status=status,id=id)
    return paginate(query)

#@urls.get("/tools/order/needed",response_model=Page[schemas.NeedToolsGet],tags=['ToolOrder'])
#async def get_needed_tools(
#    toolorder_id:int,
#    db: Session = Depends(get_db),
#    request_user: schema.UserFullBack = Depends(get_current_user),):
#    query = statisquery.needed_tools(db=db,toolorder_id=toolorder_id)
#    return paginate(query)

@urls.put("/toolorder",response_model=schemas.ToolsOrderget,tags=['ToolOrder'])
async def update_toolsorder(
    form_data:schemas.ToolOrderUpdate,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),):
    query = statisquery.tools_order_update(db=db,form_data=form_data)
    return query



# ---------------------main page statistics-----------------------------------


@urls.get("/v1/stats/main",tags=['MainPage'])
async def get_statistics(
    department: int,
    sphere_status: Optional[int] = None,
    sub_id: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    brig_requests = statisquery.brigade_openrequests(
        db=db,
        department=department,
        sphere_status=sphere_status,
    )
    new_requests = statisquery.new_requestsamount(db=db,department=department,sphere_status=sphere_status,sub_id=sub_id)
    avg_rating = statisquery.avg_ratingrequests(db=db,department=department,sphere_status=sphere_status,sub_id=sub_id)
    avg_finishtime = statisquery.avg_time_finishing(db=db,department=department,sphere_status=sphere_status,sub_id=sub_id)
    total_requests = statisquery.total_request_count(db=db,department=department,sphere_status=sphere_status,sub_id=sub_id)
    in_progress = statisquery.in_progress_requests(db=db,department=department,sphere_status=sphere_status,sub_id=sub_id)
    last_30 = statisquery.last_30_days(db=db,department=department,sphere_status=sphere_status,sub_id=sub_id)
    last_month = statisquery.current_month(db=db,department=department,sphere_status=sphere_status,sub_id=sub_id)
    data = {}
    for i in brig_requests:
        data[i[1]]=[i[0],i[2]]
    
    return {"brage_requests":data,'new_requests':new_requests[0][0],'avg_rating':avg_rating,'avg_time':avg_finishtime[0][0],'total_requests':total_requests[0][0],'in_progress':in_progress[0][0],'last_30':last_30[0][0],'last_month':last_month[0][0]}

@urls.get("/v1/excell", tags=['Excell'])
async def get_excell(
    date : Optional[date] = None,
    file:Optional[bool]=False,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.safia_eats(db=db,request_data=date) 
    folder = file_generator(data=query,file=file)
    return {"success":True,'url':folder[0],'total_food':int(folder[1]),'total_bread':int(folder[2])}



@urls.get("/v2/stats/marketing",tags=['Marketing'])
async def get_marketing(
    finished_at: Optional[date] = None,
    started_at: Optional[date] = None,
    sub_id: Optional[int] = None,
    department: Optional[int] = None,
    sphere_status: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.marketing_stats_v2(db=db,finished_at=finished_at,started_at=started_at,sub_id=sub_id,department=department,sphere_status=sphere_status)
    return query



@urls.get("/v1/stats/inventory",tags=['InventoryStats'])
async def get_inventory(
    finished_at: Optional[date] = None,
    started_at: Optional[date] = None,
    #department: Optional[int] = None,

    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    query = statisquery.inventory_stats(db=db,finished_at=finished_at,started_at=started_at,department=2)
    return query



@urls.get("/v1/stats/inventory/factory",tags=['InventoryStats'])
async def get_inventory_factory_stats(
    finished_at: Optional[date] = None,
    started_at: Optional[date] = None,
    #department: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    service_level = statisquery.inventory_stats_factory(db=db,finished_at=finished_at,started_at=started_at,department=10)
    service_efficiency = statisquery.inventory_stats_factory2(db=db, started_at=started_at, finished_at=finished_at, department=10)
    reports = {
        "service_level": service_level,
        "service_efficiency": service_efficiency
    }
    return reports



@urls.post("/v1/stats/inventory/factory/excell", tags=['InventoryStats'])
async def get_inventory_factory_stats(
    finished_at: Optional[date] = None,
    started_at: Optional[date] = None,
    report_type: Optional[int] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    data = []
    if report_type == 1:
        data = statisquery.inventory_stats_factory(
            db=db,
            finished_at=finished_at,
            started_at=started_at,
            department=10
        )
    elif report_type == 2:
        data = statisquery.inventory_stats_factory2(
            db=db,
            started_at=started_at,
            finished_at=finished_at,
            department=10
        )

    excell_file = invenory_factory_report(data=data, report_type=report_type)
    return excell_file

