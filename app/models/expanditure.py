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




class Expanditure(Base):
    __tablename__ = "expanditure"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=True)
    request = relationship("Requests", back_populates="expanditure")
    request_id = Column(Integer, ForeignKey("requests.id"))
    tool = relationship("Tools", back_populates="expanditure")
    tool_id = Column(Integer, ForeignKey("tools.id"))
    status = Column(Integer, default=0)
    comment = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="expanditure")
    created_at = Column(DateTime(timezone=True), default=func.now())


