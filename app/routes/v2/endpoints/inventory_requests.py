from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from fastapi_pagination import paginate, Page
from typing import Optional
from app.schemas.it_extra import *
from app.routes.depth import get_db, get_current_user
from app.schemas.users import UserFullBack
from app.schemas.inventory_requests import (GetRequest,
                                            GetOneRequest,
                                            CreateInventoryRequest,
                                            UpdateRequest,
                                            UpdateInventoryExpenditure
                                            )
from app.crud import inv_requests
from datetime import datetime, date
from app.crud.expanditure import create_expanditure
from app.utils.utils import( send_simple_text_message,
                             rating_request_telegram,
                             confirmation_request_telegram
                             )

from app.core.config import settings

inv_requests_router = APIRouter()


@inv_requests_router.get("/requests/inv/factory", response_model=Page[GetRequest])
async def filter_factory_requests(
        id: Optional[int] = None,
        user: Optional[str] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user),
):


    request_list = inv_requests.filter_requests_all(
        db,
        id=id,
        user=user,
        fillial_id=fillial_id,
        created_at=created_at,
        request_status=request_status,
        department=9
    )

    return paginate(request_list)


@inv_requests_router.get("/requests/inv/retail", response_model=Page[GetRequest])
async def filter_retail_requests(
        id: Optional[int] = None,
        user: Optional[str] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user),
):
    request_list = inv_requests.filter_requests_all(
        db,
        id=id,
        user=user,
        fillial_id=fillial_id,
        created_at=created_at,
        request_status=request_status,
        department=2
    )

    return paginate(request_list)


@inv_requests_router.get("/requests/inv/{id}", response_model=GetOneRequest)
async def get_request(
    id: int,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.get_request_id(db, id)
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")



@inv_requests_router.post("/requests/inv", response_model=GetOneRequest)
async def create_request(
    request: CreateInventoryRequest,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.create_request(db, request,user_id=request_user.id)
        for  item in request.expenditure:
            create_expanditure(db, amount=item.amount,tool_id=item.tool_id,request_id=request_list.id)
        send_simple_text_message(
            bot_token=settings.bottoken,
            chat_id=request_user.telegram_id,
            message_text=f"Уважаемый {request_user.full_name}, ваша заявка #{request_list.id} по Inventary: Создана."
        )
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")



@inv_requests_router.put("/requests/inv", response_model=GetOneRequest)
async def update_request(
    request: UpdateRequest,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.update_request(db, request)
        if request.status is not None:
            if request.status == 1:
                send_simple_text_message(
                    bot_token=settings.bottoken,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Уважаемый {request_list.user.full_name}, статус вашей заявки #{request_list.id} по Inventary: В процессе."
                )
            elif request.status == 4:

                rating_request_telegram(
                    bot_token=settings.bottoken,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Ваша заявка #{request_list.id}s была отменена по причине: {request_list.deny_reason}",
                    url =f"{settings.frontend_url}/rating/{request_list.id}"

                )
            elif   request.status==6:
                text_request = f"Ваша заявка #{request_list.id}s по Инвентарю была обработана. "
                for i in request_list.expanditure:
                    text_request += f"\n{i.tool.name} - {i.amount} шт. "
                text_request += "Инвентарь отправлен вам на филиал, прибудет через 12 часов. Как привезут просим вас Подтвердить заявку. \nЕсли вам не привезут их в течении выше указанного времени, можете нажать кнопку “Не сделано”"
                confirmation_request_telegram(
                    bot_token=settings.bottoken,
                    chat_id=request_list.user.telegram_id,
                    message_text=text_request,
                )
            elif request.status==7:
                send_simple_text_message(
                    bot_token=settings.bottoken,
                    chat_id=request_list.user.telegram_id,
                    message_text=f"Ваша заявка #{request_list.id}s возобновлено",
                )
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not fund")



