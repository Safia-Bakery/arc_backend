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

class KruFinishedTasks(Base):
    __tablename__ = "kru_finished_tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("kru_tasks.id"))
    task = relationship("KruTasks", back_populates="finished_task")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="finished_task")
    branch_id = Column(UUID, ForeignKey("fillials.id"))
    branch = relationship("Fillials", back_populates="kru_finished_task")
    comment = Column(String, nullable=True)
    file = relationship("Files", back_populates="kru_finished_task")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

