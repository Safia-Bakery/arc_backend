from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class GetToolParent(BaseModel):
    id: UUID
    name: str
    status: Optional[int] = None
    parent_id: Optional[UUID] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True