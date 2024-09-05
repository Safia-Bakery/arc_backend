from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
    Table,
    Time,
    JSON,
    VARCHAR,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
from app.db.base import Base
import pytz
import uuid




class NeededTools(Base):
    __tablename__ = "neededtools"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=0)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    need_tool = relationship("Tools", back_populates="tool_need")
    ordered_amount = Column(Float, nullable=True)
    amount_last = Column(Float, nullable=True)
    toolorder_id = Column(Integer, ForeignKey("toolsorder.id"))
    need_order = relationship("ToolsOrder", back_populates="order_need")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

