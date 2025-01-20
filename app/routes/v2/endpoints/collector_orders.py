from uuid import UUID

import pytz
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.crud.collector_orders import create_order, get_orders, update_order, get_one_order
from app.routes.depth import get_db, get_current_user
from app.schemas.collector_orders import CreateOrder, UpdateOrder, GetOrder, OrderItem, OrdersHistory
from app.schemas.users import GetUserFullData


collector_orders_router = APIRouter()
timezone_tash = pytz.timezone('Asia/Tashkent')


@collector_orders_router.post("/collector/order/", response_model=GetOrder)
async def create_collector_order(
        order: CreateOrder,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    order = create_order(db=db, branch_id=request_user.branch_id, data=order, created_by=request_user.id)
    if order is None:
        raise HTTPException(status_code=400, detail="Не смогли создать заказ. Проверьте остаток товаров на складе !")

    return order


@collector_orders_router.get("/collector/order/", response_model=List[GetOrder])
async def get_collector_orders(
        branch_id: Optional[str] = None,
        status: Optional[int] = None,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    return get_orders(db=db, branch_id=branch_id or request_user.branch_id, status=status)


@collector_orders_router.get("/collector/order/{id}", response_model=GetOrder)
async def get_collector_one_order(
        id: int,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    return get_one_order(db=db, id=id)


@collector_orders_router.put("/collector/order/{id}", response_model=GetOrder)
async def update_collector_order(
        id: int,
        status: int,
        message_id: Optional[int] = None,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    return update_order(
        db=db,
        id=id,
        status=status,
        message_id=message_id,
        user=request_user
    )


@collector_orders_router.get("/collector/my-orders", response_model=OrdersHistory)
async def show_my_orders(
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    active_orders = get_orders(db=db, branch_id=request_user.branch_id, status=0)
    closed_orders = get_orders(db=db, branch_id=request_user.branch_id, status=1)
    orders_history = {
        "active": active_orders,
        "closed": closed_orders
    }
    return orders_history
