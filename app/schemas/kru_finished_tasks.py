from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class KruFinishedTasksCreate(BaseModel):
    task_id: int
    comment: str
    file : Optional[str] = None

    class Config:
        orm_mode = True


