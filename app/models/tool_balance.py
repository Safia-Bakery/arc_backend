from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    DECIMAL
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class ToolBalance(Base):
    __tablename__ = "tool_balance"
    department_id = Column(UUID(as_uuid=True), ForeignKey("parentfillials.id"), primary_key=True)
    store_id = Column(UUID(as_uuid=True), ForeignKey("fillials.id"), primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), primary_key=True)
    amount = Column(DECIMAL, nullable=True)
    sum = Column(DECIMAL, nullable=True)
    price = Column(DECIMAL, nullable=True)
    updated_at = Column(DateTime, default=func.now())
    branch = relationship("ParentFillials", back_populates="tool_balance")
    store = relationship("Fillials", back_populates="tool_balance")
    tool = relationship("Tools", back_populates="tool_balance")

