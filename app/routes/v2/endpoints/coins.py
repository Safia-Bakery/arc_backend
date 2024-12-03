from typing import Optional
from uuid import UUID

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.files import timezone_tash
from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string
from fastapi_pagination import Page,paginate
from app.schemas.coins import GetCoinsRequests,UpdateCoinRequest
from app.crud.coins import get_one_request,get_requests,update_coin_request,get_last24hours_requests
from app.crud.logs import create_log
from app.utils.utils import sendtotelegramchat

from app.utils.coins_utils import excell_generate_coins,send_file_to_chat

coins_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


def generate_coins_excell_file(db:Session):
    data= get_last24hours_requests(db=db)
    file_url = excell_generate_coins(data=data)
    send_file_to_chat(bot_token=settings.bottoken,chat_id=-1002439275381,file_path=file_url)
    return True



@coins_router.on_event("startup")
def it_query_checker():
    scheduler = BackgroundScheduler()
    trigger =  CronTrigger(hour=18, minute=24, second=00,timezone=timezone_tash)  # Set the desired time for the function to run (here, 12:00 PM)
    scheduler.add_job(generate_coins_excell_file, trigger=trigger, args=[next(get_db())])
    scheduler.start()













@coins_router.get("/coins",response_model=Page[GetCoinsRequests])
async def get_coins_requests(
    user_id:Optional[int]=None,
    fillial_id:Optional[UUID]=None,
    status:Optional[int]=None,
    id:Optional[int]=None,
    db:Session=Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)):

    return  paginate(get_requests(db=db,user_id=user_id,fillial_id=fillial_id,id=id,status=status))


@coins_router.get("/coins/{coin_id}",response_model=GetCoinsRequests)
async def get_one_request_api(

    coin_id:int,
    db:Session=Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)):
    return get_one_request(db=db,id=coin_id)



@coins_router.put("/coins/{coin_id}",response_model=GetCoinsRequests)
async def update_one_request_api(
    coin_id:int,
    coint_request: UpdateCoinRequest,
    db:Session=Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)):
    old_request  = get_one_request(db=db,id=coin_id)
    query = update_coin_request(db=db, coin=coint_request, request_id=coin_id, user_manager=current_user.full_name)
    # if old_request.status != coint_request.status:
    create_log(db=db,status=coint_request.status,user_id=current_user.id,request_id=coin_id)
    if query.status==3:
        try:
            sendtotelegramchat(
                chat_id=query.user.telegram_id,
                message_text=f"Уважаемый {query.user.full_name}, ваша заявка #{query.id}s подтверждена.",
            )
        except Exception as e:
            print(e)
    if query.status==4:
        try:
            sendtotelegramchat(
                chat_id=query.user.telegram_id,
                message_text=f"Уважаемый {query.user.full_name}, ваша заявка #{query.id}s отклонена по причине: {query.deny_reason}",
            )
        except Exception as e:
            print(e)

    return query






