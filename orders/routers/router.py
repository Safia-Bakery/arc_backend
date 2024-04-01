# ----------import packages
from datetime import datetime, timedelta, date, time
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, UploadFile, status, BackgroundTasks,Query
from pydantic import ValidationError,Json
import statisquery
import schemas
import bcrypt
from typing import Annotated, Dict,Union,Any
from uuid import UUID
import models
from microservices import (
    sendtotelegramchannel,
    sendtotelegram,
    sendtotelegramaddcomment,
    inlinewebapp,authiiko,send_document_iiko
)
from typing import Optional
import crud
from microservices import get_current_user, get_db
from database import engine, SessionLocal
from fastapi_pagination import paginate, Page, add_pagination
from dotenv import load_dotenv
from microservices import (
    create_refresh_token,
    verify_password,
    create_access_token,
    checkpermissions,
)
import pytz

# from main import get_db,get_current_user
from fastapi import APIRouter, Form
from users.schema import schema
import os
from orders.crud import query
from orders.utils import util
from orders.schema import schema_router

timezonetash = pytz.timezone("Asia/Tashkent")

load_dotenv()
router = APIRouter()


bot_token = os.environ.get("BOT_TOKEN")

BASE_URL = "https://api.service.safiabakery.uz/"
FRONT_URL = "https://admin.service.safiabakery.uz/"


@router.post("/category")
async def add_category(
    name: Annotated[str, Form()],
    department: Annotated[int, Form()],
    ftime: Annotated[float, Form()] = None,
    description: Annotated[str, Form()] = None,
    status: Annotated[int, Form()] = 1,
    urgent: Annotated[bool, Form()] = True,
    sphere_status: Annotated[int, Form()] = None,
    file: UploadFile = None,
    sub_id: Annotated[int, Form()] = None,
    parent_id:Annotated[int,Form()]=None,
    is_child:Annotated[bool,Form()]=False,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    if file is not None:
        # for file in image:
        folder_name = f"files/{util.generate_random_filename()+file.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        file = folder_name
    return crud.add_category_cr(
        db=db,
        ftime=ftime,
        name=name,
        description=description,
        status=status,
        urgent=urgent,
        department=department,
        sphere_status=sphere_status,
        sub_id=sub_id,
        file=file,
        parent_id=parent_id,
        is_child=is_child,
    )


@router.put("/category")
async def update_category(
    id: Annotated[int, Form()],
    name: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    status: Annotated[int, Form()] = None,
    urgent: Annotated[bool, Form()] = None,
    department: Annotated[int, Form()] = None,
    ftime: Annotated[float, Form()] = None,
    sphere_status: Annotated[int, Form()] = None,
    file: UploadFile = None,
    sub_id: Annotated[int, Form()] = None,
    parent_id:Annotated[int,Form()]=None,
    is_child:Annotated[bool,Form()]=None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    if file is not None:
        # for file in image:
        folder_name = f"files/{util.generate_random_filename()+file.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        file = folder_name
    response = crud.update_category_cr(
        db=db,
        id=id,
        file=file,
        name=name,
        description=description,
        status=status,
        urgent=urgent,
        department=department,
        sphere_status=sphere_status,
        sub_id=sub_id,
        ftime=ftime,
        parent_id=parent_id,
        is_child=is_child
    )
    if response:
        return response
    else:
        return {"message": "not found"}


@router.get("/category", response_model=Page[schemas.GetCategorySch])
async def filter_category(
    sphere_status: Optional[int] = None,
    sub_id: Optional[int] = None,
    department: Optional[int] = None,
    category_status: Optional[int] = None,
    name: Optional[str] = None,
    parent_id:Optional[int]=None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    response = crud.filter_category(
        db,
        category_status=category_status,
        name=name,
        sub_id=sub_id,
        department=department,
        sphere_status=sphere_status,
        parent_id=parent_id
    )
    return paginate(response)


@router.get("/category/{id}", response_model=schemas.GetCategorySch)
async def get_category_id(
    id: int,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    try:
        response = crud.get_category_id(db, id)
        return response
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="info with this id not found "
        )


@router.get("/request", response_model=Page[schemas.GetRequestList])
async def filter_request(
    department: Optional[int] = None,
    sub_id: Optional[int] = None,
    id: Optional[int] = None,
    category_id: Optional[int] = None,
    fillial_id: Optional[UUID] = None,
    created_at: Optional[date] = None,
    request_status: Optional[str] = None,
    user: Optional[str] = None,
    sphere_status: Optional[int] = None,
    brigada_id: Optional[int] = None,
    arrival_date: Optional[date] = None,
    db: Session = Depends(get_db),
    rate: Optional[bool] = False,
    request_user: schema.UserFullBack = Depends(get_current_user),
    urgent: Optional[bool] = None,
    reopened: Optional[bool] = None,
    started_at: Optional[date] = None,
    finished_at: Optional[date] = None,

):  
    
    if request_user.brigada_id:
        requestdata = crud.filter_request_brigada(
            db,
            id=id,
            sub_id=sub_id,
            category_id=category_id,
            fillial_id=fillial_id,
            request_status=request_status,
            created_at=created_at,
            user=user,
            brigada_id=request_user.brigada_id,
            sphere_status=sphere_status,
            department=department,
            arrival_date=arrival_date,
            rate=rate,
            urgent=urgent,
            reopened=reopened,
            started_at=started_at,
            finished_at=finished_at

        )
        return paginate(requestdata)
    request_list = crud.filter_requests_all(
        db,
        sub_id=sub_id,
        department=department,
        id=id,
        category_id=category_id,
        fillial_id=fillial_id,
        request_status=request_status,
        created_at=created_at,
        user=user,
        sphere_status=sphere_status,
        arrival_date=arrival_date,
        rate=rate,
        brigada_id=brigada_id,
        urgent=urgent,
        reopened=reopened,
        started_at=started_at,
        finished_at=finished_at
    )
    return paginate(request_list)


@router.get("/request/{id}", response_model=schemas.GetRequestid)
async def get_request_id(
    id: int,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    try:
        request_list = crud.get_request_id(db, id)
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")


@router.put("/request/attach/brigada")
async def put_request_id(
    form_data: schemas.AcceptRejectRequest,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    request_list = crud.acceptreject(
        db, form_data=form_data, user=request_user.full_name
    )

    if form_data.status == 1:
        try:
            brigada_id = request_list.brigada.id
            brigader_telid = crud.get_user_brig_id(db, brigada_id).telegram_id
            sendtotelegramchannel(
                bot_token=bot_token,
                chat_id=brigader_telid,
                message_text=f"{request_list.brigada.name} вам назначена заявка, #{request_list.id}s {request_list.fillial.name}",
            )
        except:
            pass
        if request_list.category.department == 1:
            try:
                sendtotelegramchannel(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, на вашу заявку #{request_list.id}s назначена команда🚙: {request_list.brigada.name}",
                )
            except:
                pass
        if request_list.category.department == 5:
            try:
                sendtotelegramchannel(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, на вашу заявку #{request_list.id}s по Запросу машины🚛: В процессе.",
                )
            except:
                pass
        if request_list.category.department == 3:
            try:
                finishing_time = request_list.finishing_time
                sendtotelegramchannel(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Маркетингу: В процессе.\n\n⏳Примерный срок завершения: {finishing_time}",
                )
            except:
                pass
        if request_list.category.department==2:
            try:
                sendtotelegramchannel(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Inventary: В процессе.",
                )
                
            except:
                pass
        if request_list.category.department==4:

            try:
                sendtotelegramchannel(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s назначен специалист👨‍💻: {request_list.brigada.name}\nВремя выполнения: {int(request_list.category.ftime)} часов",
                )
            except:
                pass
    elif form_data.status == 2:
        if request_list.category.department == 5:
            try:
                sendtotelegramchannel(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, мы отправили транспорт по вашему запросу #{request_list.id}s Ожидайте его прибытия. \n🚛Грузовик: {request_list.cars.name} {request_list.cars.number}")
            except:
                pass
    elif form_data.status == 3:
        url = f"{FRONT_URL}tg/order-rating/{request_list.id}?user_id={request_list.user.id}&department={request_list.category.department}&sub_id={request_list.category.sub_id}"
        if request_list.category.department == 3:
            try:
                inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Маркетингу: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except:
                pass
        if request_list.category.department == 5:
            try:
                inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по Запросу машины🚛: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except:
                pass
        if request_list.category.department == 1:
            try:
                inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по APC: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except:
                pass
        if request_list.category.department == 6:
            try:
                inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except:
                pass
        if request_list.category.department == 4:
            try:
                inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id}s по IT: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except:
                pass
        if request_list.category.department == 2:
            # message_ready  is for sending product to user
            message_ready = f"""Уважаемый {request_list.user.full_name}, инвентарь по вашей заявке #{request_list.id}s """
            
            new_neq = []
            for i in request_list.expanditure:
                if i.status==0:
                    new_neq.append(i)
                else:
                    message_ready += f"\n{i.tool.name} - {i.amount} шт. "
                    edit_expenditure = crud.synch_expanditure_crud(db, id=i.id)
                    send_document_iiko(key=authiiko(), data=edit_expenditure)

            message_ready += "\nГотов и отправлен вам на филиал, прибудет через 12 часов."

            if new_neq:

                message_ready+=f"\n\n♻️Инвентарь в обработке:"

                new_request = crud.add_request(db=db,
                                 category_id=request_list.category_id,
                                 fillial_id=request_list.fillial_id,
                                 description=request_list.description,
                                 product=request_list.product,
                                 user_id=request_list.user_id,
                                 is_bot=0,
                                 size=request_list.size,
                                 bread_size=request_list.bread_size,
                                 location=request_list.location,
                                 arrival_date=request_list.arrival_date,
                                vidfrom=None,
                                vidto=None,
                                finishing_time=None
                                 )
                for i in new_neq:
                    message_ready+=f"\n{i.tool.name} - {i.amount} шт. "
                    query.add_expenditure(db=db,
                                         request_id=new_request.id,
                                         tool_id=i.tool_id,
                                         amount=i.amount,
                                         comment=i.comment,
                                         status=0
                                         )
                message_ready +="\nПри первой возможности будет отправлено"
            try:
                inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=message_ready,
                    url=url,
                )
            except:
                pass
    elif form_data.status == 4:
        if request_list.category.department == 4:
            url = f"{FRONT_URL}tg/order-rating/{request_list.id}?user_id={request_list.user.id}&department={request_list.category.department}&sub_id={request_list.category.sub_id}"
            inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"""❌Ваша заявка #{request_list.id}s по IT👨🏻‍💻 отменена по причине: {request_list.deny_reason}\n\nЕсли Вы с этим не согласны, поставьте, пожалуйста, рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий.""",
                    url=url,
                )
        else:
            sendtotelegramchannel(
                bot_token=bot_token,
                chat_id=request_list.user.telegram_id,
                message_text=f"Ваша заявка #{request_list.id}s была отменена по причине: {request_list.deny_reason}",
            )
    elif form_data.status == 5:
        sendtotelegramchannel(
            bot_token=bot_token,
            chat_id=request_list.user.telegram_id,
            message_text=f"Уважаемый {request_list.user.full_name}, ваша заявка #{request_list.id}s временно приостановлена по причине: {request_list.pause_reason}",
        )
    elif form_data.status == 6:

        url = f"{FRONT_URL}tg/order-rating/{request_list.id}?user_id={request_list.user.id}&department={request_list.category.department}&sub_id={request_list.category.sub_id}"

        inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"""Уважаемый {request_list.user.full_name}, Ваша заявка #{request_list.id}s решена.\n
В течение 3-х дней вы можете сказать "Спасибо" или пожаловаться на выполнение. Поставьте, пожалуйста, рейтинг решения вашей заявки от 1 до 5.""",
                    url=url,
                )
    elif form_data.status == 7:
       sendtotelegramchannel(
                bot_token=bot_token,
                chat_id=request_list.user.telegram_id,
                message_text=f"Ваша заявка #{request_list.id}s возобновлено",
            ) 
    elif form_data.status == 8:
        if request_list.category.department == 4:
            url = f"{FRONT_URL}tg/order-rating/{request_list.id}?user_id={request_list.user.id}&department={request_list.category.department}&sub_id={request_list.category.sub_id}"
            inlinewebapp(
                    bot_token=bot_token,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"""❌Ваша заявка #{request_list.id}s по IT👨🏻‍💻 отменена по причине: {request_list.deny_reason}\n\nЕсли Вы с этим не согласны, поставьте, пожалуйста, рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий.""",
                    url=url,
                )
    return request_list


@router.post("/request")
async def get_category(
    fillial_id: Annotated[UUID, Form()],
    category_id: Annotated[int,Form()],
    description: Annotated[str, Form()]=None,
    files: list[UploadFile] = None,
    cat_prod: Json=Form(None),
    factory: Annotated[bool,Form()] = False,
    location: Json=Form(None),
    size: Annotated[str,Form] = None,
    bread_size: Annotated[str,Form()]= None,
    arrival_date: Annotated[datetime,Form()] = None,
    product: Annotated[str,Form()]=None,
    expenditure:Json=Form(None),
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
    vidfrom: Annotated[str,Form()] = None,
    vidto: Annotated[str,Form()] = None
):
    # try:
    category_query = crud.get_category_id(db=db, id=category_id)


    if category_query.department == 1:
        origin = 1
    elif category_query.department == 2:
        origin = 2
    else:
        origin = None
    parent_fillial = crud.getparentfillial(db, fillial_id)
    if parent_fillial:
        if parent_fillial.is_fabrica==1:
            fillial_id = parent_fillial.id
            sklad_id = fillial_id
        else:
            filliald_od = crud.filterbranchchildid(db, fillial_id, origin=origin)
            sklad_id = filliald_od.id
    else:
        sklad_id = fillial_id
        
    if category_query.department == 4:
        deadline = timedelta(hours=category_query.ftime)
        current_time = datetime.now(tz=timezonetash)
        finishing_time = current_time + deadline
    else:
        finishing_time = None
    responserq = crud.add_request(
        db,
        category_id=category_id,
        description=description,
        fillial_id=sklad_id,
        product=product,
        user_id=request_user.id,
        is_bot=0,
        size=size,
        arrival_date=arrival_date,
        bread_size=bread_size,
        location=location,
        vidfrom=vidfrom,
        vidto=vidto,
        finishing_time=finishing_time

    )
    if cat_prod is not None:
        for product_id, amount in dict(cat_prod).items():
            query.add_product_request(
                db=db, request_id=responserq.id, product_id=product_id, amount=amount
            )

    file_obj_list = []
    # parsed_datetime = datetime.strptime(responserq.created_at,"%Y-%m-%dT%H:%M:%S.%f")
    formatted_datetime_str = responserq.created_at.strftime("%d.%m.%Y %H:%M")
    text = (
        f"📑Заявка № {responserq.id}\n\n📍Филиал: {responserq.fillial.parentfillial.name}\n"
        f"🕘Дата поступления заявки: {formatted_datetime_str}\n\n"
        f"🔰Категория проблемы: {responserq.category.name}\n"
        f"⚙️ Название оборудования: {responserq.product}\n"
        f"💬Комментарии: {responserq.description}"
    )
    if expenditure:
        for tool_id,amount in expenditure.items():
            query.add_expenditure(db=db, request_id=responserq.id, tool_id=tool_id, amount=amount[0],comment=amount[1],status=0)
    if files:
        for file in files:
            file_path = f"files/{file.filename}"
            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            file_obj_list.append(models.Files(request_id=responserq.id, url=file_path))
    crud.bulk_create_files(db, file_obj_list)
    keyboard = []
    if responserq.file:
        for i in responserq.file:
            keyboard.append(
                {"text": "Посмотреть фото/видео", "url": f"{BASE_URL}{i.url}"}
            )
    if responserq.category.sphere_status == 1 and responserq.category.department == 1:
        sendtotelegram(
            bot_token=bot_token,
            chat_id="-1001920671327",
            message_text=text,
            keyboard=keyboard,
        )
    if responserq.category.sphere_status == 2 and responserq.category.department == 1:
        sendtotelegram(
            bot_token=bot_token,
            chat_id="-1001831677963",
            message_text=text,
            keyboard=keyboard,
        )
    if responserq.category.department==8:
        sendtotelegramchannel(
            bot_token=bot_token,
            chat_id="-1002124172379",
            message_text="📑Заявка № "+str(responserq.id)+"\n\n📍Филиал: "+str(responserq.fillial.parentfillial.name)+"\n🕘Дата поступления заявки: "+str(formatted_datetime_str)+"\n\n🏳️Дата и время начало события: "+responserq.update_time['vidfrom']+"\n🏁Дата и время конца события: "+responserq.update_time['vidto']+"\n\n💬Комментарии: "+str(responserq.description),
        )

    return {"success": True, "message": "everything is saved"}


@router.get(
    "/categories/fillials",
    summary="you can get list of fillials and categories when you are creating request",
)
async def get_category_and_fillials(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    permission = checkpermissions(request_user=request_user, db=db, page=25)
    if permission:
        try:
            categories = crud.get_category_list(db)
            fillials = crud.get_fillial_list(db)
            return {"categories": categories, "fillials": fillials}
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="this is server error ",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not super user"
        )


@router.get("/users", response_model=Page[schemas.UserGetlist])
async def filter_user(
    full_name: Optional[str] = None,
    username: Optional[str] = None,
    role_id: Optional[int] = None,
    phone_number: Optional[str] = None,
    user_status: Optional[int] = None,
    position: Optional[bool] = True,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    users = crud.filter_user(
        db,
        user_status=user_status,
        username=username,
        phone_number=phone_number,
        role_id=role_id,
        full_name=full_name,
        position=position,
    )
    return paginate(users)


@router.put("/users", response_model=schemas.UserGetlist)
async def filter_user(
    form_data: schemas.UserUpdateAll,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    updateuser = crud.update_user(db, form_data=form_data)
    return updateuser


@router.get("/users/{id}", response_model=schemas.GetUserIdSch)
async def get_user_with_id(
    id: int,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    users = crud.get_user_id(db, id)
    if users:
        return users
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


@router.post("/tools", response_model=schemas.CreateTool)
async def get_user_with_id(
    form_data: schemas.CreateTool,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    permission = checkpermissions(
        request_user=request_user, db=db, page="onlysuperadmin"
    )
    if permission:
        tools = crud.create_tool(db, form_data)
        return tools
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not super user"
        )


#@router.get("/tools/", response_model=Page[schemas.GetToolList])
#async def get_tool_list(
#    db: Session = Depends(get_db),
#    request_user: schema.UserFullBack = Depends(get_current_user),
#):
#    try:
#        query_from = crud.get_list_tools(db)
#        return paginate(query_from)
#    except:
#        raise HTTPException(
#            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#            detail="database not found",
#        )


@router.get("/get/fillial/fabrica", response_model=Page[schemas.GetFillialChild])
async def get_fillials_fabrica(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    return paginate(crud.getfillialchildfabrica(db))


@router.get("/get/files")
async def get_files_another_service(
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    background_task.add_task(statisquery.get_files(db))

    return {"success": True}


@router.post("/send/message")
async def send_message_to_users(
    message: str,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    background_task.add_task(statisquery.send_to_user_message(db=db, message=message))
    return {"success": True}


@router.get("/v1/stats/marketing/pie")
async def marketing_pie_stats(
    timer: int,
    created_at: date,
    finished_at: date,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    table = query.marketing_table(
        db=db, created_at=created_at, finished_at=finished_at, timer=timer
    )
    pie = query.marketing_pie(db=db, created_at=created_at, finished_at=finished_at)
    order = {"pie": pie, "table": table}
    return order


@router.get("/v1/stats/marketing/cat")
async def marketing_cat_stats(
    created_at: date,
    finished_at: date,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    table = query.category_percent(
        db=db, created_at=created_at, finished_at=finished_at
    )
    pie = query.category_pie(db=db, created_at=created_at, finished_at=finished_at)
    return {"tables": table, "pie": pie}


@router.put("/v1/request/redirect", response_model=schemas.GetRequestid)
async def redirect_request(
    form_data: schema_router.RedirectRequest,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    db_query = query.redirect_request(db=db, form_data=form_data)
    return db_query


@router.get("/v1/department/count")
async def counter_department(
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    db_query = query.department_counter(db=db)
    return {
        "counter": db_query,
        "comment": "first data inside list is department id ||| second data is sphere_status ||| third data is number of new requests",
    }


@router.post("/v1/cat/product", response_model=schema_router.UpdateGetCatProduct)
async def create_cat_product(
    category_id: Annotated[int, Form()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()] = None,
    status: Annotated[int, Form()] = 1,
    image: UploadFile = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    if image:
        file_path = f"files/{util.generate_random_filename()}{image.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path = None
    db_query = query.createcat_product(
        category_id=category_id,
        name=name,
        image=file_path,
        status=status,
        db=db,
        description=description,
    )
    return db_query


@router.put("/v1/cat/product", response_model=schema_router.UpdateGetCatProduct)
async def update_cat_product(
    id: Annotated[int, Form()],
    status: Annotated[int, Form()] = None,
    description: Annotated[str, Form()] = None,
    category_id: Annotated[int, Form()] = None,
    name: Annotated[str, Form()] = None,
    image: UploadFile = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),
):
    if image:
        file_path = f"files/{util.generate_random_filename()}{image.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path = None
    db_query = query.updatecat_product(
        id=id,
        name=name,
        category_id=category_id,
        status=status,
        image=file_path,
        db=db,
        description=description
    )
    return db_query

#get category products list 
@router.get("/v1/cat/product", response_model=list[schema_router.UpdateGetCatProduct])
async def query_cat_product(
    id: Optional[int] = None,
    category_id: Optional[int] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user),):
    db_query = query.querycat_product(db=db, id=id, name=name, category_id=category_id)
    return db_query


@router.post("/v1/cars", response_model=schema_router.CarsGet)
async def create_cars(
    form_data: schema_router.CarsCreate,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    db_query = query.cars_add(db=db, name=form_data.name, status=form_data.status, number=form_data.number)
    return db_query


@router.put("/v1/cars", response_model=schema_router.CarsGet)
async def update_cars(
    form_data: schema_router.CarsUpdate,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    db_query = query.cars_update(db=db, id=form_data.id, name=form_data.name, status=form_data.status, number=form_data.number)
    return db_query


@router.get("/v1/cars", response_model=list[schema_router.CarsGet])
async def query_cars(
    id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[int] = None,
    number: Optional[str] = None,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    db_query = query.cars_query(db=db, id=id, name=name, status=status,number=number)
    return db_query

@router.put("/v1/expenditure", response_model=schema_router.UpdateExpenditure)
async def update_expenditure(
    form_data: schema_router.UpdateExpenditure,
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):
    db_query = query.update_expenditure(db=db, form_data=form_data)
    return db_query


@router.post("/v1/reqest/message",response_model=schema_router.MessageRequestCreate,tags=["Message"])
async def create_message(
    request_id: Annotated[int,Form()],
    message: Annotated[str,Form()] = None,
    status: Annotated[int,Form()] = None,
    photo: UploadFile = None,   
    db: Session = Depends(get_db),
    request_user: schema.UserFullBack = Depends(get_current_user)):

    if photo:
        file_path = f"files/{util.generate_random_filename()}{photo.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await photo.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path = None

    db_query = query.message_create(db=db, request_id=request_id, message=message, status=status, photo=file_path,user_id=request_user.id)
    return db_query

