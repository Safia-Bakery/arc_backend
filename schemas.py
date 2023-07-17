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
    group_id:Optional[int]=None
    group:Optional[object]=None
    class Config:
        from_attributes=True



class User(BaseModel):
    id: int
    username: str
    success:Optional[bool]=True
    full_name : Optional[str]=None
    class Config:
        from_attributes=True

class UserCreate(BaseModel):
    password : str
    username:str
    full_name: Optional[str]=None
    email:Optional[str]=None
    phone_number:str
    group_id:Optional[int]=None
    status:int
    @validator('password')
    def validate_password_length(cls, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password
    @validator('status')
    def validate_status(cls, status):
        if status not in [0,2]:
            raise ValueError("send valid  status code please send 0 or 2. 0 for default user 2 for inactive user")
        return status
    


class PagesSch(BaseModel):
    id:int
    page_name:str
    class Config:
        from_attributes=True



class CreateGroupSch(BaseModel):
    name:str
    status:int
    class Config:
        from_attributes=True
    @validator('status')
    def validate_password_length(cls, status):
        if status not in [0,1]:
            raise ValueError("send valid  status code ")
        return status
    

class UpdateGroupSch(BaseModel):
    name:str
    id :int
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
    name : str
    description: str
    status : int


    @validator('status')
    def validate_status_length(cls, status):
        if status not in [0,1]:
            raise ValueError("send valid  status code ")
        return status
    

class AddFillialSch(BaseModel):
    name:str
    longtitude:Optional[float]=None
    latitude:Optional[float]=None
    country:Optional[str]=None
    status : int
    class Config:
        from_attributes=True
    @validator('status')
    def validate_password_length(cls, status):
        if status not in [0,1]:
            raise ValueError("send valid  status code ")
        return status
    

class GetFillialSch(BaseModel):
    id : int
    name:str
    longtitude:Optional[int]=None
    latitude:Optional[int]=None
    country:Optional[str]=None
    status : int
    class Config:
        from_attributes=True


class UpdateFillialSch(BaseModel):
    id:int
    longtitude:Optional[float]=None
    latitude:Optional[float]=None
    status:Optional[int]=None


class AddCategorySch(BaseModel):
    name:str
    description:str
    status:int
    @validator('status')
    def validate_status_length(cls, status):
        if status not in [0,1]:
            raise ValueError("send valid  status code ")
        return status
    
class UpdateCategorySch(BaseModel):
    id:int
    name:Optional[str]=None
    description:Optional[str]=None
    status:Optional[int]=None
    @validator('status')
    def validate_status_length(cls, status):
        if status not in [0,1]:
            raise ValueError("send valid  status code ")
        return status
    
class GetCategorySch(BaseModel):
    name:str
    description:Optional[str]=None
    status:int
    id:int
    class Config:
        from_attributes=True



class UserGetlist(BaseModel):
    id:int
    username:str
    full_name: Optional[str]=None
    email: Optional[str]=None
    phone_number: Optional[str]=None
    group:Optional[UpdateGroupSch]=None
    status:int
    class Config:
        from_attributes=True


class GetBrigadaList(BaseModel):
    id:int
    name:str
    description:Optional[str]=None
    status:int
    class Config:
        from_attributes=True



class GetBrigadaIdSch(BaseModel):
    id:int
    name:str
    description:Optional[str]=None
    status:int
    user : list[UserGetlist]
    class Config:
        from_attributes=True

class FileSch(BaseModel):
    url:str
    class Config:
        from_attributes=True

class GetRequestList(BaseModel):
    product:Optional[str]=None
    description:Optional[str]=None
    id:int
    rating:Optional[int]=None
    created_at:datetime
    status:int
    brigada:Optional[GetBrigadaList]=None
    file:list[FileSch]
    category:Optional[GetCategorySch]=None
    fillial:Optional[GetFillialSch]=None
    finished_at:Optional[datetime]=None
    id:int
    urgent:bool
    class Config:
        from_attributes=True



class RequestAttachBrigada(BaseModel):
    request_id:int
    brigada_id:int


class UpdateBrigadaSch(BaseModel):
    id:int
    name:Optional[str]
    description:Optional[str]
    status:Optional[int]
    users:Optional[list[int]]=None





class GetUserIdSch(BaseModel):
    id:int
    username: str
    time_created :datetime
    full_name: Optional[str]=None
    status : int
    email:Optional[str]=None
    phone_number:Optional[str]=None
    group:Optional[UpdateGroupSch]=None
    brigader:Optional[GetBrigadaList]=None
    class Config:
        from_attributes=True


class CreateTool(BaseModel):
    name:str
    class Config:
        from_attributes=True