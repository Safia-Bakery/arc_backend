from typing import List

from sqlalchemy.orm import Session
from app.models.collector_orders import CollectOrders, CollectOrderItems
from app.schemas.collector_orders import CreateOrder, UpdateOrder, OrderItem


def get_orders(db: Session, branch_id, id):
    query = db.query(CollectOrders).filter(CollectOrders.branch_id == branch_id)
    if id is not None:
        query = db.query(CollectOrders).filter(CollectOrders.id == id).first()
    else:
        query = query.all()

    return query


def create_order(db: Session, data: CreateOrder):
    query = CollectOrders(
        branch_id=data.branch_id,
        created_by=data.created_by
    )
    db.add(query)
    db.commit()
    db.refresh(query)

    for item in data.products:
        create_order_item(db=db, order_id=query.id, product_id=item.product_id)

    return query


def update_order(db: Session, data: UpdateOrder):
    query = db.query(CollectOrders).filter(CollectOrders.id == data.id).first()
    query.status = data.status
    query.accepted_by = data.accepted_by

    db.commit()
    db.refresh(query)
    return query


def create_order_item(db: Session, order_id, product_id):
    query = CollectOrderItems(
        order_id=order_id,
        product_id=product_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query
