from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time,date
from fastapi import Form
from uuid import UUID



class CreateCategoryTool(BaseModel):
    category_id:int
    tool_id:int


class DeleteCategoryTool(BaseModel):
    category_id:int
    tool_id:int
