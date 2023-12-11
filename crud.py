from sqlalchemy.orm import Session
from users.schema import schema
import models
import schemas
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime 
from sqlalchemy import or_,and_,Date,cast
timezonetash = pytz.timezone("Asia/Tashkent")




def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def get_user(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()




def create_user(db:Session,user : schema.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.Users(sphere_status=user.sphere_status,username=user.username.lower(), password=hashed_password,full_name=user.full_name,email=user.email,phone_number=user.phone_number,group_id=user.group_id,status=user.status)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def tg_create_user(db:Session,user:schemas.BotRegister):
    db_user = models.Users(telegram_id=user.telegram_id,phone_number=user.phone_number,full_name=user.full_name,sphere_status=user.sphere_status)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def tg_get_user(db:Session,user:schemas.BotCheckUser):
    db_user = db.query(models.Users).filter(models.Users.telegram_id==user.telegram_id,models.Users.phone_number==user.phone_number).first()
    return db_user



def get_roles(db:Session):
    return db.query(models.ParentPage).all()


def create_group(db:Session,group:schema.CreateGroupSch):
    group_user = models.Groups(name=group.name,status=group.status)
    db.add(group_user)
    db.commit()
    db.refresh(group_user)
    return group_user


def update_group(db:Session,group:schemas.UpdateGroupSch):
    db_group_obj = db.query(models.Groups).filter(models.Groups.id==group.id).first()
    if db_group_obj:
        db_group_obj.name=group.name
        db.commit()
        db.refresh(db_group_obj)
        return db_group_obj
    else:
        return False 



def get_group(db:Session):
    return db.query(models.Groups).all()

def get_group_by_id(db:Session,id):
    return db.query(models.Groups).filter(models.Groups.id==id).first()



def get_permissions(db:Session,id):
    data = db.query(models.Roles).filter(models.Roles.group_id==id).all()
    return data


def delete_roles(db:Session,id):
    db.query(models.Roles).filter(models.Roles.group_id==id).delete()
    db.commit()
    return True



def bulk_create_per(db:Session,per_obj):
    db.bulk_save_objects(per_obj)
    db.commit()
    return True



def get_user_list(db:Session):
    return db.query(models.Users).filter(models.Users.status!=1).all()


def user_role_attach(db:Session,role:schemas.UserRoleAttachSch):
    db_user_update = db.query(models.Users).filter(models.Users.id==role.user_id).first()
    if db_user_update:
        db_user_update.group_id=role.group_id
        db.commit()
        db.refresh(db_user_update)
        return db_user_update
    else:

        return False
    

def create_brigada(db:Session,data:schemas.UservsRoleCr):
    brigada_cr = models.Brigada(description=data.description,name=data.name,status=data.status,sphere_status=data.sphere_status)
    db.add(brigada_cr)
    db.commit()
    db.refresh(brigada_cr)
    return brigada_cr


def get_brigada_id(db:Session,id):
    brigada = db.query(models.Brigada).filter(models.Brigada.id==id).first()
    return brigada




def add_fillials(db:Session,data:schemas.AddFillialSch):
    filials_cr = models.Fillials(name=data.name,latitude=data.latitude,longtitude=data.longtitude,country=data.country,status=data.status)
    db.add(filials_cr)
    db.commit()
    db.refresh(filials_cr)
    return filials_cr



def get_roles_pages_super(db:Session):
    roles_ls = db.query(models.Pages).all()
    return roles_ls



def get_roles_pages(db:Session,id):
    roles_ls = db.query(models.Roles).filter(models.Roles.group_id==id).all()
    return roles_ls



def filter_user_permission(db:Session,id,page):
    return db.query(models.Roles).join(models.Roles.page).filter(models.Roles.group_id==id,models.Pages.id==page).first()



def update_fillial_cr(db:Session,form_data:schemas.UpdateFillialSch):
    db_fillial_update = db.query(models.ParentFillials).filter(models.ParentFillials.id==form_data.id).first()
    if db_fillial_update:
        if form_data.longtitude is not None:
            db_fillial_update.longtitude = form_data.longtitude

        if form_data.latitude is not None:
            db_fillial_update.latitude = form_data.latitude
        if form_data.status is not None:
            db_fillial_update.status = form_data.status
        if form_data.is_fabrica is not None:
            db_fillial_update.is_fabrica = form_data.is_fabrica
        db.commit()
        db.refresh(db_fillial_update)
        return db_fillial_update
    return False


def update_fillil_origin(db:Session,form_data:schemas.UpdateFillialSch):
    db_fillial_update = db.query(models.Fillials).filter(models.Fillials.id==form_data.department_id).first()
    if db_fillial_update:
        if form_data.origin:
            db_fillial_update.origin=form_data.origin
        db.commit()
        db.refresh(db_fillial_update)
        return db_fillial_update
    else:
        return False



def get_fillial_list(db:Session):
    return db.query(models.Fillials).all()


def add_category_cr(db:Session,name,description,status,urgent,sub_id,department,sphere_status,file):
    db_add_category = models.Category(name=name,description=description,status=status,urgent=urgent,sub_id=sub_id,department=department,sphere_status=sphere_status,file=file)
    db.add(db_add_category)
    db.commit()
    db.refresh(db_add_category)
    return db_add_category

def update_category_cr(db:Session,id,name,description,status,urgent,department,sub_id,sphere_status,file):
    db_update_category = db.query(models.Category).filter(models.Category.id==id).first()
    if db_update_category:
        if name is not None:
            db_update_category.name = name
        if description is not None:
            db_update_category.description=description
        if status is not None:
            db_update_category.status = status
        if urgent is not None:
            db_update_category.urgent=urgent
        if department is not None:
            db_update_category.department=department

        if sub_id is not None:
            db_update_category.sub_id = sub_id
        if sphere_status is not None:
            db_update_category.sphere_status = sphere_status
        if file is not None:
            db_update_category.file = file
        db.commit()
        db.refresh(db_update_category)
        return db_update_category
    return False


def update_brigada_id(db:Session,form_data:schemas.UpdateBrigadaSch):
    db_update_brigada = db.query(models.Brigada).filter(models.Brigada.id==form_data.id).first()
    if db_update_brigada:
        if form_data.name is not None:
            db_update_brigada.name=form_data.name
        if form_data.description is not None:
            db_update_brigada.description=form_data.description
        if form_data.status is not None:
            db_update_brigada.status = form_data.status
        if form_data.sphere_status is not None:
            db_update_brigada.sphere_status=form_data.sphere_status
        db.commit()
        db.refresh(db_update_brigada)
        return db_update_brigada
    else:
        return False



def get_user_for_brig(db:Session,id):
    db_get_users = db.query(models.Users).filter((or_(models.Users.brigada_id==None,models.Users.brigada_id==id)),and_(models.Users.status==0)).all()
    return db_get_users

def get_category_list(db:Session,sub_id,sphere_status):
    query = db.query(models.Category)
    
    query = query.filter(models.Category.sub_id==sub_id)
    query = query.filter(models.Category.status==1,models.Category.sphere_status==sphere_status).all()
    return query

def get_category_id(db:Session,id):
    return db.query(models.Category).filter(models.Category.id==id).first()

def add_request(db:Session,category_id,fillial_id,description,product,user_id,is_bot,arrival_date,size,bread_size,location):
    db_add_request = models.Requests(category_id=category_id,description=description,fillial_id = fillial_id,product=product,user_id=user_id,is_bot=is_bot,size=size,arrival_date=arrival_date,bread_size=bread_size,location=location,
                                     update_time={'0':str(datetime.now(tz=timezonetash))})
    db.add(db_add_request)
    db.commit()
    db.refresh(db_add_request)
    return db_add_request



def bulk_create_files(db:Session,per_obj):
    db.bulk_save_objects(per_obj)
    db.commit()
    return True




def get_brigada_list(db:Session,sphere_status):
    query = db.query(models.Brigada)
    if sphere_status:
        query = query.filter(models.Brigada.sphere_status==sphere_status)
    return query.all()




def get_request_list(db:Session):
    return db.query(models.Requests).all()

def get_request_list_for_brigada(db:Session,id):
    return db.query(models.Requests).filter(models.Requests.brigada_id==id).all()
def get_request_id(db:Session,id):
    return db.query(models.Requests).filter(models.Requests.id==id).first()


def attach_request_brigada(db:Session,form_data:schemas.RequestAttachBrigada):
    db_add_request = db.query(models.Requests).filter(models.Requests.id==form_data.request_id).first()
    if db_add_request:

        db_add_request.brigada_id = form_data.brigada_id
        db.commit()
        db.refresh(db_add_request)
        return db_add_request
    return False

def get_fillial_id(db:Session,id):
    return db.query(models.ParentFillials).filter(models.ParentFillials.id==id).first()


#telegram bot 



def get_branch_list(db:Session):
    return db.query(models.ParentFillials).join(models.Fillials).filter(models.ParentFillials.status==1,models.Fillials.origin==1).order_by(models.ParentFillials.name).all()


def get_branch_list_location(db:Session):
    return db.query(models.ParentFillials).filter(models.ParentFillials.status==1).order_by(models.ParentFillials.name).all()

def set_null_user_brigada(db:Session,brigada_id):
    brigad_user = db.query(models.Users).filter(models.Users.brigada_id==brigada_id).update({models.Users.brigada_id:None})
    db.commit()
    return brigad_user

def attach_user_brigads(db:Session,data:list,brig_id:int):
    brigad_user = db.query(models.Users).filter(models.Users.id.in_(data)).update({models.Users.brigada_id:brig_id})
    db.commit()
    return brigad_user

def get_user_id(db:Session,id:int):
    user = db.query(models.Users).filter(models.Users.id==id).first()
    return user


def create_tool(db:Session,form_data :schemas.CreateTool):
    tool_db = models.Tools(name=form_data.name)
    db.add(tool_db)
    db.commit()
    db.refresh(tool_db)
    return tool_db


def search_tools(db:Session,query):
    tools = db.query(models.Tools).filter(models.Tools.name.ilike(f"%{query}%")).all()
    return tools


def acceptreject(db:Session,form_data:schemas.AcceptRejectRequest,user):
    db_get = db.query(models.Requests).filter(models.Requests.id==form_data.request_id).first()
    if db_get:
        if form_data.brigada_id is not None:
            db_get.brigada_id=form_data.brigada_id
        if form_data.deny_reason is not None:
            db_get.deny_reason=form_data.deny_reason
        db_get.status = form_data.status
        db_get.user_manager=user
        if form_data.finishing_time is not None:
            db_get.finishing_time= form_data.finishing_time
        if form_data.status == 1:
            db_get.started_at = func.now()
        if form_data.status == 3 or form_data.status==4:
            db_get.finished_at = func.now()
        updated_data = db_get.update_time or {}
        updated_data[str(form_data.status)] = str(datetime.now(tz=timezonetash))
        db_get.update_time= updated_data
        db.query(models.Requests).filter(models.Requests.id==form_data.request_id).update({'update_time':updated_data})
        db.commit()
        db.refresh(db_get) 
        return db_get
    else:
        return False
    

#dssd
#hello

def filter_requests_all(db:Session,id,category_id,fillial_id,created_at,request_status,user,sub_id,department,sphere_status,arrival_date):
    query = db.query(models.Requests).join(models.Category).join(models.Users)
    if id is not None:
        query = query.filter(models.Requests.id==id)
    if fillial_id is not None:
        query = query.filter(models.Requests.fillial_id==fillial_id)
    if category_id is not None:
        query = query.filter(models.Requests.category_id==category_id)
    
    if created_at is not None:
        query = query.filter(cast(models.Requests.created_at,Date)==created_at)
    if request_status is not None:
        query =  query.filter(models.Requests.status==request_status)
    if user  is not None:
        query = query.filter(models.Users.full_name.ilike(f"%{user}%"))
    if department is not None:
        query = query.filter(models.Category.department==department)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if arrival_date is not None:
        query = query.filter(cast(models.Requests.arrival_date,Date)==arrival_date)
    return query.order_by(models.Requests.id.desc()).all()


def filter_request_brigada(db:Session,id,category_id,brigada_id,fillial_id,created_at,request_status,user,sphere_status,department,sub_id,arrival_date):
    query = db.query(models.Requests).join(models.Category)
    if id is not None:
        query = query.filter(models.Requests.id==id)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    if fillial_id is not None:
        query = query.filter(models.Requests.fillial_id==fillial_id)
    if category_id is not None:
        query = query.filter(models.Requests.category_id==category_id)
    if department is not None:
        query = query.filter(models.Category.department==department)
    if created_at is not None:
        query = query.filter(models.Requests.created_at==created_at)
    if request_status is not None:
        query = query.filter(models.Requests.status==request_status)
    if user  is not None:
        query = query.filter(models.Users.full_name.ilike(f"%{user}/%"))
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if arrival_date is not None:
        query = query.filter(cast(models.Requests.arrival_date,Date)==arrival_date)
    query = query.filter(models.Requests.brigada_id==brigada_id)
    return query.order_by(models.Requests.id.desc()).all()


def filter_user(db:Session,user_status,full_name,phone_number,username,role_id,position):
    query = db.query(models.Users)
    if user_status is not None:
        query = query.filter(models.Users.status==user_status)
    if full_name is not None:
        query = query.filter(models.Users.full_name.ilike(f"%{full_name}%"))
    if phone_number is not None:
        query = query.filter(models.Users.phone_number.ilike(f"%{phone_number}%"))
    if username is not None:
        query = query.filter(models.Users.username.ilike(f"%{username}%"))
    if role_id is not None:
        query = query.filter(models.Users.group_id==role_id)
    if position:
        query = query.filter(models.Users.group_id!=None)
    if not position:
        query = query.filter(models.Users.group_id==None)
    return query.all()



def filter_category(db:Session,category_status,name,department,sub_id,sphere_status):
    query = db.query(models.Category)
    if category_status is not None:
        query = query.filter(models.Category.status==category_status)
    if  name is not None:
        query = query.filter(models.Category.name.ilike(f"%{name}%"))
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    if department is not None:
        query = query.filter(models.Category.department==department)
    if sphere_status is not None:
        query  = query.filter(models.Category.sphere_status == sphere_status)
    return query.all()


def filter_fillials(db:Session,name,country,latitude,longtitude,fillial_status,origin):
    query = db.query(models.ParentFillials).join(models.Fillials)
    if name is not None:
        query = query.filter(models.ParentFillials.name.ilike(f"%{name}%"))
    if country is not None:
        query = query.filter(models.ParentFillials.country.ilike(f"%{country}%"))
    if latitude is not None:
        query = query.filter(models.ParentFillials.latitude.ilike(f"%{latitude}%"))
    if longtitude is not None:
        query = query.filter(models.ParentFillials.longtitude.ilike(f"%{longtitude}%"))
    if fillial_status is not None:
        query = query.filter(models.ParentFillials.status ==fillial_status)
    if origin !=0:
        query = query.filter(models.Fillials.origin==origin)
    return query.all()

def get_list_tools(db:Session):
    query = db.query(models.Tools).all()
    return query


def update_user(db:Session,form_data:schemas.UserUpdateAll):
    query = db.query(models.Users).filter(models.Users.id==form_data.user_id).first()
    if query:
        if form_data.brigada_id is not None:
            set_null_user_brigada(db,form_data.brigada_id)
            query.brigada_id = form_data.brigada_id
        if form_data.email is not None:
            query.email = form_data.email
        if form_data.full_name is not None:
            query.full_name = form_data.full_name
        if form_data.group_id is not None:
            query.group_id = form_data.group_id
        if form_data.username is not None:
            query.username = form_data.username
        if form_data.phone_number is not None:
            query.phone_number=form_data.phone_number
        if form_data.telegram_id is not None:
            query.telegram_id = form_data.telegram_id
        if form_data.password is not None:
            query.password = hash_password(form_data.password)
        if form_data.status is not None:
            query.status = form_data.status
        if form_data.sphere_status is not None:
            query.sphere_status = form_data.sphere_status
        db.commit()
        db.refresh(query)
        return query
    
def getcategoryname(db:Session,name):
    query = db.query(models.Category).filter(models.Category.name.ilike(f"%{name}%")).first()
    return query

def getfillialname(db:Session,name):
    query = db.query(models.ParentFillials).filter(models.ParentFillials.name==name).first()
    return query
def getusertelegramid(db:Session,id):
    query = db.query(models.Users).filter(models.Users.telegram_id==id).first()
    return query

def tg_get_request_list(db:Session,brigada_id):
    query = db.query(models.Requests).filter(and_(models.Requests.brigada_id==brigada_id,models.Requests.status.in_([1,2]))).all()
    return query


def get_user_brig_id(db:Session,brigada_id):
    query = db.query(models.Users).filter(models.Users.brigada_id==brigada_id).first()
    return query

def tg_update_requst_st(db:Session,form_data:schemas.TgUpdateStatusRequest):
    query = db.query(models.Requests).filter(models.Requests.id==form_data.request_id).first()
    if form_data.status == 3:
        query.finished_at = datetime.now(timezonetash)
    query.status = form_data.status
    
    db.commit()
    db.refresh(query)
    return query


def expanditure_create(db:Session,form_data:schemas.ExpanditureSchema,brigada_id:int):
    expand_cr = models.Expanditure(brigada_id=brigada_id,amount=form_data.amount,tool_id=form_data.tool_id)
    db.add(expand_cr)
    db.commit()
    db.refresh(expand_cr)
    return expand_cr
    



def check_data_exist(db: Session, name: str):
    return db.query(models.ParentFillials).filter(models.ParentFillials.id == name).first()

def insert_fillials(db:Session,items):
    for item in items:
        existing_item = check_data_exist(db,name=item[1])
        if existing_item:
            continue
        new_item = models.ParentFillials(country='Uzbekistan', name=item[0],status=1,id=item[1])
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    return True


def check_otdel_exist(db: Session, id: str):
    return db.query(models.Fillials).filter(models.Fillials.id == id).first()


def insert_otdels(db:Session,items):
    for item in items:
        existing_item = check_otdel_exist(db,id=item[1])
        if existing_item:
            continue
        new_item = models.Fillials( name=item[0],status=1,id=item[1],parentfillial_id=item[2])
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

    return True



def check_group_exist(db:Session,id,modelname,fildname):
    return db.query(modelname).filter(fildname==id).first()


def commitdata(db:Session,item):
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except:
        return False


def synchtools(db:Session,groups):
    group_list = []
    for line in groups:
        if line['id'] in ['09be831f-1201-4b78-9cad-7c94c3363276','1b55d7e1-6946-4bbc-bf93-542bfdb2b584','203a26b5-a458-4c45-b85d-ad961b5345f2','6fe3e935-cbdc-41a8-9848-f44f2332be54']:
            group_list.append(line['id'])
            if check_group_exist(db,line['id'],models.ToolParents,models.ToolParents.id) is None:
                item = models.ToolParents(id=line['id'],num=line['num'],code=line['code'],name=line['name'],category=line['category'],description=line['description'])
                commitdata(db,item)
            for second in groups:
                if second['parent']==line['id']:
                    group_list.append(second['id'])
                    if check_group_exist(db,second['id'],models.FirstChild,models.FirstChild.id) is None:
                        item = models.FirstChild(id=second['id'],num=second['num'],code=second['code'],name=second['name'],category=second['category'],description=second['description'],toolparentid=second['parent'])
                        commitdata(db,item)
                    for third in groups:
                        if third['parent']==second['id']:
                            group_list.append(third['id'])
                            if check_group_exist(db,third['id'],models.SecondChild,models.SecondChild.id) is None:
                                item = models.SecondChild(id=third['id'],num=third['num'],code=third['code'],name=third['name'],category=third['category'],description=third['description'],parentid=third['parent'])
                                commitdata(db,item)
                            for fourth in groups:
                                if fourth['parent']==third['id']:
                                    group_list.append(fourth['id'])
                                    if check_group_exist(db,fourth['id'],models.ThirdChild,models.ThirdChild.id) is None:
                                        item = models.ThirdChild(id=fourth['id'],num=fourth['num'],code=fourth['code'],name=fourth['name'],category=fourth['category'],description=fourth['description'],parentid=fourth['parent'])
                                        commitdata(db,item)
                                    for five in groups:
                                        if five['parent']==fourth['id']:
                                            group_list.append(five['id'])
                                            if check_group_exist(db,five['id'],models.FourthChild,models.FourthChild.id) is None:
                                                item = models.FourthChild(id=five['id'],num=five['num'],code=five['code'],name=five['name'],category=five['category'],description=five['description'],parentid=five['parent'])
                                                commitdata(db,item)
    return group_list


def synchproducts(db:Session,grouplist,products):
    for i in products:
        parentId = i['parent']
        name = i['name']
        num = i['num']
        code = i['code']
        producttype = i['type']
        mainunit = i['mainUnit']
        id = i['id']
        price = i['defaultSalePrice']
        if parentId in grouplist:
            toolsmod = models.Tools(price=price,iikoid = id, parentid=parentId,name=name,num=num,code=code,producttype=producttype,mainunit=mainunit)
            commitdata(db,toolsmod)
    return True


def check_suppier_exist(db:Session,supplier_id):
    query = db.query(models.Suppliers).filter(models.Suppliers.id==supplier_id).first()
    return query

def synch_suppliers(db:Session,suppliers):
    for i in suppliers:
        id = i.find('id').text
        is_store = i.find('representsStore')
        store_id = i.find('representedStoreId')
        
        if not check_suppier_exist(db,supplier_id=id) and is_store.text=='true':
            name = i.find('name').text
            code = i.find('code')
            code = code.text if code else None
            taxpayernum = i.find('taxpayerIdNumber').text
            db_add = models.Suppliers(id=id,code=code,taxpayernum=taxpayernum,store_id=store_id.text,name=name)
            db.add(db_add)
            db.commit()
            db.refresh(db_add)


            
            
    return True



def getarchtools(db:Session):
    return db.query(models.ToolParents).all()

def gettools(db:Session,query):
    return db.query(models.Tools).filter(or_(models.Tools.name.ilike(f"%{query}%"),models.Tools.parentid.ilike(f"%{query}%"))).all()


def addcomment(db:Session,request_id,comment):
    query = db.query(models.Requests).filter(models.Requests.id==request_id).first()
    if query:
        query.comment = comment
        db.commit()
        db.refresh(query)
        return query
    else:
        return False

        

def addexpenditure(db:Session,request_id,amount,tool_id,user_id,comment):
    add_data = models.Expanditure(request_id=request_id,tool_id=tool_id,amount=amount,user_id=user_id,comment=comment)
    db.add(add_data)
    db.commit()
    db.refresh(add_data)
    return add_data
    
def getchildbranch(db:Session,fillial,type,factory):
    query = db.query(models.Fillials).join(models.ParentFillials)
    if factory == 1:
        if type==1:
            query = query.filter(models.ParentFillials.name.like(f"%{fillial}%"),models.Fillials.origin==1)
        elif type==2:
            query = query.filter(models.ParentFillials.name.like(f"%{fillial}%"))
        query = query.first()
    elif factory==2:
        query = query.filter(models.Fillials.name.like(f"%{fillial}%")).first()
    return query

def udpatedepartment(db:Session,form_data:schemas.DepartmenUdpate):
    query = db.query(models.Fillials).filter(models.Fillials.id==form_data.id).first()
    if query:
        query.origin = form_data.origin
    db.commit()
    db.refresh(query)
    return query



def check_expanditure_iiko(db:Session,form_data:schemas.SynchExanditureiiko):
    query = db.query(models.Expanditure).filter(models.Expanditure.request_id==form_data.request_id).all() 
    return query

def synch_expanditure_crud(db:Session,id):
    query = db.query(models.Expanditure).filter(models.Expanditure.id==id).first()
    query.status=1

    db.commit()
    db.refresh(query)
    return query

def delete_expanditure(db:Session,id):
    query = db.query(models.Expanditure).filter(models.Expanditure.id==id).delete()
    db.commit()

    return True


def add_comment(db:Session,form_data:schemas.AddComments,user_id):
    query = models.Comments(request_id=form_data.request_id,user_id=user_id,comment=form_data.comment)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_comment(db:Session):
    query = db.query(models.Comments).all()
    return query



def filterbranchchildid(db:Session,parent_id,origin:Optional[int]=None):
    query = db.query(models.Fillials).filter(models.Fillials.status==1,models.Fillials.parentfillial_id==parent_id)
    if origin:
        query  = query.filter(models.Fillials.origin==origin)


    return query.first()


def getfillialchildfabrica(db:Session):
    query = db.query(models.Fillials).join(models.ParentFillials).filter(models.ParentFillials.is_fabrica==1).all()
    return query

def workingtimeupdate(db:Session,form_data:schemas.WorkTimeUpdate):
    query = db.query(models.Working).filter(models.Working.id==1).first()
    if query:
        if form_data.from_time is not None:
            query.from_time = form_data.from_time
        if form_data.to_time is not None:
            query.to_time = form_data.to_time
        db.commit()
        db.refresh(query)
    return query


def working_time(db:Session):
    query  = db.query(models.Working).first()
    return query

