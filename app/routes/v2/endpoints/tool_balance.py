from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter
)
from fastapi_pagination import paginate, Page
from typing import Optional, List
from app.schemas.it_extra import *
from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.schemas.tool_balance import GetToolBalance, UpdateToolBalance, GetGroupToolBalances
from app.crud import tool_balance
from datetime import datetime, date


tool_balance_router = APIRouter()


@tool_balance_router.get("/tools/balances", response_model=GetGroupToolBalances)
async def get_tool_balances(
        parent_id: Optional[UUID] = None,
        name: Optional[str] = None,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    return {
        "groups": tool_balance.getarchtools(db, parent_id),
        "products": tool_balance.tools_query_iarch(db, parent_id, name, request_user.branch_id)
    }


@tool_balance_router.get("/tools/balances/{tool_id}", response_model=GetToolBalance)
async def get_tool_balance(
        tool_id: int,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    tool_balance_obj = tool_balance.get_balance(
        db=db,
        department_id=request_user.branch_id,
        tool_id=tool_id
    )
    if tool_balance_obj is None:
        return {}
        # If no balance is found, raise a 404 error
        # raise HTTPException(status_code=404, detail="Tool balance not found")

    return tool_balance_obj


@tool_balance_router.put("/tools/balances", response_model=GetToolBalance)
async def edit_tool_balance(
        data: UpdateToolBalance,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    product_balance_obj = tool_balance.create_update_balance(db=db, data=data, department_id=request_user.branch_id)
    return product_balance_obj
