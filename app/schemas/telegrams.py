from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from orders.schema import schema_router


class TelegramsGet(BaseModel):
    id: int
    chat_id: str
    name: str

    class Config:
        orm_mode = True