from datetime import datetime, time
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.schemas.tools import KRUTool
from app.schemas.branchs import GetBranchs
from app.schemas.kru_categories import KruCategoriesGet


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class ToolBranchCategoryRelation(BaseConfig):
    id: UUID
    tool: Optional[KRUTool]
    branch: Optional[GetBranchs]
    category: Optional[KruCategoriesGet]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class CreateToolBranch(BaseConfig):
    tool_ids: List[UUID]
    branch_id: UUID


class GetToolBranchCategoryRelation(BaseConfig):
    tool: Optional[KRUTool]


class DeleteToolBranch(BaseConfig):
    id: UUID
