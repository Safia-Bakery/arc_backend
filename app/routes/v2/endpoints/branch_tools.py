from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.branch_tools import create_branch_tools, get_branch_tools, delete_branch_tool
from app.routes.depth import get_db, get_current_user
from app.schemas.branch_tools import ToolBranchCategoryRelation, CreateToolBranch, GetToolBranchCategoryRelation, DeleteToolBranch
from app.schemas.users import GetUserFullData


branch_tools_router = APIRouter()



@branch_tools_router.post('/tools/branch', response_model=ToolBranchCategoryRelation)
async def create_branch_products(
        body: CreateToolBranch,
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    response = create_branch_tools(db=db, data=body, branch_id=request_user.branch_id)
    if response is None:
        raise HTTPException(status_code=400, detail="Record exits already")

    return response


@branch_tools_router.get('/tools/branch', response_model=List[GetToolBranchCategoryRelation])
async def get_branch_products(
        db: Session = Depends(get_db),
        request_user: GetUserFullData = Depends(get_current_user)
):
    response = get_branch_tools(db=db, branch_id=request_user.branch_id)
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

