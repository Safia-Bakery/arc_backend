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



class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)
    password = Column(String, nullable=True)
    time_created = Column(DateTime(timezone=True), default=func.now())
    full_name = Column(String, nullable=True)
    status = Column(Integer, default=0)
    sphere_status = Column(Integer, default=0)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship("Groups", back_populates="user")
    brigader = relationship("Brigada", back_populates="user")
    brigada_id = Column(Integer, ForeignKey("brigada.id"), nullable=True)
    telegram_id = Column(BIGINT, nullable=True, unique=True)
    request = relationship("Requests", back_populates="user")
    expanditure = relationship("Expanditure", back_populates="user")
    comments = relationship("Comments", back_populates="user")
    toolor = relationship("ToolsOrder", back_populates="user")
    communication = relationship("Communication", back_populates="user")
    arcexpense = relationship("ArcExpense", back_populates="user")
    branch = relationship("Fillials", back_populates="user")
    branch_id = Column(UUID, ForeignKey("fillials.id"), nullable=True)
    finished_task = relationship("KruFinishedTasks", back_populates="user")
