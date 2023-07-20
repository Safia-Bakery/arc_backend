from sqlalchemy.orm import Session

import models
import schemas
import bcrypt

from sqlalchemy import or_,and_

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def get_user(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()




def create_user(db:Session,user : schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.Users(username=user.username.lower(), password=hashed_password,full_name=user.full_name,email=user.email,phone_number=user.phone_number,group_id=user.group_id,status=user.status)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_roles(db:Session):
    return db.query(models.Pages).all()


def create_group(db:Session,group:schemas.CreateGroupSch):
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
    brigada_cr = models.Brigada(description=data.description,name=data.name,status=data.status)
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





def get_roles_pages(db:Session,id):
    roles_ls = db.query(models.Roles).filter(models.Roles.group_id==id).all()
    return roles_ls



def filter_user_permission(db:Session,id,page):
    return db.query(models.Roles).join(models.Roles.page).filter(models.Roles.group_id==id,models.Pages.page_name==page).first()



def update_fillial_cr(db:Session,form_data:schemas.UpdateFillialSch):
    db_fillial_update = db.query(models.Fillials).filter(models.Fillials.id==form_data.id).first()
    if db_fillial_update:
        if form_data.longtitude is not None:
            db_fillial_update.longtitude = form_data.longtitude

        if form_data.latitude is not None:
            db_fillial_update.latitude = form_data.latitude
        if form_data.status is not None:
            db_fillial_update.status = form_data.status
        db.commit()
        db.refresh(db_fillial_update)
        return db_fillial_update
    return False




def get_fillial_list(db:Session):
    return db.query(models.Fillials).all()


def add_category_cr(db:Session,form_data:schemas.AddCategorySch):
    db_add_category = models.Category(name=form_data.name,description=form_data.description,status=form_data.status)
    db.add(db_add_category)
    db.commit()
    db.refresh(db_add_category)
    return db_add_category

def update_category_cr(db:Session,form_data:schemas.UpdateCategorySch):
    db_update_category = db.query(models.Category).filter(models.Category.id==form_data.id).first()
    if db_update_category:
        if form_data.name is not None:
            db_update_category.name = form_data.name
        if form_data.description is not None:
            db_update_category.description=form_data.description
        if form_data.status is not None:
            db_update_category.status = form_data.status
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
        db.commit()
        db.refresh(db_update_brigada)
        return db_update_brigada
    else:
        return False
 


def get_user_for_brig(db:Session,id):
    db_get_users = db.query(models.Users).filter((or_(models.Users.brigada_id==None,models.Users.brigada_id==id)),and_(models.Users.status==0)).all()
    return db_get_users

def get_category_list(db:Session):
    return db.query(models.Category).all()

def get_category_id(db:Session,id):
    return db.query(models.Category).filter(models.Category.id==id).first()

def add_request(db:Session,urgent,category_id,fillial_id,description,product,user_id):
    db_add_request = models.Requests(urgent=urgent,category_id=category_id,description=description,fillial_id = fillial_id,product=product,user_id=user_id)
    db.add(db_add_request)
    db.commit()
    db.refresh(db_add_request)
    return db_add_request



def bulk_create_files(db:Session,per_obj):
    db.bulk_save_objects(per_obj)
    db.commit()
    return True




def get_brigada_list(db:Session):
    return db.query(models.Brigada).all()




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
    return db.query(models.Fillials).filter(models.Fillials.id==id).first()


#telegram bot 



def get_branch_list(db:Session):
    return db.query(models.Fillials).filter(models.Fillials.status==1).all()


def set_null_user_brigada(db:Session,brigada_id):
    brigad_user = db.query(models.Users).filter(models.Users.id==brigada_id).update({models.Users.brigada_id:None})
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


def acceptreject(db:Session,form_data:schemas.AcceptRejectRequest):
    db_get = db.query(models.Requests).filter(models.Requests.id==form_data.request_id).first()
    if db_get:
        if form_data.brigada_id is not None:
            db_get.brigada_id=form_data.brigada_id
        if form_data.comment is not None:
            db_get.comment=form_data.comment
        db_get.status = form_data.status
        db.commit()
        db.refresh(db_get)
        return db_get
    else:
        return False
    



def filter_requests_all(db:Session,id,category_id,fillial_id,urgent,created_from,created_to,finished_from,finished_to,request_status,user):
    query = db.query(models.Requests)
    if id is not None:
        query = query.filter(models.Requests.id==id)
    if fillial_id is not None:
        query = query.filter(models.Requests.fillial_id==fillial_id)
    if category_id is not None:
        query = query.filter(models.Requests.category_id==category_id)
    if urgent is not None:
        query = query.filter(models.Requests.urgent==urgent)
    if created_from is not None:
        query = query.filter(models.Requests.created_at>created_from)
    if created_to is not None:
        query = query.filter(models.Requests.created_at<created_to)
    if finished_from is not None:
        query = query.filter(models.Requests.finished_at>finished_from)
    if finished_to is not None:
        query = query.filter(models.Requests.finished_at<finished_to)
    if request_status is not None:
        query = query.filter(models.Requests.status==request_status)
    if user  is not None:
        query = query.filter(models.Users.full_name.ilike(f"%{user}%"))
    return query.all()


def filter_request_brigada(db:Session,id,category_id,brigada_id,fillial_id,urgent,created_from,created_to,finished_from,finished_to,request_status,user):
    query = db.query(models.Requests)
    if id is not None:
        query = query.filter(models.Requests.id==id)
    if fillial_id is not None:
        query = query.filter(models.Requests.fillial_id==fillial_id)
    if category_id is not None:
        query = query.filter(models.Requests.category_id==category_id)
    if urgent is not None:
        query = query.filter(models.Requests.urgent==urgent)
    if created_from is not None:
        query = query.filter(models.Requests.created_at>created_from)
    if created_to is not None:
        query = query.filter(models.Requests.created_at<created_to)
    if finished_from is not None:
        query = query.filter(models.Requests.finished_at>finished_from)
    if finished_to is not None:
        query = query.filter(models.Requests.finished_at<finished_to)
    if request_status is not None:
        query = query.filter(models.Requests.status==request_status)
    if user  is not None:
        query = query.filter(models.Users.full_name.ilike(f"%{user}/%"))
    query = query.filter(models.Requests.brigada_id==brigada_id)
    return query.all()


def filter_user(db:Session,user_status,full_name,phone_number,username,role_id):
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
    return query.all()



def filter_category(db:Session,category_status,name):
    query = db.query(models.Category)
    if category_status is not None:
        query = query.filter(models.Category.status==category_status)
    if  name is not None:
        query = query.filter(models.Category.name.ilike(f"%{name}%"))
    return query.all()


def filter_fillials(db:Session,name,country,latitude,longtitude,fillial_status):
    query = db.query(models.Fillials)
    if name is not None:
        query = query.filter(models.Fillials.name.ilike(f"%{name}%"))
    if country is not None:
        query = query.filter(models.Fillials.country.ilike(f"%{country}%"))
    if latitude is not None:
        query = query.filter(models.Fillials.latitude.ilike(f"%{latitude}%"))
    if longtitude is not None:
        query = query.filter(models.Fillials.longtitude.ilike(f"%{longtitude}%"))
    if fillial_status is not None:
        query = query.filter(models.Fillials.status ==fillial_status)
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
        db.commit()
        db.refresh(query)
        return query
        