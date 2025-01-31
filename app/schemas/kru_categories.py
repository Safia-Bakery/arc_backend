from datetime import datetime, time
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.kru_tasks import KruTasksGet, Tasks
from app.schemas.tools import KRUTool


class KruCategoriesCreate(BaseModel):
    name: str
    parent: Optional[int] = None
    description: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    file: Optional[str] = None
    # tool_id: Optional[int] = None

    class Config:
        orm_mode = True


class KruCategoriesUpdate(BaseModel):
    id : int
    name: Optional[str]=None
    parent: Optional[int] = None
    description: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    tool_id: Optional[int] = None

    class Config:
        orm_mode = True


class KruCategoriesGet(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    status: Optional[int]
    parent: Optional[int]
    start_time: Optional[time]
    end_time: Optional[time]
    # kru_task: Optional[List[Tasks]]
    # tool: Optional[KRUTool]
    products_count: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

    # @property
    # def tasks(self):
    #     return len(self.kru_task)
