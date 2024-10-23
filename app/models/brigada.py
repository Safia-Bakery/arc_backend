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


class Brigada(Base):
    __tablename__ = "brigada"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    request = relationship("Requests", back_populates="brigada")
    user = relationship("Users", back_populates="brigader", uselist=True)
    status = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    sphere_status = Column(Integer, default=1)
    department = Column(Integer, nullable=True)
    is_outsource = Column(Boolean, default=False)
    chat_id = Column(BIGINT, nullable=True, default=None)
    topic_id = Column(Integer, nullable=True, default=None)
