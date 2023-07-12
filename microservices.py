from datetime import datetime,timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import bcrypt
import schemas
from sqlalchemy.orm import Session
from typing import Union, Any
import crud
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from database import engine,SessionLocal
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
JWT_SECRET_KEY = 'thisistokenforusersecretauth'   # should be kept secret
JWT_REFRESH_SECRET_KEY =  'thisistokenforusersecretrefresh'
ALGORITHM = "HS256"

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