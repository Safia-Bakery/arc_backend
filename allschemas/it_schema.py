from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID




class generate_excell(BaseModel):
    start_date: date
    finish_date: date
    category_id: Optional[int] = None
    status: Optional[int] = None
    class Config:
        orm_mode = True
