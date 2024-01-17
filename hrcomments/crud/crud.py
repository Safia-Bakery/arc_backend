from sqlalchemy.orm import Session
from hrcomments.schema import schema

import models
import schemas
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import or_, and_, Date, cast, Integer

timezonetash = pytz.timezone("Asia/Tashkent")


def create_question(db:Session,form_data:schema.HrQuestionsCreate):
    query = models.HrQuestions(answer=form_data.answer,question=form_data.question,status=form_data.status)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_question(db:Session,form_data:schema.HrQuestionsUpdate):
    query = db.query(models.HrQuestions).filter(models.HrQuestions.id==form_data.id).first()
    if query:
        if form_data.answer is not None:
            query.answer = form_data.answer
        if form_data.question is not None:
            query.question = form_data.question
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
        return query
    return None

def get_questions(db:Session,id):
    query = db.query(models.HrQuestions)
    if id is not None:
        query = query.filter(models.HrQuestions.id==id)

    return query.all()


def get_hrrequest(db:Session,id,sphere):
    query = db.query(models.HrRequest)
    if id is not None:
        query.filter(models.HrRequest.id==id)
    if sphere is not None:
        query.filter(models.HrRequest.sphere==sphere)

    return query.all()

def update_hrrequest(db:Session,form_data:schema.HrRequestUpdate):
    query = db.query(models.HrRequest).filter(models.HrRequest.id==form_data.id).first()
    if query:
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
        return query
    return None

