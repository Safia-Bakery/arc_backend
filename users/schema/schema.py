from pydantic import BaseModel,validator
from fastapi import Form,UploadFile,File
from typing import Optional,Annotated,Dict
from datetime import datetime,time
from fastapi import Form
from uuid import UUID


class UserFullBack(BaseModel):
    id: int
    username: str
    success:Optional[bool]=True
    full_name : Optional[str]=None
    status:Optional[int]=None
    sphere_status:Optional[int]=None
    brigader:Optional[object]=None
    brigada_id:Optional[object]=None
    group_id:Optional[int]=None
    group:Optional[object]=None
    class Config:
        orm_mode=True



class User(BaseModel):
    id: int
    username: str
    sphere_status:Optional[int]=None
    success:Optional[bool]=True
    full_name : Optional[str]=None
    class Config:
        orm_mode=True



class UserCreate(BaseModel):
    password : str
    username:str
    full_name: Optional[str]=None
    sphere_status:Optional[int]=None
    email:Optional[str]=None
    phone_number:str
    group_id:Optional[int]=None
    status:Optional[int]=None
    @validator('password')
    def validate_password_length(cls, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password
    @validator('status')
    def validate_status(cls, status):
        if status not in [0,2,3]:
            raise ValueError("send valid  status code please send 0 or 2. 0 for default user 2 for inactive user")
        return status
    

class Pages(BaseModel):
    id:int
    action_name:str
    class Config:
        orm_mode=True


class ParentPage(BaseModel):
    page_name:str
    actions:list[Pages]
    class Config:
        orm_mode=True
    

class PagesSch(BaseModel):
    id:int
    page_name:str
    class Config:
        orm_mode=True


class CreateGroupSch(BaseModel):
    name:str
    status:int
    class Config:
        orm_mode=True
    @validator('status')
    def validate_password_length(cls, status):
        if status not in [0,1]:
            raise ValueError("send valid  status code ")
        return status
    
class UsersSettingsSch(BaseModel):
    id:int
    username:str
    full_name:Optional[str]=None
    sphere_status:Optional[int]=None
    time_created:datetime
    group_id:Optional[int]=None
    group:Optional[CreateGroupSch]=None
    class Config:
        orm_mode=True



class UpdateGroupSch(BaseModel):
    name:str
    id :int
    class Config:
        orm_mode=True



class UserGetlist(BaseModel):
    id:int
    username:Optional[str]=None
    full_name: Optional[str]=None
    email: Optional[str]=None
    phone_number: Optional[str]=None
    group:Optional[UpdateGroupSch]=None
    status:int
    class Config:
        orm_mode=True