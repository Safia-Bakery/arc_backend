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



class Cars(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    number = Column(String,nullable=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    request = relationship("Requests", back_populates="cars")


