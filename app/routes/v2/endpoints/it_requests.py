from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
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
from app.utils.utils import sendtotelegramchannel, inlinewebapp, confirmation_request, generate_random_filename

it_requests_router = APIRouter()


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
        request: PutRequest,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user)):
    edited_request = it_requests.edit_request(db=db, request=request)

    if request.status is not None:
        logs.create_log(db=db, data=request, user=request_user)
        if request.status == 1:
            brigader = users.get_user_brig_id(db, request.brigada.id)
            brigader_name = request.brigada.name
            if brigader:
                brigader_telid = brigader.telegram_id
                sendtotelegramchannel(
                    chat_id=brigader_telid,
                    message_text=f"{brigader_name} вам назначена заявка, #{request.id}s {request.fillial.parentfillial.name}"
                )

            try:
                sendtotelegramchannel(
                    chat_id=request.user.telegram_id,
                    message_text=f"Уважаемый {request.user.full_name}, статус вашей заявки #{request.id}s назначен специалист👨‍💻: {brigader_name}\nВремя выполнения: {int(request.category.ftime)} часов",
                )
            except:
                pass

        elif request.status == 3:
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={request.user.id}&department={request.category.department}&sub_id={request.category.sub_id}"
            try:
                inlinewebapp(
                    chat_id=request.user.telegram_id,
                    message_text=f"Уважаемый {request.user.full_name}, статус вашей заявки #{request.id}s по IT: Завершен.\n\nПожалуйста нажмите на кнопку Оставить отзыв🌟и  оцените заявк",
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
            request_text = f"Уважаемый {request.user.full_name} , Ваша заявка #{request.id}s ИТ решена. Пожалуйста, подтвердите, что она выполнена в соответствии с вашим запросом."

            confirmation_request(chat_id=request.user.telegram_id, message_text=request_text)

        elif request.status == 7:
            sendtotelegramchannel(
                chat_id=request.user.telegram_id,
                message_text=f"Ваша заявка #{request.id}s возобновлено"
            )
        elif request.status == 8:
            url = f"{settings.FRONT_URL}tg/order-rating/{request.id}?user_id={request.user.id}&department={request.category.department}&sub_id={request.category.sub_id}"
            inlinewebapp(
                chat_id=request.user.telegram_id,
                message_text=f"""❌Ваша заявка #{request.id}s по IT👨🏻‍💻 отменена по причине: {request.deny_reason}\n\nЕсли Вы с этим не согласны, поставьте, пожалуйста, рейтинг нашему решению по Вашей заявке от 1 до 5, и напишите свои комментарий.""",
                url=url,
            )

    return edited_request


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
