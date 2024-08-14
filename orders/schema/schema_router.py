from pydantic import BaseModel, Field,validator,root_validator
from fastapi import Form, UploadFile, File,Query,Depends
from typing import Optional, Annotated, Dict
from pydantic.utils import GetterDict
from datetime import datetime, time
from fastapi import Form
from users.schema.schema import User


class RedirectRequest(BaseModel):
    id: int
    category_id: int


class CatproductAdd(BaseModel):
    category_id: int
    name: str
    status: Optional[int] = 1


class UpdateGetCatProduct(BaseModel):
    id: int
    category_id: Optional[int] = None
    name: Optional[str] = None
    status: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None


    class Config:
        orm_mode = True


class CategoryNameGet(BaseModel):
    name:str
    price:Optional[float]=None
    class Config:
        orm_mode = True

class OrderProducts(BaseModel):
    name: str
    prod_cat : Optional[CategoryNameGet] = None


    class Config:
        orm_mode = True



class OrderProductsGet(BaseModel):
    id: int
    amount: Optional[int]=None
    orpr_product: Optional[OrderProducts] = None


    class Config:
        orm_mode = True


class CarsCreate(BaseModel):
    name: str
    status: Optional[int] = 1
    number :Optional[str] = None

class CarsUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    status: Optional[int] = None
    number :Optional[str] = None

class CarsGet(BaseModel):
    id: int
    name: str
    status: int
    number :Optional[str] = None

    class Config:
        orm_mode = True

class UpdateExpenditure(BaseModel):
    id: int
    status: Optional[int] = None
    amount: Optional[int] = None
    comment:Optional[str] = None
    class Config:
        orm_mode = True


class MessageRequestCreate(BaseModel):
    request_id: int
    message: str
    status: Optional[int] = 0


class MessageRequest(BaseModel):
    id: int
    message: Optional[str] = None
    status: int
    user: Optional[User] = None
    photo: Optional[str] = None
    created_at: Optional[datetime]=None
    class Config:
        orm_mode = True

    
