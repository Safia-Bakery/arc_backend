from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID
from app.schemas.branchs import GetBranchs



class GetUserFullData(BaseModel):
    id:int
    username:str
    full_name:Optional[str]=None
    telegram_id:Optional[int]=None
    branch_id:Optional[UUID]=None
    branch:Optional[GetBranchs]=None


    class Config:
        orm_mode = True


