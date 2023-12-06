from pydantic import BaseModel,validator
from fastapi import Form,UploadFile,File
from typing import Optional,Annotated,Dict
from datetime import datetime,time
from fastapi import Form



class RedirectRequest(BaseModel):
    id:int
    category_id:int