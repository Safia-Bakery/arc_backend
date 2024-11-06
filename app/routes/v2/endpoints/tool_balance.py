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
from app.schemas.tool_balance import GetBalances
from app.crud import tool_balance
from datetime import datetime, date


tool_balance_router = APIRouter()


@tool_balance_router.get("/tools/balances", response_model=Page[GetBalances])
async def store_balance(
        store_id: str,
        department_id: Optional[str] = None,
        tool_id: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: UserFullBack = Depends(get_current_user),
):

    request_list = tool_balance.get_department_store_product_balances(
        db,
        department_id=department_id,
        store_id=store_id,
        tool_id=tool_id
    )

    return paginate(request_list)

