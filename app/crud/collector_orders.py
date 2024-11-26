from typing import List
from uuid import UUID
import requests
from sqlalchemy import and_
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.collector_orders import CollectOrders, CollectOrderItems
from app.models.users_model import Users
from app.schemas.collector_orders import CreateOrder, UpdateOrder, OrderItem
from microservices import create_access_token

FRONT_URL = 'https://service.safiabakery.uz/'


def get_orders(db: Session, branch_id, status):
    query = db.query(CollectOrders)
    if branch_id is not None:
        query = query.filter(CollectOrders.branch_id == branch_id)
    if status is not None:
        query = query.filter(CollectOrders.status == status)

    query = query.all()
    return query


def get_one_order(db: Session, id):
    query = db.query(CollectOrders).filter(CollectOrders.id == id).first()
    return query


def create_order(db: Session, branch_id: UUID, data: CreateOrder, created_by):
    query = CollectOrders(
        created_by=created_by,
        branch_id=branch_id,
    )
    db.add(query)
    db.commit()
    db.refresh(query)

    for item in data.products:
        create_order_item(db=db, order_id=query.id, product_id=item.product_id,amount=item.amount)

    freezers = db.query(Users).filter(and_(Users.branch_id == branch_id, Users.group_id == 35)).all()
    url = f'https://api.telegram.org/bot{settings.collector_bottoken}/sendMessage'
    for freezer in freezers:
        payload = {
            'chat_id': freezer.telegram_id,
            'text': f"Поступила новая заявка: № {query.id}",
            'parse_mode': 'HTML'
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(e)

    return query


def update_order(db: Session, id, status, user):
    query = db.query(CollectOrders).filter(CollectOrders.id == id).first()
    query.status = status
    query.accepted_by = user.id

    db.commit()
    db.refresh(query)

    base_url = f'https://api.telegram.org/bot{settings.collector_bottoken}'

    send_url = f"{base_url}/sendMessage"
    send_payload = {
        'chat_id': query.created_user.telegram_id,
        'text': f"Заявка № {query.id} собрана",
        'parse_mode': 'HTML'
    }
    try:
        requests.post(send_url, json=send_payload)
    except Exception as e:
        print(e)

    get_updates_url = f"{base_url}/getUpdates"
    delete_url = f"{base_url}/deleteMessage"
    updates_response = requests.get(get_updates_url)
    updates = updates_response.json()
    updates_desc = updates["result"][::-1]
    last_update = updates_desc[0]
    if 'message' in last_update:
        if last_update['message']['chat']['id'] == user.telegram_id and last_update['message']['from']['is_bot']:
            delete_payload = {
                'chat_id': user.telegram_id,
                'message_id': last_update['message']['message_id']
            }
            try:
                requests.post(delete_url, data=delete_payload)
            except Exception as e:
                print(e)

            my_orders = get_orders(db=db, branch_id=user.branch_id, status=0)
            access_token = create_access_token(user.username)
            if len(my_orders) > 0:
                keyboard = {
                    "inline_keyboard": [
                        [
                            {
                                "text": "Оставить отзыв🌟",
                                "web_app": {"url": f"{FRONT_URL}/tg/collector?key={access_token}&order_id={item['id']}"}
                            } for item in my_orders[i:i + 3]
                        ] for i in range(0, len(my_orders), 3)
                    ]
                }
                text = "Выберите заявку 👇"
            else:
                keyboard = [[]]
                text = "Активных заявок нет"

            # Create the request payload
            payload = {
                "chat_id": user.telegram_id,
                "text": text,
                "reply_markup": keyboard,
                "parse_mode": "HTML",
            }

            # Send the request to send the inline keyboard message
            try:
                requests.post(send_url, json=payload)
            except Exception as e:
                print(e)

    return query


def create_order_item(db: Session, order_id, product_id,amount):
    query = CollectOrderItems(
        order_id=order_id,
        product_id=product_id,
        amount=amount
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query
