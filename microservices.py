from datetime import datetime,timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import bcrypt
import requests
import schemas
from sqlalchemy.orm import Session
from typing import Union, Any
import crud
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from database import engine,SessionLocal
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os 
from dotenv import load_dotenv
load_dotenv()


timezonetash = pytz.timezone("Asia/Tashkent")

BASE_URL = os.environ.get('BASE_URL')
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # should be kept secret
JWT_REFRESH_SECRET_KEY =  os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
LOGIN_IIKO=os.environ.get('LOGIN_IIKO')
PASSWORD_IIKO=os.environ.get('PASSWORD_IIKO')
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)



def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))




def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def checkpermissions(request_user,page,db):
    
    if request_user.status == 1:
        return True
    if request_user.status == 2:
        return False
    if request_user.group is not None:
        group_id = request_user.group_id
        repsones = crud.filter_user_permission(db=db,id=group_id,page=page)
        if repsones is not None:
            return True
        else:
            return False
    else:
        return False
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



async def get_current_user(token: str = Depends(reuseable_oauth),db:Session=Depends(get_db)) -> schemas.User:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        expire_date = payload.get('exp')
        sub = payload.get('sub')
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = crud.get_user(db,   sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user




def sendtotelegramchannel(bot_token,chat_id,message_text):

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json=payload,)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False
    


#authentication with iiko
def authiiko():
    data  = requests.get(f"{BASE_URL}/resto/api/auth?login={LOGIN_IIKO}&pass={PASSWORD_IIKO}")

    key = data.text
    return key


#get list of departments of iikoo
def list_departments(key):

    departments = requests.get(f"{BASE_URL}/resto/api/corporation/departments?key={key}")


    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall('corporateItemDto')

    names = [[item.find('name').text, item.find('id').text] for item in corporate_item_dtos]
    return names



def getgroups(key):
    groups = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/group/list?key={key}").json()
    return groups


def get_suppliers(key):
    suppliers = requests.get(f"{BASE_URL}/resto/api/suppliers?key={key}")
    root = ET.fromstring(suppliers.content)
    suppliers_list = root.findall('employee')
    return suppliers_list


def getproducts(key):
    products = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/list?key={key}&includeDeleted=false").json()

    return products


def list_stores(key):

    departments = requests.get(f"{BASE_URL}/resto/api/corporation/stores?key={key}")


    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall('corporateItemDto')

    names = [[item.find('name').text, item.find('id').text,item.find('parentId').text] for item in corporate_item_dtos]
    return names



def send_document_iiko(key,data):
    if data.tool.price:
        total_price = float(data.amount)*float(data.tool.price)
        price = data.tool.price

    else:
        total_price=0
        price = 0
    
    if data.request.category.sphere_status==1:
        headers = {
        "Content-Type": "application/xml",  # Set the content type to XML
        }
        xml_data = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <document>
            <documentNumber>newarc-{data.id}</documentNumber>
            <dateIncoming></dateIncoming>
            <useDefaultDocumentTime>false</useDefaultDocumentTime>
            <counteragentId>{data.request.fillial.supplier[0].id}</counteragentId>
            <defaultStoreId>4aafb5af-66c3-4419-af2d-72897f652019</defaultStoreId>
            <items>
                <item>
                    <productId>{data.tool.iikoid}</productId>
                    <productArticle>{data.tool.code}</productArticle>
                    <storeId>4aafb5af-66c3-4419-af2d-72897f652019</storeId>
                    <price>{price}</price>
                    <amount>{data.amount}</amount>
                    <sum>{total_price}</sum>
                    <discountSum>0.000000000</discountSum>
                </item>
            </items>
            </document>"""
    if data.request.category.sphere_status==2:
        pass
    response = requests.post(f"{BASE_URL}/resto/api/documents/import/outgoingInvoice?key={key}",data=xml_data,headers=headers)
    
    return True
    


def sendtotelegram(bot_token,chat_id,message_text,keyboard):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Yes', 'callback_data': '-1'}],
            [{'text': 'No', 'callback_data': '-2'}],
            keyboard
        ]
    }

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json=payload,)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False
    

def sendtotelegramaddcomment(bot_token,chat_id,message_text):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Add comment', 'callback_data': '4'}],
        ]
    }

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': keyboard,
        'parse_mode': 'HTML'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json=payload,)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False
    

def howmuchleft(key,store_id):
    now_time = datetime.now(timezonetash).strftime("%Y-%m-%dT%H:%M:%S")
    departments = requests.get(f"{BASE_URL}/resto/api/v2/reports/balance/stores?key={key}&store={store_id}&timestamp={now_time}")

    return departments.json()