from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class TaskAnswers(BaseModel):
    task_id: int
    comment: str
    file: Optional[str] = None

    class Config:
        orm_mode = True


class KruFinishedTasksCreate(BaseModel):
    tool_id: int
    answers: List[TaskAnswers]

    class Config:
        orm_mode = True


