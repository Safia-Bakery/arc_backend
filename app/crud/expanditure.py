from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.models.expanditure import Expanditure


def update_status(db:Session,expanditure_id):
    query = db.query(Expanditure).filter(Expanditure.id==expanditure_id).update({Expanditure.status:1})
    db.commit()
    return query


def create_expanditure(db:Session, amount, tool_id, request_id, status: Optional[int] = 0):
    query = Expanditure(
        amount=amount,
        tool_id=tool_id,
        request_id=request_id,
        status=status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def delete_expanditure(db:Session,request_id,tool_id):
    query = db.query(Expanditure).filter(Expanditure.request_id==request_id,Expanditure.tool_id==tool_id).first()
    db.delete(query)
    db.commit()
    return query


def update_expenditure(db:Session, exp_id, status):
    query = db.query(Expanditure).get(ident=exp_id)
    query.status = status
    db.commit()
    return query
