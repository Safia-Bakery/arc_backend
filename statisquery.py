from sqlalchemy.orm import Session

import models
from uuid import UUID
import schemas
from typing import Optional
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
import pytz
from sqlalchemy import distinct,case
from datetime import datetime, date,timedelta
from microservices import sendtotelegramchannel
from sqlalchemy import or_, and_, Date, cast, func, Integer, Numeric,Interval,extract,literal_column
backend_url = "https://backend.service.safiabakery.uz"
import time
import requests
from dotenv import load_dotenv

timezonetash = pytz.timezone("Asia/Tashkent")
load_dotenv()
import os

bot_token = os.environ.get("BOT_TOKEN")


def calculate_bycat(
    timer,
    db: Session,
    sphere_status: Optional[int] = None,
    department: Optional[int] = None,
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,
):
    query = db.query(
        models.Category.name.label("category_name"),
        func.count(models.Requests.id).label("count_1"),
        func.cast(
            func.avg(
                func.extract(
                    "epoch", models.Requests.finished_at - models.Requests.started_at
                )
            )
            / timer,
            Integer,
        ).label("avg_1"),
    )
    if sphere_status:
        query = query.filter(models.Category.sphere_status == sphere_status)
    if department:
        query = query.filter(models.Category.department == department)
    if started_at and finished_at:
        query = query.filter(
            models.Requests.created_at.between(started_at, finished_at)
        )

    return (
        query.join(models.Requests, models.Category.id == models.Requests.category_id)
        .filter(models.Requests.status == 3)
        .group_by(models.Category.name)
        .all()
    )


def calculate_percentage(
    db: Session,
    sphere_status,
    department,
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,
):
    total_requests = (
        db.query(models.Requests)
        .join(models.Category)
        .filter(
            models.Category.sphere_status == sphere_status,
            models.Requests.status == 3,
            models.Category.department == department,
            models.Requests.created_at.between(started_at, finished_at),
        )
        .count()
    )
    categories = (
        db.query(models.Category)
        .filter(
            models.Category.status == 1,
            models.Category.sphere_status == sphere_status,
            models.Category.department == department,
        )
        .all()
    )
    category_percentages = []
    for category in categories:
        category_name = category.name
        category_request_count = (
            db.query(models.Requests)
            .join(models.Category)
            .filter(
                models.Requests.category_id == category.id,
                models.Requests.status == 3,
                models.Category.department == department,
                models.Category.sphere_status == sphere_status,
                models.Requests.created_at.between(started_at, finished_at),
            )
            .count()
        )

        category_percentage = {
            "category_name": category_name,
            "request_count": category_request_count,
            "percentage": (category_request_count / total_requests) * 100
            if total_requests > 0
            else 0,
        }
        category_percentages.append(category_percentage)
    return category_percentages


def countfillialrequest(
    db: Session, sphere_status, department, started_at, finished_at
):
    total = (
        db.query(
            models.Fillials.name.label("fillial_name"),
            models.ParentFillials.name.label("parent_fillai"),
            func.count(models.Requests.id).label("count_1"),
        )
        .join(models.ParentFillials)
        .join(models.Requests)
        .join(models.Category)
        .filter(
            models.Requests.status == 3,
            models.Category.sphere_status == sphere_status,
            models.Category.department == department,
            models.Requests.created_at.between(started_at, finished_at),
        )
        .group_by(models.Fillials.name, models.ParentFillials.name)
        .all()
    )
    return total


def countbbrigadarequest(
    db: Session, sphere_status, department, started_at, finished_at, timer=60
):
    total = (
        db.query(
            models.Brigada.name,
            func.count(models.Requests.id),
            func.cast(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Requests.finished_at - models.Requests.started_at,
                    )
                )
                / timer,
                Integer,
            ),
        )
        .join(models.Requests)
        .join(models.Category)
        .filter(
            models.Requests.status == 3,
            models.Category.department == department,
            models.Category.sphere_status == sphere_status,
            models.Requests.created_at.between(started_at, finished_at),
        )
        .group_by(models.Brigada.name)
        .all()
    )
    return total


def countbrigadavscategory(timer, started_at, finished_at,sphere_status,department, db: Session):
    total = (
        db.query(
            models.Brigada.name.label("brigada_name"),
            models.Category.name.label("category_name"),
            func.count(models.Requests.id),
            func.cast(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Requests.finished_at - models.Requests.started_at,
                    )
                )
                / timer,
                Integer,
            ).label("avg_1"),
        )
        .join(models.Category)
        .join(models.Brigada)
        .filter(
            models.Requests.status == 3,
            models.Requests.created_at.between(started_at, finished_at),
        )
        
        .group_by(models.Brigada.name, models.Category.name)
        
    )
    if sphere_status is not None:
        total = total.filter(models.Category.sphere_status == sphere_status)
    if department is not None:
        total = total.filter(models.Category.department == department)
    return total.all()


def howmuchleftcrud(db: Session, lst, store_id):
    for i in lst:
        total = (
            db.query(models.Tools).filter(models.Tools.iikoid == i["product"]).first()
        )
        if total:
            total.total_price = float(i["sum"])
            total.amount_left = float(i["amount"])
            total.last_update = datetime.now(timezonetash)

            if total.sklad_id:
                if UUID(i["store"]) not in total.sklad_id:
                    total.sklad_id = total.sklad_id.append(UUID(i["store"]))
            else:
                total.sklad_id = [UUID(i["store"])]
            db.commit()
            db.refresh(total)

        else:
            pass
    return True


def howmuchleftgetlist(db: Session, id,name):
    query = db.query(models.Tools).filter(models.Tools.sklad_id.contains([id]))
    if name is not None:
        query = query.filter(models.Tools.name.ilike(f"%{name}%"))

    return query.all()


def getlistofdistinctexp(db: Session, started_at, finished_at,department,sphere_status):
    query = db.query(
        func.sum(cast(models.Expanditure.amount, Integer)),
        models.Tools.name,
        models.Expanditure.tool_id,
        models.Tools.price,
    ).join(models.Tools).join(models.Requests).join(models.Category)
    if department:
        query = query.filter(models.Category.department==department)
    if sphere_status:
        query = query.filter(models.Category.sphere_status==sphere_status)
    return (
        query.group_by(models.Tools.name, models.Expanditure.tool_id,models.Tools.price)
        .filter(models.Expanditure.created_at.between(started_at, finished_at))
        .all()
    )


def getexpanditureid(db: Session, id):
    query = db.query(models.Expanditure).filter(models.Expanditure.tool_id == id).all()
    return query


def get_files(db: Session):
    query = (
        db.query(models.Files)
        .join(models.Requests)
        .order_by(models.Requests.created_at.desc())
        .limit(50)
        .all()
    )
    for i in query:
        # time.sleep(2)
        file = requests.get(backend_url + f"/{i.url}")
        try:
            with open(i.url, "wb") as f:
                f.write(file.content)
        except:
            pass
    return True


def send_to_user_message(db: Session, message):
    query = db.query(models.Users).filter(models.Users.telegram_id.isnot(None)).all()
    try:
        for i in query:
            sendtotelegramchannel(
                bot_token=bot_token, chat_id=i.telegram_id, message_text=message
            )
            # time.sleep(4)
    except:
        pass
    return True

def tools_update(db: Session,form_data:schemas.ToolsUpdate):
    query = db.query(models.Tools).filter(models.Tools.id==form_data.id).first()
    if query:
        if form_data.price is not None:
            query.price = form_data.price
        if form_data.amount_left is not None:
            query.amount_left = form_data.amount_left
        if form_data.total_price:
            query.total_price = form_data.total_price
        if form_data.department is not None:
            query.department = form_data.department
        if form_data.min_amount is not None:
            query.min_amount = form_data.min_amount
        if form_data.max_amount is not None:
            query.max_amount = form_data.max_amount
        if form_data.image is not None:
            query.image = form_data.image
        if form_data.ftime is not None:
            query.ftime = form_data.ftime
        db.commit()
        db.refresh(query)
    return query


def tools_query_iarch(db: Session, parent_id):
    query = db.query(models.Tools)
    if parent_id is not None:
        query = query.filter(models.Tools.parentid == str(parent_id)).all()
    else:
        return []
    return query

def few_tools_query(db: Session):
    query = db.query(models.Tools)
    query = query.filter(models.Tools.amount_left<models.Tools.min_amount).all()
    return query

def order_tool_create(db:Session,user_id):
    tools = few_tools_query(db=db)
    if not tools:
        return False
    query = models.ToolsOrder(user_id=user_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    for i in tools:
        ordering_amount = i.max_amount - i.amount_left
        tool_query = models.NeededTools(tool_id=i.id,toolorder_id=query.id,ordered_amount = ordering_amount,amount_last=i.amount_left)
        db.add(tool_query)
        db.commit()
    return True


def tools_order_query(db: Session, status,id):
    query = db.query(models.ToolsOrder)
    if status is not None:
        query = query.filter(models.ToolsOrder.status == status)
    if id is not None:
        query = query.filter(models.ToolsOrder.id == id)
    return query.order_by(models.ToolsOrder.created_at.desc()).all()

def needed_tools(db:Session,toolorder_id):
    query = db.query(models.NeededTools).filter(models.NeededTools.toolorder_id==toolorder_id).all()
    return query

def tools_order_update(db:Session,form_data:schemas.ToolOrderUpdate):
    query = db.query(models.ToolsOrder).filter(models.ToolsOrder.id==form_data.id).first()
    if query:
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
    return query


def brigade_openrequests(db:Session,department,sphere_status):
    query = (
        db.query(
            models.Brigada.id,
            models.Brigada.name,
            func.count(
                models.Requests.id).label("request_count"),
        )
        .outerjoin(models.Requests)
        .outerjoin(models.Category)
        .filter(
            models.Requests.status.in_([1,2]),
            models.Brigada.department == department
        )
        .group_by(models.Brigada.id, models.Brigada.name)
    )

    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status == sphere_status)

    result = query.all()

    return result

def new_requestsamount(db:Session,department,sphere_status,sub_id):
    query = db.query(func.count(models.Requests.id)).join(models.Category).filter(models.Requests.status==0).filter(models.Category.department==department)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)    
    return query.all()


def avg_ratingrequests(db:Session,department,sphere_status,sub_id):
    query = db.query(cast(func.avg(models.Comments.rating), Integer)).join(models.Requests).join(models.Category).filter(models.Requests.status==3).filter(models.Category.department==department)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    return query.all()



def avg_time_finishing(db:Session,department,sphere_status,sub_id,timer=60 ):
    total = db.query(
            func.cast(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Requests.finished_at - models.Requests.started_at,
                    )
                )
                / timer,
                Integer,
            ),
        ).join(models.Category).filter(
            models.Requests.status == 3,
            models.Category.department == department)
    if sphere_status is not None:
        total = total.filter(models.Category.sphere_status == sphere_status) 
    if sub_id is not None:
        total = total.filter(models.Category.sub_id==sub_id)

        
    return total.all()


def total_request_count(db:Session,department,sphere_status,sub_id):
    query = db.query(func.count(models.Requests.id)).join(models.Category).filter(models.Category.department==department)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    return query.all()


def in_progress_requests(db:Session,department,sphere_status,sub_id):
    query = db.query(func.count(models.Requests.id)).join(models.Category).filter(models.Category.department==department).filter((or_(models.Requests.status==1,models.Requests.status==2)))
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    return query.all()

def last_30_days(db:Session,department,sphere_status,sub_id):
    query = db.query(func.count(models.Requests.id)).join(models.Category).filter(models.Category.department==department).filter(models.Requests.created_at>=datetime.now(timezonetash)-timedelta(days=30)).filter(models.Requests.status==3)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    
    return query.all()

def current_month(db:Session,department,sphere_status,sub_id):
    query = db.query(func.count(models.Requests.id)).join(models.Category).filter(models.Category.department==department).filter(models.Requests.created_at>=datetime.now(timezonetash).replace(day=1)).filter(models.Requests.status==3)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        query = query.filter(models.Category.sub_id==sub_id)
    return query.all()

def safia_eats(db:Session,request_data):
    query = db.query(models.Requests).join(models.Category).filter(models.Category.department==6).filter(cast(models.Requests.arrival_date,Date)==request_data).all()
    return query


def marketing_stats_v2(db:Session,started_at, finished_at,department,sphere_status,sub_id,timer=60):
    categories = db.query(models.Category).join(models.Requests).filter(models.Category.status==1)
    if sphere_status is not None:
        categories = categories.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        categories = categories.filter(models.Category.sub_id==sub_id)
    if department is not None:
        categories = categories.filter(models.Category.department==department)
    if finished_at is not None and started_at is not None:
        categories = categories.filter(models.Requests.created_at.between(started_at,finished_at))
    categories = categories.filter(models.Requests.status.in_([0,1,2,3]))
    categories = categories.all()
    

    data = {}
    for category in categories:
        #---------time delta create------------
        ftime_timedelta = timedelta(seconds=category.ftime*3600)

        #---------number of total requests-----------
        total_requests = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status.in_([0,1,2,3]))
        if started_at is not None and finished_at is not None:
            total_requests = total_requests.filter(models.Requests.created_at.between(started_at,finished_at))
        total_requests = total_requests.count()


        #---------number of finished on time requests-----------
        finished_on_time = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status==3).filter(
            models.Requests.finished_at - models.Requests.started_at <= ftime_timedelta
        )
        if started_at is not None and finished_at is not None:
            finished_on_time = finished_on_time.filter(models.Requests.created_at.between(started_at,finished_at))
        finished_on_time = finished_on_time.count()


        #---------number of not finished on time requests-----------
        not_finished_on_time = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status==3).filter(
            models.Requests.finished_at - models.Requests.started_at > ftime_timedelta)
        if started_at is not None and finished_at is not None:
            not_finished_on_time = not_finished_on_time.filter(models.Requests.created_at.between(started_at,finished_at))
        not_finished_on_time = not_finished_on_time.count()
        

        #---------number of status zero requests-----------
        status_zero = db.query(models.Requests).filter(models.Requests.category_id==category.id).filter(models.Requests.status.in_([0,1,2]))
        if started_at is not None and finished_at is not None:
            status_zero = status_zero.filter(models.Requests.created_at.between(started_at,finished_at))
        status_zero = status_zero.count()

        #---------calculating percentages-----------
        try:
            percentage_finished_on_time = (finished_on_time / total_requests) * 100
        except:
            percentage_finished_on_time = 0
        try:
            percentage_not_finished_on_time = (not_finished_on_time / total_requests) * 100
        except:
            percentage_not_finished_on_time = 0
        try:
            percentage_status_zero = (status_zero / total_requests) * 100

        except:
            percentage_status_zero = 0


        #------------average finishing time------------
        total = (
        db.query(
            models.Category.name,
            func.count(models.Requests.id),
            func.cast(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Requests.finished_at - models.Requests.started_at,
                    )
                )
                / timer,
                Integer,
            ),
        )
        .join(models.Requests)
        .filter(
            models.Requests.status.in_([0,1,2,3]),
            models.Category.id == category.id,
        )
        .group_by(models.Category.name)
        
        )
        if started_at is not None and finished_at is not None:
            total = total.filter(models.Requests.created_at.between(started_at,finished_at))
        total = total.all()

        #------------end avg finishing time------------



        #------------create response data------------

        if total:
            total = total[0][2]
        else: 
            total = 0
        
        dict_data = {
            "total_requests":total_requests,
            "finished_on_time":finished_on_time,
            "not_finished_on_time":not_finished_on_time,
            "status_zero":status_zero,
            "percentage_finished_on_time":percentage_finished_on_time,
            "percentage_not_finished_on_time":percentage_not_finished_on_time,
            "percentage_status_zero":percentage_status_zero,
            "avg_finishing":total,
            'category':category.name
        }
        if data.get(category.sub_id):
            data[category.sub_id].append(dict_data)
        else:
            data[category.sub_id] = [dict_data]

        
    return data



def inventory_stats(db:Session,started_at,finished_at,department,timer=60):

    parent_ids = db.query(models.Tools).join(models.Expanditure).join(models.Requests).join(models.Category).filter(models.Category.department==department)
    
    if started_at is not None and finished_at is not None:
        parent_ids = parent_ids.filter(models.Requests.created_at.between(started_at,finished_at))

    parent_ids = parent_ids.distinct(models.Tools.parentid).filter(models.Requests.status==3).filter(models.Tools.ftime!=None).all()
    data = {}

    #ftime_timedelta = timedelta(seconds=48*3600)
    ftime_timedelta = 48*3600
    for parent_id in parent_ids:

        total = (
        db.query(
            func.cast(
                func.avg(
                    func.extract(
                        "epoch",
                        models.Requests.finished_at - models.Requests.started_at,
                    )
                )
                / timer,
                Integer,
            ),
        )
        .join(models.Expanditure).join(models.Tools).join(models.Category)
        .filter(
            models.Requests.status==3,
            models.Tools.department== department,
            models.Tools.parentid == parent_id.parentid,
        )
        .group_by(models.Tools.parentid)
        )
        if started_at is not None and finished_at is not None:
            total = total.filter(models.Requests.created_at.between(started_at,finished_at))
        total = total.all()


        total_tools = db.query(models.Expanditure).join(models.Requests).join(models.Category).join(models.Tools).filter(
            models.Tools.parentid==parent_id.parentid).filter(
            models.Category.department==department).filter(
            models.Tools.ftime.is_not(None)).filter(
            models.Requests.status.in_([0,1,2,3])).count()
        
        # on_time_requests = db.query(models.Expanditure).join(models.Requests).join(models.Category).join(models.Tools).filter(models.Tools.parentid==parent_id.parentid).filter(
        #     models.Category.department==department).filter(
        #     models.Tools.ftime.is_not(None)).filter(
        #     models.Requests.status==3 ).filter(func.extract('epoch', models.Requests.finished_at - models.Requests.started_at) <= ftime_timedelta.total_seconds()).count()
         


        # not_finishedon_time =db.query(models.Expanditure).join(models.Requests).join(models.Tools).join(models.Category).filter(models.Tools.parentid==parent_id.parentid).filter(
        #     models.Category.department==department).filter(
        #     models.Tools.ftime.is_not(None)).filter(
        #     models.Requests.status==3).filter(func.extract('epoch', models.Requests.finished_at - models.Requests.started_at) <= ftime_timedelta.total_seconds()).count()



        finished_ontime = db.query(
        func.count(models.Requests.id)).join(models.Expanditure).join(models.Tools).join(models.Category).filter(
        models.Requests.status == 3,
        models.Tools.ftime!=None,
        models.Tools.parentid == parent_id.parentid,
        models.Category.department==department,
        func.extract('epoch', models.Requests.finished_at - models.Requests.started_at) <= ftime_timedelta).all()[0][0]


        not_finished_ontime = db.query(
        func.count(models.Requests.id)).join(models.Expanditure).join(models.Tools).join(models.Category).filter(
        models.Requests.status == 3,
        models.Tools.ftime!=None,
        models.Tools.parentid == parent_id.parentid,
        models.Category.department==department,
        func.extract('epoch', models.Requests.finished_at - models.Requests.started_at)> ftime_timedelta).all()[0][0]

        # not_finishedon_time =db.query(models.Expanditure).join(models.Requests).join(models.Tools).join(models.Category).filter(
        # models.Requests.status == 3,
        # models.Tools.ftime!=None,
        # extract('epoch', models.Requests.finished_at - models.Requests.started_at) > models.Tools.ftime * 3600,
        # models.Tools.parentid == parent_id.parentid,
        # models.Category.department==department
        # ).count()

        not_started = db.query(models.Expanditure).join(models.Requests).join(models.Category).join(models.Tools).filter(models.Tools.parentid==parent_id.parentid).filter(
            models.Category.department==department).filter(
            models.Tools.ftime.is_not(None)).filter(
            models.Requests.status.in_([0,1,2])).count()

        
        not_finishedon_time_percent = (finished_ontime/total_tools)*100
        on_time_requests_percent = (finished_ontime/total_tools)*100
        not_started_percent = (not_started/total_tools)*100

        parent_id_name = db.query(models.ToolParents).filter(models.ToolParents.id==parent_id.parentid).first()

        if total[0][0] is not None:
            avg_finishing = total[0][0]
        else:
            avg_finishing= 0
        data[parent_id_name.name] = {'total_tools':total_tools,
                                     "on_time_requests":finished_ontime,
                                     'not_finishedontime':not_finished_ontime,
                                     'not_even_started':not_started,
                                        'not_finishedon_time_percent':not_finishedon_time_percent,
                                        'on_time_requests_percent':on_time_requests_percent,
                                        'not_started_percent':not_started_percent,
                                        'avg_finishing':avg_finishing
                                     }

        

    return data

