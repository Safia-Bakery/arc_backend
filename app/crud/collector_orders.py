from typing import List
from uuid import UUID
import requests
from sqlalchemy import and_
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.collector_orders import CollectOrders, CollectOrderItems
from app.models.users_model import Users
from app.schemas.collector_orders import CreateOrder, UpdateOrder, OrderItem


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

    freezers = db.query(Users.telegram_id).filter(and_(Users.branch_id == branch_id, Users.group_id == 35)).all()
    for freezer in freezers:
        url = f'https://api.telegram.org/bot{settings.collector_bottoken}/sendMessage'
        payload = {
            'chat_id': freezer,
            'text': f"Поступила новая заявка: № {query.id}",
            'parse_mode': 'HTML'
        }
        requests.post(url, json=payload)

    return query


def update_order(db: Session, id, status, accepted_by):
    query = db.query(CollectOrders).filter(CollectOrders.id == id).first()
    query.status = status
    query.accepted_by = accepted_by

    db.commit()
    db.refresh(query)

    url = f'https://api.telegram.org/bot{settings.collector_bottoken}/sendMessage'
    payload = {
        'chat_id': query.created_user.telegram_id,
        'text': f"Заявка № {query.id} собрана",
        'parse_mode': 'HTML'
    }
    requests.post(url, json=payload)

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
