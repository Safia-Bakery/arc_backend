from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.models.users_model import Users


def get_user_by_username(db:Session,username:str):
    query = db.query(Users).filter(Users.username==username).first()
    return query