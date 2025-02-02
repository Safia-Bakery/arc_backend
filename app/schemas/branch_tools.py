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
    id: Optional[int]
    tool: Optional[KRUTool]
    branch: Optional[GetBranchs]
    category: Optional[KruCategoriesGet] = None
    created_at: Optional[datetime]


class CreateToolBranch(BaseConfig):
    tool_ids: List[int]
    branch_id: UUID
    category_id: Optional[int] = 26


class GetToolBranchCategoryRelation(BaseConfig):
    tool: Optional[KRUTool]


class DeleteToolBranch(BaseConfig):
    id: UUID


class ProductsGroups(BaseConfig):
    folders: Optional[list[str]] = None
    tools: Optional[list[KRUTool]] = None
