from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID



class CreateExpensetype(BaseModel):
    name:str
    name:Optional[str] = None
    status:Optional[int] = None

class GetExpensetype(BaseModel):
    name:Optional[str] = None
    status:Optional[int] = None
    created_at:Optional[date] = None
    id:Optional[int] = None
    class Config:
        orm_mode = True

class CreateExpense(BaseModel):
    amount:float
    description:Optional[str] = None
    from_date:Optional[date]=None
    to_date:Optional[date]=None
    expensetype_id:int
    status:Optional[int] = None

    class Config:
        orm_mode = True

class GetExpenses(BaseModel):
    amount:float
    description:Optional[str] = None
    from_date:Optional[date]=None
    to_date:Optional[date]=None
    expensetype_id:int
    status:Optional[int] = None
    created_at:Optional[datetime] = None
    id:Optional[int] = None
    expensetype:Optional[GetExpensetype] = None
    class Config:
        orm_mode = True

class UpdateExpense(BaseModel):
    amount:Optional[float] = None
    description:Optional[str] = None
    from_date:Optional[date]=None
    to_date:Optional[date]=None
    expensetype_id:Optional[int] = None
    status:Optional[int] = None
    id:int
