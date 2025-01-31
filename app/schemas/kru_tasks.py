from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.tools import KRUTool



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class KruTasksCreate(BaseConfig):
    name: str
    kru_category_id: int
    description : Optional[str] = None
    answers: Optional[List[str]] = None


class KruTasksUpdate(BaseConfig):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    kru_category_id: Optional[int] = None
    answers: Optional[List[str]] = None


class Tasks(BaseConfig):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    kru_category_id: Optional[int]
    status: Optional[int]
    answers: Optional[List[str]]


class KruTasksGet(BaseConfig):
    products: List[KRUTool]
    tasks: List[Tasks]
