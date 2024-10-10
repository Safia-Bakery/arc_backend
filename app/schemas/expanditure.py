from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID



class GetExpanditure(BaseModel):
    id: int
    amount: int
    tool: Optional[ToolsSearch] = None
    comment: Optional[str] = None
    user: Optional[UserGetlist] = None
    created_at: datetime
    status:Optional[int] = None

    class Config:
        orm_mode = True