# ----------import packages
from datetime import datetime, timedelta, date, time
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, UploadFile, status, BackgroundTasks
from pydantic import ValidationError,Json
import statisquery
import schemas
import bcrypt
from typing import Annotated, Dict,Union,Any
from uuid import UUID
import models
from users.schema.schema import UserFullBack
from microservices import (
    sendtotelegramchannel,
    sendtotelegram,
    sendtotelegramaddcomment,
    inlinewebapp,
)
from typing import Optional
from microservices import get_current_user, get_db
from database import engine, SessionLocal
from fastapi_pagination import paginate, Page, add_pagination
from dotenv import load_dotenv
from microservices import (
    create_refresh_token,
    verify_password,
    create_access_token,
    checkpermissions,
)
import os

# from main import get_db,get_current_user
from fastapi import APIRouter, Form
from hrcomments.schema import schema
from hrcomments.crud import crud


load_dotenv()
hrrouter = APIRouter()

HRBOT_TOKEN = os.environ.get("HRBOT_TOKEN")
@hrrouter.post("/hr/question", summary="Create question",tags=["HR"],response_model=schema.HrQuestionsGet)
async def create_question(
    form_data: schema.HrQuestionsCreate,
    db: Session = Depends(get_db),
    current_user: UserFullBack= Depends(get_current_user),
):
    return crud.create_question(db, form_data)
    
@hrrouter.put("/hr/question", summary="Update question",tags=["HR"],response_model=schema.HrQuestionsGet)
async def update_question(
    form_data: schema.HrQuestionsUpdate,
    db: Session = Depends(get_db),
    current_user: UserFullBack = Depends(get_current_user),
):
    return crud.update_question(db, form_data)

@hrrouter.get("/hr/question", summary="Get question",tags=["HR"],response_model=Page[schema.HrQuestionsGet])
async def get_questions(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user:UserFullBack = Depends(get_current_user),
):
    return paginate(crud.get_questions(db, id))


@hrrouter.get("/hr/request", summary="Get Request",tags=["HR"],response_model=Page[schema.HrRequest])
async def get_hrrequest(
    id: Optional[int] = None,
    sphere:Optional[int]=None,
    db: Session = Depends(get_db),
    current_user: UserFullBack = Depends(get_current_user),
):
    return paginate(crud.get_hrrequest(db, id,sphere=sphere))


@hrrouter.put("/hr/request", summary="Update Request",tags=["HR"],response_model=schema.HrRequest)
async def update_hrrequest(
    form_data: schema.HrRequestUpdate,
    db: Session = Depends(get_db),
    current_user:UserFullBack = Depends(get_current_user),
):
    query = crud.update_hrrequest(db, form_data)
    if form_data.answer is not None:
        sendtotelegramaddcomment(HRBOT_TOKEN,form_data.answer,query.user.telegram_id)
    return query




