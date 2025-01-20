from datetime import timedelta
from typing import List

import pytz
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from fastapi_pagination import paginate, Page
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import uniform_requests, uniform_category, it_requests, logs
from app.models.category import Category
from app.routes.depth import get_db, get_current_user
from app.schemas.it_extra import *
from app.schemas.orders import OrderProducts, CategoryProducts
from app.schemas.uniform_requests import GetRequest, GetRequestList, UpdateRequest, CreateRequest
from app.schemas.requests import GetOneRequest
from app.schemas.users import UserFullBack
from app.utils.utils import sendtotelegramchat, sendtotelegramtopic, delete_from_chat, edit_topic_message, \
    inlinewebapp, generate_random_filename, send_notification, edit_topic_reply_markup

uniform_requests_router = APIRouter()

timezonetash = pytz.timezone("Asia/Tashkent")
BASE_URL = 'https://api.service.safiabakery.uz/'


@uniform_requests_router.get("/requests/uniform/", response_model=Page[GetRequestList])
async def filter_requests(
        id: Optional[int] = None,
        fillial_id: Optional[UUID] = None,
        created_at: Optional[date] = None,
        status: Optional[int] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    request_list = uniform_requests.filtered_requests(
        db,
        id=id,
        fillial_id=fillial_id,
        created_at=created_at,
        request_status=status
    )

    return paginate(request_list)


@uniform_requests_router.get("/requests/uniform/{id}/", response_model=GetRequest)
async def get_request(
        id: int,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    try:
        request_list = uniform_requests.get_request(db, id)
        return request_list
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not found")


@uniform_requests_router.put("/requests/uniform/{id}/", response_model=GetRequest)
async def put_request_id(
        data: UpdateRequest,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):


    request = uniform_requests.edit_request(db=db, data=data, user_manager=request_user.full_name)

    if data.status is not None:
        logs.create_log(db=db, request_id=request.id, status=request.status, user_id=request_user.id)
        user_telegram_id = request.user.telegram_id if request.user else None

        product_list = ""
        request_text = ""

        if data.status == 1:
            for item in data.request_products:
                product_list += f"{item.orpr_product.prod_cat.name} [ {item.orpr_product.name} ] - {item.orpr_product.prod_cat.price} сум x {item.amount} шт\n"

            request_text = f"Ваша 📑заявка #{request.id}s на форму принята.\n" \
                           f"Как ваша форма будет готова, вы получите оповещение!\n\n" \
                           f"Вы заказали:\n" \
                           f"{product_list}\n" \
                           f"Кому: {request.description}"

        elif data.status == 3:
            for item in data.request_products:
                product_list += f"<s>{item.orpr_product.prod_cat.name} [ {item.orpr_product.name} ] - {item.orpr_product.prod_cat.price} сум x {item.amount} шт</s>  ({item.deny_reason})\n" if item.confirmed is False \
                    else f"{item.orpr_product.prod_cat.name} [ {item.orpr_product.name} ] - {item.orpr_product.prod_cat.price} сум x {item.amount} шт\n"

            request_text = f"Ваша форма по 📑заявке #{request.id}s готова.\n" \
                           f"Можете приехать в головной офис и забрать.\n\n" \
                           f"Вы заказали:\n" \
                           f"{product_list}\n" \
                           f"Кому: {request.description}\n\n" \
                           f"* С ЗП сотрудника будет удержана сумма только за выданную форму ..."

        elif data.status == 4:
            request_text = f"Ваша заявка #{request.id}s была отменена 🚫 по причине: \n{request.deny_reason}"

        try:
            sendtotelegramchat(chat_id=user_telegram_id, message_text=request_text)
        except Exception as e:
            print(e)

    return request


@uniform_requests_router.post("/requests/uniform/", response_model=GetRequest)
async def create_request(
        data: CreateRequest,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    request = uniform_requests.add_request(db, request_user, data)
    if request is None:
        raise HTTPException(status_code=400, detail="Не смогли создать заказ. Перепроверьте правильность заполнения !")

    logs.create_log(db=db, request_id=request.id, status=request.status, user_id=request_user.id)
    return request


@uniform_requests_router.get("/category/uniform/products/", response_model=List[CategoryProducts])
async def get_uniform_products(
        category_id: int,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)
):
    uniform_sizes = uniform_category.get_category_products(db=db, name=None, category_id=category_id)
    return uniform_sizes
