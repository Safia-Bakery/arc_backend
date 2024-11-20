from typing import Optional

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session
from app.core.config import settings

from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string, inlinewebapp, confirmation_request
from app.schemas.branchs import GetBranchs
from fastapi_pagination import Page,paginate
from app.crud.branchs import get_branchs
from app.schemas.arc_factory_requests import GetArcFactoryRequests,UpdateArcFactoryRequests
from app.crud.arc_factory_requests import get_arc_factory_requests,get_arc_factory_request,update_arc_factory_request
from app.crud.logs import create_log

from app.models.requests import Requests
from microservices import sendtotelegramchannel

arc_factory_requests = APIRouter()


@arc_factory_requests.get("/arc/factory/requests",response_model=Page[GetArcFactoryRequests])
async def get_requests(
        user_id:Optional[int]=None,
        fillial_id:Optional[int]=None,
        status:Optional[int]=None,
        id:Optional[int]=None,
        current_user: GetUserFullData = Depends(get_current_user),
        db:Session=Depends(get_db)):
    return paginate(get_arc_factory_requests(db=db,user_id=user_id,fillial_id=fillial_id,status=status,id=id))


@arc_factory_requests.get("/arc/factory/requests/{request_id}",response_model=GetArcFactoryRequests)
async def get_request(
        request_id:int,
        current_user: GetUserFullData = Depends(get_current_user),
        db:Session=Depends(get_db)):
    return get_arc_factory_request(db=db,request_id=request_id)


@arc_factory_requests.put("/arc/factory/requests/{request_id}",response_model=GetArcFactoryRequests)
async def update_request(
        request_id:int,
        request:UpdateArcFactoryRequests,
        db:Session = Depends(get_db),
        current_user: GetUserFullData = Depends(get_current_user)):
    old_request = get_arc_factory_request(db=db,request_id=request_id)

    updated_request = update_arc_factory_request(db=db, request_id=request_id, request=request)
    if old_request.status != updated_request.status or old_request.brigada_id != updated_request.brigada_id:
        create_log(db=db, request_id=request_id, status=updated_request.status, user_id=current_user.id)
        if updated_request.status==1:
            try:
                sendtotelegramchannel(
                    bot_token=settings.bot_token,
                    chat_id=updated_request.user.telegram_id,
                    message_text=f"Уважаемый {updated_request.user.full_name}, на вашу заявку #{updated_request.id}s назначена команда🚙: {updated_request.brigada.name}",
                )
            except:
                pass
        elif updated_request.status==3:
            url = f"{settings.FRONT_URL}tg/order-rating/{updated_request.id}?user_id={updated_request.user.id}&department={updated_request.category.department}&sub_id={updated_request.category.sub_id}"
            try:
                inlinewebapp(
                    chat_id=updated_request.user.telegram_id,
                    message_text=f"Уважаемый {updated_request.user.full_name}, статус вашей заявки #{updated_request.id}s по APC: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
                    url=url,
                )
            except:
                pass
        elif updated_request.status==4:
            try:
                sendtotelegramchannel(
                    bot_token=settings.bot_token,
                    chat_id=updated_request.user.telegram_id,
                    message_text=f"Уважаемый {updated_request.user.full_name}, ваша заявка #{updated_request.id}s отклонена по причине: {updated_request.deny_reason}",
                )
            except:
                pass

        elif updated_request.status==6:
            try:
                text_request = f"Ваша заявка #{updated_request.id}s по АРС была обработана. Пожалуйста, подтвердите, что она выполнена в соответствии с вашим запросом."
                confirmation_request(chat_id=updated_request.user.telegram_id,
                                     message_text=text_request)

            except:
                    pass

    return
