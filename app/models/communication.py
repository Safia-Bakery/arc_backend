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




class Communication(Base):
    __tablename__ = "communication"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    requestc = relationship("Requests", back_populates="communication")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="communication")
    message = Column(String, nullable=True)
    photo= Column(String, nullable=True)
    status = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
