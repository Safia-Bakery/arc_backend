from app.db.session import SessionLocal
from typing import Union, Any
from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
from openpyxl import load_workbook
import bcrypt
import random
import string

from sqlalchemy.orm import Session
from typing import Union, Any
from fastapi import (
    Depends,
    HTTPException,
    status,
)
import smtplib
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os
#from schemas import user_schema
#from queries import user_query as crud
from dotenv import load_dotenv
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
import redis

from database import SessionLocal
from app.schemas.users import GetUserFullData
from app.crud.users import get_user_by_username
from app.core.config import settings


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
) -> GetUserFullData:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
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
    user: Union[dict[str, Any], None] = get_user_by_username(db=db, username=sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user




