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



class Telegrams(Base):
    __tablename__ = "telegrams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    chat_id = Column(String, nullable=True)
    categories = relationship("Category", back_populates="telegram")

