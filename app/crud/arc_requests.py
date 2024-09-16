from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast,String,extract
from uuid import UUID

from app.models.requests import Requests


def create_arc_auto_reqeust(db:Session,
                       branch_id,
                       category_id,
                       user_id,
                       description,
                       update_time
                       ):
    query = Requests(
        fillial_id=branch_id,
        category_id=category_id,
        user_id=user_id,
        description=description,
        update_time=update_time
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query




