from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel


class KruCategoriesCreate(BaseModel):
    name: str
    parent: Optional[int] = None
    description: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    file: Optional[str] = None

    class Config:
        orm_mode = True


class KruCategoriesUpdate(BaseModel):
    id : int
    name: Optional[str]=None
    parent: Optional[int] = None
    description: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

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
    products_count: Optional[int] = None
    tasks_count: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

    # @property
    # def tasks(self):
    #     return len(self.kru_task)
