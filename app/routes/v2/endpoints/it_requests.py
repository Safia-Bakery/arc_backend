import pytz
from datetime import datetime, timedelta
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud import it_requests, users, communication, logs, files
from app.models.category import Category
from app.routes.depth import get_db, get_current_user
from app.schemas.it_extra import *
from app.schemas.it_requests import GetRequest, PutRequest, MessageRequestCreate, CreateRequest
from app.schemas.requests import GetOneRequest
from app.schemas.users import UserFullBack
from app.utils.utils import sendtotelegramchat, sendtotelegramtopic, delete_from_chat, edit_topic_message, \
    inlinewebapp, confirmation_request, generate_random_filename, send_notification, edit_topic_reply_markup


it_requests_router = APIRouter()

timezonetash = pytz.timezone("Asia/Tashkent")

scheduler = BackgroundScheduler()
scheduler.start()


def get_children(category_id, db: Session):
    children = db.query(Category).filter_by(parent_id=category_id).filter(Category.status == 1)
    children = children.all()
    for child in children:
        yield child
        yield from get_children(child.id, db=db)


@it_requests_router.get("/requests/it", response_model=Page[GetRequest])
async def filter_requests(
        id: Optional[int] = None,
        category_id: Optional[int] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        user: Optional[str] = None,
        brigada_id: Optional[int] = None,
        arrival_date: Optional[date] = None,
        rate: Optional[bool] = False,
        urgent: Optional[bool] = None,
        started_at: Optional[date] = None,
        finished_at: Optional[date] = None,
        is_expired: Optional[bool] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    # if user input data it filter all child categories
    # so in this case get child function gets all child categories
    if category_id is not None:
        cat_list = []
        cat_list.append(category_id)

        for i in get_children(category_id=category_id, db=db):
            cat_list.append(i.id)
    else:
        cat_list = None

    if request_user.brigada_id:
        requestdata = it_requests.filter_request_brigada(
            db,
            id=id,
            category_id=cat_list,
            fillial_id=fillial_id,
            request_status=request_status,
            created_at=created_at,
            user=user,
            brigada_id=request_user.brigada_id,
            arrival_date=arrival_date,
            rate=rate,
            urgent=urgent,
            started_at=started_at,
            finished_at=finished_at,
            is_expired=is_expired
        )
        return paginate(requestdata)

    request_list = it_requests.filter_requests_all(
        db,
        id=id,
        category_id=cat_list,
        fillial_id=fillial_id,
        request_status=request_status,
        created_at=created_at,
        user=user,
        arrival_date=arrival_date,
        rate=rate,
        brigada_id=request_user.brigada_id or brigada_id,
        urgent=urgent,
        started_at=started_at,
        finished_at=finished_at,
        is_expired=is_expired
    )

    return paginate(request_list)


@it_requests_router.get("/requests/it/{id}", response_model=GetOneRequest)
async def get_request(
        id: int,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    try:
        request_list = it_requests.get_request_id(db, id)
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")


@it_requests_router.put("/requests/it/{id}", response_model=GetOneRequest)
async def put_request_id(
        id: int,
        data: PutRequest,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    request = it_requests.edit_request(db=db, data=data, id=id)
    message_id = request.tg_message_id
    # brigada_id = request.brigada_id
    topic_id = request.brigada.topic_id if request.brigada_id else None

    if data.status is not None or data.brigada_id is not None:
        if data.status is not None:
            logs.create_log(db=db, request_id=id, status=request.status, user_id=request_user.id)

        formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")
        phone_number = (request.phone_number if request.phone_number.startswith('+') else f"+{request.phone_number}") if request.phone_number else None
        if request.finishing_time:
            finishing_time = request.finishing_time
            formatted_finishing_time = finishing_time.strftime("%d.%m.%Y %H:%M")
        else:
            finishing_time, formatted_finishing_time = None, None
        if request.user:
            user_fullname = request.user.full_name
            user_id = request.user.id
            user_telegram_id = request.user.telegram_id
        else:
            user_fullname, user_id, user_telegram_id = None, None, None
        if request.category:
            sla = request.category.ftime
            category_name = request.category.name
            category_department = request.category.department
            category_sub_id = request.category.sub_id
        else:
            sla, category_name, category_department, category_sub_id = None, None, None, None

        request_text = f"📑Заявка № {request.id}\n\n" \
                       f"📍Филиал: {request.fillial.parentfillial.name}\n" \
                       f"👨‍💼Сотрудник: {user_fullname}\n" \
                       f"📱Номер телефона: {phone_number}\n" \
                       f"🔰Категория проблемы: {category_name}\n" \
                       f"🕘Дата поступления заявки: {formatted_created_time}\n" \
                       f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
                       f"❗️SLA: {sla} часов\n" \
                       f"💬Комментарии: {request.description}"

        if sla == 1:
            delta_minutes = 40
        elif sla == 1.5:
            delta_minutes = 60
        elif sla == 2:
            delta_minutes = 90
            # delta_minutes = 2
        elif sla == 8:
            delta_minutes = 360
        elif sla == 24:
            delta_minutes = 1200
        elif sla == 48:
            delta_minutes = 1920
        elif sla == 72:
            delta_minutes = 2880
        elif sla == 96:
            delta_minutes = 4320
        else:
            delta_minutes = 0

        delay = timedelta(minutes=delta_minutes)
        deleting_scheduled_time = request.created_at + delay - timedelta(seconds=2)
        sending_scheduled_time = request.created_at + delay

        if data.status == 1 or data.brigada_id is not None:
            delete_from_chat(message_id=request.tg_message_id, topic_id=topic_id)
            send_notification(db=db, request_id=id, topic_id=topic_id, text=request_text, finishing_time=finishing_time)

            request = it_requests.get_request_id(db=db, id=id)
            if request.brigada:
                brigada_name = request.brigada.name
            else:
                brigada_name = None
            try:
                sendtotelegramchat(
                    chat_id=user_telegram_id,
                    message_text=f"Уважаемый {user_fullname}, статус вашей заявки #{request.id}s "
                                 f"назначен специалист👨‍💻: {brigada_name}\n"
                                 f"Время выполнения: {sla} часов"
                )
            except:
                pass

            if delta_minutes > 0:
                delete_job_id = f"delete_message_for_{request.id}"
                try:
                    scheduler.add_job(delete_from_chat, 'date', run_date=deleting_scheduled_time,
                                      args=[request.tg_message_id, topic_id], id=delete_job_id, replace_existing=True)
                except ConflictingIdError:
                    print(f"Job '{delete_job_id}' already scheduled or was missed by time. Skipping ...")

                send_job_id = f"send_message_for_{request.id}"
                try:
                    scheduler.add_job(send_notification, 'date', run_date=sending_scheduled_time,
                                      args=[db, request.id, topic_id, request_text, finishing_time], id=send_job_id,
                                      replace_existing=True)
                except ConflictingIdError:
                    print(f"Job '{send_job_id}' already scheduled or was missed by time. Skipping ...")

        elif data.status == 3:
            edit_topic_reply_markup(chat_id=settings.IT_SUPERGROUP,
                                    thread_id=topic_id,
                                    message_id=message_id
                                    )
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={user_id}&department={category_department}&sub_id={category_sub_id}"
            try:
                inlinewebapp(
                    chat_id=user_telegram_id,
                    message_text=f"Уважаемый {user_fullname}, статус вашей заявки #{request.id}s по IT: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except Exception as e:
                print(e)

        elif data.status == 4:
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={user_id}&department={category_department}&sub_id={category_sub_id}"
            try:
                inlinewebapp(
                    chat_id=user_telegram_id,
                    message_text=f"""❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\nЕсли Вы с этим не согласны, поставьте, пожалуйста, рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий.""",
                    url=url,
                )
            except:
                pass

            if request.brigada_id is None:
                delete_from_chat(message_id=message_id)
            else:
                text = request_text + "\n\n<b>Заявка отменена 🚫</b>" \
                                      f"\nПричина отмены: {request.deny_reason}"
                edit_topic_message(chat_id=settings.IT_SUPERGROUP, thread_id=topic_id, message_text=text,
                                   message_id=message_id)

                delete_job_id = f"delete_message_for_{request.id}"
                try:
                    scheduler.remove_job(job_id=delete_job_id)
                    # print(f"'{delete_job_id}' job was removed before scheduling")
                except JobLookupError:
                    print(f"'{delete_job_id}' job not found or already has completed !")

                send_job_id = f"send_message_for_{request.id}"
                try:
                    scheduler.remove_job(job_id=send_job_id)
                    # print(f"'{send_job_id}' job was removed before scheduling")
                except JobLookupError:
                    print(f"'{send_job_id}' job not found or already has completed !")

        elif data.status == 6:
            delete_job_id = f"delete_message_for_{request.id}"
            try:
                scheduler.remove_job(job_id=delete_job_id)
                # print(f"'{delete_job_id}' job was removed before scheduling")
            except JobLookupError:
                print(f"'{delete_job_id}' job not found or already has completed !")

            send_job_id = f"send_message_for_{request.id}"
            try:
                scheduler.remove_job(job_id=send_job_id)
                # print(f"'{send_job_id}' job was removed before scheduling")
            except JobLookupError:
                print(f"'{send_job_id}' job not found or already has completed !")

            started_at = request.started_at
            finished_at = request.finished_at
            finished_time = finished_at - started_at
            topic_message = f"<s>{request_text}</s>\n\n" \
                            f"<b> ✅ Вы завершили заявку за:</b>  {str(finished_time).split('.')[0]}"
            keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "Возобновить", "callback_data": "resume_request"}
                    ]
                ]
            }
            edit_topic_message(chat_id=settings.IT_SUPERGROUP, thread_id=topic_id, message_text=topic_message,
                               message_id=message_id, inline_keyboard=keyboard)
            user_message = request_text + f"\n\nСтатус вашей заявки:  Завершен ✅"
            inline_keyboard = {
                "inline_keyboard": [
                    [{"text": "Выполнен/Принимаю", "callback_data": "user_accept"},
                     {"text": "Не выполнен/Не принимаю", "callback_data": "user_not_accept"}]
                ]
            }
            try:
                sendtotelegramchat(chat_id=user_telegram_id, message_text=user_message,
                                   inline_keyboard=inline_keyboard)
            except:
                pass

        elif data.status == 7:
            try:
                sendtotelegramchat(
                    chat_id=user_telegram_id,
                    message_text=f"Ваша заявка #{request.id}s возобновлено"
                )
            except:
                pass
            remaining_time = finishing_time - datetime.now(tz=timezonetash)
            text = request_text + f"\n\n<b> ‼️ Оставщиеся время:</b>  {str(remaining_time).split('.')[0]}"
            inline_keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "Завершить заявку", "callback_data": "complete_request"},
                        {"text": "Отменить", "callback_data": "cancel_request"}
                    ]
                ]
            }
            edit_topic_message(chat_id=settings.IT_SUPERGROUP, thread_id=topic_id, message_id=message_id,
                               message_text=text, inline_keyboard=inline_keyboard)
            if delta_minutes > 0:
                delete_job_id = f"delete_message_for_{request.id}"
                try:
                    scheduler.add_job(delete_from_chat, 'date', run_date=deleting_scheduled_time,
                                      args=[request.tg_message_id, topic_id], id=delete_job_id, replace_existing=True)
                except ConflictingIdError:
                    print(f"Job '{delete_job_id}' already scheduled or was missed by time. Skipping ...")

                send_job_id = f"send_message_for_{request.id}"
                try:
                    scheduler.add_job(send_notification, 'date', run_date=sending_scheduled_time,
                                      args=[db, request.id, topic_id, request_text, finishing_time], id=send_job_id,
                                      replace_existing=True)
                except ConflictingIdError:
                    print(f"Job '{send_job_id}' already scheduled or was missed by time. Skipping ...")

        elif data.status == 8:
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={user_id}&department={category_department}&sub_id={category_sub_id}"
            try:
                inlinewebapp(
                    chat_id=user_telegram_id,
                    message_text=f"""❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\nЕсли Вы с этим не согласны, поставьте, пожалуйста, рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий.""",
                    url=url,
                )
            except:
                pass
            text = request_text + "\n\n<b>Заявка отменена 🚫</b>"
            edit_topic_message(chat_id=settings.IT_SUPERGROUP, thread_id=topic_id, message_text=text,
                               message_id=message_id)

    return request


@it_requests_router.post("/requests/it", response_model=GetOneRequest)
async def create_request(
        data: CreateRequest,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    request = it_requests.add_request(db, request_user, data)
    if data.files:
        for file in data.files:
            files.create_files_report(db, file, request.id)

    logs.create_log(db=db, request_id=request.id, status=request.status, user_id=request_user.id)

    formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")

    phone_number = (request.phone_number if request.phone_number.startswith('+') else f"+{request.phone_number}") if request.phone_number else None
    user_fullname = request.user.full_name if request.user else None

    if request.finishing_time:
        finishing_time = request.finishing_time
        formatted_finishing_time = finishing_time.strftime("%d.%m.%Y %H:%M")
    else:
        finishing_time, formatted_finishing_time = None, None

    if request.category:
        sla = request.category.ftime
        category_name = request.category.name
    else:
        sla, category_name = None, None

    request_text = f"📑Заявка № {request.id}\n\n" \
                   f"📍Филиал: {request.fillial.parentfillial.name}\n" \
                   f"👨‍💼Сотрудник: {user_fullname}\n" \
                   f"📱Номер телефона: {phone_number}\n" \
                   f"🔰Категория проблемы: {category_name}\n" \
                   f"🕘Дата поступления заявки: {formatted_created_time}\n" \
                   f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
                   f"❗️SLA: {sla} часов\n" \
                   f"💬Комментарии: {request.description}"

    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "Принять заявку", "callback_data": "accept_action"}]
        ]
    }
    try:
        response = sendtotelegramchat(chat_id=settings.IT_SUPERGROUP, message_text=request_text,
                                      inline_keyboard=inline_keyboard)
        response_data = response.json()
        tg_message_id = response_data["result"]["message_id"]
    except:
        tg_message_id = None
    request = it_requests.edit_request(db=db, id=request.id, tg_message_id=tg_message_id)

    return request



@it_requests_router.post("/requests/it/message", response_model=MessageRequestCreate, tags=["Message"])
async def create_message(
        request_id: Annotated[int, Form()],
        message: Annotated[str, Form()] = None,
        status: Annotated[int, Form()] = None,
        photo: UploadFile = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)):
    if photo:
        file_path = f"files/{generate_random_filename()}{photo.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await photo.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
    else:
        file_path = None

    db_query = communication.message_create(db=db,
                                            request_id=request_id,
                                            message=message,
                                            status=status,
                                            photo=file_path,
                                            user_id=request_user.id
                                            )
    return db_query
