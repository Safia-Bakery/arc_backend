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


class ToolsOrder(Base):
    __tablename__ = "toolsorder"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=0)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    user = relationship("Users", back_populates="toolor")
    created_at = Column(DateTime(timezone=True), default=func.now())
    order_need = relationship("NeededTools", back_populates="need_order")


