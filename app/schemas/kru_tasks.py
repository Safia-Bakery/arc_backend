from typing import Optional
from pydantic import BaseModel, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class KruTasksCreate(BaseConfig):
    name: str
    kru_category_id: int
    description : Optional[str] = None


class KruTasksUpdate(BaseConfig):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    kru_category_id: Optional[int] = None


class KruTasksGet(BaseConfig):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    kru_category_id: Optional[int]
    status: Optional[int]

