from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )



class KruReport(BaseConfig):
    start_date: date
    finish_date: date
    category_id: int
    report_type: int
    branch_id: Optional[UUID] = None
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    response: Optional[str] = None