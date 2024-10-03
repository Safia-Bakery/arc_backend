from typing import Optional

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string
from app.schemas.branchs import GetBranchs
from fastapi_pagination import Page,paginate
from app.crud.branchs import get_branchs



branchs_router = APIRouter()

@branchs_router.get("/branchs/",response_model=Page[GetBranchs])
async def get_branchs_api(
    name:Optional[str]=None,
    id:Optional[int]=None,

    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    """
    Get branchs
    """
    return paginate(get_branchs(db=db,branch_name=name,id=id))