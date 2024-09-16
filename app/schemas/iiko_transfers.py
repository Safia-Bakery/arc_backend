from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID


class IikoTransfer(BaseModel):
    request_id:int
    class Config:
        orm_mode = True