from sqlalchemy.orm import Session
from users.schema import schema
import models
import schemas
from typing import Optional
import bcrypt
from microservices import find_hierarchy
from Variables import role_ids
import pytz
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import or_, and_, Date, cast
from datetime import datetime,timedelta






def delete_tool(db:Session,id):
    query = db.query(models.Tools).filter(models.Tools.id == id).delete()
    db.commit()
    return query    