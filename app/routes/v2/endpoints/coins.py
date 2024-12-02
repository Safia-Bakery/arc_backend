from typing import Optional
from uuid import UUID

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string
from fastapi_pagination import Page,paginate
from app.schemas.coins import GetCoinsRequests,UpdateCoinRequest
from app.crud.coins import get_one_request,get_requests,update_coin_request
from app.crud.logs import create_log
from app.utils.utils import sendtotelegramchat

coins_router = APIRouter()


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

    coint_id:int,
    db:Session=Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)):
    return get_one_request(db=db,id=coint_id)



@coins_router.put("/coins/{coin_id}",response_model=GetCoinsRequests)
async def update_one_request_api(
    coint_id:int,
    coint_request: UpdateCoinRequest,
    db:Session=Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user)):
    old_request  = get_one_request(db=db,id=coint_id)
    query = update_coin_request(db=db, coin=coint_request, request_id=coint_id, user_manager=current_user.full_name)
    if old_request.status !=coint_request.status:
        create_log(db=db,status=coint_request.status,user_id=current_user.id,request_id=coint_id)
        if query.status==3:
            # try:
                print('senging')
                sendtotelegramchat(
                    chat_id=query.user.telegram_id,
                    message_text=f"Уважаемый {query.user.full_name}, ваша заявка #{query.id}s подтверждена.",
                )
            # except Exception as e:
            #     print(e)
        if query.status==4:
            try:
                sendtotelegramchat(
                    chat_id=query.user.telegram_id,
                    message_text=f"Уважаемый {query.user.full_name}, ваша заявка #{query.id}s отклонена по причине: {query.deny_reason}",
                )
            except Exception as e:
                print(e)

    return query






