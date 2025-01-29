from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID


class GetBranchs(BaseModel):
    id: Optional[UUID]=None
    name: Optional[str]=None
    status: Optional[int]=None
    country: Optional[str]=None

    class Config:
        orm_mode = True


