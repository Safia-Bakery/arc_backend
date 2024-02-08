from sqlalchemy.orm import Session

import models
import schemas
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import or_, and_, Date, cast, Integer





def all_users(db: Session):
    query = db.query(models.Users).filter(models.Users.telegram_id.isnot(None)).order_by(models.Users.id.desc()).all()
    return query

