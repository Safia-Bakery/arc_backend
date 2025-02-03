from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from uuid import UUID



class getManagers(BaseModel):
    id:int
    name:Optional[str]=None
    description:Optional[str]=None
    status : Optional[int]=None
    class Config:
        orm_mode = True


class getDivisions(BaseModel):
    id:UUID
    name:Optional[str]=None
    status:Optional[int]=None
    class Config:
        orm_mode = True
