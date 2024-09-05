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




class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    request = relationship("Requests", back_populates="comments")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="comments")
    rating = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)

