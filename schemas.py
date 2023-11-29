from pydantic import BaseModel,validator
from fastapi import Form,UploadFile,File
from typing import Optional,Annotated,Dict
from datetime import datetime,time
from fastapi import Form
from uuid import UUID



    






class UpdateGroupSch(BaseModel):
    name:str
    id :int
    class Config:
        orm_mode=True





class UserRoleAttachSch(BaseModel):
    user_id: int
    group_id:int


class UservsRoleCr(BaseModel):
    name : str
    description: str
    status : int
    sphere_status:int



    @validator('status')
    def validate_status_length(cls, status):
        if status not in [0,1,2]:
            raise ValueError("send valid  status code ")
        return status
    

class AddFillialSch(BaseModel):
    name:str
    longtitude:Optional[float]=None
    latitude:Optional[float]=None
    country:Optional[str]=None
    status : int
    class Config:
        orm_mode=True
    @validator('status')
    def validate_password_length(cls, status):
        if status not in [0,1]:
            raise ValueError("send valid  status code ")
        return status
    

class GetParentFill(BaseModel):
    name:str
    class Config:
        orm_mode=True

class GetFillialChild(BaseModel):
    id:UUID
    name:str
    origin:int
    parentfillial:Optional[GetParentFill]=None
    class Config:
        orm_mode=True

class GetFillialSch(BaseModel):
    id : UUID
    name:str
    longtitude:Optional[float]=None
    latitude:Optional[float]=None
    country:Optional[str]=None
    status : int
    is_fabrica:Optional[int]=None
    fillial_department:list[GetFillialChild]
    class Config:
        orm_mode=True





class ToolsSearch(BaseModel):
    id:int
    name:Optional[str]=None
    code:Optional[str]=None
    mainunit:Optional[str]=None
    producttype:Optional[str]=None
    class Config:
        orm_mode=True




class UpdateFillialSch(BaseModel):
    id:UUID
    longtitude:Optional[float]=None
    latitude:Optional[float]=None
    status:Optional[int]=None
    department_id:Optional[UUID]=None
    origin:Optional[int]=None
    is_fabrica:Optional[int]=None



class AddCategorySch(BaseModel):
    name:str
    description:str
    status:int
    urgent:bool
    sub_id:Optional[int]=None
    department:int
    sphere_status:Optional[int]=0
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
    urgent:Optional[bool]=None
    sub_id :Optional[int]=None
    department:Optional[int]=None
    sphere_status:Optional[int]=None
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
    urgent:bool
    sub_id:Optional[int]=None
    department:int
    sphere_status:Optional[int]=None
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



class GetBrigadaList(BaseModel):
    id:int
    name:str
    description:Optional[str]=None
    status:int
    user:list[UserGetlist]
    sphere_status:int
    class Config:
        orm_mode=True



class GetBrigadaIdSch(BaseModel):
    id:int
    name:str
    description:Optional[str]=None
    status:int
    user : list[UserGetlist]
    sphere_status:Optional[int]=None
    class Config:
        orm_mode=True

class FileSch(BaseModel):
    url:str
    status:int
    class Config:
        orm_mode=True




class GetRequestList(BaseModel):
    product:Optional[str]=None
    id:int
    rating:Optional[int]=None
    created_at:datetime
    status:int
    brigada:Optional[GetBrigadaList]=None
    file:list[FileSch]
    category:Optional[GetCategorySch]=None
    fillial:Optional[GetFillialChild]=None
    started_at :Optional[datetime]=None
    finished_at:Optional[datetime]=None
    user:Optional[UserGetlist]=None
    user_manager:Optional[str]=None
    is_bot:Optional[bool]=None
    arrival_date:Optional[datetime]=None
    bread_size:Optional[str]=None
    size:Optional[str]=None
    id:int
    location:Optional[Dict[str,str]]=None
    update_time:Optional[Dict[str,str]]=None
    class Config:
        orm_mode=True



class GetComments(BaseModel):
    id:int
    request:GetRequestList
    user:UserGetlist
    comment:str
    class Config:
        orm_mode=True


class GetExpanditure(BaseModel):
    id:int
    amount:int
    tool:Optional[ToolsSearch]=None
    comment:Optional[str]=None
    user:Optional[UserGetlist]=None
    created_at:datetime
    class Config:
        orm_mode=True

class GetRequestid(BaseModel):
    product:Optional[str]=None
    description:Optional[str]=None
    deny_reason:Optional[str]=None
    id:int
    rating:Optional[int]=None
    created_at:datetime
    status:int
    brigada:Optional[GetBrigadaList]=None
    file:list[FileSch]
    category:Optional[GetCategorySch]=None
    fillial:Optional[GetFillialChild]=None
    started_at :Optional[datetime]=None
    finished_at:Optional[datetime]=None
    user:Optional[UserGetlist]=None
    user_manager:Optional[str]=None
    expanditure:list[GetExpanditure]
    comments:list[GetComments]
    is_bot:Optional[bool]=None
    size:Optional[str]=None
    arrival_date:Optional[datetime]=None
    bread_size:Optional[str]=None
    id:int
    location:Optional[Dict[str,str]]=None
    update_time:Optional[Dict[str,str]]=None
    class Config:
        orm_mode=True



class RequestAttachBrigada(BaseModel):
    request_id:int
    brigada_id:int


class UpdateBrigadaSch(BaseModel):
    id:int
    name:Optional[str]=None
    description:Optional[str]=None
    status:Optional[int]=None
    users:Optional[list[int]]=None
    sphere_status:Optional[int]=None





class GetUserIdSch(BaseModel):
    id:int
    sphere_status:Optional[int]=None
    username: Optional[str]=None
    time_created :datetime
    full_name: Optional[str]=None
    status : int
    telegram_id : Optional[int]=None
    email:Optional[str]=None
    phone_number:Optional[str]=None
    group:Optional[UpdateGroupSch]=None
    brigader:Optional[GetBrigadaList]=None
    class Config:
        orm_mode=True


class CreateTool(BaseModel):
    name:str
    class Config:
        orm_mode=True

class GetToolList(BaseModel):
    name:str
    id:int
    class Config:
        orm_mode=True

class AcceptRejectRequest(BaseModel):
    request_id :int
    status :int
    
    brigada_id:Optional[int]=None
    deny_reason:Optional[str]=None


    @validator('status')
    def validate_status_length(cls, status):
        if status not in [4,1,2,3,5]:
            raise ValueError("send valid  status code ")
        return status
    


class UserUpdateAll(BaseModel):
    password:Optional[str]=None
    username:Optional[str]=None
    full_name:Optional[str]=None
    email:Optional[str]=None
    status:Optional[int]=None
    phone_number:Optional[int]=None
    group_id:Optional[int]=None
    brigada_id:Optional[int]=None
    telegram_id:Optional[int]=None
    sphere_status:Optional[int]=None
    user_id:int
    @validator('status')
    def validate_status_length(cls, status):
        if status not in [0,2]:
            raise ValueError("send valid  status code")
        return status
    class Config:
        orm_mode=True


class BotRegister(BaseModel):
    full_name:str
    phone_number:str
    telegram_id:int
    sphere_status:int


class BotCheckUser(BaseModel):
    phone_number:str
    telegram_id:str


class TgCreateRequest(BaseModel):
    phone_number:Annotated[str,Form()]
    telegram_id:Annotated[int,Form()]


class TgUpdateStatusRequest(BaseModel):
    status : int
    request_id : int
    @validator('status')
    def validate_status_length(cls, status):
        if status not in [2,3]:
            raise ValueError("send valid  status code ")
        return status
    

class ExpanditureSchema(BaseModel):
    amount:int
    tool_id :int

class FourChildsch(BaseModel):
    id:UUID
    name:str
    code:str
    class Config:
        orm_mode=True


class ThirdChildsch(BaseModel):
    id:UUID
    name:str
    code:str
    child:list[FourChildsch]
    class Config:
        orm_mode=True

    
class Secondchildsch(BaseModel):
    id:UUID
    name:str
    code:str
    child:list[ThirdChildsch]
    class Config:
        orm_mode=True



class Firstchildsch(BaseModel):
    id:UUID
    name:str
    code:str
    child:list[Secondchildsch]
    class Config:
        orm_mode=True

class ToolParentsch(BaseModel):
    id:UUID
    name:str
    code:str
    child:list[Firstchildsch]
    class Config:
        orm_mode=True



class DepartmenUdpate(BaseModel):
    id:UUID
    origin : int
    @validator('origin')
    def validate_status_length(cls, origin):
        if origin not in [1,2]:
            raise ValueError("send valid  status code ")
        return origin
    

class SynchExanditureiiko(BaseModel):
    request_id:int






class AddComments(BaseModel):
    request_id:int
    comment:str
    class Config:
        orm_mode=True


class TGlogin(BaseModel):
    telegram_id:int

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

class ToolsLeft(BaseModel):
    name:str
    amount_left:Optional[float]=None
    last_update:Optional[datetime]=None
    total_price:Optional[float]=None
    class Config:
        orm_mode=True


class Expanditurelist(BaseModel):
    id:int
    created_at:Optional[datetime]=None
    request_id:int
    amount:int
    class Config:
        orm_mode=True



class WorkTimeUpdate(BaseModel):
    #id:int
    from_time:Optional[time]=None
    to_time:Optional[time]=None
    class Config:
        orm_mode=True