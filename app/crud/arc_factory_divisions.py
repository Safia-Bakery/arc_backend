from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast,String,extract
from uuid import UUID
from app.schemas.arc_factory_divisions import CreateArcFactoryDivision,UpdateArcFactoryDivision

from app.models.fillials import Fillials

def create_arc_factory_division(db:Session,division:CreateArcFactoryDivision):
    query = Fillials(
        name=division.name,
        parentfillial_id='914de120-bcdb-4b59-b08c-daae2e824fcc',
        manager_id=division.manager_id,
        arc=1,
        status=1
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_arc_factory_divisions(db:Session,parent_id,name,manager_id,status):
    query = db.query(Fillials).filter(Fillials.arc==1)
    if parent_id is not None:
        query = query.filter(Fillials.parentfillial_id==parent_id)
    if name is not None:
        query = query.filter(Fillials.name==name)
    if manager_id is not None:
        query = query.filter(Fillials.manager_id==manager_id)
    return query.all()

def get_arc_factory_division(db:Session,division_id:UUID):
    return db.query(Fillials).filter(Fillials.id==division_id).first()

def update_arc_factory_division(db:Session,division_id:UUID,division:UpdateArcFactoryDivision):
    query = db.query(Fillials).filter(Fillials.id==division_id).first()
    query.name = division.name
    query.manager_id = division.manager_id
    query.status=division.status
    db.commit()
    db.refresh(query)
    return query