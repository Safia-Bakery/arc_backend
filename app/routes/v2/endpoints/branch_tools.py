from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.branch_tools import create_branch_tools, get_branch_tools, delete_branch_tool, get_groups
from app.crud.branch_tools import get_tools
from app.routes.depth import get_db, get_current_user
from app.schemas.branch_tools import ToolBranchCategoryRelation, CreateToolBranch, GetToolBranchCategoryRelation, DeleteToolBranch
from app.schemas.branch_tools import ProductsGroups
from app.schemas.users import GetUserFullData, UserFullBack

branch_tools_router = APIRouter()



@branch_tools_router.post('/tools/branch', response_model=List[ToolBranchCategoryRelation])
async def create_branch_products(
        body: CreateToolBranch,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    response = create_branch_tools(db=db, data=body)
    # if response is None:
    #     raise HTTPException(status_code=400, detail="Record exits already")

    return response


@branch_tools_router.get('/tools/branch', response_model=List[GetToolBranchCategoryRelation])
async def get_branch_products(
        branch_id: UUID,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    response = get_branch_tools(db=db, branch_id=branch_id)
    return response



@branch_tools_router.delete('/tools/branch')
async def delete_organization_screen(
        body: DeleteToolBranch,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    response = delete_branch_tool(db=db, body=body)
    if response is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return response


@branch_tools_router.get('/kru/tools/', response_model=ProductsGroups)
async  def get_tools_router(
        tool_name: str,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    if tool_name is not None:
        tools = get_tools(db=db, name=tool_name)
    else:
        tools = []
    return {"folders": [], 'tools':tools}