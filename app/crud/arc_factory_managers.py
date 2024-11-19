from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast,String,extract
from uuid import UUID
from app.schemas.arc_factory_managers import CreateArcFactoryManagers,UpdateArcFactoryManagers

from app.models.managers import Managers

def create_arc_factory_manager(db:Session,manager:CreateArcFactoryManagers):
    query = Managers(
        name=manager.name,
        description=manager.description,
        status = 1
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_arc_factory_managers(db:Session,name,description,status):
    query = db.query(Managers)
    if name:
        query = query.filter(Managers.name==name)
    if description:
        query = query.filter(Managers.description==description)
    return query.all()

def get_arc_factory_manager(db:Session,manager_id):
    return db.query(Managers).filter(Managers.id==manager_id).first()

def update_arc_factory_manager(db:Session,manager_id,manager:UpdateArcFactoryManagers):
    query = db.query(Managers).filter(Managers.id==manager_id).first()
    query.name = manager.name
    query.description = manager.description
    query.status=manager.status
    db.commit()
    db.refresh(query)
    return query




