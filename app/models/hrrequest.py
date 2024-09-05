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




class HrRequest(Base):
    __tablename__ = "hrrequest"
    id = Column(Integer, primary_key=True, index=True)
    comments = Column(String, nullable=True)
    status = Column(Integer, default=0)
    sphere = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("hruser.id"))
    user = relationship("HrUser", back_populates="request")
    created_at = Column(DateTime(timezone=True), default=func.now())
    answer = Column(String, nullable=True)