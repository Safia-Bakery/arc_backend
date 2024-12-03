from unicodedata import category

from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast,String,extract
from uuid import UUID


from app.models.category import Category
from app.schemas.arc_factory_requests import GetArcFactoryRequests,UpdateArcFactoryRequests
from app.schemas.coins import UpdateCoinRequest


from app.models.requests import Requests
from crud import timezonetash

timezonetash = pytz.timezone('Asia/Tashkent')



def get_requests(db:Session,user_id,fillial_id,status,id):
    query = db.query(Requests).join(Category).filter(Category.department ==11)
    if user_id is not None:
        query = query.filter(Requests.user_id == user_id)
    if status is not None:
        query = query.filter(Requests.status == status)
    if fillial_id is not None:
        query = query.filter(Requests.fillial_id == fillial_id)
    if id is not None:
        query = query.filter(Requests.id == id)
    return query.order_by(Requests.created_at.desc()).all()


def get_one_request(db:Session,id):
    query = db.query(Requests).filter(Requests.id==id).first()
    return query


def update_coin_request(db:Session,coin : UpdateCoinRequest,request_id:int,user_manager:str):
    query = db.query(Requests).filter(Requests.id==request_id).first()
    if query:
        query.status = coin.status
        query.deny_reason = coin.deny_reason
        query.user_manager = user_manager
        db.commit()
        db.refresh(query)
    return query


def get_last24hours_requests(db: Session):
    """
    Fetch requests created in the last 24 hours for a specific department.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        Query result of requests created in the last 24 hours.
    """
    # Calculate the timestamp for 24 hours ago
    last_24_hours = datetime.now(tz=timezonetash) - timedelta(hours=24)

    # Query the database
    query = db.query(Requests).join(Category).filter(
        Category.department == 11,  # Filter by department
        Requests.created_at >= last_24_hours  # Filter by created_at within the last 24 hours
    )

    return query.all()


