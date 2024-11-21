from uuid import UUID

import pytz
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.crud.collector_orders import create_order, get_orders, update_order, create_order_item
from app.routes.depth import get_db
from app.schemas.collector_orders import CreateOrder, UpdateOrder, GetOrder, OrderItem


collector_orders_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@collector_orders_router.post("/collector_order/", response_model=GetOrder)
async def create_collector_order(
        order: CreateOrder,
        db: Session = Depends(get_db)
):
    return create_order(db=db, data=order)


@collector_orders_router.get("/collector_order/", response_model=List[GetOrder])
async def get_collector_order(
        branch_id: str,
        id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    return get_orders(db=db, id=id, branch_id=branch_id)


@collector_orders_router.put("/collector_order/", response_model=GetOrder)
async def update_collector_order(
    data: UpdateOrder,
    db: Session = Depends(get_db)
):
    return update_order(db=db, data=data)
