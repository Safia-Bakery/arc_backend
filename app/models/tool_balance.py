from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    DECIMAL
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
from app.db.base import Base


class ToolBalance(Base):
    __tablename__ = "tool_balance"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("parentfillials.id"), nullable=True)
    store_id = Column(UUID(as_uuid=True), ForeignKey("fillials.id"))
    tool_id = Column(UUID(as_uuid=True), ForeignKey("tools.id"))
    amount = Column(DECIMAL, nullable=True)
    sum = Column(DECIMAL, nullable=True)
    price = Column(DECIMAL, nullable=True)
    branch = relationship("ParentFillials", back_populates="tool_balance")
    store = relationship("Fillials", back_populates="tool_balance")
    tool = relationship("Tools", back_populates="tool_balance")

