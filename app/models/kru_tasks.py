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

class KruTasks(Base):
    __tablename__ = "kru_tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(Integer, default=1)
    kru_category_id = Column(Integer, ForeignKey("kru_categories.id"))
    kru_category = relationship("KruCategories", back_populates="kru_task")
    finished_task = relationship("KruFinishedTasks", back_populates="task")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

