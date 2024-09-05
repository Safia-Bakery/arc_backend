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



class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    request = relationship("Requests", back_populates="file")
    request_id = Column(Integer, ForeignKey("requests.id"))
    status = Column(Integer, default=0)
