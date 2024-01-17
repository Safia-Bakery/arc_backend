from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form



class HrQuestionsCreate(BaseModel):
    question: str
    answer: Optional[str] = None
    status: Optional[int] = 1

class HrQuestionsUpdate(BaseModel):
    id: int
    question: Optional[str] = None
    answer: Optional[str] = None
    status: Optional[int] = None
    class Config:
        orm_mode = True
        



class HrQuestionsGet(BaseModel):
    id: int
    question: Optional[str] = None
    answer: Optional[str] = None
    status: int
    class Config:
        orm_mode = True


class HrRequest(BaseModel):
    id: int
    comments: Optional[str] = None
    status: Optional[int] = None
    sphere: Optional[int] = None
    created_at: Optional[datetime] = None
    answer: Optional[str] = None    
    class Config:
        orm_mode = True

class HrRequestUpdate(BaseModel):
    id: int
    status: Optional[int] = None
    answer:Optional[str] = None
    class Config:
        orm_mode = True

