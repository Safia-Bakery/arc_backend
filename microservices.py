from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import bcrypt
import requests
import schemas
from users.schema import schema
from sqlalchemy.orm import Session
from typing import Union, Any
import crud
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Header,
    Request,
    status,
)
import pandas as pd
from database import engine, SessionLocal
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()


timezonetash = pytz.timezone("Asia/Tashkent")

BASE_URL = os.environ.get("BASE_URL")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
LOGIN_IIKO = os.environ.get("LOGIN_IIKO")
PASSWORD_IIKO = os.environ.get("PASSWORD_IIKO")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def checkpermissions(request_user, page, db):
    if request_user.status == 1:
        return True
    if request_user.status == 2:
        return False
    if request_user.group is not None:
        group_id = request_user.group_id
        repsones = crud.filter_user_permission(db=db, id=group_id, page=page)
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


async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
) -> schema.User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = crud.get_user(db, sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


def sendtotelegramchannel(bot_token, chat_id, message_text):
    # Create the request payload
    payload = {"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"}

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:

        return response
    else:
        return False


# authentication with iiko
def authiiko():
    data = requests.get(
        f"{BASE_URL}/resto/api/auth?login={LOGIN_IIKO}&pass={PASSWORD_IIKO}"
    )

    key = data.text
    return key


# get list of departments of iikoo
def list_departments(key):
    departments = requests.get(
        f"{BASE_URL}/resto/api/corporation/departments?key={key}"
    )

    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall("corporateItemDto")

    names = [
        [item.find("name").text, item.find("id").text] for item in corporate_item_dtos
    ]
    return names


def getgroups(key):
    groups = requests.get(
        f"{BASE_URL}/resto/api/v2/entities/products/group/list?key={key}"
    ).json()
    return groups


def get_suppliers(key):
    suppliers = requests.get(f"{BASE_URL}/resto/api/suppliers?key={key}")
    root = ET.fromstring(suppliers.content)
    suppliers_list = root.findall("employee")
    return suppliers_list


def getproducts(key):
    products = requests.get(
        f"{BASE_URL}/resto/api/v2/entities/products/list?key={key}"
    ).json()
    return products


def list_stores(key):
    departments = requests.get(f"{BASE_URL}/resto/api/corporation/stores?key={key}")

    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall("corporateItemDto")

    names = [
        [item.find("name").text, item.find("id").text, item.find("parentId").text]
        for item in corporate_item_dtos
    ]
    return names


def get_prices(key,department_id):
    current_date = datetime.now(timezonetash).strftime("%Y-%m-%d")
    prices = requests.get(f"{BASE_URL}/resto/api/v2/reports/balance/stores?timestamp={current_date}&department={department_id}&key={key}")
    return prices.json()


def send_document_iiko(key, data):
    if data.tool.price:
        total_price = float(data.amount) * float(data.tool.price)
        price = data.tool.price

    else:
        total_price = 0
        price = 0
    if data.request.category.department == 1:
        if data.request.category.sphere_status == 1:
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
        else:
            xml_data= None

    if data.request.category.department == 2:
        headers = {
            "Content-Type": "application/xml",  # Set the content type to XML
        }
        xml_data = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <document>
            <documentNumber>newinv-{data.id}</documentNumber>
            <dateIncoming></dateIncoming>
            <useDefaultDocumentTime>false</useDefaultDocumentTime>
            <counteragentId>{data.request.fillial.supplier[0].id}</counteragentId>
            <defaultStoreId>0bfe01f2-6864-48f5-a79e-c885dc76116a</defaultStoreId>
            <items>
                <item>
                    <productId>{data.tool.iikoid}</productId>
                    <productArticle>{data.tool.code}</productArticle>
                    <storeId>0bfe01f2-6864-48f5-a79e-c885dc76116a</storeId>
                    <price>{price}</price>
                    <amount>{data.amount}</amount>
                    <sum>{total_price}</sum>
                    <discountSum>0.000000000</discountSum>
                </item>
            </items>
            </document>"""
    
    response = requests.post(
        f"{BASE_URL}/resto/api/documents/import/outgoingInvoice?key={key}",
        data=xml_data,
        headers=headers,
    )
    return True


def sendtotelegram(bot_token, chat_id, message_text, keyboard):
    keyboard = {
        "inline_keyboard": [
            [{"text": "Yes", "callback_data": "-1"}],
            [{"text": "No", "callback_data": "-2"}],
            keyboard,
        ]
    }

    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "reply_markup": keyboard,
        "parse_mode": "HTML",
    }

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json=payload,
    )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def sendtotelegramaddcomment(bot_token, chat_id, message_text):
    keyboard = {
        "inline_keyboard": [
            [{"text": "Add comment", "callback_data": "4"}],
        ]
    }

    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "reply_markup": keyboard,
        "parse_mode": "HTML",
    }

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json=payload,
    )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def inlinewebapp(bot_token, chat_id, message_text, url):
    keyboard = {
        "inline_keyboard": [
            [{"text": "Оставить отзыв🌟", "web_app": {"url": url}}],
        ]
    }

    # Create the request payload
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "reply_markup": keyboard,
        "parse_mode": "HTML",
    }

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json=payload,
    )
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False


def howmuchleft(key, store_id):
    now_time = datetime.now(timezonetash).strftime("%Y-%m-%dT%H:%M:%S")
    departments = requests.get(
        f"{BASE_URL}/resto/api/v2/reports/balance/stores?key={key}&store={store_id}&timestamp={now_time}"
    )
    return departments.json()


def find_hierarchy(data, parent_id):
    def dfs(current_id):
        result = []
        for item in data:
            if item["parent"] == current_id:
                child_id = item["id"]
                result.append({
                    "id": child_id,
                    "name": item["name"],
                    "num":item['num'],
                    'code':item['code'],
                    "parent":item["parent"],
                    "category":item["category"],
                    "description":item["description"]
                })
                result.extend(dfs(child_id))  # Recursive call for children
        return result

    # Find the parent item
    parent_item = next((item for item in data if item["id"] == parent_id), None)

    if parent_item:
        return [{
            "id": parent_id,
            "name": parent_item["name"],
            "num":parent_item['num'],
            'code':parent_item['code'],
            "parent":parent_item["parent"],
            "category":parent_item["category"],
            "description":parent_item["description"]
        }] + dfs(parent_id)
    else:
        return []
    

def name_generator(length=20):
    import random
    import string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))



statusdata = {'0':'Новый','1':'Принят',"2":'Принят','3':'Закончен','4':'Закрыт,отменен','5':'Остановлен','6':"Решен","7":'Принят','8':'Отменен'}
def file_generator(data,file):
    inserting_data = {"Номер заявки":[],"Клиент":[],'Филиал':[],'Порция еды':[],'Дата поставки':[],'Статус':[],'Порции хлеба':[]}
    for row in data:
        inserting_data['Номер заявки'].append(row.id)
        inserting_data['Клиент'].append(row.user.full_name)
        inserting_data['Филиал'].append(row.fillial.parentfillial.name)
        inserting_data['Порция еды'].append(int(row.size))
        inserting_data['Порции хлеба'].append(int(row.bread_size))
        finish_time = row.arrival_date.strftime("%d-%m-%Y")
        inserting_data['Дата поставки'].append(finish_time)

        inserting_data['Статус'].append(statusdata[str(row.status)])

    
    file_name  = f"files/{name_generator()}.xlsx"
    df = pd.DataFrame(inserting_data)
    total_food = df["Порция еды"].sum()
    total_bread = df["Порции хлеба"].sum()
    totals_row = pd.DataFrame({"Номер заявки": ["Total"], "Порция еды": [total_food], "Порции хлеба": [total_bread]})
    if file:
    # Concatenate DataFrame with totals row

        df = pd.concat([df, totals_row], ignore_index=True)


        # Generate Excel file
        df.to_excel(file_name, index=False)
    return [file_name ,total_food,total_bread]



def Excell_generate_it(data):
    inserting_data = {"Номер заявки":[],"Клиент":[],"Исполнитель":[],'Филиал':[],'Дата создания':[],'Дата окончания':[],'Дедлайн':[],'Статус':[],'Категория':[],'Комментарий':[],"Срочно":[],'Дата решения':[],'Дата отмены':[],'Переоткрыта':[], 'SLA': []}
    for row in data:
        inserting_data['Номер заявки'].append(row.id)
        inserting_data['Клиент'].append(row.user.full_name)
        
        inserting_data['Филиал'].append(row.fillial.parentfillial.name)
        inserting_data['Категория'].append(row.category.name)
        inserting_data['Комментарий'].append(row.description)
        inserting_data['Статус'].append(statusdata[str(row.status)])
        
        create_time = row.created_at.strftime("%d.%m.%Y %H:%M:%S")
        inserting_data['Дата создания'].append(create_time)
        if row.category.ftime:
            inserting_data['SLA'].append(row.category.ftime)
        else:
            inserting_data['SLA'].append('')
        if row.finishing_time:
            deadline = row.finishing_time.strftime("%d.%m.%Y %H:%M:%S")
        else:
            deadline = ""
        if row.brigada_id is not None:
            inserting_data['Исполнитель'].append(row.brigada.name)
        else:
            inserting_data['Исполнитель'].append('')
        
        if row.category.urgent:
            inserting_data['Срочно'].append("Да")
        else:
            inserting_data['Срочно'].append("Нет")

        inserting_data['Дедлайн'].append(deadline)




        if row.update_time:
            reshen_time = dict(row.update_time).get('6')
            if reshen_time:
                reshen_time = datetime.strptime(reshen_time, "%Y-%m-%d %H:%M:%S.%f%z")

                # Now you can use the strftime method
                reshen_time = reshen_time.strftime("%d.%m.%Y %H:%M:%S")
            
                inserting_data['Дата решения'].append(reshen_time)
            else:
                inserting_data['Дата решения'].append("")
            # delayed = dict(row.update_time).get('5')
            # if delayed:
                # delayed = datetime.strptime(delayed, "%Y-%m-%d %H:%M:%S.%f%z")
# 
            #    Now you can use the strftime method
                # delayed = delayed.strftime("%d.%m.%Y %H:%M:%S")
                # inserting_data['Дата приостановки'].append(delayed)
            # else:
                # inserting_data['Дата приостановки'].append("")
            finish_time = dict(row.update_time).get('3')
            if finish_time:
                try:
                    finish_time = datetime.strptime(finish_time, "%Y-%m-%d %H:%M:%S.%f%z")
                except:
                    finish_time = datetime.strptime(finish_time, "%Y-%m-%dT%H:%M:%S.%f%z")

                # Now you can use the strftime method
                finish_time = finish_time.strftime("%d.%m.%Y %H:%M:%S")
                inserting_data['Дата окончания'].append(finish_time)
            else:
                inserting_data['Дата окончания'].append("")
            reopened = dict(row.update_time).get('7')
            if reopened:
                inserting_data['Переоткрыта'].append("Да")
            else:
                inserting_data['Переоткрыта'].append("Нет")

        else:
            inserting_data['Дата решения'].append("")
            inserting_data['Дата приостановки'].append("")
        
        if row.status==4 or row.status==8:
            if row.update_time:
                cancel_time = dict(row.update_time).get('4')
                cancel_time8 =dict(row.update_time).get('8')
                if cancel_time8:
                    try:
                        cancel_time8 = datetime.strptime(cancel_time8, "%Y-%m-%d %H:%M:%S.%f%z")
                    except:
                        cancel_time8 = datetime.strptime(cancel_time8, "%Y-%m-%dT%H:%M:%S.%f%z")

                    # Now you can use the strftime method
                    cancel_time = cancel_time8.strftime("%d.%m.%Y %H:%M:%S")
                elif cancel_time:
                    try:
                        cancel_time = datetime.strptime(cancel_time, "%Y-%m-%d %H:%M:%S.%f%z")
                    except:
                        cancel_time = datetime.strptime(cancel_time, "%Y-%m-%dT%H:%M:%S.%f%z")

                    # Now you can use the strftime method
                    cancel_time = cancel_time.strftime("%d.%m.%Y %H:%M:%S")
            

                inserting_data['Дата отмены'].append(cancel_time)
            else:
                inserting_data['Дата отмены'].append("")
        else:
            inserting_data['Дата отмены'].append("")
        
        #if row.finished_at:
        #    if row.status !=3:
        #        inserting_data['Переоткрыта'].append("Да")
        #    else:
        #        inserting_data['Переоткрыта'].append("Нет")
        #else:
        #    inserting_data['Переоткрыта'].append("Нет")
        

    
    file_name  = f"files/{name_generator()}.xlsx"
    df = pd.DataFrame(inserting_data)
    # Generate Excel file
    df.to_excel(file_name, index=False)
    return file_name



def uniform_excell_generate(data):
    inserting_data = {"Номер заявки":[],"Филиал":[],'Дата поступления':[],"Форма":[],'Общ. сумма':[],'Сотрудник':[],'Статус':[]}
    for row in data:
        forma_list = ''
        total_sum = 0
        inserting_data['Номер заявки'].append(row.id)
        inserting_data['Филиал'].append(row.fillial.parentfillial.name)
        for product in row.request_orpr:
            forma_list += f"{product.orpr_product.prod_cat.name} {product.orpr_product.name} x {product.amount}\n"
            if product.orpr_product.prod_cat.price:
                total_sum += product.orpr_product.prod_cat.price*product.amount
        inserting_data['Форма'].append(forma_list)
        inserting_data['Сотрудник'].append(row.description)
        inserting_data['Статус'].append(statusdata[str(row.status)])
        create_time = (row.created_at+timedelta(hours=5)).strftime("%d.%m.%Y %H:%M:%S")
        inserting_data['Дата поступления'].append(create_time)
        inserting_data['Общ. сумма'].append(total_sum)

    file_name  = f"files/{name_generator()}.xlsx"
    df = pd.DataFrame(inserting_data)
    # Generate Excel file
    df.to_excel(file_name, index=False)
    return file_name



def confirmation_request(bot_token,chat_id,message_text):
    keyboard = {
        'inline_keyboard': [
            [{'text': 'Подтвердить', 'callback_data': '10'}],
            [{'text': 'Не сделано', 'callback_data': '11'}],
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
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload,)

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False