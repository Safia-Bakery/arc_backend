import time
from datetime import datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import expanditure as expanditure_crud
from app.crud import iiko_transfers
from app.routes.depth import get_db, get_current_user
from app.schemas.iiko_transfers import IikoTransfer
from app.schemas.users import GetUserFullData
from app.utils.iiko_tranfers import (
    send_inventory_document_iiko,
    send_arc_document_iiko, authiiko,

)
from app.utils.utils import rating_request_telegram, edit_topic_message, edit_topic_reply_markup

iiko_transfer_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


def self_closing_requests(db: Session):
    requests = iiko_transfers.get_requests_by_status(db=db, status=6)
    print('working every minute ')


    for request in requests:
        # time.sleep(1)
        url = f"{settings.front_url}/tg/order-rating/{request.id}?user_id={request.user.id}&department={request.category.department}&sub_id={request.category.sub_id}"


        updated_request = iiko_transfers.update_status_request(db=db, id=request.id, status=3)

        if request.category.department == 2:
            message_text = f'Уважаемый {request.user.full_name}, статус вашей заявки #{request.id}s по инвентарь: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟 и оцените заявку'

            # Send the inventory document
            for product in request.expanditure:
                # send_inventory_document_iiko(key=key, data=product)
                expanditure_crud.update_status(db=db, expanditure_id=product.id)

        elif request.category.department == 1 and request.category.sphere_status == 1:
            message_text = f"Уважаемый {request.user.full_name}, статус вашей заявки #{request.id}s по APC: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟 и оцените заявку"

            # Send ARC document
            for i in request.expanditure:
                # send_arc_document_iiko(key=authiiko(), data=i)
                expanditure_crud.update_status(db=db, expanditure_id=i.id)

        elif request.category.department == 4:
            message_text = f"Уважаемый {request.user.full_name}, статус вашей заявки #{request.id}s по IT: Завершен.\n\n" \
                           f"Пожалуйста нажмите на кнопку Оставить отзыв🌟 и оцените заявку"
            edit_topic_reply_markup(chat_id=settings.IT_SUPERGROUP,
                                    thread_id=request.brigada.topic_id,
                                    message_id=request.tg_message_id
                                    )

        else:
            message_text = f"Уважаемый {request.user.full_name}, статус вашей заявки #{request.id}s Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟 и оцените заявку"

        # Send the message via Telegram
        rating_request_telegram(bot_token=settings.bottoken, chat_id=request.user.telegram_id,
                                message_text=message_text, url=url)

    requests_list = iiko_transfers.get_requests_by_status(db=db, status=8)
    for request_list in requests_list:
        iiko_transfers.update_status_request(db=db, id=request_list.id, status=4)


    return True


@iiko_transfer_router.on_event("startup")
def it_query_checker():
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(minute="*/10")  # Trigger every half hour
    scheduler.add_job(self_closing_requests, trigger=trigger, args=[next(get_db())])
    scheduler.start()


@iiko_transfer_router.post("/iiko_transfer")
async def iiko_transfer(
        form_data: IikoTransfer,
        db: Session = Depends(get_db),
        current_user: GetUserFullData = Depends(get_current_user),
):
    key = authiiko()

    request = iiko_transfers.get_request_by_id(db=db, request_id=form_data.request_id)
    if request.category.department == 2:
        for i in request.expanditure:
            send_inventory_document_iiko(key=key, data=i)
            expanditure_crud.update_status(db=db, expanditure_id=i.id)
    if request.category.department == 1 and request.category.sphere_status:

        for i in request.expanditure:
            send_arc_document_iiko(key=key, data=i)
            expanditure_crud.update_status(db=db, expanditure_id=i.id)

    return request
