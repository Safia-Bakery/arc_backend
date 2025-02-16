from typing import List
from uuid import UUID
import requests
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from app.models.tool_balance import ToolBalance
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

    query = query.order_by(CollectOrders.id.desc()).all()
    return query


def get_one_order(db: Session, id):
    query = db.query(CollectOrders).filter(CollectOrders.id == id).first()
    return query


def create_order(db: Session, branch_id: UUID, data: CreateOrder, created_by):
    try:
        query = CollectOrders(
            created_by=created_by,
            branch_id=branch_id,
        )
        db.add(query)
        db.flush()
        db.refresh(query)

        for item in data.products:
            # product_balance = db.query(ToolBalance).filter(
            #     and_(
            #         ToolBalance.department_id == branch_id,
            #         ToolBalance.tool_id == item.product_id
            #     )
            # ).first()
            # if product_balance is not None and item.amount <= product_balance.amount:
            #     product_balance.amount -= item.amount
            #     # db.commit()
            #     # db.refresh(product_balance)
            #     db.flush()
            # else:
            #     raise ValueError(f"Insufficient balance for product {item.product_id}")

            order_item = CollectOrderItems(
                order_id=query.id,
                product_id=item.product_id,
                amount=item.amount
            )
            db.add(order_item)
            db.flush()

        db.commit()

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

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()  # Rollback the transaction explicitly (optional, since `begin` handles this)
        print(f"Transaction failed: {e}")
        return None

    return query


def update_order(db: Session, id, status, message_id, user):
    query = db.query(CollectOrders).filter(CollectOrders.id == id).first()
    order_items = db.query(CollectOrderItems).filter(CollectOrderItems.order_id == query.id).all()
    try:
        for item in order_items:
            product_balance = db.query(ToolBalance).filter(
                and_(
                    ToolBalance.department_id == user.branch_id,
                    ToolBalance.tool_id == item.product_id
                )
            ).first()
            if product_balance is not None and item.amount <= product_balance.amount:
                product_balance.amount -= item.amount
                db.flush()
            else:
                raise ValueError(f"Insufficient balance for product {item.product_id}")

        query.status = status
        query.accepted_by = user.id

        db.commit()
        db.refresh(query)
    except:
        db.rollback()
        raise ValueError(f"Insufficient balance for some product !")

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

    my_orders = get_orders(db=db, branch_id=user.branch_id, status=0)
    if len(my_orders) > 0:
        access_token = create_access_token(user.username)
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": f"№ {item.id}",
                        "web_app": {
                            "url": f"{FRONT_URL}/tg/collector?key={access_token}&order_id={item.id}&message_id={message_id}"
                        }
                    } for item in my_orders[i:i + 3]
                ] for i in range(0, len(my_orders), 3)
            ]
        }
        text = "Выберите заявку 👇"
    else:
        keyboard = {"inline_keyboard": [[]]}
        text = "Активных заявок нет"

    edit_url = f"{base_url}/editMessageText"
    edit_payload = {
        "chat_id": user.telegram_id,
        "message_id": message_id,
        "text": text,
        "reply_markup": keyboard,
        "parse_mode": "HTML"
    }
    try:
        requests.post(edit_url, json=edit_payload)
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
