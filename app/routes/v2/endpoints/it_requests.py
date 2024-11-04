import pytz
from datetime import datetime, timedelta
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud import it_requests, users, communication, logs
from app.models.category import Category
from app.routes.depth import get_db, get_current_user
from app.schemas.it_extra import *
from app.schemas.it_requests import GetRequest, PutRequest, MessageRequestCreate
from app.schemas.requests import GetOneRequest
from app.schemas.users import UserFullBack
from app.utils.utils import sendtotelegramchat, sendtotelegramtopic, delete_from_chat, edit_topic_message, \
    inlinewebapp, confirmation_request, generate_random_filename, request_notification, edit_topic_reply_markup


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
            finished_at=finished_at
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
        finished_at=finished_at
    )

    return paginate(request_list)


@it_requests_router.get("/requests/it/{id}", response_model=GetOneRequest)
async def get_request(
        id: int,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user),
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
    request = it_requests.edit_request(db=db, data=data, id=id, user=request_user)
    message_id = request.tg_message_id
    topic_id = request.brigada.topic_id
    brigada_id = request.brigada_id

    if request.status is not None:
        logs.create_log(db=db, request_id=id, status=request.status, user_id=request_user.id)

        formatted_created_time = request.created_at.strftime("%d.%m.%Y %H:%M")
        formatted_finishing_time = request.finishing_time.strftime("%d.%m.%Y %H:%M")
        finishing_time = request.finishing_time
        sla = request.category.ftime
        phone_number = request.phone_number if request.phone_number.startswith('+') else f"+{request.phone_number}"
        request_text = f"📑Заявка № {request.id}\n\n" \
                       f"📍Филиал: {request.fillial.parentfillial.name}\n" \
                       f"👨‍💼Сотрудник: {request.user.full_name}\n" \
                       f"📱Номер телефона: {phone_number}\n" \
                       f"🔰Категория проблемы: {request.category.name}\n" \
                       f"🕘Дата поступления заявки: {formatted_created_time}\n" \
                       f"🕘Дата дедлайна заявки: {formatted_finishing_time}\n" \
                       f"❗️SLA: {sla} часов\n" \
                       f"💬Комментарии: {request.description}"

        delta_minutes = 0
        if sla == 1:
            delta_minutes = 40
        elif sla == 1.5:
            delta_minutes = 60
        elif sla == 2:
            delta_minutes = 12
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

        delay = timedelta(minutes=delta_minutes)
        scheduled_time = request.created_at + delay
        print("Notification will sent at: ", scheduled_time)

        if request.status == 1:
            remaining_time = finishing_time - datetime.now(tz=timezonetash)
            text = request_text + f"\n\n<b> ‼️ Оставщиеся время:</b>  {str(remaining_time).split('.')[0]}"
            if brigada_id and topic_id:
                request_notification(message_id=request.tg_message_id, topic_id=topic_id, text=text, db=db,
                                     request_id=id)

                request = it_requests.get_request_id(db=db, id=id)
                sendtotelegramchat(
                    chat_id=request.user.telegram_id,
                    message_text=f"Уважаемый {request.user.full_name}, статус вашей заявки #{request.id}s "
                                 f"назначен специалист👨‍💻: {request.brigada.name}\n"
                                 f"Время выполнения: {sla} часов"
                )

                job_id = f"{request.tg_message_id}_{scheduled_time.strftime('%d.%m.%Y_%H:%M')}"
                scheduler.add_job(request_notification, 'date', run_date=scheduled_time,
                                  args=[db, id, request.tg_message_id, topic_id, text], id=job_id)

        elif request.status == 3:
            edit_topic_reply_markup(chat_id=settings.IT_SUPERGROUP,
                                    thread_id=topic_id,
                                    message_id=message_id
                                    )
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={request.user.id}&department={request.category.department}&sub_id={request.category.sub_id}"
            try:
                inlinewebapp(
                    chat_id=request.user.id,
                    message_text=f"Уважаемый {request.user.fullname}, статус вашей заявки #{request.id}s по IT: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except:
                pass

        elif request.status == 4:
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={request.user.id}&department={request.category.department}&sub_id={request.category.sub_id}"
            inlinewebapp(
                chat_id=request.user.telegram_id,
                message_text=f"""❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\nЕсли Вы с этим не согласны, поставьте, пожалуйста, рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий.""",
                url=url,
            )
        elif request.status == 6:
            for job in scheduler.get_jobs():
                if job.id.startswith(str(message_id)):
                    try:
                        scheduler.remove_job(job_id=job.id)
                        print(f"Canceled job for message - {job.id}")
                    except JobLookupError:
                        print(f"Message - {job.id} not found or already has sent !")

            started_at = request.started_at
            finished_at = request.finished_at
            finished_time = finished_at - started_at
            topic_message = f"<s>{request_text}</s>\n\n" \
                            f"<b> ✅ Вы завершили заявку за:</b>  {str(finished_time).split('.')[0]}"
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Возобновить", "callback_data": "resume_request"},
                     {"text": "Отправить сообщение заказчику", "callback_data": "send_message_to_user"}]
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
            sendtotelegramchat(chat_id=request.user.telegram_id, message_text=user_message,
                               inline_keyboard=inline_keyboard)

        elif request.status == 7:
            sendtotelegramchat(
                chat_id=request.user.telegram_id,
                message_text=f"Ваша заявка #{request.id}s возобновлено"
            )
            remaining_time = finishing_time - datetime.now(tz=timezonetash)
            text = request_text + f"\n\n<b> ‼️ Оставщиеся время:</b>  {str(remaining_time).split('.')[0]}"
            # request_notification(message_id=request.tg_message_id, topic_id=topic_id, text=text, db=db, request_id=id)
            inline_keyboard = {
                "inline_keyboard": [
                    [{"text": "Завершить заявку", "callback_data": "complete_request"},
                     {"text": "Отправить сообщение заказчику", "callback_data": "send_message_to_user"}]
                ]
            }
            edit_topic_message(chat_id=settings.IT_SUPERGROUP, thread_id=topic_id, message_id=message_id,
                               message_text=text, inline_keyboard=inline_keyboard)
            job_id = f"{message_id}_{scheduled_time.strftime('%d.%m.%Y_%H:%M')}"
            scheduler.add_job(request_notification, 'date', run_date=scheduled_time,
                              args=[db, id, request.tg_message_id, topic_id, text], id=job_id)

        elif data.status == 8:
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={request.user.id}&department={request.category.department}&sub_id={request.category.sub_id}"
            inlinewebapp(
                chat_id=request.user.telegram_id,
                message_text=f"""❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\nЕсли Вы с этим не согласны, поставьте, пожалуйста, рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий.""",
                url=url,
            )

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
