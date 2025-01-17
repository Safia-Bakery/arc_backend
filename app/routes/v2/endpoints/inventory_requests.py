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
                                            GetRequestFactoryInv,
                                            CreateInventoryRequest,
                                            UpdateRequest,
                                            UpdateInventoryExpenditure
                                            )

from app.schemas.requests import GetOneRequest,GetOneRequestInventoryFactory
from app.crud import inv_requests, logs, files
from datetime import datetime, date
from app.crud.expanditure import create_expanditure,delete_expanditure
from app.utils.utils import( send_simple_text_message,
                             rating_request_telegram,
                             confirmation_request
                             )
from app.crud.branchs import get_child_branchs

from app.core.config import settings

inv_requests_router = APIRouter()


@inv_requests_router.get("/requests/inv/factory", response_model=Page[GetRequestFactoryInv])
async def filter_factory_requests(
        id: Optional[int] = None,
        user: Optional[str] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        product:Optional[str]=None,
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
        department=10,
        product_name=product
    )

    return paginate(request_list)


@inv_requests_router.get("/requests/inv/retail", response_model=Page[GetRequest])
async def filter_retail_requests(
        id: Optional[int] = None,
        user: Optional[str] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        request_status: Optional[str] = None,
        product:Optional[str]=None,
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
        department=2,
        product_name=product
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





@inv_requests_router.get("/requests/inv/factory/{id}", response_model=GetOneRequestInventoryFactory)
async def get_request_factoty(
    id: int,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.get_request_id(db, id)
        return request_list
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@inv_requests_router.post("/requests/inv/retail")
async def create_retail_request(
    request: CreateInventoryRequest,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):

    # try:
        get_child_branch = get_child_branchs(db, request.fillial_id)
        if not get_child_branch:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Branch not found")
        request.fillial_id=get_child_branch.id
        request_list = inv_requests.create_request(db, request,user_id=request_user.id)
        logs.create_log(db=db, request_id=request_list.id, status=request_list.status, user_id=request_user.id)
        for item in request.expenditure:
            create_expanditure(db, amount=item.amount,tool_id=item.tool_id,request_id=request_list.id)
        send_simple_text_message(
            bot_token=settings.bottoken,
            chat_id=request_user.telegram_id,
            message_text=f"Уважаемый {request_user.full_name}, ваша заявка #{request_list.id} по Inventary: Создана."
        )
        return {'id':request_list.id,'status':request_list.status,'success':True}
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))



@inv_requests_router.post("/requests/inv/factory")
async def create_factory_request(
    request: CreateInventoryRequest,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):

    try:
        request_list = inv_requests.create_request(db, request, user_id=request_user.id)
        logs.create_log(db=db, request_id=request_list.id, status=request_list.status, user_id=request_user.id)
        if request.files:
            for file_url in request.files:
                files.create_files_report(db=db, url=file_url, request_id=request_list.id)
        for item in request.expenditure:
            create_expanditure(db, amount=item.amount,tool_id=item.tool_id,request_id=request_list.id)
        send_simple_text_message(
            bot_token=settings.bottoken,
            chat_id=request_user.telegram_id,
            message_text=f"Уважаемый {request_user.full_name}, ваша заявка #{request_list.id} по Inventary: Создана."
        )
        return {'id':request_list.id,'status':request_list.status,'success':True}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))





@inv_requests_router.put("/requests/inv/factory", response_model=GetOneRequestInventoryFactory)
async def update_request_inventory_facatory(
    request: UpdateRequest,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.update_request(db, request)
        if request.status is not None:
            logs.create_log(db=db, request_id=request_list.id, status=request_list.status, user_id=request_user.id)
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
                    url =f"{settings.FRONT_URL}/rating/{request_list.id}"
                )
            elif request.status == 6:
                text_request = f"Ваша заявка #{request_list.id}s по Инвентарю была обработана.\n "
                new_neq = []
                for i in request_list.expanditure:
                    if i.status == 0:
                        new_neq.append(i)

                    else:
                        text_request += f"\n{i.tool.name} - {i.amount} шт. "

                if new_neq:

                    text_request += f"\n\n♻️Инвентарь в обработке:\n"

                    new_request = inv_requests.create_auto_request(
                        db=db,
                        category_id=request_list.category_id,
                        fillial_id=request_list.fillial_id,
                        description=request_list.description,
                        product=request_list.product,
                        user_id=request_list.user_id,
                    )
                    for i in new_neq:
                        text_request += f"\n{i.tool.name} - {i.amount} шт. "
                        delete_expanditure(db=db, request_id=request_list.id, tool_id=i.tool_id)

                        create_expanditure(db=db,
                                           request_id=new_request.id,
                                           tool_id=i.tool_id,
                                           amount=i.amount,
                                           )
                    text_request += "\nПри первой возможности будет отправлено.\n"

                text_request += "\nИнвентарь отправлен вам на филиал, прибудет через 12 часов. Как привезут просим вас Подтвердить заявку. \nЕсли вам не привезут их в течении выше указанного времени, можете нажать кнопку “Не сделано”"
                confirmation_request(
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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))



@inv_requests_router.put("/requests/inv/", response_model=GetOneRequest)
async def update_request_inventory_facatory(
    request: UpdateRequest,
    db: Session = Depends(get_db),
    request_user: UserFullBack = Depends(get_current_user),
):
    try:
        request_list = inv_requests.update_request(db, request)
        if request.status is not None:
            logs.create_log(db=db, request_id=request_list.id, status=request_list.status, user_id=request_user.id)
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
                    url =f"{settings.FRONT_URL}/rating/{request_list.id}"
                )
            elif request.status==6:
                text_request = f"Ваша заявка #{request_list.id}s по Инвентарю была обработана.\n "
                new_neq = []
                for i in request_list.expanditure:
                    if i.status == 0:
                        new_neq.append(i)

                    else:
                        text_request += f"\n{i.tool.name} - {i.amount} шт. "

                if new_neq:

                    text_request += f"\n\n♻️Инвентарь в обработке:\n"

                    new_request = inv_requests.create_auto_request(
                        db=db,
                        category_id=request_list.category_id,
                        fillial_id=request_list.fillial_id,
                        description=request_list.description,
                        product=request_list.product,
                        user_id=request_list.user_id,
                    )
                    for i in new_neq:
                        text_request += f"\n{i.tool.name} - {i.amount} шт. "
                        delete_expanditure(db=db,request_id=request_list.id,tool_id=i.tool_id)

                        create_expanditure(db=db,
                                           request_id=new_request.id,
                                           tool_id=i.tool_id,
                                           amount=i.amount,
                                           )
                    text_request += "\nПри первой возможности будет отправлено.\n"

                text_request += "\nИнвентарь отправлен вам на филиал, прибудет через 12 часов. Как привезут просим вас Подтвердить заявку. \nЕсли вам не привезут их в течении выше указанного времени, можете нажать кнопку “Не сделано”"
                confirmation_request(
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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


