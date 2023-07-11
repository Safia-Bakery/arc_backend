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
    brigader:Optional[object]=None
    class Config:
        from_attributes=True


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
        from_attributes=True



class CreateGroupSch(BaseModel):
    name:str
    class Config:
        from_attributes=True


class UsersSettingsSch(BaseModel):
    id:int
    username:str
    full_name:Optional[str]=None
    time_created:datetime
    group_id:Optional[int]=None
    group:Optional[CreateGroupSch]=None
    class Config:
        from_attributes=True



class UserRoleAttachSch(BaseModel):
    user_id: int
    group_id:int


class UservsRoleCr(BaseModel):
    password : str
    username:str
    full_name: Optional[str]=None
    group_id :int
    brigada_name : str
    brigada_description: str

    @validator('password')
    def validate_password_length(cls, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password