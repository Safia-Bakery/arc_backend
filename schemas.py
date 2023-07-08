from pydantic import BaseModel,validator
from fastapi import Form,UploadFile,File
from typing import Optional
from datetime import datetime


class UserFullBack(BaseModel):
    id: int
    username: str
    success:Optional[bool]=True
    full_name : Optional[str]=None
    status:Optional[int]=None


class User(BaseModel):
    id: int
    username: str
    success:Optional[bool]=True
    full_name : Optional[str]=None


class UserCreate(BaseModel):
    password : str
    username:str
    full_name: Optional[str]=None
    @validator('password')
    def validate_password_length(cls, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password
    


class PagesSch(BaseModel):
    id:int
    page_name:str
    class Config:
        orm_mode=True



class CreateGroupSch(BaseModel):
    name:str

