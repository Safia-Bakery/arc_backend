from typing import Optional

from sqlalchemy.orm import Session,joinedload
from sqlalchemy import or_, and_, Date, cast
import re
from uuid import UUID
from sqlalchemy.sql import func

import models
from app.models.toolparents import ToolParents
from app.models.tools import Tools



def get_tools(db:Session,name:Optional[str]=None,parent_id:Optional[UUID]=None):
    query = db.query(Tools)
    if name is not None:
        query = query.filter(Tools.name.ilike(f"%{name}%"))
    if parent_id is not None:
        query = query.filter(Tools.parentid==parent_id)
    return  query.all()


def get_groups(db:Session,name,parent_id):
    query = db.query(ToolParents)
    if name is not None:
        query = query.filter(ToolParents.name.ilike(f"%{name}%"))
    return query.filter(ToolParents.parent_id==parent_id).all()



